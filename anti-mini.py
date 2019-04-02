# -*-coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
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
        if op.type == 0:
            return
        if op.type == 5:
            me.blockContact(op.param1)
        if op.type == 6:
            contact = me.getContact(op.param1)
            print ("[ 6 ] {} 試圖騷擾您 已被系統封鎖".format(contact.displayName))
        if op.type == 21 or op.type == 22 or op.type ==24:
            print ("[ 通知離開副本 ]")
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


