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
    18: "Closed Connection",

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
    def __init__(self, req):
        print("init-ing message")
        self.id = req.msgID
        #input("m_id")
        self.groupID = req.groupID
        #input("groupID")
        self.creatorID = req.userID
        #input("Creator_id")
        self.subj = req.subject
        #input("subj")
        self.body = req.body
        #input("body")
        self.timestamp = req.timestamp
        #print("timestamp, message init-ed")

class Group:
    def __init__(self, id, creatorID):
        self.id = id
        self.creatorID = creatorID
        self.msgs = {}

    def addMsg(self, msg):

        print("adding msg to group")
        if (msg.id not in self.msgs.keys()):
            self.msgs[msg.id] = msg 
        else:
            print("Message already exists")

class Request:
    def __init__(self, userID, groupID, msgID, act, obj, mod, subject, body, timestamp):
        self.userID = userID
        self.groupID = groupID
        self.msgID = msgID
        self.act = act
        self.obj = obj
        self.mod = mod
        self.subject = subject
        self.body = body
        self.timestamp = timestamp


class PostDictionary:
    # grpDict := dictionary where keys are groupIDs, and values are dictionaries where msgIDs are keys and Messages are values
    # msgs := list of Messages
    def __init__(self, grpDict, msgs):
        self.grpDict = grpDict
        for m in msgs:
            self.grpDict[m.groupID].addMsg(m)

    def addMsg(self, msg):
        print("adding msg to PostDict")
        self.grpDict[msg.groupID].addMsg(msg)
        


class BulletinBoard:

    # read_bbp_req : sets self.currReq to appropriate Request instance for
    #   the given request string
    def read_bbp_req(self, bbpReq):

        print("splitting bbpReq")

        request = bbpReq.split("\n")

        print("Current Request:\n", request)

        userID = request[0]
        groupID = request[1]

        if (groupID == ''): groupID = 'public'  

        msgID = request[2]
        reqAct = request[3]
        reqObj = request[4]
        reqMod = request[5]
        subject = request[6]
        body = ""
        timestamp = ""

        for idx in range(7, len(request)):
            body += request[idx] + '\n'

        self.currReq = Request(userID, groupID, msgID, reqAct, reqObj, reqMod, subject, body, timestamp)


    # handle_current_request : returns an appropriate response to the request
    #   stored in self.currReq
    def handle_current_request(self):

        #timestamp = ''
        print("handling request...")
        req = self.currReq
        retCode = 99
        respBody = ""

        # exists = tuple(bool for groupId's existence, bool for msgId's existence)
        exists = self.group_msg_status(req.groupID, req.msgID)

        print('exists ==', exists)

        if (req.act == "create"):

            print("CREATING....")

            if (req.obj == "msg"):

                print("....MESSAGE")

                if (not exists[0]):
                    retCode = 24
                elif (exists[1]):
                    retCode = 21
                else:
                    retCode = 11
                    print("creating message instance...")
                    m =  Message(req)
                    print("posting message....")
                    self.posts.addMsg(m)
                    print("Message Posted!")

            elif (req.obj == "group"):

                print("....GROUP")

                if (exists[0]):
                    retCode = 22
                else:
                    retCode = 12
                    grp = Group(req.groupID, req.userID)
                    self.posts.grpDict[req.groupID] = grp

        elif (req.act == "remove"):

            print("REMOVING....")
            
            if (req.obj == "msg"):

                print("....MESSAGE")
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

                print("....GROUP")
                if (not exists[0]):
                    retCode = 24
                elif (self.posts.grpDict[req.groupID].creatorID != req.userID):
                    retCode = 32
                else:
                    retCode = 14
                    self.posts.grpDict.pop(req.groupID)

        elif (req.act == "view"):

            print("VIEWING....")

            if (not exists[0]):
                retCode = 24
            else:
                if (req.obj == "msg"):

                    retCode = 15
                    isNew = False

                    if (req.mod == "new"):
                        print("....NEW....")
                        retCode = 16
                        isNew = True


                    elif (req.mod == "total"):
                        print("....TOTAL....")
                        retCode = 17
                        respBody = str(len(self.posts.grpDict[req.groupID].msgs))

                    print("....MESSAGES")

                    for mKey in self.posts.grpDict[req.groupID].msgs.keys():
                        respBody += "\n" + str(mKey)
                        respBody += "\n" + self.posts.grpDict[req.groupID].msgs[mKey].subj
                        respBody += "\n" + self.posts.grpDict[req.groupID].msgs[mKey].body
                        respBody += "\nEND\n"

        elif (req.act == 'close'):
            retCode = 18
            print("CLOSE!")
            

        print("request handled")

        response = str(retCode) + ' ' + RET_CODE_DICT[retCode] + "\n" + respBody
        print("Response:\n", response)
        return response

    
    def group_msg_status(self, groupID, msgID):

        print("checking group/msg existence")

        isGroup = False
        isMsg = False
        
        isGroup = groupID in self.posts.grpDict.keys()
        if (isGroup):
            isMsg = msgID in self.posts.grpDict[groupID].msgs.keys()

        print("existence checked")

        return (isGroup, isMsg)


    def __init__(self):
        self.posts = PostDictionary({'public': Group('public', '')}, [])
        self.currReq = Request("", "", "", "", "", "", "", "", "")



class clientThread(Thread):
    def __init__(self, ip, port, conn):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        print("New clientThread created!")

    def run(self):
        size = 4096
        while True:
            try:
                data = self.conn.recv(size)
                if data:
                    print("data received (as bytes):", data)
                    dataStr = data.decode()
                    print("data received (as str):", dataStr)
                    print("reading data...")
                    s.board.read_bbp_req(dataStr) 
                    print("data read")
                    response = s.board.handle_current_request()
                    response = bytes(response, 'utf-8')
                    self.conn.send(response)
                    print("response sent")
                else:
                    raise error('Disconnection Occurred!')
            except:
                #client.close()
                return False



# Threaded Server implementation found at:
# https://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/
class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.board = BulletinBoard()
        self.socket.bind((self.host, self.port))
        self.userViewTimes = {}

    def listen(self):
        self.socket.listen(5)
        allThreads = []

        while True:
            #print("listening...")
            client, address = self.socket.accept()
            client.settimeout(600)
            #self.listenToClient(client, address)
            ct = clientThread(address[0], address[1], client)  
            '''target = self.listenToClient, args = (client, address)'''
            ct.start()
            allThreads.append(ct)
        
        for th in allThreads:
            th.join()

''' def listenToClient(self, client, address):
    size = 4096
    while True:
        try:
            data = client.recv(size)
            if data:
                print("data received (as bytes):", data)
                dataStr = data.decode()
                print("data received (as str):", dataStr)
                self.board.read_bbp_req(dataStr) 
                print("data read")
                response = self.board.handle_current_request()
                response = bytes(response, 'utf-8')
                client.send(response)
                print("response sent")
            else:
                raise error('Disconnection Occurred!')
        except:
            client.close()
            return False'''


#def main():
host = ''
port = 13037

#print("host ==", host)

#Server(host, port).listen()
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


#main()
