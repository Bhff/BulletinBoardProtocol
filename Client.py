### Client.py ###
### Author: Alex Donaldson ###
from socket import *


MAIN_MENU = """
Please select an option (0 - 7):
0. Exit Bulletin Board
1. Post a New Message
2. Create a New Group
3. Remove Message
4. Remove Group
5. View Messages
6. View New Messages
7. View Total Messages
"""

PUBLIC_PRIVATE_MENU = """
0. Cancel
1. Public
2. Private
"""

#list_to_str: more legible way to convert a list to a string than "string-delimiter.join(list)"
def list_to_str(inList, delim):
    outStr = delim.join(inList)
    return outStr


# verifySelection: ensures user input fits correct format
def verifySelection(min, max, menuText):
    verified = False
    selection = -1
    while(not verified):
        print(menuText)
        selection = input()
        try:
            selection = int(selection)
        except TypeError:
            print("Invalid input,", selection, "cannot be converted from string to integer")
        else:
            if (selection < min or selection > max): print("Invalid menu choice!")
            else: verified = True

    return selection


class Client:
    # create_new_bbp_msg: formats data used bbp message into a string readable by the server 
    def create_new_bbp_req(groupID, msgID, reqAct, reqObj, reqMod, subject, body):
        reqList = ["u", self.userID, "g", groupID, "ms" msgID, "ra", reqAct, "ro", reqObj, "md", reqMod "s", subject, "b", body]
        delim = "\n"
        req = list_to_str(reqList, delim)
        return req

    def __init__(self, connection, userID)
        self.connection = connection
        self.userID = userID
    
    # makeRequest: given a valid main menu selection, creates and sends appropriate request to server
    def makeRequest(selection):

        # Init request variables
        groupID = 0
        msgID = 0
        reqAct = ""
        reqObj = ""
        reqMod = ""
        subject = ""
        body = ""

        # Post new message
        if (selection == 1):
            
            reqAct = "create"
            reqObj = "msg"

            print("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):")
            groupID = input()
            
            print("Please enter the subject for the message:")
            subject = input()

            print("Please enter your message body (type 'END' to finish the message):")
            bodyLine = ""
            while (bodyLine != "END"):
                body += bodyLine
                bodyLine = input()

        # Create new group
        elif (selection == 2):
            reqAct = "create"
            reqObj = "group"

            print("Please enter the group ID you want to create:")
            groupID = input()

        # Remove message
        elif (selection == 3):
            reqAct = "remove"
            reqObj = "msg"

            print("Please enter the group ID of the message you want to remove:")
            groupID = input()

            print("Please enter the message ID to remove:")
            msgID = input()

        # Remove group
        elif (selection == 4):
            reqAct = "remove"
            reqObj = "group"

            print("Please enter the group ID you want to remove:")
            groupID = input()

        # View messages
        elif (selection == 5):
            reqAct = "view"
            reqObj = "msg"

            print("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):")
            groupID = input()

        # View new messages
        elif (selection == 6):
            reqAct = "view"
            reqObj = "msg"
            reqMod = "new"

            print("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):")
            groupID = input()

        # View total messages
        elif (selection == 7):
            reqAct = "view"
            reqObj = "msg"
            reqMod = "total"

            print("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):")
            groupID = input()

        request = create_new_bbp_req(groupID, msgID, reqAct, reqObj, reqMod, subject, body)
        self.connection.send(request)


def mainMenu(client):
    selection = 999
    while (selection > 0):
        selection = verifySelection(0, 7, MAIN_MENU)
        client.makeRequest(selection)



def main():

    SERVER_NAME = "bbpserver"
    SERVER_PORT = 13037
    CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCKET.connect((serverName, serverPort))

    print("Welcome to the Bulletin Board!")
    print("Please enter your User ID:")
    userID = input()
    c = Client(CLIENT_SOCKET, userID)

    mainMenu(c)

    CLIENT_SOCKET.close()

    print("Thank you for using our Bulletin Board!")

    return