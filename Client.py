### Client.py ###
### Author: Alex Donaldson ###






def list_to_str(inList, delim):
    outStr = delim.join(inList)
    return outStr


def create_new_bbp_msg(userID, groupID, msgID, reqAct, reqObj, subject, msgData):
    hdrList = [userID, groupID, msgID, reqAct, reqObj, subject, msgData]
    delim = "\n"
    msg = list_to_str(hdrList, delim)
    return msg

"""
def test():
    uID = "A"
    gID = "B"
    mID = "C"
    act = "D"
    obj = "E"
    sub = "FGH"
    data = "IJKLMNOP"
    msg = create_new_bbp_msg(uID, gID, mID, act, obj, sub, data)
    print(msg)
"""
#test()