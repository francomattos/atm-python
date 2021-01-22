# Imports required tkinter, OS, and json libraries
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import os
import random
import json
from datetime import timedelta, date, datetime

# Creates initial GUI frame and its parameters
mainFrame = Tk()
mainFrame.title("CEN4010 Banking System")
mainFrame.geometry("360x145")
mainFrame.iconbitmap(os.path.dirname(__file__) + '\\atm.ico')
mainFrame.style = ttk.Style()
mainFrame.style.theme_use("clam")

# Initializes global variable constants
accountTypes = ("Checking", "Savings", "General Loan",
                "Mortgage", "Car Loan", "Boat Loan", "Credit Card")
withdrawAccounts = ("Checking", "Savings")
loanAccounts = ("General Loan", "Mortgage", "Car Loan", "Boat Loan")
dataFileName = "atmDatabase.json"
random.seed()
rStart = 100
rEnd = 999

# Check if json file exists if not then create it
if not os.path.exists(dataFileName):
    with open(dataFileName, 'w'):
        pass

# Validation function, accepts only float as an input


def validate_Float(usrInput):
    if not usrInput:
        return True
    try:
        float(usrInput)
        return True
    except ValueError:
        return False

# Function for creating new user


def new_User(event):

    # Creates a new user account
    def create_User(accountType, usrName, usrPin, initBalance):
        if len(accountType) == 0 or len(usrName) == 0 or len(usrPin) == 0 or len(initBalance) == 0:
            tkinter.messagebox.showwarning(
                title="Form Imcomplete", message="Please complete form prior to creating an account.", parent=newUserFrame)
        else:
            endOfDay = datetime.combine(
                date.today() + timedelta(days=1), datetime.min.time())
            try:
                with open(dataFileName, 'r') as jsonFile:
                    jsonData = json.load(jsonFile)
            except:
                jsonData = {}
            if usrName in jsonData:
                tkinter.messagebox.showwarning(
                    title="User not unique", message="There is an user already under your name.", parent=newUserFrame)
            else:
                initBalance = float(initBalance)
                if accountType not in withdrawAccounts:
                    initBalance = -initBalance
                jsonData.update({
                    usrName: {
                        "Pin": usrPin,
                        "Accounts": {
                            random.randint(rStart, rEnd): {
                                "AccountType": accountType,
                                "AccountBalance": initBalance,
                                "TransactionCount": 0,
                                "EndOfBusinessDay": datetime.strftime(endOfDay, "%Y-%m-%d %H:%M:%S.%f")
                            }
                        }
                    }
                })
                with open(dataFileName, "w") as jsonFile:
                    json.dump(jsonData, jsonFile, indent=2)

                tkinter.messagebox.showinfo(
                    title="User Created", message="Your user has been created, you may now login.", parent=mainFrame)
                newUserFrame.destroy()

    # Creates new user frame
    newUserFrame = Toplevel()
    newUserFrame.title("Create New User")
    newUserFrame.geometry("380x235")
    newUserFrame.iconbitmap(os.path.dirname(__file__) + '\\atm.ico')
    newUserFrame.focus_set()
    newUserFrame.grab_set()

    newUsrLabel = Label(newUserFrame, text="Enter new user information.")
    newUsrLabel.place(x=10, y=10)

    newUsrLabel = Label(newUserFrame, text="Account Type:")
    newUsrLabel.place(x=10, y=40)
    newAccountType = StringVar(newUserFrame)
    newAccountType.set(accountTypes[0])
    selectaccountType = OptionMenu(newUserFrame, newAccountType, *accountTypes)
    selectaccountType.place(x=90, y=36)

    newUsrLabel = Label(newUserFrame, text="Name:")
    newUsrLabel.place(x=10, y=80)
    newUsrName = Entry(newUserFrame, width=30)
    newUsrName.place(x=55, y=80)
    newUsrLabel = Label(newUserFrame, text="Pin:")
    newUsrLabel.place(x=260, y=80)
    newUsrPin = Entry(newUserFrame, width=10)
    newUsrPin.place(x=290, y=80)
    newUsrLabel = Label(newUserFrame, text="Initial Deposit/Widthdraw:")
    newUsrLabel.place(x=10, y=120)
    newBalance = Entry(newUserFrame, width=15, validate="key", validatecommand=(
        newUserFrame.register(validate_Float), '%P'))
    newBalance.place(x=160, y=120)

    loginBtn = Button(newUserFrame, text="Create", padx=10, command=lambda: create_User(
        newAccountType.get(), newUsrName.get(), newUsrPin.get(), newBalance.get()))
    loginBtn.place(x=60, y=160)
    closeBtn = Button(newUserFrame, text="Cancel", padx=10,
                      command=newUserFrame.destroy)
    closeBtn.place(x=140, y=160)

# Function for opening user account


def open_Account(_userName):

    def make_Deposit():
        accIndex = usrAccountTypes.index(accountType.get())
        accNum = accountNumbers[accIndex]
        with open(dataFileName, 'r') as jsonFile:
            jsonData = json.load(jsonFile)
        if jsonData[_userName]["Accounts"][accNum]["TransactionCount"] >= 10:
            tkinter.messagebox.showwarning(
                title="warning", message="Maximum of 10 transactions per account per day.", parent=userAccountFrame)
            return
        if len(transactionAmount.get()) == 0:
            tkinter.messagebox.showwarning(
                title="warning", message="Please enter a transaction amount.", parent=userAccountFrame)
            return
        jsonData[_userName]["Accounts"][accNum]["AccountBalance"] += float(
            transactionAmount.get())
        jsonData[_userName]["Accounts"][accNum]["TransactionCount"] += 1
        accountBalance.set(
            "$" + str(jsonData[_userName]["Accounts"][accNum]["AccountBalance"]))
        with open(dataFileName, "w") as jsonFile:
            json.dump(jsonData, jsonFile, indent=2)
        tkinter.messagebox.showinfo(
            title="Complete", message="Your transaction is complete!", parent=userAccountFrame)

    def make_Withdraw():
        accIndex = usrAccountTypes.index(accountType.get())
        accNum = accountNumbers[accIndex]
        with open(dataFileName, 'r') as jsonFile:
            jsonData = json.load(jsonFile)
        if jsonData[_userName]["Accounts"][accNum]["TransactionCount"] >= 10:
            tkinter.messagebox.showwarning(
                title="warning", message="Maximum of 10 transactions per account per day.", parent=userAccountFrame)
            return
        if len(transactionAmount.get()) == 0:
            tkinter.messagebox.showwarning(
                title="warning", message="Please enter a transaction amount.", parent=userAccountFrame)
            return
        elif float(transactionAmount.get()) > 500:
            tkinter.messagebox.showwarning(
                title="warning", message="You may only withdraw up to $500.", parent=userAccountFrame)
            return
        if jsonData[_userName]["Accounts"][accNum]["AccountBalance"] < float(transactionAmount.get()):
            tkinter.messagebox.showwarning(
                title="warning", message="Not enough funds for your transaction.", parent=userAccountFrame)
            return
        jsonData[_userName]["Accounts"][accNum]["AccountBalance"] -= float(
            transactionAmount.get())
        jsonData[_userName]["Accounts"][accNum]["TransactionCount"] += 1
        accountBalance.set(
            "$" + str(jsonData[_userName]["Accounts"][accNum]["AccountBalance"]))
        with open(dataFileName, "w") as jsonFile:
            json.dump(jsonData, jsonFile, indent=2)
        tkinter.messagebox.showinfo(
            title="Complete", message="Your transaction is complete!", parent=userAccountFrame)

    # Function for transfering funds between accounts
    def transfer_Funds():
        def make_Transfer():
            fromAccIndex = usrAccountTypes.index(fromAccount.get())
            fromAccNum = accountNumbers[fromAccIndex]
            with open(dataFileName, 'r') as jsonFile:
                jsonData = json.load(jsonFile)
            if jsonData[_userName]["Accounts"][fromAccNum]["AccountBalance"] < float(transferAmount.get()):
                tkinter.messagebox.showwarning(
                    title="Not Enough Funds", message="You do not have enough funds to make this transfer.", parent=transferFundFrame)
                return
            toAccIndex = usrAccountTypes.index(toAccount.get())
            toAccNum = accountNumbers[toAccIndex]
            jsonData[_userName]["Accounts"][fromAccNum]["AccountBalance"] -= float(
                transferAmount.get())
            jsonData[_userName]["Accounts"][toAccNum]["AccountBalance"] += float(
                transferAmount.get())
            accIndex = usrAccountTypes.index(accountType.get())
            accNum = accountNumbers[accIndex]
            accountBalance.set(
                "$" + str(jsonData[_userName]["Accounts"][accNum]["AccountBalance"]))
            with open(dataFileName, "w") as jsonFile:
                json.dump(jsonData, jsonFile, indent=2)
            tkinter.messagebox.showinfo(
                title="Complete", message="Your transfer is completed!", parent=transferFundFrame)
            transferFundFrame.destroy()

        if len(accountNumbers) == 1:
            tkinter.messagebox.showwarning(
                title="Not Enough Accounts", message="You can only make internal transfers, please create another account.", parent=transferFundFrame)
            return

        # Creates GUI frame for the transfer funds window
        transferFundFrame = Toplevel()
        transferFundFrame.title("Transfering Funds")
        transferFundFrame.geometry("360x145")
        transferFundFrame.iconbitmap(os.path.dirname(__file__) + '\\atm.ico')
        transferFundFrame.focus_set()
        transferFundFrame.grab_set()

        accLabel = Label(transferFundFrame, text="From Account:")
        accLabel.place(x=10, y=10)
        fromAccount = StringVar(transferFundFrame)
        fromAccount.set(accountTypes[0])
        fromAccountType = OptionMenu(
            transferFundFrame, fromAccount, *usrAccountTypes)
        fromAccountType.place(x=95, y=6)
        accLabel = Label(transferFundFrame, text="Amount:")
        accLabel.place(x=260, y=10)
        transferAmount = Entry(transferFundFrame, width=12, validate="key", validatecommand=(
            transferFundFrame.register(validate_Float), '%P'))
        transferAmount.place(x=255, y=30)

        accLabel = Label(transferFundFrame, text="To Account:")
        accLabel.place(x=25, y=50)
        toAccount = StringVar(transferFundFrame)
        toAccount.set(accountTypes[0])
        toAccountType = OptionMenu(
            transferFundFrame, toAccount, *usrAccountTypes)
        toAccountType.place(x=95, y=46)

        transferBtn = Button(transferFundFrame, text="Make Transfer",
                             padx=5, command=lambda: make_Transfer())
        transferBtn.place(x=40, y=95)
        closeBtn = Button(transferFundFrame, text="Cancel",
                          padx=5, command=transferFundFrame.destroy)
        closeBtn.place(x=240, y=95)

    # Function for clicking on the accounts and switching between them
    def change_Account(_accountType):
        accIndex = usrAccountTypes.index(_accountType)
        accNum = accountNumbers[accIndex]
        with open(dataFileName, 'r') as jsonFile:
            jsonData = json.load(jsonFile)
        accountBalance.set(
            "$" + str(jsonData[_userName]["Accounts"][accNum]["AccountBalance"]))
        init_Layout(jsonData[_userName]["Accounts"][accNum]["AccountType"])

    # Function for deleting account, or user if only one account left
    def delete_Account(_accountType):
        with open(dataFileName, 'r') as jsonFile:
            jsonData = json.load(jsonFile)
        accIndex = usrAccountTypes.index(_accountType)
        accNum = accountNumbers[accIndex]
        closeBal = jsonData[_userName]["Accounts"][accNum]["AccountBalance"]
        deleteBol = tkinter.messagebox.askquestion(
            title="Close account", message="Would you like to delete this account? \nYour current balance is: ${}".format(closeBal), parent=userAccountFrame)
        if deleteBol:
            if len(accountNumbers) == 1:
                deleteusr = tkinter.messagebox.askquestion(
                    title="Delete User", message="This is your last account! \nIf remove this account, your user will be delete.\nShould we proceed?", parent=userAccountFrame)
                if deleteusr:
                    del jsonData[_userName]
                    with open(dataFileName, "w") as jsonFile:
                        json.dump(jsonData, jsonFile, indent=2)
                    tkinter.messagebox.showinfo(
                        title="User Deleted", message="Your user has been deleted.", parent=mainFrame)
                    close_Window()
            else:
                del jsonData[_userName]["Accounts"][accNum]
                with open(dataFileName, "w") as jsonFile:
                    json.dump(jsonData, jsonFile, indent=2)
                tkinter.messagebox.showinfo(
                    title="Account Deleted", message="Your account has been deleted.", parent=mainFrame)
                userAccountFrame.destroy()
                open_Account(_userName)

    # Function for adding new account for user
    def new_Account(_userName):
        def create_Account():
            if len(transactionAmount.get()) == 0:
                tkinter.messagebox.showwarning(
                    title="Form Imcomplete", message="Please enter an initial balance.", parent=newAccFrame)
            else:
                with open(dataFileName, 'r') as jsonFile:
                    jsonData = json.load(jsonFile)
                initialBalance = float(transactionAmount.get())
                if accountType.get() not in withdrawAccounts:
                    initialBalance = -initialBalance
                endOfDay = datetime.combine(
                    date.today() + timedelta(days=1), datetime.min.time())
                tempUser = dict(jsonData[_userName])
                tempAccounts = dict(tempUser["Accounts"])
                tempAccounts.update({
                    random.randint(rStart, rEnd): {
                        "AccountType": accountType.get(),
                        "AccountBalance": initialBalance,
                        "TransactionCount": 0,
                        "EndOfBusinessDay": datetime.strftime(endOfDay, "%Y-%m-%d %H:%M:%S.%f")
                    }
                })
                tempUser["Accounts"] = tempAccounts
                jsonData[_userName] = tempUser
                with open(dataFileName, "w") as jsonFile:
                    json.dump(jsonData, jsonFile, indent=2)
                tkinter.messagebox.showwarning(
                    title="Account Created", message="The new account has been assigned to you.", parent=newAccFrame)
                newAccFrame.destroy()
                userAccountFrame.destroy()
                open_Account(_userName)

        def init_newAccount(_accountType):
            if _accountType in withdrawAccounts:
                acctLabel.set("Initial Deposit")
            elif _accountType in loanAccounts:
                acctLabel.set("Loan Amount")
            else:
                acctLabel.set("Credit Limit")

        # Creates GUI frame for new account window
        newAccFrame = Toplevel()
        newAccFrame.title("New Bank Account")
        newAccFrame.geometry("340x145")
        newAccFrame.iconbitmap(os.path.dirname(__file__) + '\\atm.ico')
        newAccFrame.focus_set()
        newAccFrame.grab_set()

        newAccLabel = Label(newAccFrame, text="Account Type:")
        newAccLabel.place(x=10, y=10)
        accountType = StringVar(newAccFrame)
        accountType.set(accountTypes[0])
        selectaccountType = OptionMenu(
            newAccFrame, accountType, *accountTypes, command=lambda account: init_newAccount(account))
        selectaccountType.place(x=90, y=6)

        acctLabel = StringVar(newAccFrame)
        newAccLabel = Label(newAccFrame, textvariable=acctLabel)
        newAccLabel.place(x=10, y=50)

        transactionAmount = Entry(newAccFrame, width=12, validate="key", validatecommand=(
            newAccFrame.register(validate_Float), '%P'))
        transactionAmount.place(x=10, y=73)
        transactionAmount.focus()

        createBtn = Button(newAccFrame, text="Create Account",
                           padx=10, command=lambda: create_Account())
        createBtn.place(x=100, y=70)
        closeBtn = Button(newAccFrame, text="Cancel",
                          padx=10, command=newAccFrame.destroy)
        closeBtn.place(x=230, y=70)

        init_newAccount(accountType.get())

    def close_Window():
        userAccountFrame.destroy()
        mainFrame.update()
        mainFrame.deiconify()

    def init_Layout(_userAccount):
        if _userAccount in withdrawAccounts:
            withdrawBtn.place(x=230, y=50)
            depositBtnTxt.set("Deposit")
            withdrawBtnTxt.set("Withdraw")
        elif _userAccount == "Credit Card":
            withdrawBtn.place(x=265, y=50)
            depositBtnTxt.set("Make Payment")
            withdrawBtnTxt.set("Cash Advance")
        else:
            depositBtnTxt.set("Make Payment")
            withdrawBtn.place_forget()

    # Creates GUI frame for user account window
    userAccountFrame = Toplevel()
    userAccountFrame.title("Welcome {}!".format(_userName))
    userAccountFrame.geometry("380x165")
    userAccountFrame.iconbitmap(os.path.dirname(__file__) + '\\atm.ico')
    userAccountFrame.protocol("WM_DELETE_WINDOW", close_Window)

    accountNumbers = []
    usrAccountTypes = []
    with open(dataFileName, 'r') as jsonFile:
        jsonData = json.load(jsonFile)

    for x in jsonData[_userName]["Accounts"]:
        accountNumbers.append(x)
        accType = x + ": " + jsonData[_userName]["Accounts"][x]["AccountType"]
        usrAccountTypes.append(accType)

    accLabel = Label(userAccountFrame, text="Account Type:")
    accLabel.place(x=10, y=10)
    accountType = StringVar(userAccountFrame)
    accountType.set(usrAccountTypes[0])
    selectaccountType = OptionMenu(userAccountFrame, accountType, *
                                   usrAccountTypes, command=lambda account: change_Account(account))
    selectaccountType.place(x=90, y=6)

    accLabel = Label(userAccountFrame, text="Balance:")
    accLabel.place(x=240, y=10)

    accountBalance = StringVar(userAccountFrame)
    accountBalance.set(
        "$" + str(jsonData[_userName]["Accounts"][accountNumbers[0]]["AccountBalance"]))
    accLabel = Label(userAccountFrame, textvariable=accountBalance)
    accLabel.place(x=290, y=10)

    accLabel = Label(userAccountFrame, text="Amount:")
    accLabel.place(x=10, y=50)
    transactionAmount = Entry(userAccountFrame, width=12, validate="key", validatecommand=(
        userAccountFrame.register(validate_Float), '%P'))
    transactionAmount.place(x=67, y=53)
    transactionAmount.focus()

    depositBtnTxt = StringVar(userAccountFrame)
    depositBtn = Button(userAccountFrame, textvariable=depositBtnTxt,
                        padx=10, command=lambda: make_Deposit())
    depositBtn.place(x=150, y=50)
    withdrawBtnTxt = StringVar(userAccountFrame)
    withdrawBtn = Button(userAccountFrame, textvariable=withdrawBtnTxt,
                         padx=5, command=lambda: make_Withdraw())
    withdrawBtn.place(x=240, y=50)
    transferFundBtn = Button(
        userAccountFrame, text="Transfer Funds", padx=15, command=lambda: transfer_Funds())
    transferFundBtn.place(x=10, y=90)

    accLabel = Label(userAccountFrame, text="Create New Account.",
                     fg="blue", cursor="hand2")
    accLabel.place(x=190, y=90)
    accLabel.bind("<Button-1>", lambda b: new_Account(_userName))

    deleteAcctBtn = Button(userAccountFrame, text="Delete Account",
                           padx=15, command=lambda: delete_Account(accountType.get()))
    deleteAcctBtn.place(x=190, y=120)

    # Reset end of day on account
    endOfDay = datetime.strptime(
        jsonData[_userName]["Accounts"][accountNumbers[0]]["EndOfBusinessDay"], "%Y-%m-%d %H:%M:%S.%f")
    if datetime.now() > endOfDay:
        endOfDay = datetime.combine(
            date.today() + timedelta(days=1), datetime.min.time())
        for x in jsonData[_userName]["Accounts"]:
            jsonData[_userName]["Accounts"][x]["TransactionCount"] = 0
            jsonData[_userName]["Accounts"][x]["EndOfBusinessDay"] = datetime.strftime(
                endOfDay, "%Y-%m-%d %H:%M:%S.%f")
        with open(dataFileName, "w") as jsonFile:
            json.dump(jsonData, jsonFile, indent=2)

    init_Layout(jsonData[_userName]["Accounts"]
                [accountNumbers[0]]["AccountType"])

# Function for loggin in user


def new_Login(_userName, _usrPin):
    if _userName and _usrPin:
        try:
            with open(dataFileName, 'r') as jsonFile:
                jsonData = json.load(jsonFile)
        except:
            tkinter.messagebox.showwarning(
                "Login Failed", "Please create an account.")
            return
        if _userName in jsonData and jsonData[_userName]["Pin"] == _usrPin:
            mainFrame.withdraw()
            open_Account(_userName)
        else:
            tkinter.messagebox.showwarning(
                "Login Failed", "Please enter correct username and pin.")
    else:
        tkinter.messagebox.showwarning(
            "Login Failed", "Please enter correct username and pin.")


mainLabels = Label(
    mainFrame, text="Please enter your full name and pin to sign into your account.")
mainLabels.place(x=10, y=10)
mainLabels = Label(mainFrame, text="Name:")
mainLabels.place(x=5, y=45)
mainLabels = Label(mainFrame, text="Pin:")
mainLabels.place(x=240, y=45)

usrName = Entry(mainFrame, width=30)
usrName.place(x=45, y=47)
usrName.focus()
usrPin = Entry(mainFrame, width=10)
usrPin.place(x=265, y=47)

loginBtn = Button(mainFrame, text="Login", padx=10,
                  command=lambda: new_Login(usrName.get(), usrPin.get()))
loginBtn.place(x=60, y=85)
closeBtn = Button(mainFrame, text="Close", padx=10, command=mainFrame.destroy)
closeBtn.place(x=140, y=85)

mainLabels = Label(mainFrame, text="Create New User.",
                   fg="blue", cursor="hand2")
mainLabels.place(x=240, y=85)
mainLabels.bind("<Button-1>", new_User)

mainFrame.mainloop()
