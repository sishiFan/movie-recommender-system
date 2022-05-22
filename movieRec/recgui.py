import os
if os.path.exists('data/itembased.npy'):  
    os.remove('data/itembased.npy')
if os.path.exists('data/userbased.npy'):  
    os.remove('data/userbased.npy')
if os.path.exists('data/ratingsMatrix.npy'):  
    os.remove('data/ratingsMatrix.npy')
from svdmat import svd
svd()
#只有每次登陆的时候 更新svd分解 从而更新相似度与推荐

import csv
from distutils.log import info
from os import times
import tkinter
import pandas as pd
from tkinter import *
from  tkinter import messagebox
from PIL import Image,ImageTk
from itemsvd import top_cosine_similarity
from pathlib import Path
from searchpage import searchResult
from newaccounts import checkaccount
from newaccounts import checkthename
from newaccounts import writeaccounts
from newaccounts import readaccounts
import numpy as np
import pandas as pd
from usersvd import userBasedRec
from newaccounts import accounts


movieInfo = pd.read_csv('data/allInfo.csv', sep=",", names=['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction'], engine='python')
movies = pd.read_csv('data/movielens/movies.csv',sep="::",names=["movieid","title","genres"],engine='python')
ratings = pd.read_csv('data/movielens/ratings.csv',sep="::",names=["userid","movieid","ratings","timestamp"],engine='python')
movieInfo.index = movieInfo['movieid']
accounts = pd.read_csv('data/accounts.csv',sep=",",names=["userid","username","password"],engine='python')


#这里读取每次登录那一刻 评论不足2的所有id 评论太少推荐不准确 就不推荐了
norecids = []
allids = accounts['userid'].values.tolist()
for id in allids:
    ratingnum = ratings[ratings['userid']==id]['ratings'].values.tolist()
    if len(ratingnum) < 3:
        norecids.append(id)
    
tmbdidlist = []
movienames = []
justregistered = []

picbutton_dict = {}
photos = {}
biggerphotos = {}
label_dict={}
info = {}
labels = {}
imglabels = {}
imfopages = {}
reclabels = {}
recbtns = {}
frames = {}
ascore = {}
times = {}
urscore = {}
urs = {}
rateentry = {}
pages ={}
search = {}
resultlabel = {}
track = {}
trackkey = 0
searchtime = 0
loginnum = 0

def tk_center(width, height, screen_width, screen_height):
    mainx = int(screen_width / 2 - width / 2)
    mainy = int(screen_height / 2 - height / 2 )
    size = '{}x{}+{}+{}'.format(width, height, mainx, mainy)
    return size


def nextimg():
    global loginnum
    loginnum = loginnum + 1
    if loginnum == 7:
        loginnum = 0
    label_img.configure(image=loginphotos[loginnum]) 
    
def lastimg():
    global loginnum
    loginnum = loginnum - 1
    if loginnum == -1:
        loginnum = 6
    label_img.configure(image=loginphotos[loginnum]) 

def login():
    global currentuserid
    global currentusername
    loginname = lognameEntry.get()#string
    loginpasswd = logpasswdEntry.get()
    
    if (len(loginname.strip()) == 0)|(len(loginpasswd.strip()) == 0):
        messagebox.showerror(message = "Please type in something!")
        lognameEntry.delete(0, END)
        logpasswdEntry.delete(0, END)
        return
    
    if checkaccount(loginname,loginpasswd) != 00:
        currentuserid = checkaccount(loginname,loginpasswd)[0]
        currentusername = loginname
        tkinter.messagebox.showinfo(message = 'User ' + currentusername + ' : Log in successfully.')
        lognameEntry.delete(0, END)
        logpasswdEntry.delete(0, END)
        top.withdraw() # 登入成功后隐藏登录注册窗口
        root.deiconify() # 显示窗口
        firstpage()
        
    if checkaccount(loginname,loginpasswd) == 00:
        messagebox.showerror(message = "Wrong user name or password, please try again.")
        lognameEntry.delete(0, END)
        logpasswdEntry.delete(0, END)
        
def register():
    #注册页面
    registered = Toplevel(top)
    registered.title('SIGN UP')
    registered.geometry(tk_center(285,320,top.winfo_screenwidth(),top.winfo_screenheight()))
    registerframe = tkinter.Frame(registered)
    registerframe.pack(padx=8,pady=15)
    Label(registerframe,text="SIGN UP",font=("arial",18,'bold')).grid(sticky = W,row=0,column=0,pady=(10,10))
    Label(registerframe,text='User Name').grid(sticky = W,row=1,column=0)
    Label(registerframe,text='Password').grid(sticky = W,row=3,column=0)
    Label(registerframe,text='Confirm Password').grid(sticky = W,row=5,column=0)
    signnameEntry = Entry(registerframe, width = 14)
    signnameEntry.grid(sticky = W,row=2,column=0)
    signpasswdEntry = Entry(registerframe,show='*', width = 14)
    signpasswdEntry.grid(sticky = W,row=4,column=0)
    signconEntry = Entry(registerframe,show='*', width = 14)
    signconEntry.grid(sticky = W,row=6,column=0)

    def createcheck():
        global justregistered
        signnamecontent = signnameEntry.get()
        signpasscontent = signpasswdEntry.get()
        signconfirmcontent = signconEntry.get()
       #是否为空格
        if (len(signnamecontent.strip()) == 0)|(len(signpasscontent.strip()) == 0)|(len(signconfirmcontent.strip()) == 0):
            messagebox.showerror(message = "Please type in something!")
            signnameEntry.delete(0, END)
            signpasswdEntry.delete(0, END)
            signconEntry.delete(0, END)
            return
        #用户名长度 不超过 10
        if len(signnamecontent) > 10:
            messagebox.showerror(message="User name too long! User name must be no longer than 10 digits.")
            signnameEntry.delete(0, END)
            signpasswdEntry.delete(0, END)
            signconEntry.delete(0, END)
            return
        #查用户名是否重复，调用
        if checkthename(signnamecontent) == 11:
            messagebox.showerror(message = "Username already exists! Please change your username and try again.")
            signnameEntry.delete(0, END)
            signpasswdEntry.delete(0, END)
            signconEntry.delete(0, END)
            return
        #用户名是否含有特殊符号
        specialstring = "~!@#$%^&*()_+-*/<>,.[]/"
        for i in specialstring:
            if i in signnamecontent:
                messagebox.showerror(message = "Note that your user name cannot contain any special character!")
                signnameEntry.delete(0, END)
                signpasswdEntry.delete(0, END)
                signconEntry.delete(0, END)                 
                return      
        #用户名是否含有空格
        for i in signnamecontent:
            if i.isspace():
                messagebox.showerror(message = "Note that your user name cannot contain any space!")
                signnameEntry.delete(0, END)
                signpasswdEntry.delete(0, END)
                signconEntry.delete(0, END)                 
                return   
        #查两次密码是否相同
        if signpasscontent != signconfirmcontent:
            messagebox.showerror(message = "The two passwords are not consistent, please try again.")
            signnameEntry.delete(0, END)
            signpasswdEntry.delete(0, END)
            signconEntry.delete(0, END)
            return         
        #密码是否含有特殊符号    
        for i in specialstring:
            if i in signpasscontent:
                messagebox.showerror(message = "Note that your password cannot contain any special character!")
                signnameEntry.delete(0, END)
                signpasswdEntry.delete(0, END)
                signconEntry.delete(0, END)
                return  
        #密码是否含有空格
        for i in signpasscontent:
            if i.isspace():
                messagebox.showerror(message = "Note that your user name cannot contain any space!")
                signnameEntry.delete(0, END)
                signpasswdEntry.delete(0, END)
                signconEntry.delete(0, END)                 
                return             
        #密码是否为 6-12 位之间  
        if len(signpasscontent) < 6:
            messagebox.showerror(message=" Password too short! Password must be 6 - 12 digits long.")
            signnameEntry.delete(0, END)
            signpasswdEntry.delete(0, END)
            signconEntry.delete(0, END)
            return
        if len(signpasscontent) > 12:
            messagebox.showerror(message=" Password too long! Password must be 6 - 12 digits long.")
            signnameEntry.delete(0, END)
            signpasswdEntry.delete(0, END)
            signconEntry.delete(0, END)
            return
        #注册成功 自动关闭页面 写入csv 请登陆
        else:
            tkinter.messagebox.showinfo(message = 'You have created a new account! please go back to log in.')
            writeaccounts(signnamecontent,signpasscontent)
            
            update = readaccounts()
            #当次启动程序新注册的用户id都记录下来 由于未更新svd不做推荐
            newuserid = update[update['username']==signnamecontent].values.tolist()[0][0]
            justregistered.append(newuserid)
            signnameEntry.delete(0, END)
            signpasswdEntry.delete(0, END)
            signconEntry.delete(0, END)
            
    Button(registerframe, text="Create New Account", width = 12, command=createcheck).grid(row=7,column=0,pady=(10,2))
    
def exit():
    if messagebox.askokcancel(message = "Are you sure you want to log out?"):
        root.withdraw() 
        welcomelabel.destroy()
        existbtn.destroy()
        searchbtn.destroy()
        label_popular.destroy()
        for item in label_dict:
            label_dict[item].destroy()  
        for item in picbutton_dict:
            picbutton_dict[item].destroy()
            
        if tracklabel == 1:
            labelnorec.destroy()
           
        #删除生成的电影。应该删除了吧 后续加上user-based rec进行测试
        top.deiconify()
        '''转回log in'''     #login.deiconify()
  
def firstpage():
    #每一次是层层覆盖的关系
    global welcomelabel
    global existbtn
    global searchbtn
    global label_popular
    global labelnorec
    global tracklabel 
    
    welcomelabel = Label(root, text = 'Welcome:D   user : '+ currentusername, font=("arial",15,"bold"))
    welcomelabel.place(x = 10, y = 5)
             
    existbtn = Button(root, text='Log out', font=("arial",12), width=4, command = exit)
    existbtn.place(x=541,y=6)
    
    searchbtn = Button(root, text='Search', font=("arial",12), width=4, command = searchpage)
    searchbtn.place(x=480,y=6)
       
    #热门电影推荐  
    label_popular =Label(root, text='The most popular movie recommendations: ', font=("arial",13))
    label_popular.place(x=10, y=380)    
    #推荐前五的热门电影
    PopularSeries = ratings["movieid"].value_counts()[:10]
    topId = PopularSeries.index.tolist()
    toptmdblist = []
    for id in topId:
        toptmbdID = movieInfo[movieInfo.index==id].values.tolist()[0][1]
        toptmdblist.append(toptmbdID)
    
    posxx = 20
    for id in toptmdblist[:5]:
        fixpos(root,id,posxx,405)
        posxx = posxx + 120
     
    posxx = 20   
    for id in toptmdblist[5:]:
        fixpos(root,id,posxx,560)
        posxx = posxx + 120
    
    #fixpos(root,-930,200,200)  测试similir movie推荐      
       
    #user-based推荐
    label_popular =Label(root, text='User-based movie recommendations: ', font=("arial",13))
    label_popular.place(x=10, y=30)  
    
    #如果是当次启动程序新注册的账号（无论有没有评论）不给出推荐  
    tracklabel = 0 
    if currentuserid in justregistered:
        labelnorec = Label(root, text='Opps, we do not have any personalized recommendations \n for you, please rate more movies.',font=("arial",18))
        labelnorec.place(x=60,y=170)
        tracklabel = 1
        return
        
    #如果评论数小于 3  数据太少 无法给出准确推荐 不给出推荐
    if currentuserid in norecids:
        labelnorec = Label(root, text='Opps, we do not have any personalized recommendations \n for you, please rate more movies.',font=("arial",18))
        labelnorec.place(x=60,y=170)
        tracklabel = 1
        return

    else:
        #启动user-based个性化推荐
        recindexes = userBasedRec(currentuserid)
        #推荐算法运行后，推荐list仍然过少
        if len(recindexes) == 0:
            labelnorec = Label(root, text='Opps, we do not have any personalized recommendations \n for you, please rate more movies.',font=("arial",18))
            labelnorec.place(x=60,y=170)
            tracklabel = 1
            return

        posxx = 20
        for id in recindexes[:5]:
            fixpos(root,id,posxx,55)
            posxx = posxx + 120
        
        posxx = 20   
        for id in recindexes[5:]:
            fixpos(root,id,posxx,220)
            posxx = posxx + 120

def searchpage():
    global thisuserid
    global search
    global searchtime
    global resultlabel
    
    s  = searchentry.get().strip()
    if (len(s) == 0):
        messagebox.showerror(message = "Please type in something!")
        searchentry.delete(0, END)
        return
    # 一句话输出结果个数，指输出前多少个？？ 怎么排序   
    searchentry.delete(0, END)   
    searchtime = searchtime + 1
    search[searchtime] = Toplevel(root)
    search[searchtime].title('Results that contain " '+ s +' "')
    search[searchtime].wm_geometry(tk_center(610,735,root.winfo_screenwidth(),root.winfo_screenheight()))
    search[searchtime].resizable(0, 0)
    
    if (len(searchResult(s))==0):
        resultlabel[searchtime] = Label(search[searchtime], text = "Opps, no result found. Please change your keyword and try again.", font=("arial",15), wraplength=550, justify=LEFT)
        resultlabel[searchtime].place(x = 20, y = 30) 
        return
    
    if (len(searchResult(s))==1):
        resultlabel[searchtime] = Label(search[searchtime], text = 'We have found only 1 result that contains " '+ s + ' ", only show 15 movies of the most recent year:', font=("arial",15), wraplength=550, justify=LEFT)
        resultlabel[searchtime].place(x = 20, y = 30)
        
    if (len(searchResult(s)) > 1):
        resultlabel[searchtime] = Label(search[searchtime], text = 'We have found '+ str(len(searchResult(s))) +' results that contain " '+ s + ' ", only show 15 movies of the most recent year:', font=("arial",15), wraplength=550, justify=LEFT)
        resultlabel[searchtime].place(x = 20, y = 30)
        
    #注意数量不够怎么调用
    searchx = 20
    for id in searchResult(s)[:5]:
        fixpos(search[searchtime],id,searchx,100)
        searchx = searchx + 120
    
    searchx = 20
    for id in searchResult(s)[5:10]:
        fixpos(search[searchtime],id,searchx,280)
        searchx = searchx + 120
        
    searchx = 20
    for id in searchResult(s)[10:15]:
        fixpos(search[searchtime],id,searchx,460)
        searchx = searchx + 120

def read():
    global ratings
    ratings = pd.read_csv('data/movielens/ratings.csv',sep="::",names=["userid","movieid","ratings","timestamp"],engine='python')

def ave(tmdbId):
    #id由tmbd转为wovieid
    movie_id = movieInfo[movieInfo['tmdbid']==tmdbId].values.tolist()[0][0]
    ratinglist = ratings[ratings['movieid']==movie_id]['ratings'].values.tolist()
    if (len(ratinglist) == 0):
        ave = 0;
    else:
        ave = np.mean(ratinglist) 
    averating = round(ave,2)
    times = len(ratinglist)
    ave = [averating,times]
    return ave

def writescore(userid,tmdbId,newscore): 
    # csv初始状态一定要空一行！！
    movie_id = movieInfo[movieInfo['tmdbid']==tmdbId].values.tolist()[0][0]
    
    row = [str(userid)+"::"+str(movie_id)+"::"+str(newscore)+"::"+str(0)]
    
    with open('data/movielens/ratings.csv', 'a', encoding='utf-8', newline='') as file:  
        writer = csv.writer(file) 
        writer.writerow(row)

def showMovie(tracking,i):
    global imglabels
    global labels
    global infolist
    global recbtns
    global reclist
    global track
    global pages
    global times
    global ascore
    global urscore
    global urs
    global rateentry
    
    #print('tracking',tracking)

    infolist = movieInfo[movieInfo['tmdbid']==i].values.tolist()[0]
    info[tracking] = '\n'.join(infolist[2:])
    
    pages[tracking] = Toplevel(root)
    
    #title 改为名字 根据电影变化
    pages[tracking].title(movieInfo[movieInfo['tmdbid']==i].values.tolist()[0][2][14:])
    pages[tracking].wm_geometry(tk_center(610,735,root.winfo_screenwidth(),root.winfo_screenheight()))
    pages[tracking].resizable(0, 0)
    
    imglabels[tracking] = Label(pages[tracking], image = biggerphotos[tracking])
    imglabels[tracking].place(x = 60, y = 25)
    
    labels[tracking] = Label(pages[tracking], text = info[tracking], font=("arial",12), wraplength=270, justify = LEFT)
    labels[tracking].place(x = 270, y = 33)
    
    labeltext = Label(pages[tracking], text='Similar movie recommendations:',font=("arial",13))
    labeltext.place(x=18,y=330)
    
    avelist = ave(i)
    avescore = np.float64(avelist[0])
    avetimes = np.int64(avelist[1])
    
    ascore[tracking] = Label(pages[tracking], text='Score: ' + str(avescore),font=("arial",13))
    ascore[tracking].place(x=65,y=263)
    times[tracking] = Label(pages[tracking], text='Times: ' + str(avetimes),font=("arial",13))
    times[tracking].place(x=150,y=263)
    
    urs[tracking] = Label(pages[tracking], text= 'Your score:',font=("arial",13))
    urs[tracking].place(x=55,y=288)
    
    movie_id = movieInfo[movieInfo['tmdbid']==i].values.tolist()[0][0]
    ratinglist = ratings[(ratings['movieid']==movie_id) & (ratings['userid']== currentuserid)]['ratings'].values.tolist()
    
    score = -1
    if (len(ratinglist) == 1):
        score = ratinglist[0]
        
    if (score != -1):
        urs[tracking] = Label(pages[tracking], text= score,font=("arial",13))
        urs[tracking].place(x=129,y=288)
    if (score == -1):
        rateentry[tracking] = Entry(pages[tracking], show=None, width = 4)
        rateentry[tracking].place(x=130,y=286)
    
        def rate():  
            yourrate = rateentry[tracking].get() 
                
            if yourrate == '1' or yourrate == '2' or yourrate == '3' or yourrate == '4' or yourrate == '5':
                
                if (messagebox.askokcancel(message = "Are you sure you want to rate this movie " + str(yourrate) + " ?")):
                    writescore(currentuserid,i,yourrate)
                    read()
                    pages[tracking].destroy()
                    showMovie(tracking,i) 
             
            else:
                messagebox.showerror(message = "Please only type in an integer number from 1 to 5!")
                rateentry[tracking].delete(0, END)
                       
        urscore[tracking] = Button(pages[tracking], text='Rate',font=("arial",13),width=2, command = rate)
        urscore[tracking].place(x=188,y=285)   
     
    def itembased(tracking,i):
        
        indexes = top_cosine_similarity(i)
        if (len(indexes) == 0):
            labelnote = Label(pages[tracking], text='Opps, we do not have any recommendation for this movie.',font=("arial",18))
            labelnote.place(x=60,y=450)
            
        posxx = 20
        for id in indexes[:5]:
            fixpos(pages[tracking],id,posxx,360)
            posxx = posxx + 120
        
        posxx = 20   
        for id in indexes[5:]:
            fixpos(pages[tracking],id,posxx,525)
            posxx = posxx + 120    

    itembased(tracking,i) 

def readids(window,tracking,n):
    global label_dict
    global picbutton_dict
    #海报
    path = Path('data/pics/' + str(n) + '.png')
    if path.exists():
        image = Image.open('data/pics/' + str(n) + '.png')
        photo = ImageTk.PhotoImage(image.resize((85, 120)))
        #如果n已存在 建立新的 名称 不能叫n
        photos[tracking] = photo
        #更大尺寸海报
        biggerphoto = ImageTk.PhotoImage(image.resize((171, 234)))
        biggerphotos[tracking] = biggerphoto
        #海报下面的电影题目
        #找到tmdb id对应的movie name
    else:
        image = Image.open('data/pics/nan.png')
        photo = ImageTk.PhotoImage(image.resize((85, 120)))
        #如果n已存在 建立新的 名称 不能叫n
        photos[tracking] = photo
        #更大尺寸海报
        biggerphoto = ImageTk.PhotoImage(image.resize((171, 234)))
        biggerphotos[tracking] = biggerphoto      
        
    
    label_dict[tracking]=Label(window, text=movieInfo[movieInfo['tmdbid']==n].values.tolist()[0][2][14:], font=("arial",12), height=2, anchor=NW, wraplength=105)
    
    picbutton_dict[tracking] = Button(window, image = photos[tracking], command = lambda: showMovie(tracking,n)) 
     
def fixpos(window,i,posx,posy):
    global track
    global trackkey
    track[trackkey] = i
    readids(window,trackkey,i)
    picbutton_dict[trackkey].place(x=posx,y=posy)
    label_dict[trackkey].place(x=posx-5,y=posy+125) 
    trackkey = trackkey + 1

#登陆进去后的页面
root = Tk()
root.title("Movie Recommender System")
root.wm_geometry(tk_center(610,735,root.winfo_screenwidth(),root.winfo_screenheight()))
root.resizable(0, 0)
root.withdraw()
#登陆页面
top = Toplevel()
top.wm_geometry(tk_center(430,560,top.winfo_screenwidth(),top.winfo_screenheight()))
top.title('LOGIN')
frameup = tkinter.Frame(top, height=270)
frameup.pack(side='top')
framemid = tkinter.Frame(top, height=15)
framemid.pack(side='top')
framedown = tkinter.Frame(top)
framedown.pack(side='top',padx=100)
#登陆组建
Label(framedown,text="LOGIN",font=("arial",18,'bold')).grid(sticky = W,row=0,column=0,pady=(25,10))
Label(framedown,text='User Name').grid(sticky = W,row=1,column=0)
Label(framedown,text='Password').grid(sticky = W,row=3,column=0)
lognameEntry = Entry(framedown, width = 14)
logname = lognameEntry.grid(sticky = W,row=2,column=0)
logpasswdEntry = Entry(framedown,show='*', width = 14)
logpasswd = logpasswdEntry.grid(sticky = W,row=4,column=0)
Button(framedown, text="Login", width = 12, command=login).grid(row=5,column=0,pady=(10,2))
Button(framedown, text="Sign Up", width = 12, command=register).grid(row=6,column=0)
#登陆页面介绍插图
loginimage = Image.open('data/GUIpics/loginpage.png')
loginphoto = ImageTk.PhotoImage(loginimage.resize((400, 210)))

m1 = Image.open('data//GUIpics/signandlog.png')
p1 = ImageTk.PhotoImage(m1.resize((400, 210)))
m2 = Image.open('data//GUIpics/userbased.png')
p2 = ImageTk.PhotoImage(m2.resize((400, 210)))
m3 = Image.open('data//GUIpics/popularrec.png')
p3 = ImageTk.PhotoImage(m3.resize((400, 210)))
m4 = Image.open('data//GUIpics/search.png')
p4 = ImageTk.PhotoImage(m4.resize((400, 210)))
m5 = Image.open('data/GUIpics/infoandrate.png')
p5 = ImageTk.PhotoImage(m5.resize((400, 210)))
m6 = Image.open('data/GUIpics/similar.png')
p6 = ImageTk.PhotoImage(m6.resize((400, 210)))


loginphotos = [loginphoto,p1,p2,p3,p4,p5,p6]
label_img = Label(frameup, image=loginphotos[0]) 
label_img.pack(padx=15, pady=(15,5))
#上一页按钮
lastimage = Image.open('data/GUIpics/last.png')
lastphoto = ImageTk.PhotoImage(lastimage.resize((15, 15)))
lastimgbtn = Button(framemid,image = lastphoto, command=lastimg) 
lastimgbtn.pack(side='left')
#下一页按钮
nextimage = Image.open('data/GUIpics/next.png')
nextphoto = ImageTk.PhotoImage(nextimage.resize((15, 15)))
nextimgbtn = Button(framemid,image = nextphoto, command=nextimg)  
nextimgbtn.pack(side='right')

#搜索框
searchentry = Entry(root, show=None, width = 12)
searchentry.place(x=360,y=5) 

#
mainloop()





    


