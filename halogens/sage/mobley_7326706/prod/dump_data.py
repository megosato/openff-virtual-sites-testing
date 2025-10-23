import pickle

# for reading also binary mode is important
dbfile = open('dg_error.pickle', 'rb')
db = pickle.load(dbfile)
print("err:", db)

dbfile = open('dg.pickle', 'rb')
db = pickle.load(dbfile)
print("dg: ", db)
