# coding=utf-8
# from socket import *
import json
import socket
from threading import Thread
import time

import src.crabapple as crab


def tcpServer():
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 重复使用绑定信息,不必等待2MSL时间
    tcpSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    address = ('', 7788)
    tcpSocket.bind(address)
    tcpSocket.listen(5)

    try:
        while True:
            time.sleep(0.01)
            print('开启等待')
            newData, newAddr = tcpSocket.accept()
            print('%s客户端已经连接，准备处理数据' % newAddr[0])
            p = Thread(target=recv, args=(newData, newAddr))
            p.start()
    finally:
        tcpSocket.close()


def recv(newData, newAddr):
    while True:
        recvData = newData.recv(1024)
        if len(recvData) > 0:
            newData.send('upload ok'.encode('utf-8'))
            receveInfo = json.loads(receveInfo[2:len(receveInfo) - 4])
            recvData = receveInfo['data']
            for i in recvData:
                crab.sqlExe(
                    "INSERT INTO monitor(identification,value) values (\"{}\",{})".format(i['Name'], i['Value']))
            print(recvData)
        else:
            print('%s客户端已经关闭' % newAddr[0])
            break
    newData.close()


# 获取传感器不同档位值
def getRank(req):
    values = req.get_json()
    userId=values['userId']
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect(('tcp.lewei50.com', 9960))
    tcp_client.send('{"method": "update","gatewayNo": "02","userkey": "{}"}&^!'.format(userId).encode('utf-8'))
    recv_data = tcp_client.recv(1024)
    resStr = recv_data.decode('utf-8')
    try:
        resStr = json.loads(resStr[0:len(resStr) - 4])
        if resStr['p1'] == 'ok':
            tcp_client.send('{"method":"getcear"}&^!'.encode('utf-8'))
            recv_data = tcp_client.recv(1024)
            resStr = recv_data.decode('utf-8')
            return resStr
    except:
        return 'exception'
    finally:
        tcp_client.close()