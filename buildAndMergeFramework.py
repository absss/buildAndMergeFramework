# -*- coding: utf-8 -*-
import os
import re
import shutil
import datetime


########################
CURRENT_DIR = os.getcwd()


for filePath in os.listdir(CURRENT_DIR):
    if filePath.endswith('.xcodeproj'):
        TARGET_NAME = filePath.split('.')[0]

PRO_NAME = TARGET_NAME

if len(TARGET_NAME) <= 0:
    print 'target name is not exist'
    exit(-1);

print 'project name:%s\ntarget_name:%s'%(PRO_NAME,TARGET_NAME)

WRK_DIR = '%s/build'%CURRENT_DIR

TEMP_DIR = '%s/temp'%CURRENT_DIR
TEMP_File = '%s/temp/%s'%(CURRENT_DIR,PRO_NAME)

OUT_DIR = 'output'
OUT_FILE= '%s/output/%s'%(CURRENT_DIR,PRO_NAME)

PRODUCT = '%s/product'%CURRENT_DIR
PRODUCT_DIR = '%s/product/%s.framework'%(CURRENT_DIR,PRO_NAME)

BUILD_MODE = 'Release'

DEVICE_DIR = '%s/%s-iphoneos/%s.framework'%(WRK_DIR,BUILD_MODE,PRO_NAME)
SIMULATOR_DIR = '%s/%s-iphonesimulator/%s.framework'%(WRK_DIR,BUILD_MODE,PRO_NAME)

DEVICE_FILE = '%s/%s'%(DEVICE_DIR,PRO_NAME)
SIMULATOR_FILE = '%s/%s'%(SIMULATOR_DIR,PRO_NAME)

INSTALL_DIR = '%s/Products/%s.framework'%(CURRENT_DIR,PRO_NAME)

##直接先删除多余
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)    #递归删除文件夹
if os.path.exists(WRK_DIR):
    shutil.rmtree(WRK_DIR)    #递归删除文件夹
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)    #递归删除文件夹
if os.path.exists(PRODUCT):
    shutil.rmtree(PRODUCT)    #递归删除文件夹


os.system('xcodebuild -configuration \"%s\" -target \"%s\" -sdk iphonesimulator clean build'%(BUILD_MODE,TARGET_NAME))

if os.path.exists(TEMP_File):
    os.remove(TEMP_File)
if not os.path.exists(TEMP_DIR):
    os.mkdir(TEMP_DIR)

shutil.copyfile(SIMULATOR_FILE,TEMP_File)

if os.path.exists(OUT_FILE):
    os.remove(OUT_FILE)
if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

os.system('xcodebuild -configuration \"%s\" -target \"%s\" -sdk iphoneos clean build'%(BUILD_MODE,TARGET_NAME))

lipo_cmd = 'lipo -create %s %s -output %s'%(DEVICE_FILE,TEMP_File,OUT_FILE)
os.system(lipo_cmd)
print '\n\n合并完成:%s\n\n'%OUT_FILE



os.remove(DEVICE_FILE)
shutil.copyfile(TEMP_File,DEVICE_FILE)      #复制文件


if os.path.exists(PRODUCT):
    shutil.rmtree(PRODUCT)

shutil.copytree(DEVICE_DIR,PRODUCT_DIR)
textPath = '%s/update.txt'%PRODUCT
with open(textPath,'w') as f:
    txt = 'update time:%s'% datetime.datetime.now()
    f.write(txt)
print '\n\n新的framework生成成功:%s\n\n'%(PRODUCT_DIR)

if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR)    #递归删除文件夹
if os.path.exists(WRK_DIR):
    shutil.rmtree(WRK_DIR)    #递归删除文件夹
if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)    #递归删除文件夹
print '\n\n移除temp文件夹、build文件夹\n\n'

