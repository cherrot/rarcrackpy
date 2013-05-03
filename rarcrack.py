#!/usr/bin/env python3.2 
import sys, glob, os
from rarfile import RarFile

with RarFile(sys.argv[1]) as rarFile:
    for i in range(2,len(sys.argv)):

        try:
            with open( '{}.log'.format(sys.argv[1]) ) as lastLog:
                lastFile = lastLog.readline()
                offset = lastLog.readline()
        except Exception:
            lastFile = None
            offset = 0
            pass

        for filename in glob.glob(sys.argv[i]):
            if lastFile and filename != lastFile:
                continue

            with open(filename) as dictFile:
                dictFile.seek(offset)
                count = 0
                print('Reading password from {}'.format(sys.argv[i]))
                while True:
                    password = dictFile.readline()
                    if password == '':
                        os.remove('{}.log'.format(sys.argv[1]))
                        break

                    try:
                        rarFile.extractall(pwd=password[:-1])
                        print('密码已破解：{}'.format(password))
                        #sys.stderr.write('密码已破解：{}'.format(password))
                        exit(0)

                    except Exception:
                        count += 1
                        if count == 1000:
                            print('Current : {}'.format(password))
                            with open('{}.log'.format(sys.argv[1]), 'w',
                                    encoding='utf-8') as log:
                                log.write('{}\n{}'.format(filename,dictFile.tell()))
                        continue
