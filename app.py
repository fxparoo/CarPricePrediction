from types import resolve_bases
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
db = SQLAlchemy(app)
model = pickle.load(open('random_forest_regression_model.pk1', 'rb'))


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    fuel_type_diesel = 0
    output = 0

    if request.method == "POST":
        year = int(request.form["Year"])
        present_price = float(request.form["Present_price"])
        kms_driven = int(request.form["Kms_Driven"])
        owner = int(request.form["Owner"])
        fuel_type_petrol = request.form["Fuel_Type_Petrol"]
        no_of_year = 2021 - year
        seller_type_individual = request.form["Seller_Type_Individual"]
        transmission_manual = request.form["Transmission_Manual"]

        if fuel_type_petrol == "Petrol" and fuel_type_diesel == "Diesel":
            fuel_type_petrol = 1

        if seller_type_individual == "Individual":
            seller_type_individual = 1
        else:
            seller_type_individual = 0

        if transmission_manual == "Transmission_Manual":
            transmission_manual = 1
        else:
            transmission_manual = 0

        predictions = model.predict([[present_price, kms_driven, owner, no_of_year, fuel_type_diesel, fuel_type_diesel,
                                      seller_type_individual, transmission_manual]])
        output = round(predictions[0], 2)
    if output < 0:
        return render_template("index.html", prediction_texts="Sorry you cannot sell this car")

    else:
        return render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))

    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
