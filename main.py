import time
import requests
import selectorlib
from send_email import send_email
import sqlite3


URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

connection = sqlite3.connect("data.db")


def scrape(url):
    """
    Scrape the page source from the URL
    :return:
    """
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def store(extracted_local):
    row_local = extracted_local.split(",")
    row_local = [item.strip() for item in row_local]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row_local)
    connection.commit()


def read(extracted_local):
    row_local = extracted_local.split(",")
    row_local = [item.strip() for item in row_local]
    band, city, date = row_local
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                   (band, city, date))
    rows = cursor.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            row = read(extracted)
            # Sí read devuelve una lista vacía quiere decir que existe un nuevo
            # evento, por lo tanto se niega para que se cumpla la condición
            if not row:
                store(extracted)
                send_email(message="Hey, new event was found")
        time.sleep(2)
