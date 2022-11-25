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
    if (d_mor == 0 and t_mor != '') or (d_noon == 0 and t_noon != '') or (d_night == 0 and t_night != ''):
        return
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
                c.execute("UPDATE {} SET days = '{}', start = '{}', d_mor = '{}', d_noon = '{}', d_night = '{}', t_mor = '{}', t_noon = '{}', t_night = '{}';".format(usid,days,start,d_mor,d_noon,d_night,t_mor,t_noon,t_night))
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
                queue = [{'m':i[0],'t':i[6],'d':i[3]} for i in row if i[3] != 0 and now.replace(hour=int(i[6].split(':')[0]),minute=int(i[6].split(':')[1])) > now] 
            elif now.hour in range(12,18):
                queue = [{'m':i[0],'t':i[7],'d':i[4]} for i in row if i[4] != 0 and now.replace(hour=int(i[7].split(':')[0]),minute=int(i[7].split(':')[1])) > now]
            else:
                queue = [{'m':i[0],'t':i[8],'d':i[5]} for i in row if i[5] != 0 and now.replace(hour=int(i[8].split(':')[0]),minute=int(i[8].split(':')[1])) > now]
            # c.execute("UPDATE {} SET days = start - DATE();".format(usid))
            sql = "DELETE FROM {} where days < 1".format(usid)
            c.execute(sql)
            conn.commit()
            conn.close()
            queue.sort(key=lambda x:x['t'])
    return queue

def checked(queue,med_name):
    queue = [i for i in queue if i['m'] != med_name]
    return queue


