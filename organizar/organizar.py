import os, sys
import json

path1 = "C:/Users/diego/Documents/companion_app_gh/primer_sem"
path2 = "C:/Users/diego/Documents/companion_app_gh/segundo_sem"
path3 = "C:/Users/diego/Documents/companion_app_gh/Miupi Parser"

dirs1 = os.listdir(path1)
dirs2 = os.listdir(path2)
dirs3 = os.listdir(path3)

def orderFiles1(files1):
    i = 1
    for file in dirs1:
        if file.endswith('.json'):
            files1.append({'file': file, 'num': i})
        i += 1
    return files1

def orderFiles2(files2):
    i = 1
    for file in dirs2:
        if file.endswith('.json'):
            files2.append({'file': file, 'num': i})
        i += 1
    return files2


def orderFiles3(files1, files2, files3):
    for i in range(len(files1)):
        files3.append({'file': files1[i]['file'], 'num': files1[i]['num']})
        files3.append({'file': files2[i]['file'], 'num': files1[i]['num']})
    return files3

def orderFilesProxSemestre(files):
    """ 
    Organizing all the files from Miupi Parser to a single array. The array will contain each directory of each file
    """
    i = 1
    for file in dirs3:
        if file.endswith('.json'):
            files.append({'file': file, 'num': i})
            i += 1 # parse.py esta entre medio
    return files

files1 = orderFiles1([])
files2 = orderFiles2([])
files3 = []
files3 = orderFiles3(files1, files2, files3)
proxSemFiles = orderFilesProxSemestre([])





               
            
    
