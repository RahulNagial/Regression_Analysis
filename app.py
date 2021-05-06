#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 16:46:24 2021

@author: rahulnagial
""" 
# ref: https://github.com/krishnaik06/Heroku-Demo/blob/master/app.py
# first I import the required libraries below
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# creating empty list to populate and serve as input for model prediction 
List = []
# creating Falsk app
app = Flask(__name__)
# loading the best model using pickle
model = pickle.load(open('xg_model.pkl', 'rb'))

# this will render the HTML file index.html
@app.route('/')
def home():
    return render_template('index.html')

# /predict will take input from users
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
# taking inputs as values entered on GUI by user
    features = [x for x in request.form.values()]
# printing for debugging
    # print(features)

# next I converted user provided values in a format which could be used by model for predicting monthly rent
    for j in range(0, len(features)):
        if (features[j] == 'Yes'):
            features[j] = '1'
        if (features[j] == 'No'):
            features[j] = '0'

# taking care of listing type
    if (features[8] == 'Apartment'):
        List.append(8)        

    if (features[8] == 'Shared'):
        List.append(15)

    if (features[8] == 'Basement'):
        List.append(9)        

    if (features[8] == 'Condo'):
        List.append(10)        

    if (features[8] == 'Duplex'):
        List.append(11)        

    if (features[8] == 'House'):
        List.append(12)        

    if (features[8] == 'Loft'):
        List.append(13)        

    if (features[8] == 'Main'):
        List.append(14)        

    if (features[8] == 'Townhouse'):
        List.append(16)        

# taking care of neighbourhood
    if (features[7] == 'Downtown'):
        List.append(59)

    if (features[7] == 'Beltline'):
        List.append(28)

    if (features[7] == 'Lower Mount Royal'):
        List.append(95)        

    if (features[7] == 'Applewood'):
        List.append(21)        

    if (features[7] == 'Bankview'):
        List.append(25)        
    
    if (features[7] == 'Mission'):
        List.append(106)        
    
    if (features[7] == 'Victoria Park'):
        List.append(171)        
    
    if (features[7] == 'Skyview'):
        List.append(151)        
    
    if (features[7] == 'Hillhurst'):
        List.append(85) 
    
    if (features[7] == 'Sunalta'):
        List.append(159) 

    if (features[7] == 'Crescent Heights'):
        List.append(53) 

    if (features[7] == 'Eau Claire'):
        List.append(61) 

    if (features[7] == 'Kingsland'):
        List.append(91) 

    if (features[7] == 'South Calgary'):
        List.append(152) 

    if (features[7] == 'Varsity'):
        List.append(170) 

    if (features[7] == 'Brentwood'):
        List.append(31) 

    if (features[7] == 'Radisson Heights'):
        List.append(126) 

    if (features[7] == 'Bridgeland'):
        List.append(33) 

    if (features[7] == 'Haysboro'):
        List.append(82) 

    if (features[7] == 'Bowness'):
        List.append(29) 

    if (features[7] == 'Capitol Hill'):
        List.append(35) 

    if (features[7] == 'Connaught'):
        List.append(45) 

    if (features[7] == 'Sunnyside'):
        List.append(160) 

    if (features[7] == 'Spruce Cliff'):
        List.append(156) 

    if (features[7] == 'Inglewood'):
        List.append(87) 
    
# removing used information regarding listing type and neighbourhood using .pop
    features.pop()
    features.pop()    
    # print(List)
    for x in range(1,175): 
        features.append('0')
# fixing listing description length as 1500 (avg. of the data)
    features[7] = '1500'
    for j in range(0,2):
        place = List[j]
        features[place] = '1'
   
    features = np.array(features)
    # print(features)
# features are now in a format in which they can be used for model prediction
    prediction = model.predict(features.reshape(1,-1))
    output = int(prediction[0])
# the predicted monthly rental information is returned to the GUI using the below return statement 
    return render_template('index.html', prediction_text='Estimated monthly rent as per your requirements is $ {}'.format(output))

# main function to run the whole Flask app
if __name__ == "__main__":
    app.run(debug=True)
       