import pandas as pd

userids = list(range(1,6041))
password = []

for i in userids:
    password.append('123456')
    
acc = {'userid': userids,
       'username': userids,
       'password': password, 
}

acconts = pd.DataFrame(acc, columns = ['userid','username','password']) 

acconts.to_csv("data/accounts.csv", sep=',',index = False, header = None)