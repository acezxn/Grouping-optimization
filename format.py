import sqlite3

con = sqlite3.connect('db.sqlite3')

cur = con.cursor()
def comb_format():
    blacklist = []
    user2id = dict()
    userdata = dict()
    users = []

    for row in cur.execute('SELECT * FROM auth_user'):
        username = row[4]
        id = row[0]
        if row[3] != 1:
            users.append(username)
            user2id[id] = username
        else:
            blacklist.append(id)

    for row in cur.execute('SELECT * FROM accounts_userprofile'):
        id = row[4]
        favored = row[2].split(',')
        disliked = row[3].split(',')
        if id not in blacklist:
            userdata[user2id[id]] = [favored, disliked]
    return userdata, users
