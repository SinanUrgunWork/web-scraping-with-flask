from flask import Flask, render_template
from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
import pandas as pd
app = Flask(__name__)


urlkitapyurdu="https://www.kitapyurdu.com/index.php?route=product/search&page=1&filter_name=python&filter_in_stock=1&fuzzy=0"
url_base="https://www.kitapsepeti.com"
url="https://www.kitapsepeti.com/arama?q=python"
 # MongoDB settings
uri = 'mongodb://localhost:27017/'  # MongoDB URI
db_name = 'smartmaple'              # Database name
collection_name_sepeti = 'kitapsepeti'     # Collection name
collection_name_yurd = 'kitapyurdu'     # Collection name

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/KitapSepeti')
def left_page():
    # Yükleme bitti
    LookAndAddKitapSepeti()
    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name_sepeti]

    # Find all the documents in the collection
    all_documents = collection.find()

    # Create a list to store the dictionaries
    data_list = []

    # Iterate over the documents and append them to the data list
    for document in all_documents:
        data_list.append(document)

    # Close the connection to the MongoDB
    print(data_list[1])
    client.close()
    return render_template('KitapSepeti.html', data=data_list)

@app.route('/KitapYurdu')
def right_page():

    LookAndAddKitapYurdu()
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name_yurd]

    # Find all the documents in the collection
    all_documents = collection.find()

    # Create a list to store the dictionaries
    data_list = []

    # Iterate over the documents and append them to the data list
    for document in all_documents:
        data_list.append(document)

    # Close the connection to the MongoDB
    print(data_list[1])
    client.close()
    return render_template('KitapYurdu.html', data=data_list)

def KitapSepetiScrap(url):
    html_text=requests.get(url).text
    soup =BeautifulSoup(html_text,"lxml")

    writers = []
    publishers = []
    names = []
    prices = []


    books_name=soup.find_all("a",class_="fl col-12 text-description detailLink")

    for name in books_name:
        names.append(name.text.strip())


    books_publisher=soup.find_all("a",class_="col col-12 text-title mt")

    for publisher in books_publisher:
        publishers.append(publisher.text)


    books_writer=soup.find_all("a",class_="fl col-12 text-title")

    for writer in books_writer:
        writers.append(writer.text)



    books_price=soup.find_all("div",class_="col col-12 currentPrice")

    for price in books_price:
        price_text = price.text[:-3]
        prices.append(price_text)


    data = {
        "writer": writers,
        "publisher": publishers,
        "name": names,
        "price(TL)": prices
    }

    df = pd.DataFrame(data)
    return df


def KitapYurduScrap(urlkitapyurdu):
    html_text=requests.get(urlkitapyurdu).text
    soup =BeautifulSoup(html_text,"lxml")
    product=soup.find("div",class_="product-grid")
    writers = []
    publishers = []
    names = []
    prices = []


    books_name=product.find_all("div",class_="name")

    for name in books_name:
        names.append(name.text.strip())


    books_publisher=product.find_all("div",class_="publisher")

    for publisher in books_publisher:
        publishers.append(publisher.span.text)


    books_writer=product.find_all("div",class_="author compact ellipsis")

    for writer in books_writer:
        writers.append(writer.text)



    books_price=product.find_all("div", class_="price-new")

    for price_div in books_price:
        price_span = price_div.find("span", class_="value")
        if price_span is not None:
            price_text = price_span.text.strip()
        prices.append(price_text)


    data = {
        "writer": writers,
        "publisher": publishers,
        "name": names,
        "price(TL)": prices
    }

    df = pd.DataFrame(data)
    return df


def NextPageKitapYurdu(urlkitapyurdu):
    html_text=requests.get(urlkitapyurdu).text
    soup =BeautifulSoup(html_text,"lxml")
    next_page=soup.find("a",class_="next")
    for_if =next_page.has_attr('href')
    if for_if:
        href_part=next_page['href']
        url_next=href_part
        return url_next


def NextPageKitapSepeti(url):
    html_text=requests.get(url).text
    soup =BeautifulSoup(html_text,"lxml")
    next_page=soup.find("a",class_="next")
    for_if =next_page.has_attr('href')
    if for_if:
        href_part=next_page['href']
        url_next=url_base+href_part
        return url_next
def LookAndAddKitapSepeti():
    new_df=KitapSepetiScrap(url)
    new_df=new_df.append(KitapSepetiScrap(NextPageKitapSepeti(url)), ignore_index=True)
    # Convert DataFrame to dictionary (records format) for easier insertion
    records = new_df.to_dict(orient='records')

    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name_sepeti]

    # Insert DataFrame records into the MongoDB collection
    for record in records:
    # Check if a similar record exists based on writer, publisher, name, and price
        existing_record = collection.find_one({
            'writer': record['writer'],
            'publisher': record['publisher'],
            'name': record['name'],
            'price(TL)': record['price(TL)']
        })
    # If the record doesn't exist, insert it into the collection
        if not existing_record:
            collection.insert_one(record)
    client.close()

def LookAndAddKitapYurdu():
    new_df=KitapYurduScrap(urlkitapyurdu)
    new_df=new_df.append(KitapYurduScrap(NextPageKitapYurdu(urlkitapyurdu)), ignore_index=True)
    # Convert DataFrame to dictionary (records format) for easier insertion
    records = new_df.to_dict(orient='records')

    # Connect to MongoDB
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name_yurd]

    # Insert DataFrame records into the MongoDB collection
    for record in records:
    # Check if a similar record exists based on writer, publisher, name, and price
        existing_record = collection.find_one({
            'writer': record['writer'],
            'publisher': record['publisher'],
            'name': record['name'],
            'price(TL)': record['price(TL)']
        })
    # If the record doesn't exist, insert it into the collection
        if not existing_record:
            collection.insert_one(record)
    client.close()

if __name__ == '__main__':
    app.run(debug=True)
