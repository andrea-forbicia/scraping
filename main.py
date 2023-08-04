import http.client  # Effettua richieste HTTP
from urllib.parse import urlparse  # Analizza URL
from bs4 import BeautifulSoup  # Analizza contenuto HTML
import csv  # Lavorare con file CSV

# Definizione dell'URL:
# La variabile url contiene l'indirizzo del sito "Books to Scrape" che vuoi analizzare.
url = "http://books.toscrape.com/"

# Parsing dell'URL:
# Il modulo urllib.parse viene utilizzato per analizzare l'URL in componenti come lo schema, l'host e il percorso.
# Questi componenti sono utilizzati successivamente per effettuare la richiesta HTTP.
parsed_url = urlparse(url)
host = parsed_url.netloc

# Connessione e richiesta HTTP:
connection = http.client.HTTPConnection(host)
connection.request("GET", parsed_url.path)
response = connection.getresponse()

# Analisi del contenuto HTML:
if response.status == 200:
    soup = BeautifulSoup(response.read(), "html.parser")
    books = soup.find_all("h3")
    prices = soup.find_all(class_="price_color")

    data = []

    for book, price in zip(books, prices):
        title = book.a.attrs["title"]
        price_text = price.get_text()
        data.append((title, price_text))

    # Scrittura dei dati in un file CSV:
    csv_filename = "book_data.csv"

    with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Title", "Price"])  # Intestazioni
        csv_writer.writerows(data)

    print(f"Data saved to {csv_filename}")
else:
    print("Error requesting:", response.status)
