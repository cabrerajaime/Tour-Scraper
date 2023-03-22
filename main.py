import time
import requests
import selectorlib
from send_email import Email
import sqlite3


URL = "http://programmer100.pythonanywhere.com/tours/"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class Event:
    def scrape(self, url):
        """
        Scrape the page source from the URL
        :return:
        """
        response = requests.get(url, headers=HEADERS)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
        value = extractor.extract(source)["tours"]
        return value


class DataBase:

    def __init__(self, database_path):
        self.connection = sqlite3.connect(database_path)

    def store(self, extracted_local):
        row_local = extracted_local.split(",")
        row_local = [item.strip() for item in row_local]
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO events VALUES(?,?,?)", row_local)
        self.connection.commit()

    def read(self, extracted_local):
        row_local = extracted_local.split(",")
        row_local = [item.strip() for item in row_local]
        band, city, date = row_local
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?",
                       (band, city, date))
        rows = cursor.fetchall()
        print(rows)
        return rows


if __name__ == "__main__":
    event = Event()
    email = Email()
    while True:
        scraped = event.scrape(URL)
        extracted = event.extract(scraped)
        print(extracted)

        if extracted != "No upcoming tours":
            database = DataBase(database_path="data.db")
            row = database.read(extracted)
            # Sí read devuelve una lista vacía quiere decir que existe un nuevo
            # evento, por lo tanto se niega para que se cumpla la condición
            if not row:
                database.store(extracted)
                email.send_email(message="Hey, new event was found")
        time.sleep(2)
