import numpy as np
import pandas as pd
np.seterr(divide='ignore',invalid='ignore')

movies = pd.read_csv('data/movielens/movies.csv',sep="::",names=["movieid","title","genres"],engine='python')
data = pd.read_csv('data/movielens/ratings.csv',sep="::",names=["userid","movieid","ratings","timestamp"],engine='python')
movieInfo = pd.read_csv('data/allInfo.csv', sep=",", names=['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction'], engine='python')
movieInfo.index = movieInfo['movieid']

sliced = np.load("data/userbased.npy")
ratings_mat = np.load("data/ratingsMatrix.npy")

matrixx = list(ratings_mat.shape)[0]
matrixy = list(ratings_mat.shape)[1]
listx = list(range(0,matrixx))#0-3951
listy = list(range(0,matrixy))#0-6042 

#这里所有的数据都是svd来的，因此只有每次重启才更新。

def userBasedRec(thisuser):
    index = thisuser - 1 # Movie id starts from 1
    user_row = sliced[index, :]#(20,)
    #取第index行所有列的元素
    magnitude = np.sqrt(np.einsum('ij, ij -> i', sliced, sliced))    
    similarity = np.dot(user_row, sliced.T) / (magnitude[index] * magnitude)
  
    listsimilar = list(similarity)
    listsimilar.sort(reverse=True)
    
    if (listsimilar[1]<0):
        nulllist = []
        return nulllist
    #如果所有电影与当前电影的相似度都为负数
    #说明无推荐 需要更多评论数据
    if (listsimilar[1]>0):#第一个是自己 因此从第二个开始
        selectnum = 2
    if (listsimilar[2]>0):
        selectnum = 3
    if (listsimilar[3]>0):
        selectnum = 4
    if (listsimilar[4]>0):
        selectnum = 5    
    if (listsimilar[5]>0):
        selectnum = 6

    topsim = listsimilar[1:selectnum]#相似度list
    sort_indexes = np.argsort(-similarity)
    topUserid = sort_indexes[1:selectnum]#相似用户list
    
    predictscore = {}
    for i in listx:
        if ratings_mat[i][thisuser-1] == 0: #推荐的必须是自己没有打分过的电影
            val = 0 
            for n in range(0,len(topsim)):
                val = val + ratings_mat[i][topUserid[n]]*round(topsim[n],5)
                if val != 0:
                    predictscore[i+1] = round(val,5)
                    
    recnum = 10
    if len(predictscore)<10:
        recnum = len(predictscore)  
    #判断是否有10个 不足10个的话有几个就推荐几个
                            
    dict = sorted(predictscore.items(), reverse=True, key=lambda kv: kv[1])
    userbasedrec = []
    
    for i in range(recnum):
        if dict[i][1]>2:
            userbasedrec.append(dict[i][0])
    #返回的为 基于user-based推荐的 movieid list 
    #转换为tmbdid
    
    if len(userbasedrec)==0:
        nulllist = []
        return nulllist

    tmbduserbased = []
    for id in userbasedrec:
        tmbduserbased.append(movieInfo[movieInfo.index==id].values.tolist()[0][1])             
    return tmbduserbased
