from bs4 import BeautifulSoup
import requests,openpyxl
import re

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Movie Title"
sheet.append(['S.No','Movie Name','Year Of Release','IMDB Rating','Story','Director','Gross'])
try:
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    response = requests.get("https://m.imdb.com/search/title/?genres=Adventure&sort=user_rating,desc&title_type=feature&num_votes=25000,&ref_=chttp_gnr_1", headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.find("div",class_="lister-list").find_all("div",class_="lister-item")
    for movie in movies:
        #print(movie)
        index = movie.find('h3').find('span',class_="lister-item-index").get_text(strip=True).split('.')[0]
        name = movie.find('h3').a.text
        year = movie.find('h3').find('span',class_="lister-item-year").text
        year = re.sub("\D","",year)
        rate = movie.find("div",class_="ratings-imdb-rating").strong.text
        story = movie.find("p").findNext("p").get_text(strip=True)
        director = movie.find("p").findNext("p").findNext("p").a.text
        gross = movie.find("p",class_="sort-num_votes-visible").find_all("span")[-1].get_text()
        #print(index,name,year,rate,story,director,gross)
        sheet.append([index,name,year,rate,story,director,gross])
    
    
except Exception as e:
    print(e)

excel.save('Action.xlsx')
