from flask import Flask,render_template,request,Response
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import pickle
import json
import re
import algorithms as alg
from io import BytesIO
app=Flask(__name__)
pair={}
@app.route("/")
def page():
    return render_template("add_product.html")
@app.route("/niche")
def niche():
    return render_template("Niche.html") 
@app.route("/products",methods=["GET"])
def products():
    with open("products.json") as f:
        data=json.load(f)
    products=data.values()
    return render_template("products.html",products=products)
@app.route("/sign_up",methods=["GET"])
def sign_up():
    return render_template("Signup.html")
@app.route("/graph")
def graph():
    with open("seller.json") as file:
        data=json.load(file)
    file.close() 
    a=[]
    reviews=data['username1']['reviews']
    for review in reviews:
        sentiment=alg.give_sentiment(review)
        a.append(sentiment)
    df=pd.Series(a)
    df=df.replace({1:"positive",0:"negative"})
    data=df.value_counts()
    fig,ax=plt.subplots()
    data.plot(kind="bar" ,ax=ax)
    plt.xlabel("review sentiment")
    plt.ylabel("no of reviews")
    plt.xticks(rotation=0)
    img=BytesIO()
    fig.savefig(img,format="png")
    img.seek(0)
    return Response(img, mimetype='image/png')
@app.route("/seller",methods=["GET","POST"])
def seller():
    with open("seller.json") as file:
        seller=json.load(file)
    file.close()    
    products=seller['username1']['products']
    with open("products.json") as file:
        prod=json.load(file)
    file.close()
    return render_template("seller_dashboard.html",product=prod,ids=products)

@app.route("/tell",methods=['POST',"GET"])
def tell():
    if request.method=="GET":
        return render_template("products.html")
    else:
        img_file=request.files["image"] 
        with open("vernelable_detect.pkl","rb") as file:             
            model=pickle.load(file)
        file.close()
        img=Image.open(img_file.stream)
        img=img.resize((256,256))
        img=np.array(img)
        img=img/255.0
        img=np.expand_dims(img,axis=0)
        ans=model.predict(img)
        with open("products.json") as file:
            data=json.load(file)
        last=list(data.keys())[-1]
        digit=int("".join(re.findall(r"\d",last)))
        name=request.form["name"]
        cat=request.form["category"]
        desc=request.form["description"]
        brand=request.form["brand"]
        price=request.form['price']
        if ans>0.5:
            data[f"id{digit+1}"]={"name":f"{name}","reviews":[],"clicks":0,"category":f"{cat}","price":price,"brand":f"{brand}"}
        else: 
            data[f"id{digit+1}"]={"name":f"{name}","description":desc,"reviews":[],"clicks":0,"category":f"{cat}","price":price,"brand":f"{brand}"} 
        with open("products.json","w") as file:
            json.dump(data,file)
        file.close()          
        return render_template("seller_dashboard.html")
@app.route("/chatbot",methods=["GET","POST"])   
def chatbot():
    if request.method=="GET":    
        return render_template("chatwindow.html",chat=pair)
    else:
        question=request.form['question']
        question=question.lower()
        ans=alg.ChatWithMe(question)
        pair[question]=ans
        return render_template("chatwindow.html",chat=pair)                  
if __name__=="__main__":
    app.run(debug=True)


   

