# ***********************************************************************************************************************
# *                                                                                                                     *
# *   MainWindow.py                                                                                                     *
# *   Authors: Robert B. Wilson, Alex Baker, Jordan Phillips, Gabriel Snider, Steven Dorsey, Yoshinori Agari            *
# *   The purpose of this file is to load the MainWindow UI file upon initialization and also provide logic for         *
# *   all of the widgets used throughout the MainWindow UI                                                              *
# *                                                                                                                     *
# ***********************************************************************************************************************

import PyQt5
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import *
import sys
from classes.Database import Database
from classes.User import User
from classes.Security import Security

class MainWindow(QtWidgets.QMainWindow):
    # Function: Constructor
    # Parameters: None
    # Return: MainWindow UI object
    # Loads the MainWindow.UI file and initializes all of the widget logic
    def __init__(self):
        # Call QMainWindow Constructor
        super(MainWindow, self).__init__()
        # Load MainWindow.UI
        uic.loadUi(r"./views/MainWindow.ui", self)
        # Initialize User
        self.User = User()
        # Initialize Security Object
        self.Security = Security()
        # Load Widgets
        self.Admin_Button = self.findChild(QtWidgets.QLabel, "Admin_Button")
        self.Stacked_Widget = self.findChild(QtWidgets.QStackedWidget, "stackedWidget")
        self.Login_Button = self.findChild(QtWidgets.QPushButton, "Login_Button")
        self.Username_LineEdit = self.findChild(QtWidgets.QLineEdit, "Username_LineEdit")
        self.Password_LineEdit = self.findChild(QtWidgets.QLineEdit, "Password_LineEdit")
        self.Users_List = self.findChild(QtWidgets.QListWidget, "Users_List")
        self.AddUser_Button = self.findChild(QtWidgets.QPushButton, "AddUser_Button")
        self.NewUserUsername_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewUserUsername_LineEdit")
        self.NewUserPassword_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewUserPassword_LineEdit")
        self.DeleteUsers_Button = self.findChild(QtWidgets.QPushButton, "DeleteUsers_Button")
        self.LoginError_Label = self.findChild(QtWidgets.QLabel, "LoginError_Label")
        self.NewConnectionServer_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionServer_LineEdit")
        self.NewConnectionUsername_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionUsername_LineEdit")
        self.NewConnectionPassword_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionPassword_LineEdit")
        self.NewConnectionRemoteDirectory_LineEdit = self.findChild(QtWidgets.QLineEdit, "NewConnectionRemoteDirectory_LineEdit")
        self.AddConnection_Button = self.findChild(QtWidgets.QPushButton, "AddConnection_Button")
        self.AdminConnections_Table = self.findChild(QtWidgets.QTableWidget, "AdminConnections_Table")
        self.DeleteConnectionsButton = self.findChild(QtWidgets.QPushButton, "DeleteConnections_Button")
        self.PresetsConnections_Table = self.findChild(QtWidgets.QTableWidget, "PresetsConnections_Table")
        self.PresetsFileSelector_Button = self.findChild(QtWidgets.QPushButton, "PresetsFileSelector_Button")
        self.PresetsFiles_List = self.findChild(QtWidgets.QListWidget, "PresetsFiles_List")
        self.PresetsConnections_Table = self.findChild(QtWidgets.QTableWidget, "PresetsConnections_Table")
        self.PresetsFilesClear_Button = self.findChild(QtWidgets.QPushButton, "PresetsFilesClear_Button")
        self.PresetsDisplayAll_Button = self.findChild(QtWidgets.QPushButton, "PresetsDisplayAll_Button")
        self.PresetsName_LineEdit = self.findChild(QtWidgets.QLineEdit, "PresetsName_LineEdit")
        self.PresetsAddPreset_Button = self.findChild(QtWidgets.QPushButton, "PresetsAddPreset_Button")

        # Connect Event Logic
        self.Admin_Button.mousePressEvent = self.Admin_Button_Logic
        self.Login_Button.clicked.connect(self.Login_Button_Logic)
        self.AddUser_Button.clicked.connect(self.AddUser_Button_Logic)
        self.DeleteUsers_Button.clicked.connect(self.DeleteUsers_Button_Logic)
        self.AddConnection_Button.clicked.connect(self.AddConnection_Button_Logic)
        self.DeleteConnections_Button.clicked.connect(self.DeleteConnections_Button_Logic)
        self.PresetsFileSelector_Button.clicked.connect(self.PresetsFileSelector_Button_Logic)
        self.PresetsFilesClear_Button.clicked.connect(self.PresetsFilesClear_Button_Logic)
        self.PresetsDisplayAll_Button.clicked.connect(self.PresetsDisplayAll_Button_Logic)
        self.PresetsAddPreset_Button.clicked.connect(self.PresetsAddPreset_Button_Logic)

        # Initialize default Stacked Widget Page
        self.Stacked_Widget.setCurrentIndex(0)
        # Initialize Users List
        self.Display_Users()
        # Initialize Connection Tables
        self.Display_Connections()
        # Initialize Error Messages to Hidden
        self.LoginError_Label.hide()
        # Display Window
        self.show()
    


    # Function: Admin_Button_Logic
    # Parameters: mousePressedEvent
    # Return: None
    # Checks if a user has been logged in, if yes --> it changes the current stacked widget index to the admin page. If no --> it changes the current stacked widget index to the login page.
    def Admin_Button_Logic(self, event):
        # case user is at the home page and not logged in
        if self.Stacked_Widget.currentIndex() == 0 and not self.User.isAuthenticated:
            self.Stacked_Widget.setCurrentIndex(1)
            self.Admin_Button.setText("Home")
        # case user is at the home page and are logged in
        elif self.Stacked_Widget.currentIndex() == 0 and self.User.isAuthenticated:
            self.Stacked_Widget.setCurrentIndex(2)
            self.Admin_Button.setText("Home")
        # case user is at the login page
        elif self.Stacked_Widget.currentIndex() == 1:
            self.Stacked_Widget.setCurrentIndex(0)
            self.Admin_Button.setText("Admin")
        # case user is at the admin page
        else:
            self.Stacked_Widget.setCurrentIndex(0)
            self.Admin_Button.setText("Admin")
    


    # Function: Login_Button_Logic
    # Parameters: None
    # Return: None
    # Fetches text from Username and Password QLineEdit Widgets and attempts to authenticate the user based on this data. If the user is authenticated, the user will be redirected to the admin page. Otherwise a invalid login notification will be displayed.
    def Login_Button_Logic(self):
        # get username and password claims
        username = self.Username_LineEdit.text()
        password = self.Password_LineEdit.text()
        # Show loading cursor
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        # convert password to hashed version
        hashedPassword = self.Security.getMD5(password)
        # attempt to authenticate
        if self.User.authenticate(username, hashedPassword):
            # update widgets and redirect to admin page
            self.Stacked_Widget.setCurrentIndex(2)
            self.Admin_Button.setText("Home")
            self.setWindowTitle("SFTPPipeline - Welcome " + self.User.Username)
        else:
            # Display login error notification
            self.LoginError_Label.show()
            # Reset username and password LineEdits
            self.Username_LineEdit.setText("")
            self.Password_LineEdit.setText("")
        # Restore default cursor
        QApplication.restoreOverrideCursor()
    


    # Function: Display_Users
    # Parameters: None
    # Return: None
    # Clears out the Users_List Widget in the administrative view, and populates the list widget with usernames from the database
    def Display_Users(self):
        # Establish database connection
        db = Database()
        # Clear Users_List Widget
        self.Users_List.clear()
        # Fetch users from database
        users = db.getUsers()
        # Populate Users_List widget
        for user in users:
            self.Users_List.addItem(user[1])
        # Clean up database connection
        del db



    # Function: AddUser_Button_Logic
    # Parameters: None
    # Return: None
    # Attempts to add a new user, if user input information is an empty string, the function will return
    def AddUser_Button_Logic(self):
        # Establish a database connection
        db = Database()
        # Fetch user input
        username = self.NewUserUsername_LineEdit.text()
        password = self.NewUserPassword_LineEdit.text()
        # verify user input
        if username.strip() == "" or password.strip() == "":
            del db
            return
        # Show loading cursor
        QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        # Secure password
        hashPassword = self.Security.getMD5(password)
        db.addUser(username, hashPassword)
        # Clean up database connection
        del db
        # Restore default cursor
        QApplication.restoreOverrideCursor()
        # Set LineEdits to empty string
        self.NewUserUsername_LineEdit.setText("")
        self.NewUserPassword_LineEdit.setText("")
        # Refresh List
        self.Display_Users()
    


    # Function DeleteUsers_Button_Logic
    # Parameters: None
    # Return: None
    # Deletes all selected Users in the Users_List widget from the database
    def DeleteUsers_Button_Logic(self):
        # Establish a database connection
        db = Database()
        # Get selected users in the Users_List widget
        selectedUsers = self.Users_List.selectedItems()
        # Iterate through each selected user
        for user in selectedUsers:
            # Delete the user from the datbase
            db.deleteUser(user.text())
        # Clean up database connection
        del db
        # Update the Users_List widget
        self.Display_Users()
        


    # Function: AddConnection_Button_Logic
    # Parameters: None
    # Return: None
    # Attempts to add a new connection to the database. If a LineEdit is empty, it will return.
    def AddConnection_Button_Logic(self):
        # Fetch user input data
        server = self.NewConnectionServer_LineEdit.text()
        username = self.NewConnectionUsername_LineEdit.text()
        password = self.NewConnectionPassword_LineEdit.text()
        remoteDirectory = self.NewConnectionRemoteDirectory_LineEdit.text()
        # validate user input
        if server.strip() == "" or username.strip() == "" or password.strip() == "" or remoteDirectory.strip() == "":
            return
        # Establish database connection
        db = Database()
        # Add new connection
        db.addConnection(server, username, password, remoteDirectory)
        # Clean up database connection
        del db
        # Reset LineEdit text
        self.NewConnectionServer_LineEdit.setText("")
        self.NewConnectionUsername_LineEdit.setText("")
        self.NewConnectionPassword_LineEdit.setText("")
        self.NewConnectionRemoteDirectory_LineEdit.setText("")
        # Refresh Connection Tables
        self.Display_Connections()



    # Function: Display_Connections
    # Parameters: None
    # Return: None
    # Resets all of the connection tables in the application, then fetches connections from the database and displays them on all connection tables in the application.
    def Display_Connections(self):
        # Clear tables
        self.AdminConnections_Table.clearContents()
        self.AdminConnections_Table.setRowCount(0)
        self.PresetsConnections_Table.clearContents()
        self.PresetsConnections_Table.setRowCount(0)
        # Establish database connection
        db = Database()
        # Fetch Connection Data
        connections = db.getConnections()
        # clean up database connection
        del db
        # set new rows for the tables
        self.AdminConnections_Table.setRowCount(len(connections))
        self.PresetsConnections_Table.setRowCount(len(connections))
        # enumerate connections list and insert data into the tables
        for row, connection in enumerate(connections):
            self.AdminConnections_Table.setItem(row, 0, QTableWidgetItem(connection[1]))
            self.AdminConnections_Table.setItem(row, 1, QTableWidgetItem(connection[4]))
            self.PresetsConnections_Table.setItem(row, 0, QTableWidgetItem(connection[1]))
            self.PresetsConnections_Table.setItem(row, 1, QTableWidgetItem(connection[4]))
    


    #
    def DeleteConnections_Button_Logic(self):
        print("hi")
        selectedItems = self.AdminConnections_Table.selectedItems()
        selectedRows = set()
        for item in selectedItems:
            selectedRows.add(item.row())
        if selectedRows:
            db = Database()
            connections = []
            for row in selectedRows:
                server = self.AdminConnections_Table.item(row, 0)
                remote = self.AdminConnections_Table.item(row, 1)
                con = db.getConnection(server.text(), remote.text())
                connections.append(con[0][0])
                print(server.text() + remote.text())
                #print(item.text())
            for c in connections:
                db.deleteConnection(c)
            del db
            self.Display_Connections()




    def SelectFiles(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        if file_dialog.exec_():
            filenames = file_dialog.selectedFiles()
            return filenames
    


    def PresetsFileSelector_Button_Logic(self):
        files = self.SelectFiles()
        if files is not None:
            self.PresetsFiles_List.addItems(files)
    


    def PresetsFilesClear_Button_Logic(self):
        self.PresetsFiles_List.clear()
    


    def PresetsDisplayAll_Button_Logic(self):
        self.Display_Connections()
    


    def PresetsAddPreset_Button_Logic(self):
        # get files
        files = [self.PresetsFiles_List.item(index).text() for index in range(self.PresetsFiles_List.count())]
        # get name
        name = self.PresetsName_LineEdit.text()
        # get selected rows
        selectedItems = self.PresetsConnections_Table.selectedItems()
        selectedRows = set()
        for item in selectedItems:
            selectedRows.add(item.row())
        # if there are selected rows
        if selectedRows:
            db = Database()
            connections = []
            # for each row, get connection id
            for row in selectedRows:
                server = self.PresetsConnections_Table.item(row, 0)
                remotedirectory = self.PresetsConnections_Table.item(row, 1)
                con = db.getConnection(server.text(), remotedirectory.text())
                # append connection id
                connections.append(con[0][0])
            # insert preset into db (name, files[], connections[])
            db.addPreset(name, files, connections)
            del db
            print(connections)
        




#app = QApplication(sys.argv)
#window = MainWindow()
#app.exec_()