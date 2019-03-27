# -*-coding: utf-8 -*-
from linepy import *
from datetime import datetime
from time import sleep
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, timeit, _thread
import urllib.request
#==============================================================================#
me = LINE()
meMID = me.profile.mid
botStart = time.time()
oepoll = OEPoll(me)
Me = [meMID,"u6949f816dddef051b5762322e5597f1e"]
#==============================================================================#
def restartBot():
    print ("[ INFO ] 機器重啟")
    python = sys.executable
    os.execl(python, python, *sys.argv)
def logError(text):
    me.log("[ 錯誤 ] " + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))
def sendMention(to, text="", mids=[]):
    arrData = ""
    arr = []
    mention = "@yinmo©2019 "
    if mids == []:
        raise Exception("Wrong mid")
    if "@!" in text:
        if text.count("@!") != len(mids):
            raise Exception("Wrong mid")
        texts = text.split("@!")
        textx = ""
        for mid in mids:
            textx += str(texts[mids.index(mid)])
            slen = len(textx)
            elen = len(textx) + 15
            arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mid}
            arr.append(arrData)
            textx += mention
            textx += str(texts[len(mids)])
    else:
        textx = ""
        slen = len(textx)
        elen = len(textx) + 15
        arrData = {'S':str(slen), 'E':str(elen - 4), 'M':mids[0]}
        arr.append(arrData)
        textx += mention + str(text)
    me.sendMessage(to, textx, {'AGENT_NAME':'line', 'AGENT_LINK': 'line://ti/p/~{}'.format(me.profile.userid), 'AGENT_ICON': "http://dl.profile.line-cdn.net/" + me.profile.picturePath, 'MENTION': str('{"MENTIONEES":' + json.dumps(arr) + '}')}, 0)    
#==============================================================================#
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            sendMention(op.param1, " @! 感謝您加我好友",[op.param1])
            sendMention(op.param1, " @! 基於安全考量暫時將您封鎖。",[op.param1])
            me.blockContact(op.param1)
        if op.type == 6:
            contact = me.getContact(op.param1)
            print ("[ 6 ] {} 試圖騷擾您 已被系統封鎖".format(contact.displayName))
        if op.type == 21 or op.type == 22 or op.type ==24:
            print ("[ 通知離開副本 ]")
            me.leaveRoom(op.param1)
        if (op.type == 25 or op.type == 26) and op.message.contentType == 0:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != me.profile.mid:
                    to = sender
                else:
                    to = receiver
            elif msg.toType == 2:
                to = receiver
            if text is None:
                return
            if sender in Me:
                if text.lower() in ['speed','sp']:
                    me.sendMessage(to,"約"+str(timeit.timeit('"-".join(str(n) for n in range(100))',number=1000)) + "秒")
                elif text.lower() == 'runtime':
                       me.sendMessage(to, "系統已運行 {}".format(str(format_timespan(time.time() - botStart))))
                elif text.lower() == 'restart':
                       me.sendMessage(to, "重啟成功")
                       restartBot()
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
                thread = threading.Thread(target=bot, args=(op,))
                thread.start()
    except:
        pass


