from tkinter import *
#from PIL import ImageTk, Image
from re import search
import sqlite3
import datetime

root = Tk()
root.title('Car Rental Server')
root.geometry("400x400")

conn = sqlite3.connect('CarRental.db')
c = conn.cursor()

# add new customer
def createNewCustWindow():

    def submitCustomer():
        conn = sqlite3.connect('CarRental.db')
        c = conn.cursor()
        #print("This is the name" + Name)
        c.execute("INSERT INTO Customer(Name, Phone) VALUES(:Name, :Phone)",
                    {
                        'Name': Name.get(),
                        'Phone': Phone.get()
                    })

        #commit changes
        conn.commit()

        #close connection
        conn.close()

        #clear the text boxes
        Name.delete(0, END)
        Phone.delete(0, END)

    custWindow = Toplevel(root)
    custWindow.geometry("400x400")
    custWindow.title('New Customer Registration')

    conn = sqlite3.connect('CarRental.db')
    c = conn.cursor()

    # entry box
    Name = Entry(custWindow, width =30)
    Name.grid(row = 1, column =1,  padx = 20)

    Phone = Entry(custWindow, width =30)
    Phone.grid(row = 2, column =1)

    #labels
    newCustLabel = Label(custWindow, text = "Please add the new customer's information")
    newCustLabel.grid(row = 0, column =0, columnspan = 2)

    NameLabel = Label(custWindow, text = "Full Name")
    NameLabel.grid(row =1, column =0)

    PhoneLabel = Label(custWindow, text = "Phone Number")
    PhoneLabel.grid(row =2, column =0)


    submitButton = Button(custWindow, text="Save new customer to DB", command = submitCustomer)
    submitButton.grid(row=6, column =0, columnspan = 2, pady=10, padx=10, ipadx=100 )

    quitButton = Button(custWindow, text="Exit without saving", command = custWindow.destroy)
    quitButton.grid(row=7, column =0, columnspan = 2, pady=10, padx=10, ipadx=100 )

    conn.close()



# add new vehicle
def createNewVehicleWindow():
    def submitVehicle():

        conn = sqlite3.connect('CarRental.db')
        c = conn.cursor()

        c.execute("INSERT INTO Vehicle VALUES(:VehicleID, :Description, :Year, :Type, :Category)",
                    {
                        'VehicleID': VehicleID.get(),
                        'Description': Description.get(),
                        'Year': Year.get(),
                        'Type': Type.get(),
                        'Category': Category.get()
                    })
            #c.execute("SELECT * from addresses where city = ? AND state = ?",(city.get(), state.get()))

        #commit changes
        conn.commit()

        #close connection
        conn.close()

        #clear the text boxes
        VehicleID.delete(0, END)
        Description.delete(0, END)
        Year.delete(0, END)
        Type.delete(0, END)
        Category.delete(0, END)




    vehiWindow = Toplevel(root)
    vehiWindow.geometry("400x400")
    vehiWindow.title('New Vehicle Registration')

    conn = sqlite3.connect('CarRental.db')
    c = conn.cursor()

    # entry box
    VehicleID = Entry(vehiWindow, width =30)
    VehicleID.grid(row = 1, column =1,  padx = 20)

    Description = Entry(vehiWindow, width =30)
    Description.grid(row = 2, column =1)

    Year = Entry(vehiWindow, width =30)
    Year.grid(row = 3, column =1)

    Type = Entry(vehiWindow, width =30)
    Type.grid(row = 4, column =1)

    Category = Entry(vehiWindow, width =30)
    Category.grid(row = 5, column =1)

    #labels
    newCustLabel = Label(vehiWindow, text = "Please add the new vehicle's information")
    newCustLabel.grid(row = 0, column =0, columnspan = 2)

    VINLabel = Label(vehiWindow, text = "ID Number (VIN)")
    VINLabel.grid(row =1, column =0)

    DescriptionLabel = Label(vehiWindow, text = "Description")
    DescriptionLabel.grid(row =2, column =0)

    YearLabel = Label(vehiWindow, text = "Year")
    YearLabel.grid(row =3, column =0)

    TypeLabel = Label(vehiWindow, text = "Type (type 1 for Compact,\n 2 for Medium, 3 for Large, \n 4 for SUV, 5 for Truck, \n or 6 for Van)")
    TypeLabel.grid(row =4, column =0)

    CategoryLabel = Label(vehiWindow, text = "Category (type 0 for Basic,\n 1 for Luxury)")
    CategoryLabel.grid(row =5, column =0)


    submitButton = Button(vehiWindow, text="Save new vehicle to DB", command = submitVehicle)
    submitButton.grid(row=8, column =0, columnspan = 2, pady=10, padx=10, ipadx=100 )

    quitButton = Button(vehiWindow, text="Exit without saving", command = vehiWindow.destroy)
    quitButton.grid(row=9, column =0, columnspan = 2, pady=10, padx=10, ipadx=100 )

    conn.close()



# new reservation
# ask for start and return date
# ask for type and ask for category
# then show menu of availble cars
def createNewRentalWindow():

    def findVehicle():

        def getCustomer(StartDate, ReturnDate, Qty, RentalType, Rate):

            def newRental(rentalVehicle, vcustPhone, paid, vStartDate, vReturnDate, vQty, vRentalType, vRate):
                #print(rentalVehicle, vcustPhone, paid)

                conn = sqlite3.connect('CarRental.db')
                c = conn.cursor()

                c.execute("SELECT CustID FROM Customer WHERE Phone = '" + vcustPhone + "'")

                vCustID = c.fetchone()[0] #.replace('(','').replace(')','').replace(',','')
                #print(vCustID)

                c.execute("SELECT DATE()")
                vOrderDate = c.fetchone()[0]

                vPaymentDate = 'NULL'

                # if paid = 1 then payment day = vOrderDate, else NULL
                if paid == 1:
                    vPaymentDate = vOrderDate

                vTotalAmount = int(vRate) * int(vQty)

                vVehicleID = rentalVehicle[2]
                #print(vVehicleID)


                # MAKE THE RENTAL IN SQL

                print("INSERT INTO Rental " +
                "VALUES(" + str(vCustID) + ", '" + vVehicleID +"', '" + vStartDate +
                "', '" + vOrderDate + "', " + vRentalType + ", " + str(vQty) +
                ", '" + vReturnDate + "', " + str(vTotalAmount) + ", '" + vPaymentDate + "', 0)")

                c.execute("INSERT INTO Rental " +
                "VALUES(" + str(vCustID) + ", '" + vVehicleID +"', '" + vStartDate +
                "', '" + vOrderDate + "', " + vRentalType + ", " + str(vQty) +
                ", '" + vReturnDate + "', " + str(vTotalAmount) + ", '" + vPaymentDate + "', 0)")

                createdLabel = Label(rentWindow, text = "Your Rental has been reserved")
                createdLabel.grid(row = 10, column = 0)

                conn.commit()
                conn.close()


            rentalVehicle = (selected.get()).replace(', ', ':').replace('\'','').replace('(', '').replace(')', '').split(':')
            vStartDate = StartDate
            vReturnDate = ReturnDate
            vQty = Qty
            vRentalType = RentalType
            vRate = Rate


            custPhone = Entry(rentWindow, width =20)
            custPhone.grid(row = 8, column =1)

            custPhoneLabel = Label(rentWindow, text = "Customer Phone Number:")
            custPhoneLabel.grid(row =8, column =0)

            paid = IntVar()
            payNow = Checkbutton(rentWindow, text="Pay now?", variable=paid)
            payNow.grid(row=9, column = 0)

            rentalButton = Button(rentWindow, text = "Create New Rental", command = lambda : newRental(rentalVehicle, custPhone.get(), paid.get(), vStartDate, vReturnDate, vQty, vRentalType, vRate))
            rentalButton.grid(row=9, column = 1)



        conn = sqlite3.connect('CarRental.db')
        c = conn.cursor()

        vType = Type.get()
        vCategory = Category.get()
        vStartDate = StartDate.get()
        vRentalType = RentalType.get()
        vQty = Qty.get()
        vReturnDate = vStartDate
        vRate = '500'

        if vRentalType == '1':
            print("hello")
            c.execute("SELECT DATE('" + vStartDate + "', '" + vQty + " days') AS mydate")
            vReturnDate = c.fetchall()

            c.execute("SELECT Daily From Rate WHERE Type = " + vType + " AND Category = " + vCategory)
            vRate = c.fetchone()[0]
        elif vRentalType == '7':
            days = int(vQty) * 7
            c.execute("SELECT DATE('" + vStartDate + "', '" + str(days) + " days') AS mydate")
            vReturnDate = c.fetchall()

            c.execute("SELECT Weekly From Rate WHERE Type = " + vType + " AND Category = " + vCategory)
            vRate = c.fetchone()[0]


        #print(vReturnDate[0][0])

        c.execute( "SELECT V.Year, V.Description, V.VehicleID FROM Vehicle V WHERE V.type = " + vType + " AND V.category = " +
                    vCategory + " AND v.vehicleid NOT IN (select V.Vehicleid FROM vehicle V LEFT JOIN RENTAL R ON " +
                    "v.vehicleID = R.vehicleID WHERE NOT((R.startDate < '" + vStartDate +"') OR" +
                   "(R.returnDate > '" + vReturnDate[0][0] + "')))")

        foundVehicles = list(c.fetchall())

        vehicles = foundVehicles

        selected = StringVar()
        selected.set(vehicles[0]) #sets the default option of options

        availbleVehicles = OptionMenu(rentWindow, selected, *vehicles)
        availbleVehicles.grid(row = 5, column = 1)

        SelectButton = Button( rentWindow , text = "Select vehicle" , command = lambda : getCustomer(vStartDate, vReturnDate[0][0], vQty, vRentalType, vRate))
        SelectButton.grid(row = 6, column = 0)

        conn.close()


    rentWindow = Toplevel(root)
    rentWindow.geometry("500x500")
    rentWindow.title('New Rental')

    conn = sqlite3.connect('CarRental.db')
    c = conn.cursor()

    Type = Entry(rentWindow, width =10)
    Type.grid(row = 1, column =1)

    Category = Entry(rentWindow, width =10)
    Category.grid(row = 2, column =1)

    StartDate = Entry(rentWindow, width =10)
    StartDate.grid(row = 1, column =3)

    RentalType = Entry(rentWindow, width =10)
    RentalType.grid(row = 2, column =3)

    Qty = Entry(rentWindow, width = 10)
    Qty.grid(row=3, column = 3)



    TypeLabel = Label(rentWindow, text = "Type (type 1 for Compact,\n 2 for Medium, 3 for Large, \n 4 for SUV, 5 for Truck, \n or 6 for Van)")
    TypeLabel.grid(row =1, column =0)

    CategoryLabel = Label(rentWindow, text = "Category (type 0 for Basic,\n 1 for Luxury)")
    CategoryLabel.grid(row =2, column =0)

    StartDateLabel = Label(rentWindow, text = "Start Date (must be in \n YYYY-MM-DD format)")
    StartDateLabel.grid(row = 1, column =2)

    RentalTypeLabel = Label(rentWindow, text = "Rental Type (type 1 Daily \n or 7 for Weeks)")
    RentalTypeLabel.grid(row = 2, column =2)

    QtyLabel = Label(rentWindow, text = "How Many?")
    QtyLabel.grid(row = 3, column = 2)


    submitButton = Button(rentWindow, text="Find availble vehicles", command = findVehicle)
    submitButton.grid(row=4, column =0, columnspan = 2, pady=10, padx=10)

    quitButton = Button(rentWindow, text="Exit", command = rentWindow.destroy)
    quitButton.grid(row=13, column =0, columnspan = 2, pady=10, padx=10, ipadx=50 )

    conn.close()


# return rental
def createReturnRentalWindow():

    def retreveRental():
        conn = sqlite3.connect('CarRental.db')
        c = conn.cursor()


        vReturnDate = ReturnDate.get()
        vName = Name.get()
        vVehicleID = VehicleID.get()
        vBalance = '$0.00'

        c.execute("SELECT CustID FROM Customer WHERE Name = '" + vName + "'")
        vCustID = c.fetchone()[0]

        c.execute("SELECT PaymentDate FROM Rental WHERE CustID = '" + str(vCustID) + "' AND VehicleID = '" +
                  vVehicleID + "' AND ReturnDate = '" + vReturnDate +"'")
        vPaymentDate = c.fetchone()[0]
        print(vPaymentDate)

        if str(vPaymentDate) == "None":
            c.execute("SELECT DATE()")
            vPaymentDate = c.fetchone()[0]

            c.execute("UPDATE Rental SET Returned = 1, PaymentDate = '" + vPaymentDate + "' WHERE CustID = '" + str(vCustID) +
                      "' AND VehicleID = '" + vVehicleID + "' AND ReturnDate = '" + vReturnDate +"'")

            c.execute("SELECT TotalAmount FROM Rental WHERE CustID = '" + str(vCustID) + "' AND VehicleID = '" +
                      vVehicleID + "' AND ReturnDate = '" + vReturnDate +"'")
            money = c.fetchone()[0]
            vBalance = "${:,.2f}".format(float(money))
        else:
            c.execute("UPDATE Rental SET Returned = 1 WHERE CustID = '" + str(vCustID) +
                      "' AND VehicleID = '" + vVehicleID + "' AND ReturnDate = '" + vReturnDate +"'")


        balanceLabel = Label(returnWindow, text = "The remaining balance is: " + vBalance)
        balanceLabel.grid(row = 6, column = 0)

        conn.commit()
        conn.close()

    returnWindow = Toplevel(root)
    returnWindow.geometry("500x500")
    returnWindow.title('Return Rental')

    conn = sqlite3.connect('CarRental.db')
    c = conn.cursor()

    PromptLabel = Label(returnWindow, text = "Enter information to retrieve rental order")
    PromptLabel.grid(row = 1, column = 0, columnspan = 2)

    ReturnDate = Entry(returnWindow, width = 25)
    ReturnDate.grid(row = 2, column = 1)

    Name = Entry(returnWindow, width = 25)
    Name.grid(row = 3, column = 1)

    VehicleID = Entry(returnWindow, width = 25)
    VehicleID.grid(row = 4, column = 1)

    submitButton = Button(returnWindow, text = "Find Rental", command = retreveRental)
    submitButton.grid(row = 5, column = 0, columnspan = 2)


    ReturnDateLabel = Label(returnWindow, text = "Return Date (must be in \n YYYY-MM-DD format)")
    ReturnDateLabel.grid(row = 2, column = 0)

    NameLabel = Label(returnWindow, text = "Customer Name (FI. Last Name)")
    NameLabel.grid(row = 3, column = 0)

    VehicleIDLabel = Label(returnWindow, text = "Vehicle Identification Number")
    VehicleIDLabel.grid(row = 4, column = 0)

    quitButton = Button(returnWindow, text="Exit", command = returnWindow.destroy)
    quitButton.grid(row=13, column =0, columnspan = 2, pady=10, padx=10, ipadx=50 )

    conn.close()

# view results
# 	- every customer
# 5a
def createViewCustomersWindow():
    def retrieveCustomerResult():

        conn = sqlite3.connect('CarRental.db')
        c = conn.cursor()

        for query_label in customerWindow.grid_slaves():
            if( query_label.grid_info()["row"]) == 10:
                query_label.grid_forget()

        vCustID = CustomerID.get()
        vName = Name.get()
        vBalance = '$0.00'

        print_records = f"{'Customer ID':<25}{'Name':^25}{'Remaining Balance':>25}\n"

        if len(vCustID) == 0 and len(vName) == 0:
            c.execute("SELECT CustomerID, CustomerName, RentalBalance FROM vRentalInfo GROUP BY CustomerName")
            records = c.fetchall()
            for record in records:
                money = "${:,.2f}".format(float(record[2]))
                print_records += f"{str(record[0]):<25}{str(record[1]):^25}{money:>25}\n"

        elif len(vCustID) != 0 and len(vName) == 0:
            c.execute("SELECT CustomerID, CustomerName, RentalBalance FROM vRentalInfo WHERE CustomerID = '" + str(vCustID)+ "' GROUP BY CustomerName")
            records = c.fetchall()
            for record in records:
                money = "${:,.2f}".format(float(record[2]))
                print_records += f"{str(record[0]):<25}{str(record[1]):^25}{money:>25}\n"

        elif len(vCustID) == 0 and len(vName) != 0:
                c.execute("SELECT CustomerID, CustomerName, RentalBalance FROM vRentalInfo GROUP BY CustomerName")
                tempRecords = c.fetchall()
                for tempRecord in tempRecords:
                    print(vName)
                    print(str(tempRecord[1]));
                    if search(vName, str(tempRecord[1])):
                        money = "${:,.2f}".format(float(tempRecord[2]))
                        print_records += f"{str(tempRecord[0]):<25}{str(tempRecord[1]):^25}{money:>25}\n"

        else:
            c.execute("SELECT CustomerID, CustomerName, RentalBalance FROM vRentalInfo GROUP BY CustomerName")
            tempRecords = c.fetchall()
            for tempRecord in tempRecords:
                if search(vName, str(tempRecord[1])):
                    c.execute("SELECT CustomerID, CustomerName, RentalBalance FROM vRentalInfo WHERE CustomerID = '" + str(vCustID) + "' AND CustomerName = '" +str(tempRecord[1]) + "' GROUP BY CustomerName")
                    records = c.fetchall()
                    for record in records:
                        money = "${:,.2f}".format(float(record[2]))
                        print_records += f"{str(record[0]):<25}{str(record[1]):^25}{money:>25}\n"

        query_label = Label(customerWindow, text = print_records)
        query_label.grid( row =10, column =0, columnspan=2)

        conn.commit()
        conn.close()

    customerWindow = Toplevel(root)
    customerWindow.geometry("400x400")
    customerWindow.title('View Customer Balance')


    conn = sqlite3.connect('CarRental.db')
    c = conn.cursor()

    PromptLabel = Label(customerWindow, text = "Enter information to view remaining balance ")
    PromptLabel.grid(row = 1, column = 0, columnspan = 2)

    CustomerID = Entry(customerWindow, width = 25)
    CustomerID.grid(row = 3, column = 1)

    Name = Entry(customerWindow, width = 25)
    Name.grid(row = 4, column = 1)

    submitButton = Button(customerWindow , text = "Get Balance", command = retrieveCustomerResult)
    submitButton.grid(row = 6, column = 0, columnspan = 2)


    CustomerIDLabel = Label(customerWindow , text = "Customer ID")
    CustomerIDLabel.grid(row = 3, column = 0)

    NameLabel = Label(customerWindow , text = "Customer Name")
    NameLabel.grid(row = 4, column = 0)


    quitButton = Button(customerWindow , text="Exit", command = customerWindow .destroy)
    quitButton.grid(row=13, column =0, columnspan = 2, pady=10, padx=10, ipadx=50 )

    conn.close()



# 5b
def createViewVehiclesWindow():
    def retrieveVehicleResult():
        conn = sqlite3.connect('CarRental.db')
        c = conn.cursor()

        for query_label in vehicleWindow.grid_slaves():
            if(query_label.grid_info() ["row"]) == 10:
                query_label.grid_forget()

        vVIN = VIN.get()
        vDescription = Description.get()
        vBalance = '$0.00'

        printVehicles = f"{'VIN':<25}{'Vehicles description':^25}{'Rate':>25}{'Available':<10}\n"

        if len(vVIN) == 0 and len(vDescription) == 0:
            c.execute("SELECT VehicleID, Description, Daily FROM Vehicle NATURAL JOIN Rate GROUP BY Description ORDER BY Daily ASC ")
            Vehicles = c.fetchall()
            for Vehicle in Vehicles:
                rate = "${:,.2f}".format(float(Vehicle[2]))
                printVehicles += f"{str(Vehicle[0]):<25}{str(Vehicle[1]):^25}{rate:>25}\n"

        elif len(vVIN) !=0 and len(vDescription) == 0:
            c.execute("SELECT VehicleID, Description, Daily FROM Vehicle NATURAL JOIN Rate  WHERE VehicleID = '"+ str(vVIN)+"' GROUP BY VehicleID")
            Vehicles = c.fetchall()
            for Vehicle in Vehicles:
                rate = "${:,.2f}".format(float(Vehicle[2]))
                printVehicles += f"{str(Vehicle[0]):<30}{str(Vehicle[1]):^25}{rate:>25}\n"

        elif len(vVIN) == 0 and len(vDescription) != 0:
            c.execute("SELECT VehicleID, Description, Daily FROM Vehicle NATURAL JOIN Rate ")
            tempVehicles = c.fetchall()
            for tempVehicle in tempVehicles:
                print(vVIN)
                print(str(tempVehicle[1]));
                if search(vDescription, str(tempVehicle[1])):
                    rate = "${:,.2f}".format(float(tempVehicle[2]))
                    printVehicles += f"{str(tempVehicle[0]):<25}{str(tempVehicle[1]):^25}{rate:>25}\n"


        query_label = Label(vehicleWindow, text = printVehicles);
        query_label.grid( row =10, column =0, columnspan=2)


        conn.commit()
        conn.close()

    vehicleWindow = Toplevel(root)
    vehicleWindow.geometry("400x400")
    vehicleWindow.title('View Vehicle Information')

    conn = sqlite3.connect('CarRental.db')
    c = conn.cursor()

    PromptLabel = Label(vehicleWindow, text = "Enter information to view Vehicle ")
    PromptLabel.grid(row = 1, column = 0, columnspan = 2)

    VIN = Entry(vehicleWindow, width = 25)
    VIN.grid(row = 3, column = 1)

    Description = Entry(vehicleWindow, width = 25)
    Description.grid(row = 4, column = 1)


   # submitButton = Button(vehicleWindow , text = "Get Balance", lambda: [f() for f in [retrieveVehicleResult, funct2]])


    submitButton = Button(vehicleWindow , text = "View Vehicles", command = retrieveVehicleResult)
    submitButton.grid(row = 6, column = 0, columnspan = 2)


    VINLabel = Label(vehicleWindow , text = "VIN")
    VINLabel.grid(row = 3, column = 0)

    DescriptionLabel = Label(vehicleWindow , text = "Vehicle Description")
    DescriptionLabel.grid(row = 4, column = 0)


    quitButton = Button(vehicleWindow , text="Exit", command = vehicleWindow .destroy)
    quitButton.grid(row=13, column =0, columnspan = 2, pady=10, padx=10, ipadx=50 )

    conn.close()





label = Label(root, text = 'Car Rental Application')
label.grid(row = 0, column =2,  padx = 70)

newCustButton = Button(root, text='New Customer Registration', command = createNewCustWindow)
newCustButton.grid(row = 2, column =2,  padx = 70)

newVehicleButton = Button(root, text='New Vehicle Registration', command = createNewVehicleWindow)
newVehicleButton.grid(row = 4, column =2,  padx = 70)

newRentalButton = Button(root, text='New Rental', command = createNewRentalWindow)
newRentalButton.grid(row = 6, column =2,  padx = 70)

returnVehicleButton = Button(root, text='Return a Vehicle', command = createReturnRentalWindow)
returnVehicleButton.grid(row = 8, column =2,  padx = 70)

viewCustomersBButton = Button(root, text='View All Customers', command = createViewCustomersWindow)
viewCustomersBButton.grid(row = 10, column =2,  padx = 70)

viewVehiclesButton = Button(root, text='View All Vehicles', command = createViewVehiclesWindow)
viewVehiclesButton.grid(row = 12, column =2,  padx = 70)

root.mainloop()


def viewCustomerWindow():


    conn = sqlite3.connect('CarRental.db')
    c = conn.cursor()
