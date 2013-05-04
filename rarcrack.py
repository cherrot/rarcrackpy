#!/usr/bin/env python3.2 
import sys, glob, os
#from rarfile import RarFile

try:
    with open( '{}.log'.format(sys.argv[1]) ) as lastLog:
        lastFile = lastLog.readline()
        offset = lastLog.readline()
        print('Reading password at {} from {}'.format(offset, lastFile))
except Exception:
    lastFile = None
    offset = 0

#with RarFile(sys.argv[1]) as rarFile:
for i in range(2,len(sys.argv)):
    for filename in glob.glob(sys.argv[i]):
        if lastFile and filename != lastFile[:-1]:
            continue

        with open(filename) as dictFile:
            dictFile.seek(int(offset))
            count = 0
            print('Reading password from {}'.format(sys.argv[i]))
            while True:
                try:
                    password = dictFile.readline()
                except Exception: #encoding Exception
                    lastFile = None
                    offset = 0
                    print('Error in readline')
                    break
                if password == '':
                    try:
                        os.remove('{}.log'.format(sys.argv[1]))
                    except Exception:
                        pass
                    break

                #rarFile.extractall(pwd=password[:-1])
                try:
                    a = os.popen("unrar t -y -p{} {} 2>&1 | grep 'All OK'".format(
                        password[:-1], sys.argv[1]))
                    for i in a.readlines():
                        if i == 'All OK\n':
                            print('密码已破解：{}'.format(password))
                            sys.stderr.write('密码已破解：{}'.format(password))
                            exit(0)
                except Exception:
                    print('error in popen')
                    continue

                count += 1
                if count == 200:
                    count = 0
                    print('Current : {}'.format(password[:-1]))
                    with open('{}.log'.format(sys.argv[1]), 'w',
                            encoding='utf-8') as log:
                        log.write('{}\n{}'.format(filename,dictFile.tell()))
