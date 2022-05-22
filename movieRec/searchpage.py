import numpy as np
import pandas as pd

movies = pd.read_csv('data/movielens/movies.csv',sep="::",names=["movieid","title","genres"],engine='python')
movieyear = pd.read_csv('data/movieyear.csv',sep=",",names=["movieid","year","genres"],engine='python')
movieInfo = pd.read_csv('data/allInfo.csv', sep=",", names=['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction'], engine='python')

movies.index = movies['movieid']
movieyear.index = movieyear['movieid']
list = movieyear.index.values.tolist()

def searchResult(typein):    
    result = []
    for x in list:
        if ((movies[movies.index==x].values.tolist()[0][1][:14].lower()).find(typein.lower()) != -1):
            #忽略大小写
            result.append(movieInfo[movieInfo['movieid']==x].values.tolist()[0][1])
    return result
        
