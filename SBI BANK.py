import mysql.connector

db_connection=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ramya2003$",
    database="SBIBankDatabase"
)
cursorObj=db_connection.cursor()

def managingRequests():
    allReqs=viewAllRequests()
    print(allReqs,'allReqs 13')

    inp=input("enetr req_type to fetch pending,   rejected, approved") #pending
    inpReq=input("enetr req_type to fetch loan,   atm_card,   check_book,   nte_banking") #loan

    for t in allReqs:
        name,r_type,bal,status=t
        print(t)
    if status == inp and r_type== inpReq:   
        userName=input("enter person anme :--- ")
        cursorObj.execute("select user_id from users where user_name=%s",(userName,))
        user_details=cursorObj.fetchone()
        user_id=user_details[0]
        if userName == t[0]:
            if bal > 500000: 
                staus_Updated="rejected"
                cursorObj.execute("update requests  set req_status=%s  where user_id=%s ",(staus_Updated,user_id))
                db_connection.commit()
                print("rejected cause , bid amount > limit amount")
            else:
                staus_Updated="approved"
                cursorObj.execute("update requests  set req_status=%s  where user_id=%s ",(staus_Updated,user_id))
                db_connection.commit()
                print("approved enjoy with friends and comlete loan then come again for loan")
    
def viewAllRequests():
    # inp=input("enetr req_type to fetch loan,   atm_card,   check_book,   nte_banking")
    cursorObj.execute("select users.user_name,requests.req_type,requests.req_bal,requests.req_status from users left join requests  using (user_id) ")
    allRequests=cursorObj.fetchall()
    print(allRequests)
    return allRequests

def  DeleteCustomer():
    deletePersonUser_id=int(input("enetr user_id here to delete that customer:---"))
    cursorObj.execute("delete from accounts where user_id=%s",(deletePersonUser_id,))
    cursorObj.execute("delete from requests where user_id=%s",(deletePersonUser_id,))
    cursorObj.execute("delete from users where user_id=%s",(deletePersonUser_id,))
    db_connection.commit()
    print("deleted successfully----")

def  searchCustomer():
    cursorObj.execute("select users.user_id,users.user_name,accounts.acc_bal,requests.req_type from users left join accounts using(user_id) left join requests using (user_id)")
    id=int(input ("enetr searching customer id :-- "))
    data=cursorObj.fetchall()
    for i in data :
        if i[0] == id:
            print(i)

def requestRaise(user_id,req_mode):
    qtAmt=int(input("enter quoting amt for loan:---"))
    cursorObj.execute("insert into requests(user_id,req_type,req_bal)values(%s,%s,%s)",(user_id,req_mode,qtAmt))
    db_connection.commit()
    print("loan saction successfully")

def deposit(user_id):
    depoAmt=int(input("enter depoAmt:---"))
    if depoAmt>0:
         cursorObj.execute("update accounts set acc_bal=acc_bal+%s where user_id = %s",(depoAmt,user_id))
         db_connection.commit()
         print("depo successfully")
    else:
        print("deposit amt should be >0 rupees but not negative rupees")

def check_Bal(user_id):
    cursorObj.execute("select * from accounts where user_id=%s",(user_id,))
    mainBal=cursorObj.fetchone()
    return mainBal

def withdraw(userid):
    amt=int(input("enter amount to drawn :----     "))
    abc=check_Bal(userid)
    acId,userId,accType,Main_Amt=abc
    print(abc,"abc")
    if amt>Main_Amt:
        print(f"you are trying to draw{ amt} but you are having only main bal {Main_Amt}")
    elif amt<=Main_Amt:
        cursorObj.execute("update accounts set acc_bal=acc_bal-%s where user_id = %s",(amt,userid))
        db_connection.commit()
        cursorObj.execute("select * from accounts where user_id=%s",(userid,))
        mainBal=cursorObj.fetchone()
        acId,userId,accType,Main_Amt=mainBal
        print(f"{amt } drwan successfully....",f"main bal {Main_Amt}")

def signup():
    name=input("enetr yr name :-- ").strip().lower()
    pswd=input("eneytr yr pswd hetre :--  ").strip().lower()
    userRole=input("enter role here (customer / admin ):--- ").strip().lower()
    cursorObj.execute("insert into users (user_name,user_pswd,user_role) values (%s,%s,%s)",(name,pswd,userRole))
    db_connection.commit()
    cursorObj.execute("select * from users where user_name = %s",(name,))

    data=cursorObj.fetchone()
    print(data,"data")
    user_id,un,up,uRole=data
    print(user_id,"id")
    
    acc_type=input("enter ac/type ( savings / current ):--  ")
    cursorObj.execute("insert into accounts (user_id,acc_type,acc_bal) values (%s,%s,%s) ",(user_id,acc_type,5000))
    db_connection.commit()    

def login():
    name=input("enetr name here :-- ")
    password=input("enetr pswd here :--- ")
    role=input("enter role  ( customer/admin ) :--    ")
    cursorObj.execute("select * from users where user_name=%s",(name,))
    data=cursorObj.fetchone()
    # print(data,"data")
    user_id,userN,userP,userR=data
    print(userR,"role")
    if userR == "customer":
        print("---------customerMenu----------")
        print("---------1.withdraw----------")
        print("---------2.deposit----------")
        print("---------3.checkBal----------")
        print("---------4.requestraise----------")
        # print("---------customerMenu----------")
        choose=input("enetr one option here :----      ") 

        if choose == "1":
            withdraw(user_id)
        if choose == "2":
            deposit(user_id)
        if choose == "3":
            print(check_Bal(user_id)) 
        if choose == "4":
            print("1.loan 2.atm_card 3.checkbook 4.netbanking")
            req_type=int(input("enter your choice here:----")) 
            if req_type ==1:
                req="loan"
                requestRaise(user_id,req)
            if req_type ==2:
                req="atm_card"
                requestRaise(user_id,req)
            if req_type ==3:
                req="checkbook"
                requestRaise(user_id,req)
            if req_type ==4:
                req="netbanking"
                requestRaise(user_id,req)




    if userR == userR and userP == pswd:
        print("---------adminMenu----------")
        print("--------1.Delete Customer-----------")
        print("---------2.search customer----------")
        print("---------3.view allrequests----------")
        print("---------4.view accounts----------")
        print("---------5.managing requests----------")
        choose=input("enter option here :--     ")
        if choose == "1":
            DeleteCustomer()
        if choose == "2":
            searchCustomer()
        if choose == "3":
            viewAllRequests()
        if choose == "4":
            viewAccounts()
        if choose == "5":
            managingRequests()



print("--- SBI bank project-----")
print("1.signup")
print("2.login")
print("3.exit")

choose=input("enetr yr option :--    "  )


if choose == "1":
    signup()
if choose == "2":
    login()
if choose == "3":
    exit()