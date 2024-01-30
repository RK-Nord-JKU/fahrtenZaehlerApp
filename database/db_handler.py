import sqlite3
import pandas as pd
from dataclasses import dataclass
from datetime import date

@dataclass
class RD_Shift:
    date: date # YYYY-MM-DD
    type: str # TD or ND / dayshift or nightshift
    events: int # number of rides
    resthours: float # break

class DB_Handler():

    def __init__(self) -> None:
        self.conn = sqlite3.connect("database/rides_statistic.sqlite")
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

        return pd.DataFrame(data,columns=names)

    def __del__(self):
        self.conn.close

        

