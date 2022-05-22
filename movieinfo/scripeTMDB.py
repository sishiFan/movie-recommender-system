from bs4 import BeautifulSoup
import requests
import pandas as pd
import os.path

links = pd.read_csv('data/movielens/links.csv',names=["movieid","imdbId","tmdbId"],engine='python').drop(['imdbId'], axis=1, inplace=False)

movieidx= links['movieid'].tolist()
tmdbidx = links['tmdbId'].tolist()

movieid = []
tmdbid = []

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

title = []
year = []
runtime = []
genresCate = []
autherName = []
language = []
budget = []
introduction = []

def movieinfo(id): 
    try:
        source = requests.get(url="https://www.themoviedb.org/movie/"+str(id),headers=headers)
        source.raise_for_status()
        soup = BeautifulSoup(source.text,'html.parser')
    
        #title
        name = soup.select('div.single_column > section > div > section > div > h2 > a')   
        n = name[0].text.lstrip().rstrip()
        nn = "Movie Title : " + n
        if (len(nn) == 0):
            title.append('')
        else:
            title.append(nn)
        
        #year and location
        yandl = soup.select('.release')
        y = yandl[0].text
        yy = "Release Date : " + y.lstrip().rstrip()
        if (len(yy) == 0):
            year.append('')
        else:
            year.append(yy)
        
        #runtime
        dur = soup.select('.runtime')
        s = dur[0].text
        #得在此处判断list长度
        ss = "Runtime : " + s.lstrip().rstrip()
        if (len(ss) == 0):
            runtime.append('')
        else:
            runtime.append(ss)
        
        #genres
        genres = soup.select('.genres')   
        g = genres[0].text.lstrip().rstrip()
        gg = "Genres : " + ''.join(g.split())
        if (len(gg) == 0):
            genresCate.append('')
        else:
            genresCate.append(gg)
        
        #auther,一般是director
        auther = soup.select('.profile')
        a = auther[0].text.lstrip().rstrip()
        #print(auther[0].text.lstrip().rstrip().replace("\n",": "))
        alist = a.split("\n")
        parts = [alist[1], alist[0]]
        aa = alist[1] + " : " + alist[0]
        if (len(aa) == 0):
            autherName.append('')
        else:
            autherName.append(aa)
        
        #original language and budget
        content = soup.select('div.content_wrapper > div.grey_column > div > section.split_column > div > div > section > p')   
        ll = "Original Language : " + content[1].text[18:]
        bb = "Budget : " + content[3].text[8:]
        if (len(ll) == 0):
            language.append('')
        else:
            language.append(ll)
            
        if (len(bb) == 0):
            budget.append('')
        else:
            budget.append(bb)
        
        #introduction
        doc = soup.find('p').text
        ii = "Introduction : " + doc
        if (len(ii) == 0):
            introduction.append('')
        else:
            introduction.append(ii)
   
        #img
        picpath = "data/pics/"+ str(id) +".png"
        if os.path.exists(picpath):
            print('This image is already there.')
        else:
            img = soup.select('div.poster > div > img')
            endurl = img[0].get('data-src')
            fronturl = 'https://image.tmdb.org'
            picurl = fronturl + endurl
            pic = requests.get(picurl).content
            with open(picpath, 'wb') as f:
                f.write(pic)
            print('Image is written.')
    except Exception as e: 
        print(e)
          
for x in range(0,2944):
    print(tmdbidx[x],x)
    movieid.append(movieidx[x])
    tmdbid.append(tmdbidx[x])
    movieinfo(int(tmdbidx[x])) 
    
info = {'movieid': movieid,
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

movieInfomation = pd.DataFrame(info, columns = ['movieid','tmdbid','title','year','runtime','genres','auther','language','budget','introduction']) 

print(movieInfomation)

movieInfomation.to_csv("data/movieinfo.csv", sep=',',index = False, header = None)
#movieInfomation.to_csv("data/movieinfo.csv", sep=',',index = False)

   


