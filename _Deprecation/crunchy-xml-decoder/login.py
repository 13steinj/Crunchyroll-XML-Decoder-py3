#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import requests
import re
from getpass import getpass
from configparser import ConfigParser
import random
import string
from time import sleep
from colorama import Fore, Style, init
init()
#import altfuncs
from altfuncs import config


if int(re.findall(r'(\d)\.(\d\.?\d?)',sys.version)[0][0]) >= 3:
    if float(re.findall(r'(\d)\.(\d\.?\d?)', sys.version)[0][1]) >= 5.3:
        from proxy_cr import get_proxy
    else:
        def get_proxy(types_,countries_):
            return '64.33.171.19:8080'
        
    

def getuserstatus_old(sess_id_renew = False,sess_id_usa=''):
    status = 'Guest'
    user1 = 'Guest'
    session = requests.session()
    cookies_ = ConfigParser()
    if sess_id_usa=='':
        cookies_.read('cookies')
        sess_id_usa = cookies_.get('COOKIES', 'sess_id_usa')
        sess_id_ = cookies_.get('COOKIES', 'sess_id')
        auth = cookies_.get('COOKIES', 'auth')
    if sess_id_renew:
        session.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id_usa).json()
        session.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id_).json()
    checkusaid = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id_usa).json()
    if checkusaid['code'] == 'ok':
        if checkusaid['data']['user'] != None:
            user1 = checkusaid['data']['user']['username']
            if checkusaid['data']['user']['premium'] == '':
                status = 'Free Member'
            else:  # later will add Premium+ status
                status = 'Premium'
    else:
        payload = {'device_id': ''.join(random.sample(string.ascii_letters + string.digits, 32)),'api_ver': '1.0','device_type': 'com.crunchyroll.crunchyroid','access_token': 'Scwg9PRRZ19iVwD','version': '2313.8','locale': 'jaJP','duration': '9999999999', 'auth' : auth}
        payload_t = {'device_id': ''.join(random.sample(string.ascii_letters + string.digits, 32)),'api_ver': '1.0','device_type': 'com.crunchyroll.crunchyroid','access_token': 'Scwg9PRRZ19iVwD','version': '2313.8','locale': 'jaJP','duration': '9999999999', 'auth' : auth}
        #if altfuncs.config()[8] != '':
        #    proxies = {'http': altfuncs.config()[8]}
        #else:
        #    proxies = {}
        proxies = {}
        checkusaid2 = session.post('http://api-manga.crunchyroll.com/cr_start_session', params=payload_t).json()
        print(session.post('http://api-manga.crunchyroll.com/cr_start_session', params=payload_t).url)
        #print(session.post('http://api-manga.crunchyroll.com/cr_start_session', params=payload_t).history)
        #print(checkusaid2)
        sess_id_usa = checkusaid2['data']['session_id']
        try:
            sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()['data']['session_id']
        except requests.exceptions.ProxyError:
            sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']['session_id']
        open("cookies", "w" , encoding='utf8').write('[COOKIES]\nsess_id = '+sess_id_+'\nsess_id_usa = '+sess_id_usa+'\nauth = '+auth)
        if checkusaid2['data']['user'] != None:
            user1 = checkusaid2['data']['user']['username']
            if checkusaid2['data']['user']['premium'] == '':
                status = 'Free Member'
            else:  # later will add Premium+ status
                status = 'Premium'
    return [status,user1]

def login_old(username, password):
    session = requests.session()
    device_id = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    device_id_usa = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    payload_usa = {'device_id': device_id_usa, 'api_ver': '1.0',
               'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'Scwg9PRRZ19iVwD', 'version': '2313.8',
               'locale': 'jaJP', 'duration': '9999999999'}
    payload = {'device_id': device_id, 'api_ver': '1.0',
               'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'Scwg9PRRZ19iVwD', 'version': '2313.8',
               'locale': 'jaJP', 'duration': '9999999999'}
    #if altfuncs.config()[8] != '':
    #    proxies = {'http': altfuncs.config()[8]}
    #else:
    #
    proxies = {}
    print(session.get('http://api-manga.crunchyroll.com/cr_start_session', params=payload_usa).url)
    sess_id_usa = session.get('http://api-manga.crunchyroll.com/cr_start_session', params=payload_usa).json()['data']['session_id']
    try:
        sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()['data']['session_id']
    except requests.exceptions.ProxyError:
        sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']['session_id']
    #for now we dont need unblocker server
    '''
    try:
        session.cookies['usa_sess_id'] = requests.get('https://cr.onestay.moe/getid').json()['sessionId']
    except:
        sleep(10)  # sleep so we don't overload crunblocker
        session.cookies['usa_sess_id'] = requests.get('http://rssfeedfilter.netne.net/').json()['sessionId']
    '''
    auth = ''
    if username != '' and password != '':
        payload = {'session_id' : sess_id_usa,'locale': 'jaJP','duration': '9999999999','account' : username, 'password' : password}
        try:
            auth = session.post('https://api.crunchyroll.com/login.0.json', params=payload).json()['data']['auth']
            auth_x = session.post('https://api.crunchyroll.com/login.0.json', params={'session_id' : sess_id_, 'auth': auth})
        except:
            pass
    userstatus = getuserstatus(False,sess_id_usa)
    if username != '' and userstatus[0] == 'Guest':
        print('Login failed.' if 'idlelib.run' in sys.modules else '\x1b[31m' + 'Login failed.' + '\x1b[0m')
        #sys.exit()
    else:
        print('Login as ' + userstatus[1] + ' successfully.' if 'idlelib.run' in sys.modules else 'Login as ' + '\x1b[32m' + userstatus[1] + '\x1b[0m' + ' successfully.')
    cookies_out = '''[COOKIES]
device_id = '''+device_id+'''
device_id_usa = '''+device_id_usa+'''
sess_id = '''+sess_id_+'''
sess_id_usa = '''+sess_id_usa+'''
auth = '''+auth+'''
'''
    #open("cookies", "w").write('[COOKIES]\nsess_id = '+sess_id_+'\nsess_id_usa = '+sess_id_usa+'\nauth = '+auth)
    open("cookies", "w").write(cookies_out)
def getuserstatus(sess_id_renew = False,sess_id_usa=''):
    status = 'Guest'
    user1 = 'Guest'
    session = requests.session()
    cookies_ = ConfigParser()
    cookies_.read('cookies')
    
    
    
    if sess_id_usa=='':
        device_id = cookies_.get('COOKIES', 'device_id')
        device_id_usa = cookies_.get('COOKIES', 'device_id_usa')
        sess_id_usa = cookies_.get('COOKIES', 'sess_id_usa')
        sess_id_ = cookies_.get('COOKIES', 'sess_id')
        auth = cookies_.get('COOKIES', 'auth')
    if sess_id_renew:
        session.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id_usa).json()
        session.get('http://api.crunchyroll.com/end_session.0.json?session_id='+sess_id_).json()
    checkusaid = session.get('http://api.crunchyroll.com/start_session.0.json?session_id='+sess_id_usa).json()
    if checkusaid['code'] == 'ok':
        if checkusaid['data']['user'] != None:
            user1 = checkusaid['data']['user']['username']
            if checkusaid['data']['user']['premium'] == '':
                status = 'Free Member'
            else:  # later will add Premium+ status
                status = 'Premium'
    else:
        payload_usa = {'device_id': device_id_usa, 'api_ver': '1.0',
                       'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'Scwg9PRRZ19iVwD',
                       'version': '2313.8',
                       'locale': 'jaJP', 'duration': '9999999999', 'auth' : auth}
        payload = {'device_id': device_id, 'api_ver': '1.0',
                   'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'Scwg9PRRZ19iVwD', 'version': '2313.8',
                   'locale': 'jaJP', 'duration': '9999999999', 'auth' : auth}
        #if altfuncs.config()[8] != '':
        #    proxies = {'http': altfuncs.config()[8]}
        #else:
        #    proxies = {}
        proxies = {}
        sess_id_usa = create_sess_id_usa(payload_usa)
        try:
            checkusaid2 = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()
        except requests.exceptions.ProxyError:
            checkusaid2 = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()
        sess_id_ = checkusaid2['data']['session_id']
        cookies_out = '''[COOKIES]
device_id = ''' + device_id + '''
device_id_usa = ''' + device_id_usa + '''
sess_id = ''' + sess_id_ + '''
sess_id_usa = ''' + sess_id_usa + '''
auth = ''' + auth + '''
'''
        open("cookies", "w").write(cookies_out)
        if not checkusaid2['data']['user'] is None:
            user1 = checkusaid2['data']['user']['username']
            if checkusaid2['data']['user']['premium'] == '':
                status = 'Free Member'
            else:  # later will add Premium+ status
                status = 'Premium'
    return [status, user1]


def login(username, password):
    session = requests.session()
    device_id = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    device_id_usa = ''.join(random.sample(string.ascii_letters + string.digits, 32))
    payload_usa = {'device_id': device_id_usa, 'api_ver': '1.0',
               'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'Scwg9PRRZ19iVwD', 'version': '2313.8',
               'locale': 'jaJP', 'duration': '9999999999'}
    payload = {'device_id': device_id, 'api_ver': '1.0',
               'device_type': 'com.crunchyroll.crunchyroid', 'access_token': 'Scwg9PRRZ19iVwD', 'version': '2313.8',
               'locale': 'jaJP', 'duration': '9999999999'}
    #if altfuncs.config()[8] != '':
    #    proxies = {'http': altfuncs.config()[8]}
    #else:
    #
    proxies = {}
    sess_id_usa = create_sess_id_usa(payload_usa)
    #print(sess_id_usa)
    try:
        sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', proxies=proxies, params=payload).json()['data']['session_id']
    except requests.exceptions.ProxyError:
        sess_id_ = session.post('http://api.crunchyroll.com/start_session.0.json', params=payload).json()['data']['session_id']
    auth = ''
    if username != '' and password != '':
        payload = {'session_id' : sess_id_usa,'locale': 'jaJP','duration': '9999999999','account' : username, 'password' : password}
        try:
            auth = session.post('https://api.crunchyroll.com/login.0.json', params=payload).json()['data']['auth']
        except:
            pass
    userstatus = getuserstatus(False, sess_id_usa)
    if username != '' and userstatus[0] == 'Guest':
        print('Login failed.' if 'idlelib.run' in sys.modules else '\x1b[31m' + 'Login failed.' + '\x1b[0m')
    # sys.exit()
    else:
        print('Login as ' + userstatus[1] + ' successfully.' if 'idlelib.run' in sys.modules else 'Login as ' + '\x1b[32m' + userstatus[1] + '\x1b[0m' + ' successfully.')
    cookies_out = '''[COOKIES]
device_id = ''' + device_id + '''
device_id_usa = ''' + device_id_usa + '''
sess_id = ''' + sess_id_ + '''
sess_id_usa = ''' + sess_id_usa + '''
auth = ''' + auth + '''
'''
        # open("cookies", "w").write('[COOKIES]\nsess_id = '+sess_id_+'\nsess_id_usa = '+sess_id_usa+'\nauth = '+auth)
    open("cookies", "w").write(cookies_out)

def create_sess_id_usa(params_v):
    usa_session = requests.session()
    sess_id_usa = ''
    usa_session_post = usa_session.post('http://api-manga.crunchyroll.com/cr_start_session', params=params_v)
    #print(usa_session_post.url)
    if usa_session_post.json()['error'] != "true":
        sess_id_usa = usa_session_post.json()['data']['session_id']
    if sess_id_usa=='':
        for prxy_ in get_proxy(['HTTPS'],['US']):
            proxies = {'https': prxy_}
            #print(proxies)
            try:
                usa_session_post = usa_session.post('https://api.crunchyroll.com/start_session.0.json', proxies=proxies,
                                                    params=params_v).json()
                sess_id_usa = usa_session_post['data']['session_id']
                return sess_id_usa
            except:
                pass

    return sess_id_usa



if __name__ == '__main__':
    try:
        if sys.argv[1][0] == 'y':
            username = input(u'Username: ')
            password = getpass('Password(don\'t worry the password are typing but hidden:')
    except IndexError:
        username = ''
        password = ''
    login(username, password)
