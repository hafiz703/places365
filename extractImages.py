import pandas as pd
import numpy as np
import cv2
from shutil import copy2
import glob 
import random 
import os
import json
import matplotlib.pyplot as plt 
from sklearn.utils import shuffle
from PIL import Image
import re
from sklearn.model_selection import train_test_split
import random

np.random.seed(0)
def convertDateformat(datestr):
    # print("DATESTR",datestr)
    dic = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    ls = datestr.split('-')
    res=[]

    if(len(ls[0])<2):ls[0]='0'+ls[0]
    res.append(ls[0])
    res.append(dic[ls[1]])
    res.append('20'+ls[2])
    return ''.join(res)
        
CSVSOURCE = "E:/CSV files_base 1/merge0630_104days.csv"
IMAGESOURCE = "E:/Passive Data base 1/"
TRAIN_SAVE = "E:/Scenes/train/"
VAL_SAVE = "E:/Scenes/val/"


full_df = pd.read_csv(CSVSOURCE)
df = full_df[['participant_id','imagefile','date','food_court']]
train_df, val_df = train_test_split(df, test_size=0.3)
print("TRAIN ROWS:",len(train_df))
print("VAL ROWS:",len(val_df))

def copyTrainVal(dataf,train=True):
    toTxt = ""
    if(train):
        print("-------------------------TRAINING--------------------------")
        save_folder = TRAIN_SAVE
    else:
       print("-------------------------VALIDATION--------------------------")
       save_folder = VAL_SAVE

    count =0 
    for index, row in dataf.iterrows():
    #    print (row['participant_id'], row['imagefile'])
        participantDir =  IMAGESOURCE+row['participant_id'] + "/*"
        participantFolders = glob.glob(participantDir)
    #participantFoldersDate = [re.split('-|_| ',os.path.basename(i))[-1] for i in participantFolders]
        rowDate = convertDateformat(row['date'])
        # print("DATE",rowDate)
        imgdir=''
        for folder in participantFolders:        
            if rowDate in folder:
                imgdir = folder           
                break

                    
        if(len(imgdir)>0):
            imgdir = folder + "/" + row['imagefile']
             
        else:
            count+=1
            continue
            #print(row['imagefile'],rowDate,[os.path.basename(i) for i in participantFolders])

         
        try:
            im = Image.open(imgdir)
            if row['food_court'] == 1:
                savedir = save_folder + 'food_court/'+ row['participant_id']+'_'+os.path.basename(imgdir)
                
            else:
                savedir = save_folder + 'not_food_court/'+ row['participant_id']+'_'+os.path.basename(imgdir)
            toTxt+= os.path.basename(savedir)+ " " + str(row['food_court']) +"\n"
            
            # print(savedir) 
        except:
            print(imgdir, "not found") 
            pass
            # count+=1
            # print("NOT FOUND:",imgdir)
        im.save(savedir)
        print("Saved to",savedir)
    
        # im.save(os.path.basename(imgdir) + ext)
        # print("SAVED RESIZED:",os.path.basename(imageFile) + ext)
            
        # print(TRAIN_SAVE+os.path.basename(imgdir))
    print("REJECTED:",count)
    print("ACCEPTED:",len(dataf)-count)

    with open(save_folder+"labels.txt", "w") as text_file:
        text_file.write(toTxt)
            
copyTrainVal(train_df,train=True)
copyTrainVal(val_df,train=False)      

