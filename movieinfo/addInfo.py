from re import T
import numpy as np
import pandas as pd
import csv

movies = pd.read_csv('data/movielens/movies.csv',sep="::",names=["movieid","title","genres"],engine='python')
movieInfo = pd.read_csv('data/movieinfo.csv', sep=",", names=['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction'], engine='python')

movies.index = movies['movieid']
movieindex = movies.index.tolist()
movieInfo.index = movieInfo['movieid']
movieinfoindex = movieInfo.index.tolist()

#找到movieindex有 而movieinfoindex没有的部分
difference = list(set(movieindex).difference(set(movieinfoindex)))  
# bb中有而aa中没有的
difference.sort()
movieid = difference

title = []
year = []
for id in movieid:
    t ="Movie Title : " + movies[movies['movieid']==id].values.tolist()[0][1][:-7]
    d = "Release Date : " + movies[movies['movieid']==id].values.tolist()[0][1][-5:-1]
    title.append(t)
    year.append(d)

genresCate = []
for id in movieid:
    g = "Genres : " + movies[movies['movieid']==id].values.tolist()[0][2].replace("|", ",")
    genresCate.append(g)

tmdbid = list(range(-939, 0))
#造一些负数用于tmdb标记
runtime = np.array(['Runtime : -']*939).tolist()
autherName = np.array(['Director : -']*939).tolist()
language = np.array(['Original Language : -']*939).tolist()
budget = np.array(['Budget : -']*939).tolist()
introduction = np.array(['Introduction : -']*939).tolist()

add = {'movieid': movieid,
        'tmdbid': tmdbid,
        'title': title,
        'year': year,
        'runtime': runtime,  
        'genres': genresCate,
        'auther': autherName,
        'language': language,
        'budget': budget,
        'introduction': introduction    
}

info = pd.DataFrame(add, columns = ['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction']) 
movieInfo = movieInfo.append(info)
movieInfo.index = movieInfo['movieid']
#排列index
movieInfo = movieInfo.sort_index()
#去掉表头
movieInfo.to_csv("data/allInfo.csv", sep=',',index = False, header = None)


# list = movieInfo[movieInfo['tmdbid']==2054].values.tolist()[0]
# print(list)
# print('\n'.join(list[2:]))