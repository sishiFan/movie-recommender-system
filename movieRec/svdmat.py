import numpy as np
import pandas as pd
np.seterr(divide='ignore',invalid='ignore')

movies = pd.read_csv('data/movielens/movies.csv',sep="::",names=["movieid","title","genres"],engine='python')
data = pd.read_csv('data/movielens/ratings.csv',sep="::",names=["userid","movieid","ratings","timestamp"],engine='python')

def svd():
    ratings_mat = np.ndarray(
    shape=(np.max(data.movieid.values), np.max(data.userid.values)),dtype=np.uint8)
    ratings_mat[data.movieid.values-1, data.userid.values-1] = data.ratings.values
    np.save("data/ratingsMatrix.npy",ratings_mat)  
    
    #calculate the mean rating by each user (excluding zeros)
    nonzero_average = []
    for i in range(0,np.shape(ratings_mat)[0]):
        nonzero_rating_perrow = []  
        for item in ratings_mat[i]:
            if item!= 0:
                nonzero_rating_perrow.append(item)
        if len(nonzero_rating_perrow) != 0:
            average_per_row = np.mean(nonzero_rating_perrow)
        else:
            average_per_row = 0
        nonzero_average.append(average_per_row)
         
    ll =len(nonzero_average)
    nonzero_average = np.asarray(nonzero_average)
    nonzero_average = nonzero_average.reshape(ll,1)
    
    #matrix1 = (ratings_mat - np.asarray([(np.mean(ratings_mat, 1))]).T) # subtract the mean ratings (6040, 3952)
    
    matrix1 = (ratings_mat - nonzero_average) # subtract with the mean     
    matrix = matrix1.T # matrix transpose (3952, 6040)
    U, S, V = np.linalg.svd(matrix)
    sliced = V.T[:, :20] # representative data (3952, 20)
    np.save("data/itembased.npy",sliced)
    U1, S1, V1 = np.linalg.svd(matrix1)
    sliced1 = V1.T[:, :20] # representative data (6040, 20)
    np.save("data/userbased.npy",sliced1)
    
#去掉 .T 变为 user based
# np.mean(ratings_mat, 1) 压缩列，对各行求均值, 求的是每个movie的平均分
# T转制 又一行变为一列，用来给矩阵减去平均分
# normalise matrix (subtract mean off)
svd()