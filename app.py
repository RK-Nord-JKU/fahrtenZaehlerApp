# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:13 2022
@author: Hammerle
"""
import csv
import os
from datetime import date, timedelta
from flask import Flask, render_template, request, flash

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
            add_to_database("rides", data)
            flash("Danke für deine Mithilfe!", "success")
    return render_template("rides.html", minDate=minDate, data=data)


def add_to_database(db_name, data_to_add):
    with open(f"database/{db_name}.csv", "a", newline='') as f:
        dict_writer = csv.DictWriter(f, data_to_add.keys())
        dict_writer.writerow(data_to_add)


if __name__ == "__main__":
    app.run()  # localhost
    #app.run(host="0.0.0.0")  # in network