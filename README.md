# web-scraping-with-flask
# How to run the application:  
Ensure that you have installed Python and the required packages from the requirements.txt file.  
Navigate to the project folder containing app.py, main.html, KitapSepeti.html, and KitapYurdu.html.  
Open a terminal or command prompt in the project folder.  
Run the Flask application using the following command: python app.py  
The application will start running on a local server, and you can access it through your web browser by going to http://127.0.0.1:5000/.  
The Flask application provides a web interface to fetch and display data from the KitapSepeti and KitapYurdu websites. Here is a brief overview of each page:  
# Main Page (main.html):
This is the home page of the application.  
It provides two buttons: "Kitap Sepeti" (Book Basket) and "Kitap Yurdu" (Book World).  
Clicking on these buttons will take the user to the respective pages where the data is displayed.  
# KitapSepeti Page (KitapSepeti.html):  
This page displays the data scraped from the KitapSepeti website.  
It shows a table containing columns for "Author," "Publisher," "Name," and "Price (TL)."  
The data is fetched from the MongoDB collection named "kitapsepeti."  
# KitapYurdu Page (KitapYurdu.html):  
This page displays the data scraped from the KitapYurdu website.  
It also shows a table containing columns for "Author," "Publisher," "Name," and "Price (TL)."  
The data is fetched from the MongoDB collection named "kitapyurdu."  
# Web Scraping:  
To accomplish web scraping, the following four functions are primarily used:  
# KitapSepetiScrap:  
Fetches the HTML content of the page using request.get().  
Parses the HTML content using BeautifulSoup and the "lxml" parser.  
Finds all elements containing book names, publishers, authors, and prices using BeautifulSoup's find_all() method.  
Extracts the text content of these elements and stores them in separate lists (names, publishers, authors, prices).  
Creates a dictionary (data) from these lists and converts it into a pandas DataFrame (df).  
The KitapSepetiScrap function returns the DataFrame (df) containing the scraped data.  
# KitapYurduScrap:  
Fetches the HTML content of the page using request.get().  
Parses the HTML content using BeautifulSoup and the "lxml" parser.  
Finds the container element containing multiple book items using BeautifulSoup's find() method.  
Within this container, finds all elements containing book names, publishers, authors, and prices using find_all().  
Extracts the text content of these elements and stores them in separate lists (names, publishers, authors, prices).  
Creates a dictionary (data) from these lists and converts it into a pandas DataFrame (df).  
The KitapYurduScrap function returns the DataFrame (df) containing the scraped data.  
# Next Page URLs:  
Defines NextPageKitapSepeti and NextPageKitapYurdu functions to manage pagination on the KitapSepeti and KitapYurdu websites, respectively.  
These functions take the current page URL as input, fetch the HTML content of the page, and use BeautifulSoup to find the URL of the next page.  
If the next page is found, the function returns the URL as a string; otherwise, it returns None.  
# Checking and Storing Data in MongoDB:  
We have two functions, LookAndAddKitapSepeti and LookAndAddKitapYurdu, to handle the web scraping and data storage.  
These functions call the respective scraping functions and store the scraped data in MongoDB collections.  
Before adding data to the MongoDB collections, they check for existing records to avoid duplicates.  
The scraped data is stored in a list of records that is converted to a dictionary using to_dict(orient='records').  
# Additional Notes:  
I have not added a refreshing function for the web scraping part; it will not perform a complete re-scrape after a certain interval. It will only re-scrape from the beginning when we manually refresh the page, but it will not add duplicate data if there are no changes.  
In your Flask routes (main_page, left_page, and right_page), you fetch data from the MongoDB collections and pass it to the respective HTML templates for rendering. In the HTML templates (main.html, KitapSepeti.html, and KitapYurdu.html), you use Jinja2 template to loop through the data and display it in tables.  
