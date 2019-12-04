### Server.py ###
### Author: Alex Donaldson ###

from socket import *
from threading import *
from time import *

RET_CODE_DICT = {
    #Success Codes#
    11: "Message Created",
    12: "Group Created",
    13: "Message Removed",
    14: "Group Removed",
    15: "All Messages Found",
    16: "New Messages Found",
    17: "Messages Totaled",

    #Error Codes#
    21: "Message ID Already Exists",
    22: "Group Already Exists",
    23: "Message Does Not Exist",
    24: "Group Does Not Exist",

    31: "User Does Not Have Permission to Remove Message",
    32: "User Does Not Have Permission to Remove Group",

    99: "Unknown request"
}


class Message:
    def __init__(self, id, groupID, creatorID, subj, body, timestamp):
        self.id = id
        self.groupID = groupID
        self.creatorID = creatorID
        self.subj = subj
        self.body = body
        self.timestamp = timestamp

class Group:
    def __init__(self, id, creatorID):
        self.id = id
        self.creatorID = creatorID
        self.msgs = {}

    def addMsg(self, msg):
        self.msgs[msg.id] = msg if (msg.id not in self.msgs.keys()) else print("Message already exists")

class Request:
    def __init__(self, userID, groupID, msgID, act, obj, mod, subject, body):
        self.userID = userID
        self.groupID = groupID
        self.msgID = msgID
        self.act = act
        self.obj = obj
        self.mod = mod
        self.subject = subject
        self.body = body


class PostDictionary:
    # grpDict := dictionary where keys are groupIDs, and values are dictionaries where msgIDs are keys and Messages are values
    # msgs := list of Messages
    def __init__(self, grpDict, msgs):
        self.grpDict = grpDict
        for m in msgs:
            self.grpDict[m.groupID].addMsg(m)

    def addMsg(self, msg):
        self.grpDict[msg.groupID].addMsg(msg)
        


class BulletinBoard:
    def load_groups(self, fileName):
        file = open(fileName, "r")
        for line in file:
            line = line.strip()
            print(line)
            
        file.close()

    def read_bbp_req(self, bbpReq):

        strReq = str(bbpReq)
        strReq = strReq.decode('utf-8')

        print("strReq:\n", strReq)

        request = strReq.split("\n")

        userID = request[0]
        groupID = request[1]
        msgID = request[2]
        reqAct = request[3]
        reqObj = request[4]
        reqMod = request[5]
        subject = request[6]
        body = ""

        for idx in range(7, len(request)):
            body += request[idx]

        self.currReq = Request(userID, groupID, msgID, reqAct, reqObj, reqMod, subject, body)
        print("Current Request:\n", self.currReq)


    def handle_current_request(self):

        req = self.currReq
        retCode = 99
        respBody = ""

        # exists = tuple(bool for groupId's existence, bool for msgId's existence)
        exists = self.group_msg_status(req.groupID, req.msgID)

        if (req.act == "create"):

            if (req.obj == "msg"):
                if (not exists[0]):
                    retCode = 24
                elif (exists[1]):
                    retCode = 21
                else:
                    retCode = 11
                    msg = Message(req.msgID, req.groupID, req.userID, req.subj, req.body, time())
                    self.posts.addMsg(msg)

            elif (req.obj == "group"):
                if (exists[0]):
                    retCode = 22
                else:
                    retCode = 12
                    grp = Group(req.groupID, req.userID)
                    self.posts.grpDict[req.groupID] = grp

        elif (req.act == "remove"):
            
            if (req.obj == "msg"):
                if (not exists[0]):
                    retCode = 24
                elif (not exists[1]):
                    retCode = 23
                elif (self.posts.grpDict[req.groupID].msgs[req.msgID].creatorID != req.userID):
                    retCode = 31
                else:
                    retCode = 13
                    self.posts.grpDict[req.groupID].msgs.pop(req.msgID)
                    

            elif (req.obj == "group"):
                if (not exists[0]):
                    retCode = 24
                elif (self.posts.grpDict[req.groupID].creatorID != req.userID):
                    retCode = 32
                else:
                    retCode = 14
                    self.posts.grpDict.pop(req.groupID)

        elif (req.act == "view"):

            if (not exists[0]):
                retCode = 24
            else:
                if (req.obj == "msg"):

                    for mKey in self.posts.grpDict[req.groupID].msgs.keys():
                        respBody += "\n" + mKey
                        respBody += "\n" + self.posts.grpDict[req.groupID].msgs[mKey].subject
                        respBody += "\n" + self.posts.grpDict[req.groupID].msgs[mKey].body
                        respBody += "\n\nEND\n"

                elif (req.mod == "new"):
                    retCode = 16

                elif (req.mod == "total"):
                    retCode = 17
                    respBody = str(len(self.posts.grpDict[req.groupID].msgs))


        response = str(retCode) + RET_CODE_DICT[retCode] + "\n" + respBody
        print("Response:\n", response)
        return response

    
    def group_msg_status(self, groupID, msgID):

        isGroup = False
        isMsg = False
        
        if (groupID in self.posts.grpDict.keys()):
            isGroup = True
            if (msgID in self.posts.grpDict[groupID].keys()):
                isMsg = True

        return (isGroup, isMsg)


    def __init__(self, fileName, currReq):
        self.posts = PostDictionary({}, [])#self.load_groups(fileName)
        self.currReq = currReq


# Threaded Server implementation found at:
# https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.board = BulletinBoard("messages.txt", Request("", "", "", "", "", "", "", ""))
        self.socket.bind((self.host, self.port))

    def listen(self):
        self.socket.listen(5)
        while True:
            print("listening...")
            client, address = self.socket.accept()
            client.settimeout(60)
            self.listenToClient(client, address)
            #Thread(target = self.listenToClient, args = (client, address)).start()
            #t.run()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    print("data received:", data)
                    self.board.read_bbp_req(data) 
                    print("data read")
                    response = self.board.handle_current_request()
                    response = bytes(response)
                    client.send(response)
                    print("response sent")
                else:
                    raise error('Disconnection Occurred!')
            except:
                client.close()
                return False


def main():
    host = ''
    port = 13037

    #print("host ==", host)

    Server(host, port).listen()
    s = Server(host, port)
    s.listen()

'''
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('', port))
    serverSocket.listen(1)
    print('The server is ready to receive')
    while 1:
        connectionSocket, addr = serverSocket.accept()
        sentence = connectionSocket.recv(1024)
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence)
        connectionSocket.close()
'''


main()
