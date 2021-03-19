'''
Author: Gtylcara.
Date: 2021-03-05 01:23:40
LastEditors: Gtylcara.
LastEditTime: 2021-03-18 15:12:47
'''
import socket
import threading
import sqlite3
import time
import json

from threading import Condition, Lock

con = Condition()

def timerCallback(socket):
    print('call timer')

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()

    sql = f"SELECT * FROM Guard_datadb"
    cursor.execute(sql)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    for i in range(len(data)):
        s = f"{{\"id\":{i + 1},\"status\":{data[i][2]}}}"
        socket.send(bytes(s, 'ascii'))

    global timer
    timer = threading.Timer(1, timerCallback, [socket])
    timer.start()


def recv(client_socket, ip_port):

    global timer
    timer = threading.Timer(1, timerCallback, [client_socket])
    timer.start()
    
    while True:
        client_text = client_socket.recv(1024)

        if client_text:
            print(client_text.decode("gbk"))
            print("[客户端消息]", ip_port, ":", client_text.decode("gbk"))
            # name, status, work, power, stat
            jsonStr = client_text.decode("gbk").split('$', 2)
            jsonObj = json.loads(jsonStr[0])

            name = "\'" + str(jsonObj['id']) + "\'"
            status = jsonObj['status']
            working = jsonObj['work']
            power = jsonObj['power']
            stat = 0
            if jsonObj['status'] == 0:
                stat = 1
            elif jsonObj['power'] < 20:
                stat = 2
            # {"id":1, "status":1, "power":100, "work":1}
            conn = sqlite3.connect("db.sqlite3")
            cursor = conn.cursor()

            sql = f"UPDATE Guard_datadb SET status={status} where name={name} "
            cursor.execute(sql)
            sql = f"UPDATE Guard_datadb SET working={working} where name={name} "
            cursor.execute(sql)
            sql = f"UPDATE Guard_datadb SET power={power} where name={name} "
            cursor.execute(sql)

            sql = f"INSERT INTO Guard_logdb(name, status, time) VALUES({name}, {stat}, {time.time() + 8 * 60 * 60}) "
            cursor.execute(sql)
            
            cursor.close()
            conn.commit()
            conn.close()




def main():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    tcp_socket.bind(("", 2333))

    tcp_socket.listen(128)
    
    

    
    while True:

        client_socket, ip_port = tcp_socket.accept()
        
        print("[新客户端]:", ip_port, "已连接")

        t1 = threading.Thread(target=recv, args=(client_socket, ip_port))

        t1.setDaemon(True)

        t1.start()

        

        


if __name__ == '__main__':
    main()
