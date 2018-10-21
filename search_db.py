









### PARSING USER QUERY
def splitUserQuery(q):
    splitted= q.split('"')
    trimmed=[s.strip() for s in splitted]
    cleaned=[t for t in trimmed if t]
    return cleaned

def getPreparedSubparts(cleaned):
    splittedByBlank= [k.split() for k in cleaned]
    print(splittedByBlank)
    joinedWithAnd=[' <-> '.join(spb) for spb in splittedByBlank ]
    bracketsAdded=['({})'.format(n) for n in joinedWithAnd]
    return bracketsAdded

def getUserQuery(q,operator):
    sqlOperator=' & ' if operator == 'AND' else ' | '
    parts=splitUserQuery(q)
    prepared=getPreparedSubparts(parts)
    return sqlOperator.join(prepared)