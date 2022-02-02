from os import O_TRUNC
from flask import Flask,render_template,request
import requests
import pickle
import numpy as np


app = Flask(__name__)

with open("src/Thyroid_model.pkl","rb") as model_file:
    model=pickle.load(model_file)

@app.route('/')
def index():
   return render_template('home.html')

@app.route("/moreinfo", methods = ["GET", "POST"])
def moreinfo():
    return render_template('moreinfo.html')

@app.route("/predict", methods = ["GET", "POST"])
def predict():
    return render_template('predict.html')

@app.route("/predictresult", methods = ["GET", "POST"])
def predictresult():
    if request.method == "POST":
        Age=float(request.form.get('age'))
        Sex= request.form.get('sex')
        Level_thyroid_stimulating_hormone= float(request.form.get('TSH'))
        Total_thyroxine_TT4= float(request.form.get('TT4'))
        Free_thyroxine_index=float(request.form.get('FTI'))
        On_thyroxine= request.form.get('on_thyroxine')
        On_antithyroid_medication= request.form.get('on_antithyroid_medication')
        Goitre= request.form.get('goitre')
        Hypopituitary = request.form.get('hypopituitary')
        Psychological_symptoms = request.form.get('psych')
        T3_measured= request.form.get('T3_measured')


        #Sex
        if Sex=="Male":
            Sex=1
        else:
            Sex=0
        #On_thyroxine
        if On_thyroxine=="True":
            On_thyroxine=1
        else:
            On_thyroxine=0

        #On_antithyroid_medication
        if On_antithyroid_medication=="True":
            On_antithyroid_medication=1
        else:
            On_antithyroid_medication=0
        
        #Goitre
        if Goitre=="True":
            Goitre=1
        else:
            Goitre=0

        #Hypopituitary
        if Hypopituitary=="True":
            Hypopituitary=1
        else:
            Hypopituitary=0

        #Psychological_symptoms
        if Psychological_symptoms=="True":
            Psychological_symptoms=1
        else:
            Psychological_symptoms=0

        #T3_measured
        if T3_measured=="True":
            T3_measured=1
        else:
            T3_measured=0



        arr=np.array([[Age,Sex,Level_thyroid_stimulating_hormone,Total_thyroxine_TT4,Free_thyroxine_index,
        On_thyroxine,On_antithyroid_medication,Goitre,Hypopituitary,Psychological_symptoms,T3_measured]])
        pred=model.predict(arr)


        if pred==0:
            res_Val="Compensated Hypothyroid"
        elif pred==1:
            res_Val="No Thyroid"
        elif pred==2:
            res_Val='Primary Hypothyroid'
        elif pred==3:
            res_Val='Secondary Hypothyroid'

        
        Output=f"Patient has {res_Val}"
        return render_template('predictresult.html',output=Output)


    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=False)
