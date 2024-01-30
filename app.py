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

from database.db_handler import DB_Handler, RD_Shift


# FOLDER = "src/"  # docker
FOLDER = ""  # local
DB_NAME = "database/rides_statistic.sqlite"
db_handler = DB_Handler(filename=DB_NAME)

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.urandom(12)

@app.route("/", methods=["GET", "POST"])
def rides():

    shift = RD_Shift()

    if request.method == "POST":

        shift.date = request.form.get("date")
        shift.type = request.form.get("type")
        shift.events = request.form.get("events")
        shift.resthours = request.form.get("restingHours")

        error_msg = shift.is_valid()
        if error_msg:
            flash(error_msg, "danger")    
        else:
            db_handler.addShift(shift=shift)
            flash("Danke für deine Mithilfe!", "success")
    return render_template("rides.html", minDate=date.today() - timedelta(days=7), data=shift.as_dict())

@app.route("/ansicht", methods=["GET"])
def plot():
    df = db_handler.selectDF()

    # print(date.today())
    # print(date.today()-timedelta(days=21))
    print(df)
    
    # add weekday
    return render_template("plotDF.html", df=df)

if __name__ == "__main__":
    if FOLDER == "":
        app.run()  # localhost
    else:
        app.run(host="0.0.0.0")  # in network