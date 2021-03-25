from tkinter import *
from tkinter import messagebox
from dateutil import relativedelta
from datetime import date, datetime
import Products as ProductsMenu
import Stocks
import csv
import os
from reportlab.pdfgen import canvas

emailErrorFlag = True
bdayErrorFlag = True
row = None
customer = list()
idList = list()
selectedCustomer = -1

def DialogBox(message, title):
    messagebox.showinfo(title, message)

def CheckNumber(entryget):
    try: 
        int(entryget)
    except:
        return True
    return False

def AddOrder():
    Stocks.SetEmptyOrderIndex(selectedCustomer)
    unitPrice = float(ProductsMenu.productLaborCost.get()) + float(ProductsMenu.productOverheadCost.get()) + float(ProductsMenu.productDesiredProfit.get())
    unitPrice += float(Stocks.productVariations[ProductsMenu.selectedRow][ProductsMenu.selectedVariation][5]) / (float(Stocks.productVariations[ProductsMenu.selectedRow][ProductsMenu.selectedVariation][4]) + float(Stocks.productVariations[ProductsMenu.selectedRow][ProductsMenu.selectedVariation][7]))
    unitPrice = (unitPrice*100)/100

    # UPDATE DATABASE
    order = [ProductsMenu.selectedVariation,
    str(selectedCustomer + 100),
    Stocks.productVariations[ProductsMenu.selectedRow][ProductsMenu.selectedVariation][0],
    Stocks.productVariations[ProductsMenu.selectedRow][ProductsMenu.selectedVariation][1],
    Stocks.productVariations[ProductsMenu.selectedRow][ProductsMenu.selectedVariation][2],
    str(1),
    str(unitPrice),
    str(ProductsMenu.productDateReceived.get())]

    Stocks.SetOrders(order, selectedCustomer, ProductsMenu.selectedVariation, ProductsMenu.selectedRow)

    Stocks.SetEmptyOrderIndex(selectedCustomer)

    OrderTable()

    # UPDATE ORDER COLUMNS
    ProductsMenu.UpdateProductOrderColumns()

    Stocks.WriteOrdersFile()
    Stocks.WriteProductsFile()
    Stocks.WriteStockInsFile()

def OrderTable():
    end = len(customer) + 4
    stockInLabel = Label(window, text="Invoice #", width=15, height=1, background="yellow")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 5)

    stockInLabel = Label(window, text="(P) ID", width=15, height=1, background="yellow")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 6)

    stockInLabel = Label(window, text="(P) Type", width=15, height=1, background="yellow")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 7)

    stockInLabel = Label(window, text="(P) Description", width=15, height=1, background="yellow")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 8)

    stockInLabel = Label(window, text="(P) Quantity", width=15, height=1, background="yellow")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 9)

    stockInLabel = Label(window, text="(P) Unit Price", width=15, height=1, background="yellow")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 10)

    stockInLabel = Label(window, text="(P) Date", width=15, height=1, background="yellow")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 11)

    if selectedCustomer != -1:
        for x in range(len(Stocks.customerOrders[0])):
            for y in range(len(Stocks.customerOrders[0][0])):
                if Stocks.customerOrders[selectedCustomer][x][y] != None and Stocks.customerOrders[selectedCustomer][x][y] != '':
                    if y != 0:
                        variationEntries = Entry(window, width=18)
                        variationEntries.insert(END, Stocks.customerOrders[selectedCustomer][x][y])
                        variationEntries.grid(row=x+end+1, column=y+4)
                        variationEntries.config(state=DISABLED)

def addOrderButtonPressed():
    errorFlag = False
    message = "Please input the following: \n"

    try:
        if ProductsMenu.productLaborCost.get() == "" or CheckNumber(ProductsMenu.productLaborCost.get()):
            errorFlag = True
            message += "- Labor Cost\n"
        if ProductsMenu.productOverheadCost.get() == "" or CheckNumber(ProductsMenu.productOverheadCost.get()):
            errorFlag = True
            message += "- Overhead Cost\n"
        if ProductsMenu.productDesiredProfit.get() == "" or CheckNumber(ProductsMenu.productDesiredProfit.get()):
            errorFlag = True
            message += "- Desired Profit\n"
        if selectedCustomer == -1:
            errorFlag = True
            message += "- CLICK WHICH CUSTOMER!\n"
        if ProductsMenu.selectedRow == None:
            errorFlag = True
            message += "- CLICK WHICH PRODUCT!\n"
        if ProductsMenu.selectedVariation == None:
            errorFlag = True
            message += "- CLICK WHICH VARIATION!\n"
        if not ProductsMenu.CheckStockAvailability():
            errorFlag = True
            message += "- NO AVAILABLE STOCK!\n"
        if Stocks.customerOrders[selectedCustomer][9][0] != None and Stocks.customerOrders[selectedCustomer][9][0] != '':
            errorFlag = True
            message = "ORDER SLOTS FULL!"

    except Exception as e:
        errorFlag = True
        if isinstance(e, AttributeError):
            message = "Open Products menu first!"
        else:
            print(type(e))

    if errorFlag == False:
        DialogBox("Save?", "Record Information")
        AddOrder()
    else:
        DialogBox(message, "Record Information Error")

def OnClickCustomerEntry(event):
    global selectedCustomer
    selectedCustomer = event.widget._index
    print(selectedCustomer)
    customerID.set(customer[event.widget._index][0])
    customerName.set(customer[event.widget._index][1])
    customerAddress.set(customer[event.widget._index][2])
    customerContact.set(customer[event.widget._index][3])
    customerEmail.set(customer[event.widget._index][4])
    customerBirthday.set(customer[event.widget._index][5])
    customerSex.set(customer[event.widget._index][6])

    # DELETE ORDER TABLE
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) > len(customer) + 2 and int(widget.grid_info()["column"]) > 4:
            widget.grid_forget()
    
    OrderTable()

def SetCustomerID():
    currentID = 0
    idList.sort()
    for x in range(len(idList)):
        if idList[x-1] + 1 != idList[x] and 1 in idList:
            currentID = idList[x-1] + 1
            customerID.set(str(currentID))
        elif 1 not in idList:
            currentID = 1
            customerID.set(str(currentID))
    
    # CHECK IF EMPTY
    if not idList:
        currentID = 1
        customerID.set(str(currentID))

def AddCustomer():
    SetCustomerID()

    # ADD CUSTOMER TO DATABASE
    customer.append([customerID.get(), customerName.get(), customerAddress.get(), 
    customerContact.get(), customerEmail.get(), customerBirthday.get(), customerSex.get()])

    idList.append(int(customerID.get()))

    SetCustomerID()
    DataTable()

    if len(idList) == 10:
        customerID.set("MAX")

    # DELETE ORDER TABLE
    for widget in window.grid_slaves():
        if int(widget.grid_info()["row"]) > len(customer) + 2 and int(widget.grid_info()["column"]) > 4:
            widget.grid_forget()
    
    OrderTable()

    WriteCustomersFile()

def WriteCustomersFile():
    with open("customers.csv", "w", newline="") as file:
        write = csv.writer(file)
        write.writerows(customer)

def ReadCustomersFile():
    global customer, idList
    try:
        with open("customers.csv", "r") as file:
            reader = csv.reader(file)
            customer = list(reader)

        for x in range(len(customer)):
            if customer[x][0] != None:
                idList.append(int(customer[x][0]))

        DataTable()
        SetCustomerID()
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print("customers.csv file to be created!")
        else:
            print("Error reading customer file: ", type(e))

def DataTable():
    #CREATE TABLE
    global tableEntries
    for x in range(len(customer)):
        for y in range(len(customer[0])):
            tableEntries = Entry(window, width=18)
            tableEntries.insert(END, customer[x][y])
            tableEntries.grid(row=x+3, column=y+5)
            tableEntries._index = x
            tableEntries.bind("<Button-1>", OnClickCustomerEntry)
            tableEntries.config(state=DISABLED)

def DeleteDataFromTable():
    for entry in window.grid_slaves():
        if int(entry.grid_info()["row"]) > len(customer)+2 and int(entry.grid_info()["column"]) > 4:
            entry.grid_forget()

def customerEmailKeyUp(e):
    global emailErrorFlag
    emailErrorFlag = True
    atFlag = False
    comFlag = False
    for x in range(len(customerEmail.get())):
        if x > 3 and customerEmail.get()[x] == "@":
            atFlag = True
        if x > 5 and customerEmail.get()[-4:] == ".com" and atFlag ==  True:
            comFlag = True
        if atFlag and comFlag:
            emailErrorFlag = False
            labelEmail.config(text="Good Email", foreground="green")
        else:
            labelEmail.config(text="Bad Email", foreground="red")

def CalculatePeriod(mm, dd, yyyy):
    today = date.today()
    bday = date(yyyy, mm, dd)
    period = relativedelta.relativedelta(today, bday)
    return int(period.years)

def customerBirthdayKeyUp(e):
    global bdayErrorFlag
    bdayErrorFlag = True
    mm = 0
    dd = 0
    yyyy = 0

    if len(customerBirthday.get()) == 10:
        if customerBirthday.get()[2] == "/" and customerBirthday.get()[5] == "/":
            # GET the values
            try:
                mm = int(customerBirthday.get()[0:2])
                dd = int(customerBirthday.get()[3:5])
                yyyy = int(customerBirthday.get()[6:])
            except:
                print("Invalid Birthday!")

            # CALL method for period difference calculation
            try:
                if CalculatePeriod(mm, dd, yyyy) >= 18:
                    bdayErrorFlag = False
                    labelBirthday.config(text="Valid Birthday", foreground="green")
                else: 
                    labelBirthday.config(text="Invalid Birthday", foreground="red")
            except:
                labelBirthday.config(text="Invalid Birthday", foreground="red")
        else:
            labelBirthday.config(text="Invalid Birthday", foreground="red")
    else:
        labelBirthday.config(text="Invalid Birthday", foreground="red")

def saveButtonPressed():
    errorFlag = False
    message = "Please input a valid:\n"
    if customerID.get() != "MAX":
        if int(customerID.get()) >= 11:
            errorFlag = True
            message = "MAXIMUM CUSTOMERS REACHED!"
            customerID.set("MAX")
        elif int(customerID.get()) == 10:
            customerID.set("MAX")
    elif customerID.get() == "MAX":
        errorFlag = True
        message = "MAXIMUM CUSTOMERS REACHED!"
        customerID.set("MAX")
    if customerName.get() == "":
        errorFlag = True
        message += "- Name\n"
    if customerAddress.get() == "":
        errorFlag = True
        message += "- Address\n"
    if customerContact.get() == "":
        errorFlag = True
        message += "- Contact #\n"
    if emailErrorFlag:
        errorFlag = True
        message += "- Email\n"
    if bdayErrorFlag:
        errorFlag = True
        message += "- Birthday\n"
    if errorFlag == False:
        message = "Save?"
        DialogBox(message, "Record Information")
        AddCustomer()
    else:
        DialogBox(message, "Record Information Error")
    
def deleteButtonPressed():
    try:
        idList.remove(int(customerID.get()))

        del customer[selectedCustomer]

        del Stocks.customerOrders[selectedCustomer]

        for x in range(len(customer)):
            for y in range(len(customer[0])):
                print(customer[x][y])

        DeleteDataFromTable()
        DataTable()

        WriteCustomersFile()
        Stocks.WriteOrdersFile()
    except ValueError: 
        print("Not in list!")
    except TypeError:
        print("Select a row!")
    except:
        print("Select Valid Row!")

def updateButtonPressed():
    contents = [customerName.get(), customerAddress.get(),
    customerContact.get(), customerEmail.get(), customerBirthday.get(), customerSex.get()]
    
    if int(customerID.get()) in idList:
        if len(customer) != 0 and len(customer) >= int(customerID.get()):
            for y in range(1,7):
                customer[selectedCustomer][y] = contents[y-1]
        else:
            print("Nothing to update!")
    else:
        print("Nothing to update!")


    DataTable()

    WriteCustomersFile()

def printInvoiceButtonPressed():
    if selectedCustomer != -1 and selectedCustomer < len(idList) and (Stocks.customerOrders[selectedCustomer][0][1] != None and Stocks.customerOrders[selectedCustomer][0][1] != ''):
        try:
            PrintInvoice()
        except:
            print("Error Printing invoice!")
    else:
        print("Select a valid customer with an order!")

def PrintInvoice():
    c = canvas.Canvas("C:\\Users\\CYRIL\\Desktop\\Programs\\Python\\Programming 2\\Prog2Exer12\\invoice.pdf")

    # HEADER
    c.setFont('Helvetica', 12)
    c.drawString(50, 790, "Cyril's Computer Store")
    c.drawString(50, 770, "Purok 7, San Pedro, Marapangi 3, Toril")
    c.drawString(50, 750, "Davao City, 8000")
    c.drawString(50, 730, "Phone: 09566925939")

    c.setFont('Helvetica-Bold', 12)
    c.drawString(450, 790, "Invoice")
    c.setFont('Helvetica', 12)
    c.drawString(450, 770, "Date: " + datetime.now().strftime("%m/%d/%Y"))
    c.drawString(450, 750, "Invoice #: " + Stocks.customerOrders[selectedCustomer][0][1])
    c.drawString(450, 730, "Customer #:" + customer[selectedCustomer][0])

    # 1ST LINE
    c.line(50, 715, 540, 715)

    # BILL TO
    c.setFont('Helvetica-Bold', 12)
    c.drawString(50, 700, "Bill To:")
    c.setFont('Helvetica', 12)
    c.drawString(50, 680, customer[selectedCustomer][1]) # Customer Name
    c.drawString(50, 660, customer[selectedCustomer][2]) # Customer Address
    c.drawString(50, 640, customer[selectedCustomer][3]) # Customer Contact

    # 2ND LINE
    c.line(50, 625, 540, 625)

    # TABLE
    c.setFont('Helvetica-Bold', 12)
    c.drawString(100, 610, "Product/Description")
    c.drawString(350, 610, "Quantity")
    c.drawString(450, 610, "Unit Price")
    c.setFont('Helvetica', 12)

    # 3RD LINE
    c.line(50, 600, 540, 600)

    # LIST
    x = 50
    y = 580

    for i in range(len(Stocks.customerOrders[0])):
        if Stocks.customerOrders[selectedCustomer][i][0] == '' or Stocks.customerOrders[selectedCustomer][i][0] == None:
            break
        c.drawString(x + 25, y, Stocks.customerOrders[selectedCustomer][i][3])
        c.drawString(x + 130, y, Stocks.customerOrders[selectedCustomer][i][4])
        c.drawString(x + 320, y, Stocks.customerOrders[selectedCustomer][i][5])
        c.drawString(x + 400, y, "P " + Stocks.customerOrders[selectedCustomer][i][6])
        y = y - 20

    # 4TH LINE
    c.line(50, y, 540, y)
    y = y - 20

    # COMPUTATION
    subtotal = 0
    total = 0
    tax = 0

    for i in range(len(Stocks.customerOrders[0])):
        if Stocks.customerOrders[selectedCustomer][i][0] == '' or Stocks.customerOrders[selectedCustomer][i][0] == None:
            break
        subtotal = float(Stocks.customerOrders[selectedCustomer][i][5]) * float(Stocks.customerOrders[selectedCustomer][i][6])

    tax = subtotal * 0.12;
    total = subtotal + tax;

    c.setFont('Helvetica-Bold', 12)
    c.drawString(350, y, "Subtotal: P " + str(subtotal))
    y = y - 20
    c.drawString(350, y, "Tax 12%: P " + str(tax))
    y = y - 20
    c.drawString(350, y, "Total: P " + str(total))
    
    # SAVE FILE
    c.save()

    # AUTO OPEN FILE
    os.startfile("C:\\Users\\CYRIL\\Desktop\\Programs\\Python\\Programming 2\\Prog2Exer12\\invoice.pdf")

def Products():
    ProductsMenu.OpenWindow()

window = Tk()
window.title("Customer Registration System")
window.geometry("1300x440")
window.configure(bg = "orange")

# MENU BAR
menubar = Menu(window, tearoff=0)
filemenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Products", command=Products)
filemenu.add_command(label="Orders", command=None)
filemenu.add_separator()
filemenu.add_command(label="Close", command=window.quit)

editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)

window.configure(menu=menubar)

dataLabel = Label(window, bg="yellow", text="ID", height=1, width=15)
dataLabel.config(font=("consolas", 10))
dataLabel.grid(column=5, row=2)

dataLabel = Label(window, bg="yellow", text="Name", height=1, width=15)
dataLabel.config(font=("consolas", 10))
dataLabel.grid(column=6, row=2)

dataLabel = Label(window, bg="yellow", text="Address", height=1, width=15)
dataLabel.config(font=("consolas", 10))
dataLabel.grid(column=7, row=2)

dataLabel = Label(window, bg="yellow", text="Contact #", height=1, width=15)
dataLabel.config(font=("consolas", 10))
dataLabel.grid(column=8, row=2)

dataLabel = Label(window, bg="yellow", text="Email", height=1, width=15)
dataLabel.config(font=("consolas", 10))
dataLabel.grid(column=9, row=2)

dataLabel = Label(window, bg="yellow", text="Birthday", height=1, width=15)
dataLabel.config(font=("consolas", 10))
dataLabel.grid(column=10, row=2)

dataLabel = Label(window, bg="yellow", text="Sex", height=1, width=15)
dataLabel.config(font=("consolas", 10))
dataLabel.grid(column=11, row=2)

# TITLE
labelTitle = Label(window, text="Customer Registration System", width=30, height=2, bg="yellow", anchor="center")
labelTitle.config(font=("consolas", 10))
labelTitle.grid(column=2, row=1)

# LABEL for CUSTOMER ID
label = Label(window, text="Customer ID", width=20,height=1, bg="yellow")
label.config(font=("consolas", 10))
label.grid(column=1, row=2)

# ENTRY for CUSTOMER ID
customerID = StringVar(window)
customerID.set("1")
Entry(window, width=35, state=DISABLED, textvariable=customerID).grid(column=2, row=2)

# LABEL for CUSTOMER NAME
label = Label(window, text="Customer Name", width=20, height=1, bg="yellow")
label.config(font=("consolas", 10))
label.grid(column=1, row=3)

# ENTRY for CUSTOMER NAME
customerName = StringVar(window)
Entry(window, textvariable=customerName, width=35).grid(column=2, row=3)

# GUIDE for CUSTOMER NAME
label = Label(window, text="LastName, FirstName", width=20, height=1, bg="orange")
label.config(font=("tahoma", 7))
label.grid(column=3, row=3)

# LABEL for CUSTOMER ADDRESS
label = Label(window, text="Customer Address", width=20, height=1, bg="yellow")
label.config(font=("consolas", 10))
label.grid(column=1, row=4)

# ENTRY for CUSTOMER ADDRESS
customerAddress = StringVar(window)
Entry(window, textvariable=customerAddress, width=35).grid(column=2, row=4)

# LABEL for CUSTOMER CONTACT
label = Label(window, text="Customer Contact #", width=20, height=1, bg="yellow")
label.config(font=("consolas", 10))
label.grid(column=1, row=5)

# ENTRY for CUSTOMER CONTACT
customerContact = StringVar(window)
Entry(window, textvariable=customerContact, width=35).grid(column=2, row=5)

# LABEL for CUSTOMER EMAIL
label = Label(window, text="Customer E-mail", width=20, height=1, bg="yellow")
label.config(font=("consolas", 10))
label.grid(column=1, row=6)

# ENTRY for CUSTOMER EMAIL
customerEmail = StringVar(window)
entryCustomerEmail = Entry(window, textvariable=customerEmail, width=35)
entryCustomerEmail.grid(column=2, row=6)
entryCustomerEmail.bind("<KeyRelease>", customerEmailKeyUp)

# GUIDE for CUSTOMER EMAIL
labelEmail = Label(window, text="[a-z]@[a-z].com", width=20, height=1, bg="orange")
labelEmail.config(font=("tahoma", 7))
labelEmail.grid(column=3, row=6)

# LABEL for CUSTOMER BIRTHDAY
label = Label(window, text="Customer Birthday", width=20, height=1, bg="yellow")
label.config(font=("consolas", 10))
label.grid(column=1, row=7)

# ENTRY for CUSTOMER BIRTHDAY
customerBirthday = StringVar(window)
entryCustomerBirthday = Entry(window, textvariable=customerBirthday, width=35)
entryCustomerBirthday.grid(column=2, row=7)
entryCustomerBirthday.bind("<KeyRelease>", customerBirthdayKeyUp)

# GUIDE for CUSTOMER BIRTHDAY
labelBirthday = Label(window, text="mm/dd/yyyy", width=20, height=1, bg="orange")
labelBirthday.config(font=("tahoma", 7))
labelBirthday.grid(column=3, row=7)

# LABEL for CUSTOMER SEX
label = Label(window, text="Customer Sex", width=20, height=1, bg="yellow")
label.config(font=("consolas", 10))
label.grid(column=1, row=8)

# OPTION MENU for CUSTOMER SEX  
customerSex = StringVar(window)
customerSex.set("Male") #Default
optionCustomerSex = OptionMenu(window, customerSex, "Male", "Female")
optionCustomerSex.config(bg="white", width=10)
optionCustomerSex.grid(column=2, row=8)

# BUTTON SAVE
buttonSave = Button(window, text="Save", command=saveButtonPressed, foreground="green", bg="white")
buttonSave.grid(column=1, row=9)

# BUTTON DELETE
buttonDelete = Button(window, text="Delete", command=deleteButtonPressed, foreground="red", bg="white")
buttonDelete.grid(column=1, row=10)

# BUTTON EDIT
buttonEdit = Button(window, text="Update", command=updateButtonPressed, bg="white")
buttonEdit.grid(column=1, row=11)

# BUTTON ADD ORDER
buttonAddCustomer = Button(window, text="Add Order", command=addOrderButtonPressed, bg="white")
buttonAddCustomer.grid(column=2, row=10)

# BUTTON PRINT INVOICE
buttonAddCustomer = Button(window, text="Print Invoice", command=printInvoiceButtonPressed, bg="white")
buttonAddCustomer.grid(column=2, row=11)

# INITIALIZE
ReadCustomersFile()
try:
    Stocks.ReadOrdersFile()
    OrderTable()
except Exception as e:
    if isinstance(e, FileNotFoundError):
        print("orders.csv file to be created!")
    else:
        print("Error reading orders file: ", type(e))

if len(idList) == 10:
        customerID.set("MAX")

window.mainloop()