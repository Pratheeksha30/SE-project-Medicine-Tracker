import sqlite3
def ad(Usid,password,email,usr):
    if usr == 'User':
        conn = sqlite3.connect('User_database.db')
        c=conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS User(
                        usid text primary key,
                        user_password text,
                        email_id text)""")
        c.execute("INSERT INTO User VALUES ('{}','{}','{}')".format(Usid,password,email))
        conn.commit()
        conn.close()