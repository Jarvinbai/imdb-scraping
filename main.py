from bs4 import BeautifulSoup
import requests,openpyxl


excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Movie Title"
sheet.append(['Rank','Movie Name','Year of Release','IMDB Rating'])
try:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get("https://m.imdb.com/chart/top/", headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    #print(soup)
    movies = soup.find('ul',class_="ipc-metadata-list").find_all("li")

    for movie in movies:
        #print(movie)
        rank = movie.find('div',class_="ipc-title").a.text.split('.')[0]
        movie_name = movie.find('div',class_="ipc-title").a.text.split('.')[1]
        rate = movie.find('div',class_="iKUUVe").span.text.replace('(','')
        rate=rate.replace(')','')
        year = movie.find('div',class_="kZGNjY").span.text
        #print(rank,movie_name,year,rate)
        sheet.append([rank,movie_name,year,rate])
    
except Exception as e:
    print(e)

excel.save('Movies.xlsx')
