#-*- coding:utf-8 -*-

import os, sys, string

def ListFiles(path, suffix):
    files = []
    for name in os.listdir(path):
        file = os.path.join(path, name)
        if os.path.isfile(file):
            if os.path.splitext(file)[1] in suffix:
                files.append(file)
        if os.path.isdir(file):
            files.extend(ListFiles(file, suffix))
    return files

def GenMarkDown(path, suffix, outputFileName):
    files = ListFiles(path, suffix)
    files = sorted(files)
    mainFile = open(outputFileName, 'wb')
    for name in files:
        f = open(name, mode='rb', buffering=1)
        temp = os.path.split(name)
        mainFile.write('# %s\n\n<div>\n' % string.join(temp[1:], '/'))
        lines = f.readlines()
        for line in lines:
            line = line.replace('\r\n', '<br>')
            line = line.replace('\n', '<br>')
            line = line.replace('\t', '    ')
            line = line.replace(' ', '&nbsp;')
            mainFile.write(line)
        mainFile.write('</div>')
        #mainFile.writelines(lines)
        #mainFile.writelines(f.readlines())
        mainFile.write('<br>\n<br>\n')
        f.close()
    mainFile.close()

if __name__ == '__main__':
    #GenMarkDown('./poe', ['.cs'], 'poe.txt')
    print("python GenTxtMarkdown.py ./dir, ['.cs'], 'ouput.txt'")