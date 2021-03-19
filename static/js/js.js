/*
 * @Author: Gtylcara.
 * @Date: 2021-03-05 12:34:24
 * @LastEditors: Gtylcara.
 * @LastEditTime: 2021-03-12 20:27:26
 */

$.ajaxSetup({
    async: false
});

function statusReverse(id) {
    var elem = document.getElementById("ctrlPannel" + id)
    var flag
    if (elem.classList[1] == "label-danger") {
        flag = true
        elem.classList.remove("label-danger")
        elem.classList.add("label-success")
    }
    else{ 
        flag = false
        elem.classList.add("label-danger")
        elem.classList.remove("label-success")
    }
    
    
    if (elem.textContent == "停止")
        elem.innerText = "打开"
    else
        elem.innerText = "停止"
    cmd = flag ? "on" : "off"
    
    $.post("/api/control", { cmd : id + ',' + cmd }, function (data, status) {
        console.log("log:" + data)
        if (data == 'true') {
        }
    })
}

$(document).ready(function () {

    // 'use strict';
    var token = localStorage.getItem("token")

    if (token == undefined) {
        window.location.href = "/login/";
    }

    token = token.split('.')

    token = window.atob(token[1])
    token = JSON.parse(token)
    var now = new Date().getTime() / 1000;
    if (now > token.exp) {
        alert("登录过期，请重新登陆")
        window.location.href = "/login/";
    }
    console.log(token)

});


