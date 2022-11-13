import sqlite3

def retrieve(usid):
    if usid != "":
        conn = sqlite3.connect('UserHealth.db')
        c=conn.cursor()
        sql_query = """SELECT * FROM user_health where usid=?"""
        c.execute(sql_query,(usid,))
        row=c.fetchall()
        conn.commit()
        conn.close()
        if row == [] :
            return ["","","","","","","",""]
        else :
            return list(row[0])

def add_health(usid,age,gen,h,w,bg,all,hc):
    if usid != "":
        conn = sqlite3.connect('UserHealth.db')
        c=conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS user_health(
                        usid text primary key,
                        age int,
                        gender varchar(1),
                        height int,
                        weight int,
                        blood_group varchar(2),
                        allergies varchar(150),
                        health_cond varchar(150))""")
        sql_query = """SELECT * FROM user_health where usid=?"""
        c.execute(sql_query,(usid,))
        row=c.fetchall()
        if row != [] :
            c.execute("UPDATE user_health SET age = '{}', gender = '{}', height = '{}', weight ='{}', blood_group = '{}', allergies = '{}', health_cond ='{}' WHERE usid ='{}';".format(age,gen,h,w,bg,all,hc,usid))
        else:
            c.execute("INSERT INTO user_health VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(usid,age,gen,h,w,bg,all,hc))
        conn.commit()
        conn.close()



