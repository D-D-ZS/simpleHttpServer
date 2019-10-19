#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# Version : 1.0  
# Time    : 2019/10/18 16:28  
# Author  : DanDan Zhao 
# File    : view.py
# 
from django.shortcuts import render
from . import simpleHttpServer
from django.core.handlers.wsgi import WSGIRequest,HttpRequest



def sub(request: WSGIRequest):
    context = {'hello': 'Hello World!'}
    return render(request, 'hello.html', context)

def hello(request: WSGIRequest):
    context = {'hello': 'Hello World!'}
    return render(request, 'base.html', context)

def home(request:HttpRequest):
    if request.method == 'POST':
        replace = {}
        msg = simpleHttpServer.upload(request)
        path_list = simpleHttpServer.list_dir(request)
        if isinstance(path_list, str):
            result = simpleHttpServer.download(path_list)
            return result
        else:
            replace["path_dis"] = "Directory listing for " + path_list[2]
            replace["path_list"] = path_list[3]
        replace['result'] = msg[0]
        replace['current_path'] = msg[1]
        return render(request, 'home.html', replace)
    else:
        path_list = simpleHttpServer.list_dir(request)
        if isinstance(path_list, str):
            result = simpleHttpServer.download(path_list)
            return result
        else:
            replace = {}
            replace["path_dis"] = "Directory listing for " + path_list[2]
            replace["path_list"] = path_list[3]
            return render(request, 'home.html', replace)
