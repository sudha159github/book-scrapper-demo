# python -m pip install requests = get data from web(html, json, xml)
# python -m pip install beautifulsoup4 = parse html
# pypi =library



# git config --global user.name "FIRSTNAME LAST_NAME"
# git config --global user.email "MY_NAME@rxample.com"

# git tutorial
#install git
# create repository in github

# go to git bash
# git config --global user.name "sudhaghimire"
# git config --global user.email "sudhaghimire159@g,mail.com"

# git init
# git status => if you want to check what are the status of files
# git diff=> if you want to check what are the changes
# git add .=> file track
# git commit -m "your message"
# copy paste git code from github

#1. change the code
# 2. git add .
#3. git commit -m "your message"
# 4 git push origin


import requests 
import sqlite3


from bs4 import BeautifulSoup

URL = "http://books.toscrape.com/"

def create_database():
  conn = sqlite3.connect("books.sqlite3")
  cursor = conn.cursor()
  cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    price REAL,
    currency TEXT
    )
    """
  )
  conn.commit()
  conn.close()

def insert_book(title, price, currency):
  conn = sqlite3.connect("books.sqlite3")
  cursor = conn.cursor()
  cursor.execute(
    """
    INSERT INTO books (title , price, currency) VALUES(?, ?, ?)
    """,
    (title, price, currency),

  )
  conn.commit()
  conn.close()



def scrape_books(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"failed to fetch the page, ststus code: {response.ststus_code}")
        return
  
    # set encoding explicitly to handle special characters
    response.encoding = response.apparent_encoding
   


    soup = BeautifulSoup(response.text, "html.parser")
    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.h3.a["title"]
        price_text= book.find("p", class_="price_color").text
        


      # extract currency and numeric part
      # the first character should be the currency symbol (e.g, $)

        currency = price_text[0]
        price = price_text[1:]

        insert_book(title, price, currency)

create_database()
scrape_books(URL)

