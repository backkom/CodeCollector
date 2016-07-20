#-*- coding:utf-8 -*-

__author__ = 'Deqiang.li'

import sys
import os
import string
import zlib
import time
import shutil

def listDirectory(dir, fileExtList):
    '''get list of file info objects for files of paticular extensions'''
    fileList=[]
    fileAndDir=[os.path.normcase(f) for f in os.listdir(dir)]
    for f in fileAndDir:
        if ".svn" != f and os.path.isdir(os.path.join(dir, f)):
            fileList.extend(listDirectory(os.path.join(dir, f), fileExtList))
        if os.path.isfile(os.path.join(dir, f)):
            if string.lower(os.path.splitext(f)[1]) not in fileExtList:
                continue
            fileList.append(os.path.join(dir, f))
    return fileList

def getFileCRC(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def ImportPhoto(dir):
    files = listDirectory(dir, ['.jpg', '.png', '.mov'])
    for fileName in files:
        MergeOneFile(fileName)

def MergeOneFile(fileName):
    mtime = os.path.getmtime(fileName)
    date = time.localtime(int(mtime))
    year = date.tm_year
    month = date.tm_mon
    dirs = os.path.split(fileName)

    CopyToFile(fileName, '%d/%d' % (year, month), dirs[1])
    pass

def ConfirmDirExist(dir):
    dirs = string.split(dir, '/')
    if os.path.exists(dir):
        return
    for i in xrange(0, len(dirs)):
        subDir = string.join(dirs[0:i+1], '/')
        if not os.path.exists(subDir):
            os.mkdir(subDir)
    if not os.path.exists(dir):
        assert False

def CopyToFile(fullName, destFolder, fileName):
    ConfirmDirExist(destFolder)
    destFileName = destFolder + '/' + fileName
    if not os.path.exists(destFileName):
        print('move file', fullName, destFileName)
        shutil.move(fullName, destFileName)
    else:
        if not FileEqual(fullName, destFileName):
            tempData = fileName.split('.')
            newFileName = string.join(tempData[:-1], '.') + '_new' + '.' + tempData[-1]
            print('new move file', fullName, newFileName)
            shutil.move(fullName, destFolder + '/' + newFileName)
        else:
            print('same file, skip', fullName, destFileName)

def FileEqual(oldFile, newFile):
    if not os.path.exists(oldFile) or not os.path.exists(newFile):
        return False
    oldTime = os.path.getmtime(oldFile)
    newTime = os.path.getmtime(newFile)
    if oldTime != newTime:
        return False
    oldSize = os.path.getsize(oldFile)
    newSize = os.path.getsize(newFile)
    if oldSize != newSize:
        return False
    if True:
        return True
    else:
        oldCrc = getFileCRC(oldFile)
        newCrc = getFileCRC(newFile)
        return oldCrc == newCrc

if __name__ == '__main__':
    ImportPhoto(sys.argv[1])
    pass