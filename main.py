import http.client
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/"

parsed_url = urlparse(url)
host = parsed_url.netloc

connection = http.client.HTTPConnection(host)
connection.request("GET", parsed_url.path)
response = connection.getresponse()

if response.status == 200:
    soup = BeautifulSoup(response.read(), "html.parser")
    books = soup.find_all("h3")
    prices = soup.find_all(class_="price_color")

    data = []

    for book, price in zip(books, prices):
        title = book.a.attrs["title"]
        price_text = price.get_text()
        data.append((title, price_text))

    csv_filename = "book_data.csv"

    with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Title", "Price"])  # Intestazioni
        csv_writer.writerows(data)

    print(f"Data saved to {csv_filename}")
else:
    print("Error requesting:", response.status)
