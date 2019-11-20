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


    def __init__(self, fileName):
        self.groups = self.load_groups(fileName)

def main():
    board = BulletinBoard("messages.txt")

main()