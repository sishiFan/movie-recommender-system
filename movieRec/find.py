import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ratings = pd.read_csv('data/movielens/ratings.csv',sep="::",names=["userid","movieid","ratings","timestamp"],engine='python')

movieInfo = pd.read_csv('data/allInfo.csv', sep=",", names=['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction'], engine='python')

movies = pd.read_csv('data/movielens/movies.csv',sep="::",names=["movieid","title","genres"],engine='python')

movieInfo.index = movieInfo['movieid']
movieindex = movieInfo.index.tolist()

def unrated():
    ###从未被评过分的以及不存在的movieid
    ratedmovies = ratings["movieid"].value_counts()
    um = ratedmovies.index.tolist()
    um.sort()
    unrated = list(set(movieindex).difference(set(um)))  
    unrated.sort()
    
    return unrated
    
#不存在的id

whole = list(range(1,3953))
nonexist = list(set(whole).difference(set(movieindex)))  
nonexist.sort()
    

#专门一个表格 保存movie year
movies.index = movies['movieid']
for x in range(0,3883):
    movies.iloc[x,1] = movies.iloc[x,1][-5:-1]
    
movies.index = movies['movieid']
movies.sort_values(by = "title", inplace=True, ascending=False)
movies.to_csv("data/movieyear.csv", sep=',',index = False, header = None)
