import os
from flask import Flask, render_template, request
import requests
from urllib.parse import quote
import pickle
import numpy as np
import pandas as pd

api_key = 'pk.1a34e455dc7a1c2ce1b1b7c1da0877e7'

city = ['birmingham',
 'bristol',
 'buckinghamshire',
 'edinburgh',
 'glasgow',
 'gloucestershire',
 'hampshire',
 'liverpool',
 'london',
 'nottingham',
 'oxford',
 'sheffield',
 'aberdeenshire',
 'manchester']

lat_lon_tol = 0.6

model_folder = 'G:\DA-IICT\SEM1\PC503\Project\Model'

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def predict():
    result = {}
    if request.method == 'POST':
        bed = int(request.form['bed'])
        bath = int(request.form['bathroom'])
        reception = int(request.form['reception'])

        if 'ch' in request.form:
            ch = 1
        else:
            ch = 0

        if 'dg' in request.form:
            dg = 1
        else:
            dg = 0
        
        address = request.form['address']

        c = None

        for i in city:
            if i in address.lower():
                c = i

        x = f'https://eu1.locationiq.com/v1/search?key={api_key}&q={quote(address)}&format=json'
        y = requests.get(x)

        lat = float(y.json()[0]['lat'])
        lon = float(y.json()[0]['lon'])

        x = f'https://eu1.locationiq.com/v1/search?key={api_key}&q={quote(c)}&format=json'
        y = requests.get(x)

        latc = float(y.json()[0]['lat'])
        lonc = float(y.json()[0]['lon'])
        
        t1 = not (abs(lat) > (abs(latc) - lat_lon_tol) and abs(lat) < (abs(latc) + lat_lon_tol))
        t2 = not (abs(lon) > (abs(lonc) - lat_lon_tol) and abs(lon) < (abs(lonc) + lat_lon_tol))

        if t1 or t2:
            lat, lon = latc, lonc

        d = {'bed':bed, 'bath':bath, 'reception':reception, 'lat':lat, 'lon': lon, 'ch':ch, 'dg':dg}
        #   {'bed':3,   'bath':1,    'reception':1,         'lat':52.478308, 'lon': -1.893538, 'ch':1, 'dg':1}
        for file in os.listdir(model_folder):
            if c in file:
                with open(os.path.join(model_folder, file), 'rb') as model_file:
                    model = pickle.load(model_file)
                
                break
        print(pd.Series(d))
        print(f'Predicted Price is -> {model.predict([pd.Series(d)])}')


        result = {'text': 'hello'}
        return render_template('predict.html')    
    return render_template('predict.html')

if __name__ == "__main__":
    app.run(debug = True, port=8001)