# -*-coding: utf-8 -*-
from linepy import *
from datetime import datetime
#==============================================================================#
me = LINE()
meMID = me.profile.mid
oepoll = OEPoll(me)
#==============================================================================#
def logError(text):
    me.log("[ 錯誤 ] " + str(text))
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 5:
            me.blockContact(op.param1)
        if op.type == 21 or op.type == 22 or op.type ==24:
            me.leaveRoom(op.param1)
    except Exception as error:
        print(error)
#==============================================================================#
while 1:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except:
        pass


