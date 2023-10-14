from tkinter import *
import os
from tkinter.ttk import Combobox
from datetime import datetime

master = Tk()
master.title("Banking App")

# Funcs
def finish_reg():
      name = temp_name.get()
      age = temp_age.get()
      gender = temp_gender.get()
      password = temp_password.get()

      all_accounts = os.listdir()

      try:
            age = int(age)
      except ValueError:
            notif.config(fg='red', text="Your age should be a positive integer")
            return
      
      if name == "" or age  == "" or gender == "" or password == "":
           notif.config(fg='red', text="All fields required")
           return
      if len(password)<4:
            notif.config(fg='red', text="The password is too short")
            return
      if len(password)>16:
            notif.config(fg='red', text="The password is too long")
            return
      if age > 100:
            notif.config(fg='red', text="Please insert your real age")
            return
            
      
      
      for name_check in all_accounts:
          if name == name_check:
                notif.config(fg="red", text="Account already exists!")
                return
          else:
                 new_file = open(name,"w")
                 new_file.write(name+"\n")
                 new_file.write(password+"\n")
                 age = str(age)
                 new_file.write(age+"\n")
                 new_file.write(gender+"\n")
                 new_file.write("0")
                 new_file.close()
                 notif.config(fg="green", text = "Account has been created succesfully")

                 hist_file = open(f"history_{name}","w")
                 
                 

                
def register():
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notif
    
    
    #Vars
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()
      
    # Register Screen
    register_screen = Toplevel(master)
    register_screen.title("Register Window")


    Label(register_screen, text="Please enter your details below!",font=("Calibri", 12)).grid(row=0, sticky=N, pady=5)
    Label(register_screen, text="Name",font=("Calibri", 12)).grid(row=1, sticky=W)
    Label(register_screen, text="Age",font=("Calibri", 12)).grid(row=2, sticky=W)
    Label(register_screen, text="Gender",font=("Calibri", 12)).grid(row=3, sticky=W)
    Label(register_screen, text="Password",font=("Calibri", 12)).grid(row=4, sticky=W)
    notif = Label(register_screen, text="",font=("Calibri", 12))
    notif.grid(row=6, sticky=N, pady=10)


    Entry(register_screen, textvariable=temp_name).grid(row=1,column=1)
    Entry(register_screen, textvariable=temp_age).grid(row=2,column=1)
    gender_combobox = Combobox(register_screen, textvariable=temp_gender, values=["Male", "Female"], state="readonly")
    gender_combobox.grid(row=3,column=1)
    Entry(register_screen, textvariable=temp_password, show="*").grid(row=4,column=1)

    Button(register_screen, text = "Register", command = finish_reg, font=("Calibri", 12)).grid(row=5, sticky=N)


def view_history():
      view_history_screen = Toplevel(master)
      view_history_screen.title("View history")

      hist_file = open(f"history_{login_name}","r")
      data = hist_file.read()

      file = open(login_name, "r+")
      file_data = file.read()
      details = file_data.split("\n")
      current_balance = details[4]
      current_balance = float(current_balance)
      
      Label(view_history_screen, text="User's transactions",font=("Calibri", 16)).grid(row=0, sticky=N)
      Label(view_history_screen, text="Date/Time                  |       Transaction Type      |           Amount             |       Description       ",font=("Calibri", 11)).grid(row=1, sticky=W)
      Label(view_history_screen, text=f"Your balance: {current_balance:,.2f}$",font=("Calibri", 16)).grid(row=3, sticky=N)
      
      text_widget = Text(view_history_screen, height=25, width=70, state=DISABLED)
      text_widget.grid(row=2, sticky=N)
           
      text_widget.config(state=NORMAL)  
      text_widget.delete('1.0', END)
      text_widget.insert(END, data)
      text_widget.config(state=DISABLED)  
            
def login_session():
    global login_name
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_pass = temp_login_pass.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name, "r")
            file_data = file.read()
            file_data = file_data.split("\n")
            password = file_data[1]
            #Dashboard
            if login_pass == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title("Dashboard")
                #labels

                Label(account_dashboard, text="Account Dashboard", font=("Calibri", 12)).grid(row=0, sticky=N, pady=10)
                Label(account_dashboard, text=f"Welcome {name}!", font=("Calibri", 12)).grid(row=1, sticky=N, pady=10)


                Button(account_dashboard, text="Personal Details", font=("Calibri", 12), width=30, command = personal_details).grid(row=2, sticky=N, padx=10)
                Button(account_dashboard, text="Deposit", font=("Calibri", 12), width=30, command=deposit).grid(row=3, sticky=N, padx=10)
                Button(account_dashboard, text="Withdraw", font=("Calibri", 12), width=30, command=withdraw).grid(row=4, sticky=N, padx=10)
                Button(account_dashboard, text="View Transactions", font=("Calibri", 12), width=30, command=view_history).grid(row=5, sticky=N, padx=10)






            else:
                login_notif.config(fg="red", text="Password incorrect!")
                return
            

    login_notif.config(text="No account found!", fg="red")


def finish_deposit():
    global current_balance
    if amount.get() == "":
        deposit_notif.config(text="Amount is required", fg="red")
        return
    if float(amount.get()) <=0:
        deposit_notif.config(text="Amount should be more than 0", fg="red")
        return
    
    file = open(login_name, "r+")
    file_data = file.read()
    details = file_data.split("\n")
    current_balance = details[4]
    updated_balance = float(current_balance)
    updated_balance += float(amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    file = open(f"history_{login_name}","a")
    current_datetime = datetime.now()
    # Format the datetime as "8/11/2023 11:15 AM"
    formatted_datetime = current_datetime.strftime("%m/%d/%Y %I:%M %p")
    file.write(f"{formatted_datetime}  | Deposited  |   +{float(amount.get())}$  | \n")


    

    current_balance_label.config(text=f"Current Balance: {updated_balance:,.2f}$", fg="green")
    deposit_notif.config(text="Balance Updated", fg = "green")
            

def deposit():
    global amount
    global deposit_notif
    global current_balance_label

    amount = StringVar()
    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split("\n")
    details_balance = float(user_details[4])
    deposit_screen = Toplevel(master)
    deposit_screen.title("Deposit")
    Label(deposit_screen, text="Deposit",font=("Calibri", 16)).grid(row=0, sticky=W)
    current_balance_label = Label(deposit_screen, text=f"Current balance: {details_balance:,.2f}$",font=("Calibri", 12))
    current_balance_label.grid(row=1, sticky=W)
    Label(deposit_screen, text="Amount to deposit:",font=("Calibri", 12)).grid(row=2, sticky=W)
    deposit_notif = Label(deposit_screen, font=("Calibri", 12))
    deposit_notif.grid(row=4, sticky=N, pady=5)
    Entry(deposit_screen, textvariable = amount).grid(row=2, column=1, sticky=W)

    Button(deposit_screen, text="Finish", font=("Calibri", 12), command = finish_deposit).grid(row=3, pady=5, sticky=W)

def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(text="Amount is required", fg="red")
        return
    if float(withdraw_amount.get()) <=0:
        withdraw_notif.config(text="Amount should be more than 0", fg="red")
        return
    
    file = open(login_name, "r+")
    file_data = file.read()
    details = file_data.split("\n")
    current_balance = details[4]

    if float(withdraw_amount.get()) >float(current_balance):
        withdraw_notif.config(text="Insuffisient funds", fg="red")
        return

    updated_balance = float(current_balance)
    updated_balance -= float(withdraw_amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    current_balance_label.config(text=f"Current Balance: {updated_balance:,.2f}$", fg="green")
    withdraw_notif.config(text="Balance Updated", fg = "green")

    file = open(f"history_{login_name}","a")
    current_datetime = datetime.now()
    # Format the datetime as "8/11/2023 11:15 AM"
    formatted_datetime = current_datetime.strftime("%m/%d/%Y %I:%M %p")
    file.write(f"{formatted_datetime}  | Withdrawed |   -{float(withdraw_amount.get())}$   |   {money_destination.get()} \n")


def withdraw():
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    global money_destination

    withdraw_amount = StringVar()
    money_destination = StringVar()
    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split("\n")
    details_balance = float(user_details[4])
    withdraw_screen = Toplevel(master)
    withdraw_screen.title("Withdraw")
    
    Label(withdraw_screen, text="Withdraw",font=("Calibri", 16)).grid(row=0, sticky=W)
    current_balance_label = Label(withdraw_screen, text=f"Current balance: {details_balance:,.2f}$",font=("Calibri", 12))
    current_balance_label.grid(row=1, sticky=W)
    
    Label(withdraw_screen, text="Amount to deposit:",font=("Calibri", 12)).grid(row=2, sticky=W)
    Label(withdraw_screen, text="What is it spent on?",font=("Calibri", 12)).grid(row=3, sticky=W)

    Entry(withdraw_screen, textvariable = money_destination).grid(row=3, column=1, sticky=W)
    
    withdraw_notif = Label(withdraw_screen, font=("Calibri", 12))
    withdraw_notif.grid(row=5, sticky=N, pady=5)
    
    Entry(withdraw_screen, textvariable = withdraw_amount).grid(row=2, column=1, sticky=W)

    Button(withdraw_screen, text="Finish", font=("Calibri", 12), command = finish_withdraw).grid(row=4, pady=5, sticky=W)

def personal_details():
    pass
    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split("\n")
    details_name = user_details[0]
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = float(user_details[4])
    #screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title("Personal details")
    Label(personal_details_screen, text=f"Personal Details:", font=("Calibri", 16)).grid(row=0, sticky=N, pady=10)
    Label(personal_details_screen, text=f"Name: {details_name}", font=("Calibri", 12)).grid(row=1, sticky=W, pady=0)
    Label(personal_details_screen, text=f"Age: {details_age}", font=("Calibri", 12)).grid(row=2, sticky=W, pady=0)
    Label(personal_details_screen, text=f"Gender: {details_gender}", font=("Calibri", 12)).grid(row=3, sticky=W, pady=0)
    Label(personal_details_screen, text=f"Balance: {details_balance:,.2f}$", font=("Calibri", 12)).grid(row=4, sticky=W, pady=0)

def login():
    global temp_login_name
    global temp_login_pass
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_pass = StringVar()
    
    login_screen = Toplevel(master)
    login_screen.title("Login Page")
    Label(login_screen, text="Login", font=("Calibri", 14)).grid(row=0, sticky=N, pady=5)
    Label(login_screen, text="Username", font=("Calibri", 12)).grid(row=1, sticky=W)
    Label(login_screen, text="Password", font=("Calibri", 12)).grid(row=2, sticky=W)
    login_notif = Label(login_screen, font=("Calibri", 12))
    login_notif.grid(row=4, sticky=N)

    Entry(login_screen, textvariable=temp_login_name, font=("Calibri", 12)).grid(row=1, column=1)
    Entry(login_screen, textvariable=temp_login_pass, show="*", font=("Calibri", 12)).grid(row=2, column=1)

    Button(login_screen, text="Login", command=login_session, width=15, font=("Calibri", 12)).grid(row=3, sticky=W, pady=5, padx=5)



Label(master, text="Welcome to the Bank of America!",
      font=("Calibri", 14)).grid(row=0, sticky=N, pady=10)

Label(master, text="The most secure bank in America",
      font=("Calibri", 14)).grid(row=1, sticky=N, pady=10)

Label(master).grid(row=2, sticky=N, pady=15)

# btns
Button(master, text="Register", font=("Calibri", 12), width=20, command=register).grid(row=3, sticky=N, pady=5)
Button(master, text="Login", font=("Calibri", 12), width=20, command=login).grid(row=4, sticky=N, pady=2)

master.mainloop()
