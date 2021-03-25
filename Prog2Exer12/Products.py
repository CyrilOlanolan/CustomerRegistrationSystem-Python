from os import write
from tkinter import *
from datetime import date
import Stocks #CONTAINS ALL THE METHODS TO USE
from tkinter import messagebox
import csv

# THIS FILE IS FOR GUI ONLY
idList = list() #1D
selectedRow = None
selectedVariation = None #CHANGE BACK TO ZERO IF ERROR
productLaborCost = None
productDesiredProfit = None
productOverheadCost = None

def OpenWindow():
    global windowProducts, productID, productType, productDescription, productSupplier, productQuantity, productQuantityAdd, productTotalCost, productDateReceived
    global productLaborCost, productDesiredProfit, productOverheadCost, idList

    windowProducts = Tk()
    windowProducts.title("New Products Stock-In")
    windowProducts.geometry("1400x440")
    windowProducts.configure(bg = "yellow")
    
    # DECLARE GLOBAL VARIABLES
    #productIDCounter = 1

    # TITLE
    label = Label(windowProducts, text="New Products Stock-In", width=30, height=2, bg="orange")
    label.configure(foreground="black", font=("consolas", 10))
    label.grid(column=2, row=1)

    # LABEL for PRODUCT ID
    label = Label(windowProducts, text="Product ID", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=2)

    # ENTRY for PRODUCT ID
    productID = StringVar(windowProducts)
    #productID.set(str(productIDCounter))
    Entry(windowProducts, width=35, state=DISABLED, textvariable=productID).grid(column=2, row=2)

    # LABEL for PRODUCT TYPE
    label = Label(windowProducts, text="Product Type", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=3)

    # ENTRY for PRODUCT TYPE
    productType = StringVar(windowProducts)
    Entry(windowProducts, textvariable=productType, width=35).grid(column=2, row=3)

    # LABEL for PRODUCT DESCRIPTION
    label = Label(windowProducts, text="Product Description", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=4)

    # ENTRY for PRODUCT DESCRIPTION
    productDescription = StringVar(windowProducts)
    Entry(windowProducts, textvariable=productDescription, width=35).grid(column=2, row=4)

    # LABEL for PRODUCT SUPPLIER
    label = Label(windowProducts, text="Product Supplier", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=5)

    # ENTRY for PRODUCT SUPPLIER
    productSupplier = StringVar(windowProducts)
    Entry(windowProducts, textvariable=productSupplier, width=35).grid(column=2, row=5)

    # LABEL for QUANTITY
    label = Label(windowProducts, text="Quantity", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=6)

    # ENTRY for QUANTITY
    productQuantity = StringVar(windowProducts)
    entryProductQuantity= Entry(windowProducts, textvariable=productQuantity, width=35)
    entryProductQuantity.grid(column=2, row=6)

    # LABEL for ADDITIONAL QUANTITY
    label = Label(windowProducts, text="+", width=2, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=3, row=6)

    # LABEL for ADDITIONAL SPACE
    label = Label(windowProducts, text="", width=10, height=1, bg="yellow")
    label.config(font=("consolas", 10))
    label.grid(column=4, row=5)
    
    # ENTRY for ADDITIONAL QUANTITY
    productQuantityAdd = StringVar(windowProducts)
    entryProductQuantityAdd = Entry(windowProducts, textvariable=productQuantityAdd, width=10)
    entryProductQuantityAdd.grid(column=4, row=6)

    # LABEL for TOTAL COST
    label = Label(windowProducts, text="Total Cost", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=7)

    # ENTRY for TOTAL COST
    productTotalCost = StringVar(windowProducts)
    entryTotalCost = Entry(windowProducts, textvariable=productTotalCost, width=35)
    entryTotalCost.grid(column=2, row=7)

    # LABEL for DATE RECEIVED
    label = Label(windowProducts, text="Date Received", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=8)

    # ENTRY for DATE RECEIVED
    dateToday = date.today()
    productDateReceived = StringVar(windowProducts)
    productDateReceived.set(dateToday.strftime("%m/%d/%Y"))
    entryDateReceived = Entry(windowProducts, textvariable=productDateReceived, width=35, state=DISABLED)
    entryDateReceived.grid(column=2, row=8)

    # BUTTON SAVE
    buttonNewProduct = Button(windowProducts, text="New Product", command=ButtonNewProductClicked, bg="white")
    buttonNewProduct.grid(column=1, row=9)

    # BUTTON EDIT
    buttonStockIn = Button(windowProducts, text="Stock In", command=ButtonStockInClicked, bg="white")
    buttonStockIn.grid(column=1, row=10)

    # TABLE HEADERS
    tableLabel = Label(windowProducts, bg="orange", text="ID", height=1, width=15)
    tableLabel.config(font=("consolas", 10))
    tableLabel.grid(column=5, row=2)

    tableLabel = Label(windowProducts, bg="orange", text="Type", height=1, width=15)
    tableLabel.config(font=("consolas", 10))
    tableLabel.grid(column=6, row=2)

    tableLabel = Label(windowProducts, bg="orange", text="Description", height=1, width=15)
    tableLabel.config(font=("consolas", 10))
    tableLabel.grid(column=7, row=2)

    tableLabel = Label(windowProducts, bg="orange", text="Supplier", height=1, width=15)
    tableLabel.config(font=("consolas", 10))
    tableLabel.grid(column=8, row=2)

    tableLabel = Label(windowProducts, bg="orange", text="Total Quantity", height=1, width=15)
    tableLabel.config(font=("consolas", 10))
    tableLabel.grid(column=9, row=2)

    tableLabel = Label(windowProducts, bg="orange", text="Orders", height=1, width=15)
    tableLabel.config(font=("consolas", 10))
    tableLabel.grid(column=10, row=2)

    # LABEL for LABOR COST
    label = Label(windowProducts, text="Labor Cost", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=11)

    # ENTRY for LABOR COST
    productLaborCost = StringVar(windowProducts)
    entryLaborCost = Entry(windowProducts, textvariable=productLaborCost, width=35)
    entryLaborCost.grid(column=2, row=11)

    # LABEL for OVERHEAD COST
    label = Label(windowProducts, text="Overhead Cost", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=12)

    # ENTRY for LABOR COST
    productOverheadCost = StringVar(windowProducts)
    entryOverheadCost = Entry(windowProducts, textvariable=productOverheadCost, width=35)
    entryOverheadCost.grid(column=2, row=12)

    # LABEL for DESIRED PROFIT
    label = Label(windowProducts, text="Desired Profit", width=20, height=1, bg="orange")
    label.config(font=("consolas", 10))
    label.grid(column=1, row=13)

    # ENTRY for DESIRED PROFIT
    productDesiredProfit = StringVar(windowProducts)
    entryDesiredProfit = Entry(windowProducts, textvariable=productDesiredProfit, width=35)
    entryDesiredProfit.grid(column=2, row=13)

    # BUTTON SAVE
    buttonCosts = Button(windowProducts, text="Save Costs", command=ButtonCostsClicked, bg="white")
    buttonCosts.grid(column=1, row=14)

    # INITIALIZE VALUES
    ReadCostsFile()

    try:
        Stocks.ReadProductsFile()
        ProductsTable()

        for x in range(len(Stocks.products)):
            if Stocks.products[x][0] != '0':
                idList.append(int(Stocks.products[x][0]))

    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print("products.csv file to be created!")
        else:
            print("Error reading products file: ", type(e))

    try:
        Stocks.ReadStockInsFile()
        VariationsTable()
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print("stockins.csv file to be created!")
        else:
            print("Error reading stock-ins file: ", type(e))  

    SetProductID()

def ButtonCostsClicked():
    errorFlag = False
    message = "Input valid values: \n"
    try:
        if productLaborCost.get() == "":
            errorFlag = True
            message += "- Labor Cost\n"
        if productOverheadCost.get() == "":
            errorFlag = True
            message += "- Overhead Cost\n"
        if productDesiredProfit.get() == "":
            errorFlag = True;
            message += "- Desired Profit\n"
        
        int(productLaborCost.get())
        int(productOverheadCost.get())
        int(productDesiredProfit.get())
    except Exception as e:
        errorFlag = True
        if isinstance(e, ValueError):
            message = "Input numbers only!"
        else:
            print("Costs button error: " , type(e))

    if errorFlag:
        DialogBox(message, "Error")
    else:
        DialogBox("Saved.", "costs.csv")
        WriteCostsFile()

def WriteCostsFile():
    costs = [productLaborCost.get(), productOverheadCost.get(), productDesiredProfit.get()]

    with open("costs.csv", "w", newline="") as file:
        write = csv.writer(file)
        write.writerow(costs)

def ReadCostsFile():
    try:
        with open("costs.csv", "r") as file:
            reader = csv.reader(file)
            costs = list(reader)
            productLaborCost.set(costs[0][0])
            productOverheadCost.set(costs[0][1])
            productDesiredProfit.set(costs[0][2])
    except Exception as e:
        if isinstance(e, FileNotFoundError):
            print("costs.csv file to be created!")
        else:
            print("Error reading orders file: ", type(e))

def DialogBox(message, title):
    messagebox.showinfo(title, message, master=windowProducts)

def CheckNumber(entryget):
    try: 
        int(entryget)
    except:
        return True
    return False

def UpdateProductOrderColumns():
    try:
        for widget in windowProducts.grid_slaves():
            if int(widget.grid_info()["row"]) > 2 and int(widget.grid_info()["column"]) > 4:
                widget.grid_forget()
    
        ProductsTable()
        VariationsTable()
    except:
        pass

def CheckStockAvailability():
    try: 
        print(Stocks.productVariations[selectedRow][selectedVariation][4])
        if int(Stocks.productVariations[selectedRow][selectedVariation][4]) <= 0:
            return False
        else:
            return True
    except Exception as e:
        print("Variation isn't existing!")
        return False

def ProductsTable():
    global productEntries
    for x in range(len(Stocks.products)):
        for y in range(len(Stocks.products[0])):
            productEntries = Entry(windowProducts, width=18)
            productEntries.insert(END, Stocks.products[x][y])
            productEntries.grid(row=x+3, column=y+5)
            productEntries.config(state=DISABLED)
            productEntries._index = x
            productEntries.bind("<Button-1>", OnClickProductEntry)

def VariationsTable():
    global selectedRow
    if selectedRow == None:
        selectedRow = 0

    end = len(Stocks.products) + 4
    
    stockInLabel = Label(windowProducts, text="ID", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 5)

    stockInLabel = Label(windowProducts, text="Type", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 6)

    stockInLabel = Label(windowProducts, text="Description", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 7)

    stockInLabel = Label(windowProducts, text="Supplier", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 8)

    stockInLabel = Label(windowProducts, text="Quantity", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 9)

    stockInLabel = Label(windowProducts, text="Cost", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 10)

    stockInLabel = Label(windowProducts, text="Date Received", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 11)

    stockInLabel = Label(windowProducts, text="Orders", width=15, height=1, background="orange")
    stockInLabel.config(font=("consolas", 10))
    stockInLabel.grid(row = end, column = 12)
        
    for x in range(len(Stocks.productVariations[0])):
        for y in range(len(Stocks.productVariations[0][0])):
            if Stocks.productVariations[selectedRow][x][0] != 0 and Stocks.productVariations[selectedRow][x][0] != '0':
                variationEntries = Entry(windowProducts, width=18)
                variationEntries.insert(END, Stocks.productVariations[selectedRow][x][y])
                variationEntries.grid(row=x+end+1, column=y+5)
                variationEntries.config(state=DISABLED)
                variationEntries._index = x
                variationEntries.bind("<Button-1>", OnClickVariationEntry)

def SetProductID():
    currentID = 0
    idList.sort()
    for x in range(len(idList)):
        if idList[x-1] + 1 != idList[x] and 1 in idList:
            currentID = idList[x-1] + 1
            productID.set(str(currentID))
        elif 1 not in idList:
            currentID = 1
            productID.set(str(currentID))
    
    # CHECK IF EMPTY
    if not idList:
        currentID = 1
        productID.set(str(currentID))

def AddProduct():
    SetProductID()
    # 0 IS FOR ORDERS COLUMN
    Stocks.SetProduct([productID.get(), productType.get(), productDescription.get(),
    productSupplier.get(), productQuantity.get(), productTotalCost.get(), productDateReceived.get(), "0"])

    # ADD TO IDLIST
    idList.append(int(productID.get()))

    SetProductID()

    if (len(idList) == 10):
        productID.set("MAX")

    # SHOW TABLE
    ProductsTable()

    # DELETE VARIATION TABLE
    for widget in windowProducts.grid_slaves():
        if int(widget.grid_info()["row"]) > len(Stocks.products) + 2 and int(widget.grid_info()["column"]) > 4:
            widget.grid_forget()
    
    # SHOW VARIATIONS TABLE
    VariationsTable()

    # WRITE PRODUCTS FILE
    Stocks.WriteProductsFile()
    Stocks.WriteStockInsFile()
    
def AddVariation():
    Stocks.SetProductVariations([productID.get(), productType.get(), productDescription.get(),
    productSupplier.get(), productQuantityAdd.get(), productTotalCost.get(), productDateReceived.get(), "0"])

    ProductsTable()
    VariationsTable()
    Stocks.WriteStockInsFile()

def OnClickProductEntry(event):
    global selectedRow, selectedVariation
    selectedRow = event.widget._index
    selectedVariation = None

    productID.set(Stocks.products[selectedRow][0])
    productType.set(Stocks.products[selectedRow][1])
    productDescription.set(Stocks.products[selectedRow][2])
    productSupplier.set(Stocks.products[selectedRow][3])
    productQuantity.set(Stocks.products[selectedRow][4])
    productTotalCost.set("")
    productQuantityAdd.set("")

    # DELETE VARIATION TABLE
    for widget in windowProducts.grid_slaves():
        if int(widget.grid_info()["row"]) > len(Stocks.products) + 2 and int(widget.grid_info()["column"]) > 4:
            widget.grid_forget()
    VariationsTable() 

def OnClickVariationEntry(event):
    global selectedVariation
    selectedVariation = event.widget._index
    print(selectedVariation)

def ButtonNewProductClicked():
    errorFlag = False
    message = "Please input a valid:\n"
    if productType.get() == "":
        errorFlag = True
        message += "- Product Type\n"
    if productDescription.get() == "":
        errorFlag = True
        message += "- Product Description\n"
    if productSupplier.get() == "":
        errorFlag = True
        message += "- Product Supplier\n"
    if productQuantity.get() == "" or CheckNumber(productQuantity.get()):
        errorFlag = True
        message += "- Quantity\n"
    if productTotalCost.get() == "" or CheckNumber(productTotalCost.get()):
        errorFlag = True
        message += "- Total Cost\n"
    if productID.get() == "MAX":
        errorFlag = True
        message = "MAXIMUM PRODUCTS REACHED!\n"

    if errorFlag == False:
        # SUCCESS
        message = "Save?"
        DialogBox(message, "Record Information")
        AddProduct()
    else:
        DialogBox(message, "Error")

def ButtonStockInClicked():
    errorFlag = False
    message = "Please input a valid:\n"
    if productType.get() == "":
        errorFlag = True
        message += "- Product Type\n"
    if productDescription.get() == "":
        errorFlag = True
        message += "- Product Description\n"
    if productSupplier.get() == "":
        errorFlag = True
        message += "- Product Supplier\n"
    if productQuantityAdd.get() == "" or CheckNumber(productQuantityAdd.get()):
        errorFlag = True
        message += "- Additional Quantity\n"
    if productTotalCost.get() == "" or CheckNumber(productTotalCost.get()):
        errorFlag = True
        message += "- Total Cost\n"
    if productID.get() != "MAX":
        if int(productID.get()) not in idList:
            errorFlag = True
            message = "- Product is non-existent!\n"
    else:
        errorFlag = True
        message = "Select a row!\n"
    if Stocks.productVariations[selectedRow][9][0] != 0 and Stocks.productVariations[selectedRow][9][0] != '0':
        errorFlag = True
        message = "- MAXIMUM VARIATIONS!"
        

    if errorFlag == False:
        # SUCCESS
        message = "Save?"
        DialogBox(message, "Record Information")
        AddVariation()
    else:
        DialogBox(message, "Error")