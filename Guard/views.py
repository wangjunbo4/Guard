'''
Author: Gtylcara.
Date: 2021-02-01 16:27:16
LastEditors: Gtylcara.
LastEditTime: 2021-03-18 15:36:28
'''

import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection
import json
import jwt


def index(request):

    conn = connection.cursor()

    conn.execute(
        f'SELECT * FROM Guard_datadb')
    res = conn.fetchall()
    conn.close()
    data = []

    for i in res:
        data.append([i[1], i[2], i[3], i[4]])
    
    datas = {"data": data}

    return render(request, "index.html", datas)

def battery(request):

    conn = connection.cursor()

    conn.execute(
        f'SELECT * FROM Guard_datadb')
    res = conn.fetchall()
    conn.close()
    data = []

    for i in res:
        data.append([i[1], i[2], i[3], i[4]])

    datas = {"data": data}
    
    return render(request, "battery.html", datas)

def log(request):

    conn = connection.cursor()

    conn.execute(
        f'SELECT * FROM Guard_logdb ORDER BY time DESC LIMIT 50')
    res = conn.fetchall()
    conn.close()
    data = []

    cnt = 0
    for i in res:
        if i[2] != 0:
            cnt += 1
            t = time.localtime(float(i[3]))
            t = time.strftime("%Y/%m/%d %H:%M:%S", t)
            data.append([i[1], i[2], t, cnt])
        

    datas = {"data": data}
    
    return render(request, "log.html", datas)


def login(request):
    return render(request, "login.html", {})

def register(request):
    return render(request, "register.html", {})


def generate_token(key, expire=60):
    now = time.time()
    data = {
        "iat": now,
        "exp": now+expire
    }
    data.update(key)
    token = jwt.encode(data, "secret", algorithm="HS256")

    return token


def certify_token(token):
    try:
        data = jwt.decode(token, "secret", algorithms=["HS256"])
    except BaseException:
        return False
    now = time.time()
    if now < data["iat"] or now > data["exp"]:
        return False
    return True


def api_login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    conn = connection.cursor()

    conn.execute(
        f'SELECT password FROM Guard_userdb where username=\'{username}\'')
    res = conn.fetchone()

    conn.close()
    print(res)
    if res == [] or res == None:
        return HttpResponse("")

    if res[0] == password:
        token = generate_token({"username": username}, 60*60*24*365)
    else:
        token = ""

    return HttpResponse(token)


def api_register(request):
    username = request.POST["username"]
    password = request.POST["password"]

    if username == "" or password == "":
        return HttpResponse("n")

    conn = connection.cursor()

    conn.execute(
        f'SELECT username FROM Guard_userdb')
    res = conn.fetchall()

    for i in res:
        if i[0] == username:
            return HttpResponse("n")

    conn.execute(
        f'INSERT INTO Guard_userdb(username, password) VALUES(\'{username}\', \'{password}\') ')

    conn.connection.commit()
    conn.close()

    return HttpResponse("y")


def api_data(request):

    return HttpResponse("")

def api_control(request):

    cmd = request.POST.get("cmd")
    cmd = cmd.split(',', 2)
    
    conn = connection.cursor()
    flag = 1
    if cmd[1] == 'on':
        flag = 0
    print(flag)
    sql = f"UPDATE Guard_datadb SET working={flag} where name={cmd[0]}"
    conn.execute(sql)
    conn.connection.commit()

    conn.close()
    
    return HttpResponse(cmd)
