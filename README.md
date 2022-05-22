# movie-recommender-system
运行 recgui.py 来运行整个电影推荐系统，第一次打开比较慢，需要1-2分钟。
登录系统的话 账号在accounts.csv中，也可以自己注册。
如果注册新账号，在评论完一些电影后（最好是5个电影以上），要重启系统再登录，个性化推荐才会更新。 
因为每次重启系统才会重新SVD分解矩阵。

文件目录子文件简单介绍：

data文件夹中：
GUIpics文件夹：包含登录界面的介绍图片；
movielens文件夹： 包含movielens数据；
pics文件夹： 包含爬取的电影海报；
accounts.csv 账号信息；
allInfo.csv 爬取到的电影信息 + 其他电影的信息（因为种种原因无法从TMDB上爬信息的电影）；
itembased.npy 降维后的item矩阵；
movieinfo.py 爬取到的电影信息；
movieyear.csv 电影年代；
ratingsMatrix.npy 完整矩阵；
userbased.npy 降维后的user矩阵。

movieinfo文件夹中：
addInfo.py 对于未能爬取到数据的电影进行信息的补充；
scripeTMDB.py 从TMDB数据库 爬取电影信息。

movieRec文件夹中：
createaccounts.py 写入数据库中本来存在的6040个账号 用户名为1-6040，密码全部为123456；
find.py 多余的movieid的筛选处理；
itemsvd.py 相似电影推荐；
newaccounts.py 注册新用户 新账号写入；
recgui.py 系统界面 运行它来运行整个系统；
searchpage.py 搜索引擎；
svdmat.py 矩阵的SVD分解；
temptCodeRunnerFile.py；
usersvd.py 基于用户的协同过滤算法。

