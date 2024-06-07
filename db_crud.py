from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3

try:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get("https://m.imdb.com/chart/top/", headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    movies = soup.find('ul',class_="ipc-metadata-list").find_all("li")
    movie_list = {"movie_rank":[],"movie_name":[],"movie_year":[],"movie_rate":[]}

    for movie in movies:
        #print(movie)
        rank = movie.find('div',class_="ipc-title").a.text.split('.')[0]
        movie_name = movie.find('div',class_="ipc-title").a.text.split('.')[1]
        rate = movie.find('div',class_="iKUUVe").span.text.replace('(','')
        rate=rate.replace(')','')
        year = movie.find('div',class_="kZGNjY").span.text
        #print(rank,movie_name,year,rate)
        movie_list["movie_rank"].append(rank)
        movie_list["movie_name"].append(movie_name)
        movie_list["movie_year"].append(year)
        movie_list["movie_rate"].append(rate)
    
except Exception as e:
    print(e)
df = pd.DataFrame(data = movie_list)
print(df.head())

connection = sqlite3.connect("test.db")
cursor = connection.cursor()
qry = "create table if not exists movies(movie_rank,movie_name,movie_year,movie_rate)"
cursor.execute(qry)

for i in range(len(df)):
    cursor.execute("insert into movies values (?,?,?,?)", df.iloc[i])

connection.commit()
connection.close()

