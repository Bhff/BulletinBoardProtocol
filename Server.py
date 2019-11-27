### Server.py ###
### Author: Alex Donaldson ###

from socket import *
from threading import *


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
        #self.msgs = msgs

    #def addMsg(self, msg):
     #   self.msgs.append(msg)

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
            self.grpDict[m.groupID][m.id] = m

    def addMsg(self, msg):
        self.grpDict[msg.groupID][msg.id] = msg
        



class BulletinBoard:
    def load_groups(self, fileName):
        file = open(fileName, "r")
        #postDict = PostDictionary
        for line in file:
            line = line.strip()
            print(line)
            
        file.close()

    def read_bbp_req(self, bbpReq):

        request = bbpReq.split("\n")

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



    def handle_current_request(self):

        retCode = 0

        if (self.currReq.act == "create"):

            if (self.currReq.obj == "msg"):
                pass
            elif (self.currReq.obj == "group"):
                pass

        elif (self.currReq.act == "remove"):
            
            if (self.currReq.obj == "msg"):
                pass
            elif (self.currReq.obj == "group"):
                pass

        elif (self.currReq.act == "view"):
            
            if (self.currReq.obj == "msg"):

                if (self.currReq.mod == "new"):
                    pass
                if (self.currReq.mod == "total"):
                    pass
                else:
                    pass

        response = ''
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

    def listen(self):
        self.socket.listen(5)
        while True:
            client, address = self.socket.accept()
            client.settimeout(60)
            t = Thread(target = self.listenToClient,args = (client,address))
            t.start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    self.board.read_bbp_req(data) 
                    response = self.board.handle_current_request()
                    client.send(response)
                else:
                    raise error('Disconnection Occurred!')
            except:
                client.close()
                return False


def main():
    host = "bbpserver"
    port = 13037

    s = Server(host, port)
    s.listen()


'''
def testLoop():
    test = "Sometimes\n I wish\n testing was easier\n than this bullshit\n uh \n \n fuck"
    testList = test.split("\n")

    print("testList ==", testList)

    for idx in range(len(testList)):
        print("idx ==", idx)
        print("item @ idx ==", testList[idx])
        idx += 1
        print("item @ new idx ==", testList[idx])


testLoop()'''