from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from myapp.models import myapp
# ---------------------------
import datetime
from OpenSSL import SSL
import idna
import time
from socket import socket
from collections import namedtuple
import ssl
import socket
import pandas as pd
from datetime import datetime, timedelta
import OpenSSL.crypto as crypto


# ---------------------------

# Create your views here.

def sayhello(request):
    return HttpResponse("Hello Django!")


def djpost(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if username == 'Duke' and password == '1234':
            #            return HttpResponse('歡迎光臨本網站！')
            return render(request, "list_domain.html", locals())

        else:
            return HttpResponse('帳號或密碼錯誤！')
    else:
        return render(request, "djpost.html", locals())


def addomain(request):
    if request.method == "POST":  # 如果是以POST方式才處理
        cName = request.POST['cName']  # 取得表單輸入資料
        usefor = request.POST['usefor']

        # 新增一筆記錄
        unit = myapp.objects.create(cName=cName, usefor=usefor)
        unit.save()  # 寫入資料庫
        return redirect('/list/')
    else:
        message = '請輸入資料(資料不作驗證)'
    return render(request, "list_domain.html", locals())


'''
def show(request):
    try:
        units = myapp.objects.all()
    except:
        error_message = 'error'
    return render(request, "show.html", locals())
'''


def show(request):
    units = myapp.objects.values('cName', 'usefor')

    return render(request, "show.html", locals())


# ---------------
dms = myapp.objects.values_list('cName', flat=True)
datas = []
now = datetime.utcnow()


# ---------------

def grab(request):
    #    if request.method == "POST":
    for i in dms:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with ctx.wrap_socket(socket.socket(), server_hostname=i) as s:
            s.connect((i, 443))
            cert = s.getpeercert(True)
            x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
            cName = x509.get_subject().CN
            enddate = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
            startdate = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
            expire_time_first = x509.get_notAfter()[:-1].decode()
            expire_time = datetime.strptime(expire_time_first, '%Y%m%d%H%M%S')
            limit = expire_time - now
            usefor = myapp.objects.values('usefor')

            unit = myapp.objects.create(cName=cName, usefor=usefor, startdate=startdate, enddate=enddate,
                                        limit=limit.days)
            unit.save()  # 寫入資料庫
            return redirect('/list/')


#        else:
#            return render(request, "list_domain.html", locals())
# ---------------


def grab2(request, id=None):
    unit = myapp.objects.get(id=id)
    cName = unit.cName
    usefor = unit.usefor
    # dmm = myapp.objects.values_list('cName', flat=True)
    i = cName

    # for i in dmm:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with ctx.wrap_socket(socket.socket(), server_hostname=i) as s:
        s.connect((i, 443))
        cert = s.getpeercert(True)
        x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
        commonName = x509.get_subject().CN
        enddate = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        startdate = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        expire_time_first = x509.get_notAfter()[:-1].decode()
        expire_time = datetime.strptime(expire_time_first, '%Y%m%d%H%M%S')
        limit = expire_time - now

        #下面這個是可以的，但是還是會新增成一條
        unit = myapp.objects.create(cName=cName, usefor=usefor, startdate=startdate, enddate=enddate,
                                    limit=limit.days)
        #unit = myapp.objects.filter(id=id).update(cName=cName, usefor=usefor).create(startdate=startdate, enddate=enddate, limit=limit.days)
        #unit = myapp.objects.filter(id=id).update(startdate=startdate, enddate=enddate, limit=limit.days)
        #unit = myapp.objects.filter(id=id).update(usefor=30)


        # unit = myapp.objects.update_or_create(cName=cName, usefor=usefor, startdate=startdate, enddate=enddate,
        #                                      limit=limit.days)
        unit.save()  # 寫入資料庫
        '''
        for j in unit:
            unit[j].cName = unit.cName
            unit[j].usefor = 'usefor'
            unit[j].startdate = 'startdate'
            unit[j].enddate = 'enddate'
            unit[j].limit = 'limit.days'
            unit[j].save()
        '''
        return redirect('/list/')


def grab3(request, id=None):
    #unit = myapp.objects.get(id=id)
    if request.method == "POST":  # 如果是以POST方式才處理
        cName = request.POST['cName']  # 取得表單輸入資料
        usefor = request.POST['usefor']


    # dmm = myapp.objects.values_list('cName', flat=True)
        i = request.POST['cName']

    # for i in dmm:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with ctx.wrap_socket(socket.socket(), server_hostname=i) as s:
        s.connect((i, 443))
        cert = s.getpeercert(True)
        x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
        commonName = x509.get_subject().CN
        enddate = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        startdate = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        expire_time_first = x509.get_notAfter()[:-1].decode()
        expire_time = datetime.strptime(expire_time_first, '%Y%m%d%H%M%S')
        limit = expire_time - now

        #下面這個是可以的，但是還是會新增成一條
        unit = myapp.objects.create(cName=cName, usefor=usefor, startdate=startdate, enddate=enddate,
                                    limit=limit.days)
        unit.save()  # 寫入資料庫

        return redirect('/list/')


def listt(request):
    return render(request, "list_domain.html", locals())


def post1(request):
    if request.method == "POST":  # 如果是以POST方式才處理
        cName = request.POST['cName']  # 取得表單輸入資料
        usefor = request.POST['usefor']
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        limit = request.POST['limit']

        # 新增一筆記錄
        unit = myapp.objects.create(cName=cName, usefor=usefor, startdate=startdate, enddate=enddate, limit=limit)
        unit.save()  # 寫入資料庫
        return redirect('/list/')
    else:
        message = '請輸入資料(資料不作驗證)'
    return render(request, "post1.html", locals())


def list(request):
    myapps = myapp.objects.all().order_by('enddate')  # 讀取資料表, 依 id 遞增排序
    return render(request, "list_domain.html", locals())


def delete(request, id=None):  # 刪除資料
    #    if id != None:
    #        if request.method == "POST":  # 如果是以POST方式才處理
    #            id = request.POST['cId']  # 取得表單輸入的編號
    #        try:
    unit = myapp.objects.get(id=id)
    unit.delete()
    return redirect('/list/')
#        except:
#            message = "讀取錯誤!"
#    return render(request, "list_domain.html", locals())

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
