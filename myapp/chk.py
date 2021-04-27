# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 01:48:43 2021

@author: duke.kuo
"""
import os
import django
os.environ.setdefault('DJANGO_SETTING_MODULE', 'ssll.settings')
os.environ['DJANGO_SETTINGS_MODULE'] = 'ssll.settings'
django.setup()

import ssl
import socket
import pandas as pd
from datetime import datetime, timedelta
import OpenSSL.crypto as crypto
from myapp.models import myapp

# hostname = myapp.objects.values('cName')
# hostname = ['www.google.com', '24h.pchome.com.tw']
hostname = myapp.objects.values_list('cName', flat=True)
# hostname = str(host)
datas = []
now = datetime.utcnow()

for i in hostname:
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with ctx.wrap_socket(socket.socket(), server_hostname=i) as s:
        s.connect((i, 443))
        cert = s.getpeercert(True)
        x509 = crypto.load_certificate(crypto.FILETYPE_ASN1, cert)
        commonName = x509.get_subject().CN
        notAfter = datetime.strptime(x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        notBefore = datetime.strptime(x509.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
        expire_time_first = x509.get_notAfter()[:-1].decode()
        expire_time = datetime.strptime(expire_time_first, '%Y%m%d%H%M%S')
        remain_time = expire_time - now
        print('domain:', commonName)
        print('startdate', notBefore)
        print('enddate', notAfter)
        print('limit', remain_time.days, 'day')
        print('\n')
