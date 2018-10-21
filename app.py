from flask import Flask, render_template, request,jsonify
from flask_cors import CORS

import json


import psycopg2

import insert_movie



app = Flask(__name__)
CORS(app)


conn = psycopg2.connect("dbname=FTS_db user=postgres password=strato79")
cur = conn.cursor()
cur.execute('SELECT movie_id from movie order by movie_id desc', 'dan')
print(cur.fetchall())


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


    dummyQuery='QUERRRRYYYYY'
    nDocs=771
    ranks=['row1','row2','row3']
    responsePreparedByKarla={
        'query':dummyQuery,
        'nDocs':nDocs,
        'ranks':ranks
    }
    return jsonify(responsePreparedByKarla)




if __name__ == '__main__':
    app.debug = True
    app.run()
