import sqlite3
def ver(usr,usid,password):
    if usr == 'User' and usid != "":
        conn = sqlite3.connect('User_database.db')
        c=conn.cursor()
        sql_query = """SELECT * FROM User where usid=?"""
        c.execute(sql_query,(usid,))
        row=c.fetchall()
        conn.commit()
        conn.close()
        if row != [] and password == row[0][1]:
            return "Verified"
        else:
            return "Not verified"



