import sqlite3
import pandas as pd
from dataclasses import dataclass
from datetime import date

@dataclass
class RD_Shift:
    date: date = date.today() # YYYY-MM-DD
    type: str = None # TD or ND / dayshift or nightshift
    events: int = None # number of rides
    resthours: float = None # break

    def is_valid(self) -> str:
        if self.date is None or self.type is None or self.events is None or self.resthours is None:
            return "Bitte alle Felder ausfüllen"
        elif self.date == date.today() and self.type == "ND":
            return "Nachtdienste beginnen immer am Vortag! "
        else:
            return None  

    def as_dict(self):
        return {"date": self.date, "type": self.type, "events": self.events, "resthours": self.resthours}

class DB_Handler():

    def __init__(self, filename: str) -> None:
        self.conn = sqlite3.connect(filename, check_same_thread=False)
        self.cur = self.conn.cursor()

    def createTable(self) -> None:
        '''creates the table is not exits'''
        sql = """CREATE TABLE IF NOT EXISTS shifts (
            date DATE NOT NULL UNIQUE,
            events_day INTEGER,
            resthours_day REAL,
            events_night INTEGER,
            resthours_night REAL
            )"""
        self.cur.execute(sql)

    def addShift(self, shift: RD_Shift):
        '''Adds a new shift to the database or updates an old one'''
        try: # insert new one
            if shift.type == "TD":
                sql = """INSERT INTO shifts (date, events_day, resthours_day) VAlUES (?,?,?)"""
                self.cur.execute(sql, (shift.date, shift.events, shift.resthours))
            elif shift.type == "ND":
                sql = """INSERT INTO shifts (date, events_night, resthours_night) VAlUES (?,?,?)"""
                self.cur.execute(sql, (shift.date, shift.events, shift.resthours))
            else:
                raise ValueError  
        except: #update
        
            if shift.type == "TD":
                sql = """UPDATE shifts SET events_day = ?, resthours_day = ? WHERE date = ?"""
                self.cur.execute(sql, (shift.events, shift.resthours, shift.date))
            elif shift.type == "ND":
                sql = """UPDATE shifts SET events_night = ?, resthours_night = ? WHERE date = ?"""
                self.cur.execute(sql, (shift.events, shift.resthours, shift.date))
            else:
                raise ValueError
        self.conn.commit()

    def selectRange(self, start: date, stop: date) -> list:
        sql = """SELECT * FROM shifts WHERE date BETWEEN ? AND ?"""
        self.cur.execute(sql, (start, stop))
        return self.cur.fetchall()
    
    def selectDF(self, start:date=None, stop:date=None):
        '''returns the data as dataframe'''

        # get data
        if start and stop:
            sql = """SELECT * FROM shifts WHERE date BETWEEN ? AND ?"""
            self.cur.execute(sql, (start, stop))
        else:
            sql = """SELECT * FROM shifts"""
            self.cur.execute(sql)   
        data = self.cur.fetchall()
        # header
        names = list(map(lambda x: x[0], self.cur.description))

        df = pd.DataFrame(data,columns=names)

        return df
    
        # df['date']= pd.to_datetime(df['date'])
        # print(df)
        # df['date'] = df["date"].dt.strftime('%d.%m.%Y')
        # print(df)
    
        # df.insert(loc=0, column='weekday', value=df["date"].dt.strftime('%a'))

    def __del__(self):
        self.conn.close

if __name__ == '__main__':
    DB_NAME = "database/rides_statistic.sqlite"
    db_handler = DB_Handler(filename=DB_NAME)
    db_handler.selectDF()

