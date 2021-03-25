import csv
from os import remove
from tkinter import image_types

# INCLUDES ALL THE METHODS TO USE IN PRODUCTS
productVariations = list() # 3D
products = list() # 2D
customerOrders = list() # 3D
customerOrdersIn2D = list() # TEMPORARY 2D
productVariationsIn2D = list() # TEMPORARY 2D
nextVariation = 0
emptyOrderSlotIndex = 0

#BOUNDS
x = 10 # PRODUCT TYPE
z = 10 # VARIATIONS
y = 8 #COLUMNS

# INITIALIZE VALUES FOR productVariations
for a in range(x):
    productVariations.append([])
    for b in range(z):
        productVariations[a].append([])
        for c in range(y):
            productVariations[a][b].append(0)

# INITIALIZE VALUES FOR customerOrders
for a in range(x):
    customerOrders.append([])
    for b in range(z):
        customerOrders[a].append([])
        for c in range(y):
            customerOrders[a][b].append(None)

def PrintArray():
    for a in range(x):
        for b in range(z):
            for c in range(y):
                print(customerOrders[a][b][c], end = ", ")
            print("")
        print("")
    print("--END--")

def PrintProductVariationsArray():
    for a in range(x):
        for b in range(z):
            for c in range(y):
                print(productVariations[a][b][c], end = ", ")
            print("")
        print("")
    print("--END--")

def SetProduct(product): #ACCEPTS A LIST (1D)
    products.append([product[0], product[1], product[2], product[3], product[4], product[7]])

    if product[0] not in productVariations:
        SetProductVariations(product)

def NextVariation(product):
    global nextVariation
    nextVariation = 0

    for x in range(len(productVariations[0])):
        if productVariations[int(product[0])-1][x][0] == 0 or productVariations[int(product[0])-1][x][0] == '0':
            nextVariation = x
            break

def SetProductVariations(product):
    NextVariation(product)

    productVariations[int(product[0])-1][nextVariation] = product

    if nextVariation != 0:
        products[int(product[0])-1][4] = int(products[int(product[0])-1][4]) + int(product[4])
        WriteProductsFile()
        WriteStockInsFile()

def SetEmptyOrderIndex(selectedCustomer):
    global emptyOrderSlotIndex
    for i in range(len(customerOrders[0])):
        if customerOrders[selectedCustomer][i][0] == None or customerOrders[selectedCustomer][i][0] == '':
            emptyOrderSlotIndex = i
            break
        elif customerOrders[selectedCustomer][9][0] != None and customerOrders[selectedCustomer][9][0] != '':
            emptyOrderSlotIndex = 9
            break

def SetOrders(order, selectedCustomer, selectedVariation, selectedRow): # ACCEPTS 1D LIST
    global customerOrders
    SetEmptyOrderIndex(selectedCustomer)
    arrayFound = -1

    for i in range(len(customerOrders[0][0])):
        if str(customerOrders[selectedCustomer][i][0]) == str(selectedVariation) and str(customerOrders[selectedCustomer][i][2]) == str(selectedRow + 1):
            arrayFound = i

    if arrayFound != -1:
        customerOrders[selectedCustomer][arrayFound][5] = str(int(customerOrders[selectedCustomer][arrayFound][5])+1)
        UpdateOrders(customerOrders[selectedCustomer][arrayFound][2], customerOrders[selectedCustomer][arrayFound][0])
    elif arrayFound == -1:
        customerOrders[selectedCustomer][emptyOrderSlotIndex] = order
        UpdateOrders(customerOrders[selectedCustomer][emptyOrderSlotIndex][2], customerOrders[selectedCustomer][emptyOrderSlotIndex][0])

    arrayFound = -1

def UpdateOrders(productID, selectedVariation):
    id = int(productID)
    variation = int(selectedVariation)

    productVariations[id-1][variation][7] = str(int(productVariations[id-1][variation][7]) + 1)
    productVariations[id-1][variation][4] = str(int(productVariations[id-1][variation][4]) - 1)
    products[id-1][5] = str(int(products[id-1][5]) + 1)
    products[id-1][4] = str(int(products[id-1][4]) - 1)

def WriteOrdersFile():
    global customerOrdersIn2D

    customerOrdersIn2D = []
    for group in customerOrders:
        for row in group:
            customerOrdersIn2D.append(row)

    with open("orders.csv", "w", newline="") as file:
        write = csv.writer(file)
        write.writerows(customerOrdersIn2D)

def ReadOrdersFile():
    global customerOrders, idList

    with open("orders.csv", "r") as file:
        reader = csv.reader(file)
        customerOrdersIn2D = list(reader)

    customerOrders = []
    count = 0
    for a in range(x):
        customerOrders.append([])
        for b in range(z):
            customerOrders[a].append([])
            for c in range(y):
                customerOrders[a][b].append(customerOrdersIn2D[count][c])
            count = count + 1

def WriteProductsFile():
    with open("products.csv", "w", newline="") as file:
        write = csv.writer(file)
        write.writerows(products)

def ReadProductsFile():
    global products

    with open("products.csv", "r") as file:
        reader = csv.reader(file)
        products = list(reader)
    
def WriteStockInsFile():
    global productVariationsIn2D

    productVariationsIn2D = []
    for group in productVariations:
        for row in group:
            productVariationsIn2D.append(row)

    with open("stockins.csv", "w", newline="") as file:
        write = csv.writer(file)
        write.writerows(productVariationsIn2D)

def ReadStockInsFile():
    global productVariations

    with open("stockins.csv", "r") as file:
        reader = csv.reader(file)
        productVariationsIn2D = list(reader)

    productVariations = []
    count = 0
    for a in range(x):
        productVariations.append([])
        for b in range(z):
            productVariations[a].append([])
            for c in range(y):
                productVariations[a][b].append(productVariationsIn2D[count][c])
            count = count + 1

    #PrintProductVariationsArray()
    