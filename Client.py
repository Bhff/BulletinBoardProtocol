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

SERVER_NAME = '127.0.0.1'
SERVER_PORT = 13037

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
    def create_new_bbp_req(self, groupID, msgID, reqAct, reqObj, reqMod, subject, body):
        reqList = [self.userID, groupID, msgID, reqAct, reqObj, reqMod, subject, body]
        delim = "\n"
        req = list_to_str(reqList, delim)
        return req

    def __init__(self, connection, userID):
        self.connection = connection
        self.userID = userID
    
    # makeRequest: given a valid main menu selection, creates and sends appropriate request to server
    def makeRequest(self, selection):
 
        # Init request variables
        groupID = ""
        msgID = ""
        reqAct = "close"
        reqObj = ""
        reqMod = ""
        subject = ""
        body = ""

        # Post new message
        if (selection == 1):
            
            reqAct = "create"
            reqObj = "msg"
            groupID = input("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):\n")
            msgID = input("Please give your message an ID:\n")
            subject = input("Please enter the subject for the message:\n")

            print("Please enter your message body (type 'END' to finish the message):")
            bodyLine = ""
            while (bodyLine != "END"):
                body += (bodyLine + "\n")
                bodyLine = input()

        # Create new group
        elif (selection == 2):
            reqAct = "create"
            reqObj = "group"
            groupID = input("Please enter the group ID you want to create:\n")

        # Remove message
        elif (selection == 3):
            reqAct = "remove"
            reqObj = "msg"
            groupID = input("Please enter the group ID of the message you want to remove (leave blank or type 'public' for the public group):\n")
            msgID = input("Please enter the message ID to remove:\n")

        # Remove group
        elif (selection == 4):
            reqAct = "remove"
            reqObj = "group"
            groupID = input("Please enter the group ID you want to remove:\n")

        # View messages
        elif (selection == 5):
            reqAct = "view"
            reqObj = "msg"
            groupID = input("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):\n")

        # View new messages
        elif (selection == 6):
            reqAct = "view"
            reqObj = "msg"
            reqMod = "new"
            groupID = input("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):\n")

        # View total messages
        elif (selection == 7):
            reqAct = "view"
            reqObj = "msg"
            reqMod = "total"
            groupID = input("Please enter the group ID for the messages you wish to view (leave blank or type 'public' for the public group):\n")

        request = self.create_new_bbp_req(groupID, msgID, reqAct, reqObj, reqMod, subject, body)
        request = bytes(request, 'utf-8')
        self.connection.send(request)

    def handle_response(self, resp):

        respStr = resp.decode()
        print(respStr)
        '''
        strResp = str(resp)
        try:
            code = int(strResp[0:2])
        except TypeError:
            print("Invalid response code")
        else:
            print(strResp)
        '''


def mainMenu(client):
    selection = 999
    while (selection > 0):
        #client.connection.connect((SERVER_NAME, SERVER_PORT))
        selection = verifySelection(0, 7, MAIN_MENU)
        client.makeRequest(selection)
        response = client.connection.recv(4096)
        client.handle_response(response)
        #client.connection.close()



def main():

    CLIENT_SOCKET = socket(AF_INET, SOCK_STREAM)

    print("Welcome to the Bulletin Board!")
    userID = input("Please enter your User ID:\n")

    CLIENT_SOCKET.connect((SERVER_NAME, SERVER_PORT))
    c = Client(CLIENT_SOCKET, userID)

    mainMenu(c)



    print("Thank you for using our Bulletin Board!")

    '''CLIENT_SOCKET.connect((SERVER_NAME,SERVER_PORT))
    sentence = input('Input lowercase sentence:')
    sentence = bytes(sentence, 'utf-8')
    CLIENT_SOCKET.send(sentence)
    modifiedSentence = CLIENT_SOCKET.recv(1024)
    print ('From Server:', modifiedSentence)
    CLIENT_SOCKET.close()'''


main()