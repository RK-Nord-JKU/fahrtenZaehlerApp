# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:13 2022
@author: Hammerle
"""
import csv
import os
from flask import Flask, render_template, request, flash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.secret_key = os.urandom(12)

@app.route("/", methods=["GET", "POST"])
def rides():
    if request.method == "POST":
        data = {
            "date": request.form.get("date"),
            "shift": request.form.get("shift"),
            "numberOfRides": request.form.get("numberOfRides"),
        }

        add_to_database("rides", data)
        flash("Danke für deine Mithilfe!", "success")
    return render_template("rides.html")


def add_to_database(db_name, data_to_add):
    with open(f"database/{db_name}.csv", "a", newline='') as f:
        dict_writer = csv.DictWriter(f, data_to_add.keys())
        dict_writer.writerow(data_to_add)


if __name__ == "__main__":
    app.run()  # localhost
    #app.run(host="0.0.0.0")  # in network