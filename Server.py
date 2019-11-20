### Server.py ###
### Author: Alex Donaldson ###

class Message:
    def __init__(self, id, groupID, creatorID, subj, data):
        self.id = id
        self.groupID = groupID
        self.creatorID = creatorID
        self.subj = subj
        self.data = data

class Group:
    def __init__(self, id, creatorID, msgs):
        self.id = id
        self.creatorID = creatorID
        self.msgs = msgs

    def addMsg(self, msg):
        self.msgs.append(msg)

class BulletinBoard:
    def load_groups(self, fileName):
        file = open(fileName, "r")
        groups = []
        for i, line in file:
            line = line.strip()
            
        file.close()
        return groups

    def read_bbp_req(self, bbpReq):

        request = bbpReq.split("\n")

        userID = ""
        groupID = ""
        msgID = ""
        reqAct = ""
        reqObj = ""
        reqMod = ""
        subject = ""
        body = ""

        for item in bbpReq:
            if (item == "u"):
                item += 1
                userID = item
            elif (item == "g"):
                item += 1
                groupID = item
            elif (item == "ms"):
                item += 1
                msgID = item
            elif (item == "ra"):
                item += 1
                reqAct = item
            elif (item == "ro"):
                item += 1
                reqObj = item
            elif (item == "rm"):
                item += 1
                reqMod = item
            elif (item == "s"):
                item += 1
                subject = item
            elif (item == "b"):
                item += 1
                body = item



    def __init__(self, fileName):
        self.groups = self.load_groups(fileName)

def main():
    board = BulletinBoard("messages.txt")

main()