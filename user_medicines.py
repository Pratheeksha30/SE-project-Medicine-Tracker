import sqlite3
from datetime import datetime

def list_meds(usid):
    if usid != "":
        conn = sqlite3.connect('UserMedicines.db')
        c=conn.cursor()
        c.execute("SELECT * FROM {}".format(usid))
        r = [dict((c.description[i][0], value) \
               for i, value in enumerate(row)) for row in c.fetchall()]
        conn.commit()
        conn.close()
        return r

def add_meds(usid,medicine,days,d_mor,d_noon,d_night,t_mor,t_noon,t_night):
    if usid != "" :
        conn = sqlite3.connect('UserMedicines.db')
        c=conn.cursor()
        c.execute(""" CREATE TABLE IF NOT EXISTS {}(
                        med text primary key,
                        days number,
                        start date,
                        d_mor int,
                        d_noon int,
                        d_night int,
                        t_mor time,
                        t_noon time,
                        t_night time)""".format(usid))
        if medicine != "":
            n = datetime.now()
            start = str(n.year)+'-'+str(n.month)+'-'+str(n.day)
            c.execute("SELECT * FROM {} where med = '{}'".format(usid,medicine))
            row=c.fetchall()
            if row != [] :
                c.execute("UPDATE {} SET med = '{}',days = '{}', start = '{}', d_mor = '{}', d_noon = '{}', d_night = '{}', t_mor = '{}', t_noon = '{}', t_night = '{}';".format(usid,medicine,days,start,d_mor,d_noon,d_night,t_mor,t_noon,t_night))
            else:
                c.execute("INSERT INTO {} VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(usid,medicine,days,start,d_mor,d_noon,d_night,t_mor,t_noon,t_night))
        conn.commit()
        conn.close()

def remove_med(usid,med):
    if med != '':
        conn = sqlite3.connect('UserMedicines.db')
        c=conn.cursor()
        c.execute("DELETE FROM {} where med = '{}'".format(usid,med))
        conn.commit()
        conn.close()

def remind(usid):
    queue = []
    if usid != "" :
        now = datetime.now()
        conn = sqlite3.connect('UserMedicines.db')
        c=conn.cursor()
        c.execute("SELECT * FROM {}".format(usid))
        row=c.fetchall()
        if row != []:
            if now.hour in range(0,12):
                queue = [{'m':i[0],'t':i[6],'d':i[3]} for i in row if i[3] != 0]    
            elif now.hour in range(12,18):
                queue = [{'m':i[0],'t':i[7],'d':i[4]} for i in row if i[4] != 0]
            else:
                queue = [{'m':i[0],'t':i[8],'d':i[5]} for i in row if i[5] != 0]
            # c.execute("UPDATE {} SET days = start - DATE();".format(usid))
            c.execute("DELETE FROM {} where days < 1".format(usid))
            conn.commit()
            conn.close()
            queue.sort(key=lambda x:x['t'])
    return queue


