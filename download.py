#!/usr/bin/env python

import urllib
import urllib2
import urlparse
import cookielib
import HTMLParser
import subprocess
import sys
import os


import optparse
import netrc
import getpass


import base64
import datetime
from dateutil.relativedelta import relativedelta


### ---------------------------------------------------------------------------------------- ###
### ------------------------------------- USER SETTING ------------------------------------- ###
### ---------------------------------------------------------------------------------------- ###
INITIAL_DATE = datetime.datetime(1, 1, 1, 1)
FINAL_DATE   = datetime.datetime(1, 1, 1, 1)

DATA_HOUR_DELTA = 6         # DOWNLOAD EVERY ${HOUR_DELTA} HOURS. If every 1 day, HOUR_DELTA=24.

TRY_MAX = 5                 # If download is failed, retry ${TRY_MAX} times

# ${DIRECTORY}YYYYMM/${TITLE}.YYYYMMDDHH is downloaded
# THIS IS NOT THE PATH IN THIS COMPUTER, BUT THE PATH IN DIAS
DIAS_DIRECTORY = '/JRA3Q/Hist/Daily/fcst_phyp125/'
TITLE          = 'XXXXXXXXXXXXXXXX'

COMP_DIRECTORY = '/mnt/jet12/JRA3Q/Daily/fcst_phyp125'
#COMP_DIRECTORY = './fcst_phyp125'

# This seems to be the url of the download page.
# https://data.diasjp.net/dl/storages/filelist/dataset:645 for JRA3Q, 
# https://data.diasjp.net/dl/storages/filelist/dataset:204 for JRA55, etc.
targeturl='https://data.diasjp.net/dl/storages/filelist/dataset:645'
### ---------------------------------------------------------------------------------------- ###
### ---------------------------------------------------------------------------------------- ###
### ---------------------------------------------------------------------------------------- ###

clargs = sys.argv
#print clargs
try:
    INITIAL_DATE = datetime.datetime.strptime(clargs[1], '%Y/%m/%d/%H')
    FINAL_DATE   = datetime.datetime.strptime(clargs[2], '%Y/%m/%d/%H')
    TITLE        = clargs[3]
except:
    INITIAL_DATE = INITIAL_DATE
    FINAL_DATE   = FINAL_DATE
    TITLE        = TITLE

DIAS_URL = 'https://data.diasjp.net/dl/storages/downloadCmd/'
#DIAS_URL = 'https://data.diasjp.net/dl/storages/file/'
LOGFILE = 'log/log_' + TITLE +'_' + datetime.datetime.strftime(INITIAL_DATE, '%Y%m%d') + '_' + datetime.datetime.strftime(FINAL_DATE,
'%Y%m%d') + '.txt'

log = open(LOGFILE, 'w')


# Function Made By Kosei Ohara
def get_filename_data(title, YYYYMMDDHH):
    
    # Make file name of the downloaded data
    # This is  to download ${DIRECTORY}YYYYMM/${TITLE}.YYYYMMDDHH file.
    # Change the definision of FILE to get other kinds of file name.
    output = title + '.' + YYYYMMDDHH
    return output


# Function Made By Kosei Ohara
def get_filename_grads(title, YYYYMM):

    # Make file name of the control files and index files
    share = title + '.' + YYYYMM + '.'
    ctl = share + 'ctl'
    idx = share + 'idx'

    return ctl, idx


# Function Made By Kosei Ohara
def get_dias_directory(directory, YYYYMM):
    if (directory[-1] != '/'):
        available_path = directory + '/'
    else:
        available_path = directory

    output = available_path + YYYYMM + '/'
    return output


# Function Made By Kosei Ohara
def get_computer_directory(absPath, YYYYMM):
    if (absPath[-1] != '/'):
        available_path = absPath + '/'
    else:
        available_path = absPath

    output = available_path + YYYYMM + '/'
    return output
    

# Function Made By Kosei Ohara
def get_url(FULLPATH):

    # Encode the file name
    FULLPATHtoBYTE = FULLPATH.encode('utf-8')
    # Base64 encode
    ENCODED = base64.b64encode(FULLPATHtoBYTE)
    # Cut some unnecessary characters
    ENCODED = str(ENCODED)

    URL = DIAS_URL + ENCODED

    return URL


def get_account(file):
    user_account = open(file, 'r')
    username = user_account.readline()
    password = user_account.readline()

    user_account.close()

    return username[:-1], password[:-1]
    #return username.rstrip('\n'), password.rstrip('\n')


def get_now():
    present_datetime = datetime.datetime.now()
    present_str = datetime.datetime.strftime(present_datetime, '%Y/%m/%d %H:%M:%S')

    return present_str


def mkinfo(file, DIRECTORY_IN_DIAS, TITLE, DIRECTORY_IN_COMPUTER):
    log.write('\n')
    log.write('INITIAL : ' + datetime.datetime.strftime(INITIAL_DATE, '%Y/%m/%d %H:%M') + '\n')
    log.write('FINAL   : ' + datetime.datetime.strftime(  FINAL_DATE, '%Y/%m/%d %H:%M') + '\n')
    log.write('\n')
    log.write('DATA HOUR DELTA : ' + str(DATA_HOUR_DELTA) + '\n')
    log.write('\n')
    log.write('TARGET URL     : ' + targeturl + '\n')
    log.write('DOWNLOAD URL   : ' + DIAS_URL + '\n')
    log.write('DIAS DIRECTORY : ' + DIRECTORY_IN_DIAS + '\n')
    log.write('TITLE          : ' + TITLE + '\n')
    log.write('\n')
    log.write('DOWLOADED TO ' + DIRECTORY_IN_COMPUTER + '\n')
    log.write('\n\n')
    log.flush()


# Function Made By Kosei Ohara
def DownloadData(DIRECTORY_IN_DIAS, TITLE, DIRECTORY_IN_COMPUTER):

    mkinfo(log, DIRECTORY_IN_DIAS, TITLE, DIRECTORY_IN_COMPUTER)

    delta = FINAL_DATE - INITIAL_DATE
    hours = delta.days * 24
    hours = hours + int(delta.seconds/(60*60))
    hours = hours + DATA_HOUR_DELTA
    tnum  = int(hours / DATA_HOUR_DELTA)

    NOW = INITIAL_DATE
    for t in range(0, tnum):
        YYYYMMDDHH = datetime.datetime.strftime(NOW, '%Y%m%d%H')
        YYYYMM = YYYYMMDDHH[:-4]

        # get the file name of download
        file = get_filename_data(TITLE, YYYYMMDDHH)

        # get the directory of download
        # NOTE that this is not the path in this computer, but the path in DIAS.
        # check the path before setting the format
        diasPath = get_dias_directory(DIRECTORY_IN_DIAS, YYYYMM)

        compPath = get_computer_directory(DIRECTORY_IN_COMPUTER, YYYYMM)

        # make download url
        file_url = get_url(diasPath + file)

        # make the relative path of downloaded file
        absFullPath = compPath + file
        
        if (os.path.exists(absFullPath)):
            exec_datetime = get_now()
            log.write(exec_datetime + "  " + absFullPath + "  EXIST\n")      # if file has already been exist, the process is skiped
        else:
            access.dl(file_url, compPath, file)

        NOW = NOW + datetime.timedelta(hours=DATA_HOUR_DELTA)
        log.flush()

    log.write('\n---\n')


# Function Made By Kosei Ohara
def DownloadGrads(DIRECTORY_IN_DIAS, TITLE, DIRECTORY_IN_COMPUTER):

    mkinfo(log, DIRECTORY_IN_DIAS, TITLE, DIRECTORY_IN_COMPUTER)
    
    NOW = INITIAL_DATE

    ini_year = INITIAL_DATE.year
    fin_year = FINAL_DATE.year
    ini_month = INITIAL_DATE.month
    fin_month = FINAL_DATE.month
    tnum = (fin_year - ini_year) * 12 + (fin_month - ini_month) + 1

    #while (FINAL_DATE.year != NOW.year or FINAL_DATE.month != NOW.month):
    for t in range(0, tnum):
        
        YYYYMM = datetime.datetime.strftime(NOW, '%Y%m')
        # get the file name of control and index files
        CTL, IDX = get_filename_grads(TITLE, YYYYMM)

        # get the directory of download
        # NOTE that this is not the path in this computer, but the path in DIAS.
        # check the path before setting the format
        diasPath = get_dias_directory(DIRECTORY_IN_DIAS, YYYYMM)

        compPath = get_computer_directory(DIRECTORY_IN_COMPUTER, YYYYMM)

        # make download url
        ctl_url = get_url(diasPath + CTL)
        idx_url = get_url(diasPath + IDX)

        # make the relative path of downloaded files
        ctl_absFullPath = compPath + CTL
        idx_absFullPath = compPath + IDX
        # download control file
        
        if (os.path.exists(ctl_absFullPath)):
            exec_datetime = get_now()
            log.write(exec_datetime + "  " + ctl_absFullPath + '  EXIST\n')
        else:
            access.dl(ctl_url, compPath, CTL)
        # download index file
        if (os.path.exists(idx_absFullPath)):
            exec_datetime = get_now()
            log.write(exec_datetime + "  " + idx_absFullPath + '  EXIST\n')
        else:
            access.dl(idx_url, compPath, IDX)

        NOW = NOW + relativedelta(months=1)
        log.flush()

    log.write('\n---\n')



class CASLoginParser(HTMLParser.HTMLParser):
    def __init__(self):
        HTMLParser.HTMLParser.__init__(self)
        self.action = None
        self.data = {}

    def handle_starttag(self, tagname, attribute):
        if tagname.lower() == 'form':
            attribute = dict(attribute)
            if 'action' in attribute:
                self.action = attribute['action']
        elif tagname.lower() == 'input':
            attribute = dict(attribute)
            if 'name' in attribute and 'value' in attribute:
                self.data[attribute['name']] = attribute['value']

class DIASAccess():
    def __init__(self, username, password):
        self.__cas_url = 'https://auth.diasjp.net/cas/login?'
        self.__username = username
        self.__password = password
        #self.__cj = cookielib.CookieJar()
        self.__cj = cookielib.MozillaCookieJar()
        self.__opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self.__cj))

    def open(self, url, data=None):
        response = self.__opener.open(url, data)
        response_url = response.geturl()

        if response_url != url and response_url.startswith(self.__cas_url):
            # redirected to CAS login page
            response = self.__login_cas(response)
            if data != None:
                # If POST (data != None), need reopen
                response.close()
                response = self.__opener.open(url, data)

        return response

    def __login_cas(self, response):
        parser = CASLoginParser()
        parser.feed(response.read())
        parser.close()

        if parser.action == None:
            raise LoginError('Not login page')

        action_url = urlparse.urljoin(response.geturl(), parser.action)
        data = parser.data
        data['username'] = self.__username
        data['password'] = self.__password

        response.close()
        response = self.__opener.open(action_url, urllib.urlencode(data))

        if response.geturl() == action_url:
            log.write('Authorization fail\n')
            log.flush()
            quit()

        return response

    def dl(self, url, path, file, data=None):

        for i in range(TRY_MAX):
            try:
                response = self.__opener.open(url, data)
                #if not os.path.exists('.' + path):
                #    os.makedirs('.' + path)
                if not os.path.exists(path):
                    os.makedirs(path)

                #f = open('.' + path + file, 'wb')
                f = open(path + file, 'wb')
                file_size_dl = 0
                block_size = 8192
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break

                    file_size_dl += len(buffer)
                    f.write(buffer)

                f.close
                exec_datetime = get_now()
                #print '.' + path + file + "  OK"
                log.write(exec_datetime + "  " + path + file + "  OK\n")
                log.flush()
                return response

            except urllib2.HTTPError,e:
                exec_datetime = get_now()
                #print '.' + path + file + "  NG"
                log.write(exec_datetime + "  " + path + file + "  NG\n")
                log.flush()


class LoginError(Exception):
    def __init__(self, e):
        Exception.__init__(self, e)


if __name__ == '__main__':
    
    host = 'data.diasjp.net'

    usage ='''usage: %prog [options]'''
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-n', '--netrc', default=None,
                      help='specify the netrc file', metavar='FILE')
    parser.add_option('-u', '--user', default=None,
                      help='specify the DIAS account name',
                      metavar='USERNAME')

    (options, args) = parser.parse_args()

    (login, password) = (None, None)

    try:
      auth = netrc.netrc(options.netrc).authenticators(host)
      if auth is not None:
            (login, account, password) = auth
    except (IOError):
      pass

    if options.user is not None:
        login = options.user
        password = None

    try:
        login, password = get_account('account.txt')
        #print 'login: ', login
        #print 'pass : ', password
    except:
        if login is None:
            login = raw_input('Username: ')

        if password is None:
            password = getpass.getpass('Password: ')

    try:
        access = DIASAccess(login, password)

        response = access.open(targeturl)
        response.close()
    except:
        log.write('\nFailed to login DIAS : python2 ' + clargs[0] + ' ' + clargs[1] + ' ' + clargs[2] + ' ' + clargs[3] + ' &\n\n')
        log.close()
        exit(1)

    log.write('\nSTART PROCESS\n\n')
    log.flush()


    ####access.dl('https://data.diasjp.net/dl/storages/downloadCmd/L0pSQTNRL0NsaW05MTIwL01vbnRobHkvYW5sX2lzZW50cm9wL2FubF9pc2VudHJvcF9idmYyLmNsaW05MTIwLm1vbjAx', '/JRA3Q/Clim9120/Monthly/anl_isentrop/', 'anl_isentrop_bvf2.clim9120.mon01')

    try:
        DownloadGrads(DIAS_DIRECTORY, TITLE, COMP_DIRECTORY)
        DownloadData( DIAS_DIRECTORY, TITLE, COMP_DIRECTORY)
    except:
        log.write('\nError Stop : Cannot continue downloading because of an unknown reason\n\n')
        log.close()
        exit(1)

    log.write('\nCOMPLETE PROCESS\n\n')
    log.flush()

log.close()

