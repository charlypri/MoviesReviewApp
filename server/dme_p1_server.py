from flask import Flask, make_response, jsonify, abort
from bson.objectid import ObjectId
import pymongo
import json

import sentimientosTwitter
import scrapersServidor

app = Flask(__name__)

# Connect to mongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

# Get the desired database
db = myclient['dmeDB']

@app.route("/movies", methods=["GET"])
def getMovies():

    global db

    # Get a list of movies from the database
    
    # Get the movies collection
    movies = db['movies']

    return_movies = []

    for movie in movies.find():

        buffer = {}
        buffer['id'] = str(movie['_id'])
        buffer['name'] = movie['name']

        return_movies.append(buffer)

    # Return the movies in the response
    response =jsonify(return_movies)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/movies/<movie_id>", methods=["GET"])
def getMovieById(movie_id):

    global db

    # Get the information from a given movie (DB)
    movies = db['movies']

    return_movies = []

    for movie in movies.find({"_id": ObjectId(movie_id)}):

        buffer = {}
        buffer['id'] = str(movie['_id'])
        buffer['name'] = movie['name']

        return_movies.append(buffer)

    if len(return_movies) == 0:
        # Wrong movie id
        # Resource not found
        abort(404)

    # Return the movies in the response
    response =jsonify(return_movies)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/movies/<movie_id>/opinions", methods=["GET"])
def getMovieOpinions(movie_id):

    global db

    # Get the opinions from a given movie
    movies = db['movies']

    return_movie = {}

    for movie in movies.find({"_id": ObjectId(movie_id)}):

        return_movie['id'] = str(movie['_id'])
        return_movie['name'] = movie['name']


    if not return_movie:
        # Wrong movie id
        # Resource not found
        abort(404)

    res_1 = None
    res_2 = None
    res_3 = None

    try:
        res_1 = scrapersServidor.recogerDatosFilmaffinity(return_movie['name'])
    except Exception as e:
        pass

    try:
        res_2 = scrapersServidor.getRottenTomatoes(return_movie['name'])
    except Exception as e:
        pass

    try:
        res_3 = scrapersServidor.recogerDatosIMDb(return_movie['name'])
    except Exception as e:
        pass

    
    return_movie['Criticas'] = []

    if res_1 is not None:
        return_movie['Criticas'].extend(res_1['Criticas'])

    if res_2 is not None:
        return_movie['Criticas'].extend(res_2['Criticas'])

    if res_3 is not None:
        return_movie['Criticas'].extend(res_3['Criticas'])

    if len(return_movie['Criticas']) == 0:
        abort(404)

    # Movie found, use scraper for opinions
    response =jsonify(return_movie)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/movies/<movie_id>/rating", methods=["GET"])
def getMovieRating(movie_id):

    global db

    # Get the opinions from a given movie
    movies = db['movies']

    return_movie = {}

    for movie in movies.find({"_id": ObjectId(movie_id)}):

        return_movie['id'] = str(movie['_id'])
        return_movie['name'] = movie['name']


    if not return_movie:
        # Wrong movie id
        # Resource not found
        abort(404)

    res_1 = None
    res_2 = None
    res_3 = None

    try:
        res_1 = scrapersServidor.recogerDatosFilmaffinity(return_movie['name'])
    except Exception as e:
        pass

    try:
        res_2 = scrapersServidor.getRottenTomatoes(return_movie['name'])
    except Exception as e:
        pass

    try:
        res_3 = scrapersServidor.recogerDatosIMDb(return_movie['name'])
    except Exception as e:
        pass

    return_movie['Puntuacion'] = 0

    counter = 0

    if res_1 is not None:
        counter += 1
        return_movie['Puntuacion'] += float(res_1['Puntuacion'])

    if res_2 is not None:
        counter += 1
        return_movie['Puntuacion'] += float(res_2['Puntuacion'])
    
    if res_3 is not None:
        counter += 1
        return_movie['Puntuacion'] += float(res_3['Puntuacion'])

    if counter == 0:
        abort(404)

    return_movie['Puntuacion'] = float(return_movie['Puntuacion']/counter)

    # Movie found, use scraper for opinions
    response =jsonify(return_movie)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/movies/<movie_id>/twitter", methods=["GET"])
def getMovieTwitter(movie_id):

    global db

    # Get the twitter info from a given movie
    movies = db['movies']

    return_movies = []

    for movie in movies.find({"_id": ObjectId(movie_id)}):

        buffer = {}
        buffer['id'] = str(movie['_id'])
        buffer['name'] = movie['name']

        return_movies.append(buffer)

    if len(return_movies) == 0:
        # Wrong movie id
        # Resource not found
        abort(404)

    # Movie found, use twitter
    res = None

    try:
        res = sentimientosTwitter.scrappingTwitter(return_movies[0]['name'])
    except Exception as e:
        pass
    # res = res.replace("\'", "\"")
    # res = json.loads(res)
    
    if not res or res is None:
        abort(404)

    res['id'] = movie_id

    response =jsonify(res)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response



if __name__ == "__main__":

    app.run(host="127.0.0.1", port=5002)