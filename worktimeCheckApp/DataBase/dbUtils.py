import datetime

import psycopg2



class dbUtils():

    def __init__(self, props):
        dict_db = props.read_properties('DBINFO')
        dict_table = props.read_properties('TABLEINFO')
        self.host = dict_db.get('host')
        self.dbname = dict_db.get('dbname')
        self.user = dict_db.get('user')
        self.tableName = dict_table.get('scheduletablename')
        self.getConn()
        self.createScheduleTable()


    def createScheduleTable(self):
        cur = con.cursor()

        cur.execute(
            "CREATE TABLE IF NOT EXISTS "+self.tableName+" (date DATE PRIMARY KEY, start_w TIME NOT NULL, end_w TIME NOT NULL, work_time DOUBLE PRECISION)")
        con.commit()
        print("create schedule table")

    def getConn(self):
        global con
        con = psycopg2.connect(host=self.host, dbname=self.dbname, user=self.user)

    def insertData(self, today, startWorkTime, endWorkTime):
        todayworktime = (datetime.datetime.now().strptime(endWorkTime.toString('hh:mm:ss'), '%H:%M:%S')-
              datetime.datetime.now().strptime(startWorkTime.toString('hh:mm:ss'),'%H:%M:%S')).total_seconds()
        print(todayworktime)
        cur = con.cursor()
        sql ="INSERT INTO " + self.tableName + "(date,start_w,end_w,work_time) VALUES('"\
             +today+"','"+startWorkTime.toString('hh:mm:ss')+"', '"\
             +endWorkTime.toString('hh:mm:ss')+"', '"\
             +str(todayworktime)+"')"
        try:
            cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()

    def updateData(self, today, endtime):
        cur = con.cursor()
        sql = "UPDATE " + self.tableName + " SET end_w = '"+endtime+ "' WHERE date = '"+today+"'"
        try:
           cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()

    def resetByDate(self, day):
        cur = con.cursor()
        sql = "DELETE FROM " + self.tableName + " WHERE date = '"+day+"'"
        try:
            cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()

    def selectDay(self, day):
        cur = con.cursor()
        sql = "SELECT work_time FROM " + self.tableName + " WHERE date = '" + day + "'"

        print(sql)
        try:
            cur.execute(sql)
        except psycopg2.Error as e:
            print(e)
        con.commit()
        rows = cur.fetchall()
        print("\nRows: \n")
        for row in rows:
            return row[0]

    def calcRemainTime(self,startDay):
        cur = con.cursor()
        sql = "select sum(work_time) FROM " + self.tableName + " WHERE date >= '"+startDay+"'"
        print(sql)
        try:
            cur.execute(sql)

        except psycopg2.Error as e:
            print(e)
        con.commit()

        rows = cur.fetchall()
        print("\nRows: \n")
        for row in rows:
            return row[0]


    def closeConn(self):
        con.close()