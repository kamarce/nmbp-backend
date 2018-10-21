from flask import Flask, render_template, request,jsonify
from flask_cors import CORS

import json


import psycopg2

import insert_movie

import search_db



app = Flask(__name__)
CORS(app)


conn = psycopg2.connect("dbname=FTS_db user=postgres password=strato79")
cur = conn.cursor()
#cur.execute('SELECT movie_id from movie order by movie_id desc', 'dan')
#print(cur.fetchall())

#search_db.search_movie(conn,'dog','OR')

search_db.getAuto(conn,'saga')


@app.route('/')
def index():
    return jsonify("HELLO FLASK")

@app.route('/add', methods=['POST'])
def addMovie():
    print(request.data)
    data=json.loads(request.data)
    print('dataa',data)
    for k,v in data.items():
        print(k,v)

    newMovieId=insert_movie.insert(
        conn,
        data['title'],
    data['category'],
    data['summary'],
    data['description']
    )
    return jsonify({"movieId":newMovieId})


@app.route('/search', methods=['POST'])
def search():
    print(request.data)
    data=json.loads(request.data)
    print('dataa',data)
    for k,v in data.items():
        print(k,v)

    resultQuery, resultRanks=search_db.search_movie(conn,data['userQuery'], data['operator'])
    return jsonify(search_db.prepareJson(resultQuery,resultRanks))


@app.route('/auto', methods=['POST'])
def auto():
    print(request.data)
    data=json.loads(request.data)
    if data['userQuery']:
        autocompleteResult=search_db.getAuto(conn,data['userQuery'])


        print('AUTOCOMPLETE RESULT',autocompleteResult)
        return jsonify({'options':autocompleteResult})
    else:
        return jsonify({'options':[]})



if __name__ == '__main__':
    app.debug = True
    app.run()
