
import psycopg2


def insert(conn, title, categories, summary, description):
    """ insert a new movie into the movie table """
    print('INSERT FUN CALLED WITH:',(conn, title, categories, summary, description))
    sql = """INSERT INTO movie(title,categories,summary,description)
             VALUES(%s,%s,%s,%s) RETURNING movie_id;"""

    movie_id = None
    try:
      # create a new cursor
        cur = conn.cursor()

        # execute the INSERT statement
        cur.execute(sql, (title, categories, summary, description))

        # get the generated id back
        movie_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


    return movie_id
