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
model = pickle.load(open('random_forest_regression_model.pk1','rb'))

@app.route('/', methods=['GET'])
def home():
   return render_template('index.html')
   
@app.route('/predict', methods=['GET','POST'])
def predict():
    Fuel_type_Diesel=0
    if request.method == "POST": 
       Year = int(request.form["Year"])
       Present_Price = float(request.form["Present_price"])
       kms_Driven = int(request.form["Kms_Driven"])
       Owner = int(request.form["Owner"])
       Fuel_Type_Petrol =request.form["Fuel_Type_Petrol"]
       
       if(Fuel_Type_Petrol=="Petrol"):
            Fuel_Type_Petrol = 1
            Fuel_type_Diesel = 0
       
       elif(Fuel_Type_Petrol=="Diesel"):
            Fuel_Type_Petrol = 0
            Fuel_type_Diesel = 1
       
       else:
            Fuel_Type_Petrol = 0
            Fuel_type_Diesel = 0
            No_Of_Year = 2021-Year
            Seller_Type_Individual =request.form["Seller_Type_Individual"]
       
       if(Seller_Type_Individual=="Individual"):
            Seller_Type_Individual = 1
       else: Seller_Type_Individual = 0
       
       Transmission_Manual = request.form["Transmission_Manual"]
       if(Transmission_Manual == "Transmission_Manual"):
             Transmission_Manual = 1
       else:
          Transmission_Manual = 0
       
       
       
       predictions= model.predict([[Present_Price,kms_Driven,Owner,No_Of_Year,Fuel_type_Diesel,Fuel_type_Diesel,Seller_Type_Individual,Transmission_Manual]])
       output=round(predictions[0],2)
       
       
       if output < 0:
         return render_template("index.html",prediction_texts="Sorry you cannot sell this car")
       else:
         return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    
    else:
         return render_template('index.html')
if __name__ =="__main__":
 app.run(debug=True)
 
