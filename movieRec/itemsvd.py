import numpy as np
import pandas as pd
from find import unrated
from find import nonexist

np.seterr(divide='ignore',invalid='ignore')

movies = pd.read_csv('data/movielens/movies.csv',sep="::",names=["movieid","title","genres"],engine='python')
data = pd.read_csv('data/movielens/ratings.csv',sep="::",names=["userid","movieid","ratings","timestamp"],engine='python')
movieInfo = pd.read_csv('data/allInfo.csv', sep=",", names=['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction'], engine='python')
movieInfo.index = movieInfo['movieid']

sliced = np.load("data/itembased.npy")

def top_cosine_similarity(tmdbId):
    tmbdMovie = []
    #接受的为tmbd 转换为movieid
    movie_id = movieInfo[movieInfo['tmdbid']==tmdbId].values.tolist()[0][0]
    #如果电影属于从未被评论过的电影 不给出相似推荐
    if (movie_id in unrated()):
        return tmbdMovie
    
    index = movie_id - 1 # Movie id starts from 1
    movie_row = sliced[index, :] #(20,)
    #取第index行所有列的元素
    
    magnitude = np.sqrt(np.einsum('ij, ij -> i', sliced, sliced))
    similarity = np.dot(movie_row, sliced.T) / (magnitude[index] * magnitude)
    sort_indexes = np.argsort(-similarity)
    
    #这里检查过滤，去除没有的movieid数据
    sort = [ i+1 for i in sort_indexes]
    #去掉自己 自己为第一个
    sortMovieid = sort[1:11] 
    sortMovieid = list(set(sortMovieid).difference(set(nonexist)))
    for id in sortMovieid:
        tmbdMovie.append(movieInfo[movieInfo.index==id].values.tolist()[0][1])       
    return tmbdMovie 



