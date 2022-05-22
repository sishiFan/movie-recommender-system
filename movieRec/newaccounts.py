import numpy as np
import pandas as pd
import csv

accounts = pd.read_csv('data/accounts.csv',sep=",",names=["userid","username","password"],engine='python')

def readaccounts():
    global accounts
    accounts = pd.read_csv('data/accounts.csv',sep=",",names=["userid","username","password"],engine='python')   
    return accounts

#密码都是123456  userid 1-6040
def checkaccount(username,passw):
    checkname = accounts[accounts['username']==username].values.tolist()
    if (len(checkname)==0):
        return 00
    if (len(checkname)==1):
        checkpassword = checkname[0][2]
        if str(checkpassword) == passw:
            return checkname[0]
        if str(checkpassword) != passw:
            return 00    
#注册得检查username 是否重复 userid ➕1

#查注册用的用户名是否和之前的重复
def checkthename(username):
    checkname = accounts[accounts['username']==username].values.tolist()
    if (len(checkname)==0):#无重复数据
        return 00
    else:
        return 11
    
def writeaccounts(username,userpasswd):
    count = 0
    with open('data/accounts.csv', 'r', encoding='utf-8', newline='') as f:  
        reader = csv.reader(f) 
        for row in reader:
            count += 1
    userid = count + 1
    
    row = [str(userid),username,userpasswd]

    with open('data/accounts.csv', 'a', encoding='utf-8', newline='') as file:  
        writer = csv.writer(file) 
        writer.writerow(row)
        
    