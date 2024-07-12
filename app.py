from flask import Flask, render_template, request
import joblib
import numpy as np
import pickle

app = Flask(__name__, template_folder="templates", static_folder="static")

model = joblib.load('model/dt.sav')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the input values from the form
        pm10 = request.form.get("pm10")
        so2 = request.form.get("so2")
        co = request.form.get("co")
        o3 = request.form.get("o3")
        no2 = request.form.get("no2")
        
        if not (pm10 and so2 and co and o3 and no2):
            return render_template("index.html", error="Please fill in all the fields.")
        
        try:
            pm10 = float(pm10)
            so2 = float(so2)
            co = float(co)
            o3 = float(o3)
            no2 = float(no2)
        except ValueError:
            return render_template("index.html", error="Please enter valid numeric values.")
        
        input_arr = np.array([pm10, so2, co, o3, no2]).reshape(1, -1)
        
        prediction = model.predict(input_arr)
        output = prediction[0]
        
        # Baik
        if output == 0:
            return render_template("baik.html")
        # Sangat tidak sehat
        elif output == 1:
            return render_template("sangat tidak sehat.html")
        # Sedang
        elif output == 2:
            return render_template("sedang.html")
        # Tidak sehat
        else:
            return render_template("tidak sehat.html")
    
    return render_template('predict.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=9123)
