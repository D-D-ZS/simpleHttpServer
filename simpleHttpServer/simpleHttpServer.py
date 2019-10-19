#!/usr/bin/env python  
# _*_ coding:utf-8 _*_  
#  
# Version : 1.0  
# Time    : 2019/10/18 17:36  
# Author  : DanDan Zhao 
# File    : simpleHttpServer.py  
#
import os
import shutil
from urllib import parse
import html
from django.core.handlers.wsgi import WSGIRequest, HttpRequest
from django.http import response, StreamingHttpResponse


def get_ip():
    import socket
    my_name = socket.gethostname()
    my_ip = socket.gethostbyname(my_name)
    return my_ip


def list_dir(request: WSGIRequest):
    # 根据请求获取当前获取目录，相对当前程序根目录
    # path = request.path
    # if path == "/":
    #     path = os.getcwd()
    # else:
    #     root = os.getcwd()
    #     for i in path.split("/")[1:]:
    #         root = root + os.sep + i

    # 根据url输入路径获取，绝对路径
    path = request.path
    print("=======================" + path + "=============================")
    try:
        if os.path.isdir(path):
            list = os.listdir(path)
        else:
            return str(path)
        print(list)
    except os.error:
        response.Http404
        return None

    list.sort(key=lambda a: a.lower())
    display_path = html.escape(parse.unquote(path))
    d_path_list = []
    c_name_list = []
    l_name_list = []
    for name in list:
        fullname = os.path.join(path, name)
        color_name = display_name = link_name = name
        # Append / for directories or @ for symbolic links
        if os.path.isdir(fullname):
            color_name = '<span style="background-color: #CEFFCE;">' + name + '/</span>'
            display_name = name
            link_name = name + os.sep
        if os.path.islink(fullname):
            color_name = '<span style="background-color: #FFBFFF;">' + name + '@</span>'
            display_name = name
        print("=======================" + link_name + "=============================")
        filename = display_path + os.sep + display_name
        c_name_list.append(color_name)
        d_path_list.append(display_name)
        l_name_list.append(link_name)

    return c_name_list, d_path_list, display_path, l_name_list



def file_iterator(path: str, chunk_size=512):
    with open(path,'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def download(the_file_name: str):
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + str(the_file_name.split(os.sep)[-1])
    return response

def copy_file(source, target):
    outfile = open(target, 'wb')
    shutil.copyfileobj(source, outfile)
    outfile.close()


def str_stream(file, chunk_size=512):
    while True:
        c = file.read(chunk_size)
        if c:
            yield c
        else:
            break

def req_stream(request: HttpRequest):
    while True:
        text = request.body()
        if text:
            yield text
        else:
            break


def upload(request: HttpRequest):
    root = os.getcwd()
    for i in request.path.split("/")[1:]:
        root = root + os.sep + i
    if request.FILES is not None:
        file_name = request.FILES['file']
        output = root + str(file_name)
        copy_file(file_name,output)
        return str(file_name) + " 已上传到 " + output , root
    else:
        return "上传内容为空，请选择上传文件"
