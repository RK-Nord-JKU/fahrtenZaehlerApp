# -*- coding: utf-8 -*-
"""
@author: Weiss
"""
import csv
import os
from datetime import date, timedelta
from flask import Flask, render_template, request, flash
import pandas as pd
import locale
import numpy as np

# FOLDER = "src/"  # docker
FOLDER = ""  # local
DB_NAME = "rides"

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.urandom(12)

@app.route("/", methods=["GET", "POST"])
def rides():
    # current dates
    today = str(date.today())
    minDate = date.today() - timedelta(days=7)

    data = {
            "date": today,
            "shift": None,
            "numberOfRides": None,
            "restingHours": None,
    }
    if request.method == "POST":
        data = {
            "date": request.form.get("date"),
            "shift": request.form.get("shift"),
            "numberOfRides": request.form.get("numberOfRides"),
            "restingHours": request.form.get("restingHours"),
        }       
        if not all(bool(val) or val==0 for val in data.values()):  # dataset not complete
            flash("Bitte alle Felder ausfüllen", "danger")
        elif data["date"] == today and data["shift"] == "ND":
            flash("Nachtdienste beginnen immer am Vortag! ", "danger")    
        else:
            add_to_database(db_name=DB_NAME, data_to_add=data)
            flash("Danke für deine Mithilfe!", "success")
    return render_template("rides.html", minDate=minDate, data=data)

@app.route("/ansicht", methods=["GET"])
def plot():
    return render_template("plotDF.html", df=database_to_dataframe(db_name=DB_NAME))


def add_to_database(db_name: str, data_to_add) -> None:
    '''adds data to the csv file'''
    with open(f"database/{db_name}.csv", "a", newline='') as f:
        dict_writer = csv.DictWriter(f, data_to_add.keys())
        dict_writer.writerow(data_to_add)

def database_to_dataframe(db_name: str) -> pd.DataFrame:
    '''reades the data from the csv file, process as the
    data as dataframe'''

    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

    # import data
    columnHeaders = ['shiftDate', 'shiftType','numRides','numRestHours']
    df = pd.read_csv(f"database/{db_name}.csv", header=None, names=columnHeaders)
    df['shiftDate'] = pd.to_datetime(df['shiftDate']) # convert object to datetime

    # remove duplicates of data
    df = df.drop_duplicates(
        subset = ['shiftDate', 'shiftType'],
        keep = 'last').reset_index(drop = True)

    df = df.sort_values(['shiftDate', 'shiftType'], ascending=[False, False]).reset_index(drop=True)

    # Merge columns with same date
    s = df.groupby(['shiftDate']).cumcount()
    df = df.set_index(['shiftDate', s]).unstack().sort_index(level=1, axis=1)
    df.columns = [f'{x}{y}' for x, y in df.columns]
    df = df.reset_index()

    # Change rows if shiftType == 'ND'
    s = df['shiftType0'] == 'ND' # boolean condition
    df.loc[s, ['numRestHours0','numRestHours1']] = df.loc[s, ['numRestHours1','numRestHours0']].values
    df.loc[s, ['numRides0','numRides1']] = df.loc[s, ['numRides1','numRides0']].values
    df.loc[s, ['shiftType0','shiftType1']] = df.loc[s, ['shiftType1','shiftType0']].values

    # latest date on top
    df = df.sort_values('shiftDate', ascending=False).reset_index(drop=True)

    # drop columns
    df = df.drop(['shiftType0', 'shiftType1'], axis=1)

    # format date
    df.insert(loc=0, column='Weekday', value=df["shiftDate"].dt.strftime('%a'))
    df['shiftDate'] = df["shiftDate"].dt.strftime('%d.%m.%Y')
    df = df[['Weekday','shiftDate', 'numRides0', 'numRestHours0', 'numRides1', 'numRestHours1']]
    

    #
    df[['numRides0', 'numRides1']] = df[['numRides0', 'numRides1']].astype("Int64")
    df = df.replace(np.nan, pd.NA)

    # remove .0
    df[['numRestHours0','numRestHours1']] = df[['numRestHours0','numRestHours1']].fillna(-1)
    df[['numRestHours0', 'numRestHours1']] = df[['numRestHours0', 'numRestHours1']].astype(str)
    df['numRestHours0'] = df['numRestHours0'].apply(lambda x: x.replace(".0",""))
    df['numRestHours1'] = df['numRestHours1'].apply(lambda x: x.replace(".0",""))
    df[['numRestHours0','numRestHours1']] = df[['numRestHours0','numRestHours1']].replace("-1", pd.NA)

    return df

if __name__ == "__main__":
    if FOLDER == "":
        app.run()  # localhost
    else:
        app.run(host="0.0.0.0")  # in network