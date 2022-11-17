import sqlite3
def ad(usid_,password,email,usr):
    if usr == 'User':
        conn = sqlite3.connect('User_database.db')
        c=conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS User(
                        usid text primary key,
                        user_password text,
                        email_id text)""")
        sql_query = """SELECT * FROM User where usid=?"""
        c.execute(sql_query,(usid_,))
        row=c.fetchall()
        if row != [] :
            return 0
        c.execute("INSERT INTO User VALUES ('{}','{}','{}')".format(usid_,password,email))
        conn.commit()
        conn.close()
        return 1

