import pymongo
import sys
import datetime
import time
import logging

logging.basicConfig(filename="db.log", level=logging.INFO, format="%(levelname)s | %(asctime)s | %(module)s | %(message)s")

import scrapersDW

if __name__ == "__main__":

    logging.info("First load...")

    # Connect to mongo
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")

    # Get the desired database
    db = myclient['dmeDB']

    res = scrapersDW.cargaInicial()

    if len(res) == 0:
        # Error
        sys.exit(1)

    # Get the movies collection
    movies = db['movies']

    return_movies = []

    for movie in movies.find():

        return_movies.append(movie['name'])

    for element in res:

        if element['name'] not in return_movies:

            # Insert
            movies.insert_one(element)


    while True:

        try:
            # Get the day of the week 
            day = datetime.datetime.now().weekday()

            if day == 6: # SUNDAY

                logging.info("Sunday...")

                logging.info("Weekly load...")
                res = scrapersDW.cargaSemanal()
                # Get the movies collection
                movies = db['movies']

                return_movies = []

                for movie in movies.find():

                    return_movies.append(movie['name'])

                for element in res:

                    if element['name'] not in return_movies:

                        # Insert
                        movies.insert_one(element)

                logging.info("Sleeping 6 days...")

                # Sleep 6 days
                time.sleep(518400)

            else:

                # Wait 1 hour
                logging.info("Not sunday...")
                logging.info("Sleeping 1 hour...")
                time.sleep(3600)

        except Exception as e:
            pass