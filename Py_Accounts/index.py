#importing
import os
import csv
import hashlib
from tqdm import tqdm
from datetime import date
from prettytable import from_csv
from prettytable import PrettyTable
import matplotlib.pyplot as plt 
import stdiomask

#global function
today = date.today()

#global_initilization
path = 'D:/Python Project/Py_Accounts/Py_Accounts_filedata'
account_field = ["id","Date","Type","Debit","Credit","Amount","Reason"]
current_stamp = today.strftime("%B %d, %Y")

#system begin
def system_start():
    if os.path.exists(path):
        login()
    else:
        app_setup()
        for _ in tqdm(range(int(9e6))):
            pass
        print("Directory is created")
        #login()

#app installation
def app_setup():
    print("+-----------APP SETUP----------+")
    name = input("|     ENTER NAME : ")
    password = input("| ENTER PASSWORD : ")
    print("+------------------------------+")
    os.mkdir('Py_Accounts_filedata')
    f = open(os.path.join(path,'admin_data.csv'), 'x')
    f = open(os.path.join(path,'sales_data.csv'), 'x')
    f.close()
    secure = hashlib.md5(password.encode())

    with open(os.path.join(path,'admin_data.csv'),'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["id","Name","Password"])
        writer.writerow([1,name,secure.hexdigest()])

    with open(os.path.join(path,'sales_data.csv'),'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=account_field)
        writer.writeheader()

    login()
#login
def login():
    print("\n+==============LOGIN==============+")
    name = input(" ENTER USER-NAME : ")
    password = stdiomask.getpass(prompt="  ENTER PASSWORD : ")
    secure = hashlib.md5(password.encode())
    data = []
    with open(os.path.join(path,'admin_data.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
        name_data = data[0]["Name"]
        pass_data = data[0]["Password"]

        if(name_data == name and pass_data == secure.hexdigest()):
            print("\n")
            main()
        else:
            print("------>  ****ACCESS DENIED****")
            login()




#credit - income
def credit():
    results=[]
    print("================================")
    amt = input("ENTER AMOUNT : ₹ ")
    reason = input("ENTER DETAIL : ")
    print("================================\n") 
    with open(os.path.join(path,'sales_data.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            results.append(row)
    if(results==[]):
        with open(os.path.join(path,'sales_data.csv'),'w+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=account_field)
            writer.writeheader()
            writer.writerow({'id':1, 'Date':current_stamp, 'Type':'CREDIT', 'Debit':0, 'Credit':amt, 'Amount':amt, 'Reason':reason.upper()})
    else:
        x = results[-1]["id"]
        exist = results[-1]["Amount"]
        x=int(x)+1
        exist = int(exist) + int(amt)
        with open(os.path.join(path,'sales_data.csv'),'a+', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=account_field)
            writer.writerow({'id':x, 'Date':current_stamp, 'Type':'CREDIT', 'Debit':0, 'Credit':amt, 'Amount':exist, 'Reason':reason.upper()})       

#debit - expense
def debit():
    results=[]
    print("================================")
    amt = input("ENTER AMOUNT : ₹ ")
    reason = input("ENTER DETAIL : ")
    print("================================\n")   
    with open(os.path.join(path,'sales_data.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            results.append(row)
    if(results==[]):
        print(" Sorry : No cash in hand ")
        main()
    else:
        x = results[-1]["id"]
        exist = results[-1]["Amount"]
        x=int(x)+1
        exist = int(exist) - int(amt)
        if (exist >= 0):
            with open(os.path.join(path,'sales_data.csv'),'a+', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=account_field)
                writer.writerow({'id':x, 'Date':current_stamp, 'Type':'DEBIT', 'Debit':amt, 'Credit':0, 'Amount':exist,  'Reason':reason.upper()})
        else:
            print(" Less cash in Hand")   

#view transaction
def view():
    with open(os.path.join(path,'sales_data.csv'), "r") as fp:
        x = from_csv(fp)
    print(x)
    print(" VIEW ONLY INCOME : PRESS 'I' ")
    print("VIEW ONLY EXPENSE : PRESS 'E' ")
    print("       VIEW GRAPH : PRESS 'G' ")
    print("             BACK : ANY OTHER BUTTON ")
    print("==============================================")
    command = input("ENTER COMAND : ")
    print("==============================================\n")

    result=[]

    #CREDIT VIEW
    if(command.lower()=='i'):
        with open(os.path.join(path,'sales_data.csv')) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if(row["Type"]=='CREDIT'):
                    del row['Debit']
                    del row['id']
                    del row['Amount']
                    del row['Type']
                    result.append(row)

            table = PrettyTable()
            table.field_names = ['Date', 'Value', 'Detail']

            
            for i in result:
                table.add_row(i.values())
            print(table)

    elif (command.lower()=='e'):
        with open(os.path.join(path,'sales_data.csv')) as file:
            reader = csv.DictReader(file)
            for row in reader:
                if(row["Type"]=='DEBIT'):
                    del row['Credit']
                    del row['id']
                    del row['Amount']
                    del row['Type']
                    result.append(row)

            table = PrettyTable()
            table.field_names = ['Date', 'Value', 'Detail']

            for i in result:
                table.add_row(i.values())
            print(table)


    elif (command.lower()=='g'):
        amt=[]
        dt=[]
        with open(os.path.join(path,'sales_data.csv')) as file:
            reader = csv.DictReader(file)
            for row in reader:
                x = int(row["Amount"])
                amt.append(x)
                y = int(row["id"])
                dt.append(y)

            # plotting the points  
            plt.plot(dt, amt) 
            
            # naming the x axis 
            plt.ylabel('AMOUNT') 
            # naming the y axis 
            plt.xlabel('FREQUENCY') 
            
            # giving a title to my graph 
            plt.title('PY ACCOUNTS') 
            # function to show the plot 
            plt.show()

    else:
        pass

#about
def about():
    print("+=============== ABOUT US =================+")
    print("| PROGRAM BY : SANDEEP SHAW                |")
    print("| PURE PYTHON TERMINAL PROGRAM             |")
    print("| BASIC PROGRAM TO MANAGE YOUR ACCOUNT     |")
    print("| -> FILE OPERATION  -> CSV                |")
    print("| -> HASHLIB         -> TQDM(LOADER)       |")
    print("| -> PRETTY TABLES   -> MATPLOTLIB         |")
    print("| -> STDIOMASK       -> FUNCTIONS          |")
    print("+==========================================+\n")


#main 
def main():
    results = []
    with open(os.path.join(path,'admin_data.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            results.append(row)
        name = results[0]["Name"]

    check_amt=[]
    with open(os.path.join(path,'sales_data.csv')) as file:
        reader = csv.DictReader(file)
        for row in reader:
            check_amt.append(row)
    if(check_amt==[]):
        cash=0
    else:
        cash = int(check_amt[-1]["Amount"])

    print("+----------PY ACCOUNTS----------+")
    print("|===============================|")
    print(f"     WELCOME {name.upper()}")
    print(f" AMOUNT : ₹ {cash}")
    print("|===============================|")
    print(" VIEW TRANSACTION : PRESS 'V' ")
    print("  DEBIT / EXPENSE : PRESS 'D' ")
    print("  CREDIT / INCOME : PRESS 'C' ")
    print("            ABOUT : PRESS 'A' ")
    print("      SYSTEM EXIT : ANY OTHER ")
    print("|===============================|")
    command = input("ENTER YOUR COMMAND : ")
    if( command.lower()=='v' ):
        view()
        main()
    elif( command.lower()=='d' ):
        debit()
        main()
    elif( command.lower()=='c' ):
        credit()
        main()
    elif( command.lower()=='a' ):
        about()
        main()
    else:
        print("System Closing...")
        for _ in tqdm(range(int(9e6))):
            pass
        clear = lambda: os.system('cls')
        clear()
        exit()

system_start()