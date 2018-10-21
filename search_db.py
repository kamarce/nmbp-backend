import psycopg2

def getAuto(conn,userInput):

    sql = """
            SELECT summary,similarity(summary,%s) slicnost
            FROM movie ORDER BY slicnost DESC LIMIT 5;
          """
    result=None
    summary=None
    slicnost=None

    try:
            # create a new cursor
            cur = conn.cursor()

            # execute SQL
            cur.execute(sql, (userInput,))

            result = cur.fetchmany(20)
            #print(result)

            firstParts=[t[0] for t in result]
            secondParts=[t[1] for t in result]

            print(userInput)
            firstIndex=[st.lower().find(userInput.lower()) for st in firstParts]
            print(firstIndex)



            result=[s[i:] for s,i in zip(firstParts,firstIndex)]





            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    return result



def search_movie(conn, user_input_str, user_operator):
    """ search user input in movie table, operator can be AND or OR """
   # print('SEARCH FUN CALLED WITH:', (conn, user_input_str, user_operator))

    my_query_final = getUserQuery(user_input_str, user_operator)

   # print('final query : ', my_query_final)

    sql = """
        SELECT
          ts_headline('english',title,keywords) AS result_title,
          ts_headline('english',description,keywords) AS result_descr,
          ts_rank_cd(allTSV,keywords, 1) AS my_rank
        FROM movie,to_tsquery('english',%s) keywords  
        WHERE keywords @@ allTSV
        ORDER BY my_rank DESC;"""


    movie_id = None
    try:
        # create a new cursor
        cur = conn.cursor()

        # n is number of rows in movie table
        num_rows = cur.execute("SELECT COUNT(*) FROM movie;")
        k = cur.fetchone()
        n = k[0]

        # execute SQL
        cur.execute(sql, (my_query_final,))

        # fetching results (max n records in table movie)
        result = cur.fetchmany(n)
        print(result)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return sql % my_query_final,result


### PARSING USER QUERY
def splitUserQuery(q):
    splitted = q.split('"')
    trimmed = [s.strip() for s in splitted]
    cleaned = [t for t in trimmed if t]
    return cleaned


def getPreparedSubparts(cleaned):
    splittedByBlank = [k.split() for k in cleaned]
    print(splittedByBlank)
    joinedWithAnd = [' <-> '.join(spb) for spb in splittedByBlank]
    bracketsAdded = ['({})'.format(n) for n in joinedWithAnd]
    return bracketsAdded


def getUserQuery(q, operator):
    sqlOperator = ' & ' if operator == 'AND' else ' | '
    parts = splitUserQuery(q)
    prepared = getPreparedSubparts(parts)
    return sqlOperator.join(prepared)

def prepareJson(resultQuery,rankList):
    p={'query':resultQuery}
    ranksPrepList=[];
    for r in rankList:
        ranksPrepList.append(
            {'title':r[0],'description':r[1],'rank':r[2]}
        )
    p['ranks']=ranksPrepList
    p['nDocs']=len(ranksPrepList)

    return p