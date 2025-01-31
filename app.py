from flask import Flask,render_template,request,Response,jsonify,session,redirect,url_for
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from keras.preprocessing.sequence import pad_sequences
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
import pickle
import os
import json
import re
import algorithms as alg
from io import BytesIO
app=Flask(__name__)
folder='static/images'
pat='images'
app.config["UPLOAD_FOLDER"]=folder
app.secret_key="mykey"
pair={}
@app.route("/")
def page():
    return render_template("welcome.html")
@app.route("/niche")
def niche():
    return render_template("Niche.html") 
@app.route("/product_panel/<product_id>",methods=["GET"])
def product_panel(product_id):
    with open("products.json") as f:
        data=json.load(f)
    f.close()
    vectors=[]
    for ids in data:    
        vectors.append(data[ids]["vector"]) 
    vect_arr=np.array(vectors) 
    to_compare=np.array(data[product_id]["vector"]).reshape(1,-1)
    sim=[]
    indexes=[]
    rec={}
    for vec in vect_arr:
        sim.append(cosine_similarity(to_compare,vec.reshape(1,-1)))
    sorted_sim=sorted(sim)[1:4]
    for similar in sorted_sim:
        indexes.append(sim.index(similar))
    for i in indexes:
        rec[list(data)[i]]=data[list(data)[i]]
    return render_template("product_panel.html",product=data[product_id],rec_pro=rec)
@app.route("/products",methods=["GET"])
def products():
    if 'user' not in session:
       return redirect(url_for('login'))
    with open("products.json") as f:
        data=json.load(f)
    f.close()
    return render_template("products.html",products=data)
@app.route("/login",methods=['GET',"POST"])
def login():
    if 'user' in session:
        with open("products.json") as file:
            data=json.load(file)
        file.close()    
        return redirect(url_for('products',products=data))
    if request.method=="POST":
        with open("seller.json") as f:
            data=json.load(f)
        name=request.form['name']
        password=request.form['password']
        if name not in list(data):
            return render_template("Signup.html")
        elif password=="":
            return render_template("login.html")
        elif int(password) == data[name]['password']:
            session['user']=name
            with open("products.json") as f:
                pro=json.load(f)
            f.close()    
            return render_template("products.html",products=pro)
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")
@app.route("/sign_up",methods=["GET","POST"])
def sign_up():
    if "user" in session:
        with open("products.json") as f:
            data=json.load(f)
        f.close()  
        return redirect(url_for("products.html",products=data))
    if request.method=="GET":
        return render_template("Signup.html")
    else:
        with open("seller.json") as f:
            data=json.load(f)
        f.close()    
        name=request.form['name']
        if name in list(data):
            return render_template("login.html")
        else:
            session['user']=name
            password=request.form['confirm']
            data[name]={"password":int(password),"products":[],"reviews":[]}
            with open("seller.json","w") as f:
                json.dump(data,f)
            f.close()    
            return render_template("Niche.html")
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
    reviews=seller[session['user']]['reviews']   
    products=seller[session['user']]['products']
    with open("products.json") as file:
        prod=json.load(file)
    file.close()
    return render_template("seller_dashboard.html",product=prod,ids=products,reviews=reviews)

@app.route("/tell",methods=['POST',"GET"])
def tell():
    if request.method=="GET":
        return render_template("add_product.html")
    else:
        img_file=request.files["image"] 
        img_file.save(os.path.join(app.config['UPLOAD_FOLDER'],img_file.filename))
        path=os.path.join(pat,img_file.filename)
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
        file.close()    
        last=list(data.keys())[-1]
        digit=int("".join(re.findall(r"\d",last)))
        name=request.form["name"]
        cat=request.form["category"]
        desc=request.form["description"]
        brand=request.form["brand"]
        price=request.form['price']
        vector=name+" "+brand+" "+desc
        with open("tokenize_description.pkl","rb") as file:
            tokenizer=pickle.load(file)
        file.close()    
        with open("seller.json") as file:
            seller=json.load(file)
        file.close()
        new_product_id = f"id{digit+1}"
        if new_product_id not in seller[session['user']]["products"]:
            seller[session['user']]["products"].append(new_product_id)     
        with open("seller.json","w") as file:
            json.dump(seller,file)
        file.close()    
        seq=[tokenizer.word_index[word] for word in vector.split() if word in tokenizer.word_index]
        seq.extend([0,0,0])
        pad_seq=pad_sequences([seq],maxlen=22)
        vector=pad_seq[0].tolist()
        if ans>0.5:
            data[f"id{digit+1}"]={"name":f"{name}","description":desc,"reviews":[],"clicks":0,"category":f"{cat}","price":price,"brand":f"{brand}","img":path,"vector":vector}
        else: 
            data[f"id{digit+1}"]={"name":f"{name}","description":desc,"reviews":[],"clicks":0,"category":f"{cat}","price":price,"brand":f"{brand}","img":'',"vector":vector} 
        with open("products.json","w") as file:
            json.dump(data,file)
        file.close()          
        return render_template("seller_dashboard.html",ids=seller[session['user']]["products"],product=data,reviews=seller[session['user']]["reviews"])
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
@app.route("/predict", methods=["POST","GET"])
def predict():
    if request.method=="POST":
        data = request.json
        input_text = data.get("text", "")
        sugg=alg.pred_next(input_text,1)
        return jsonify({"suggestions": [sugg]})      
    else:
        return render_template("products.html")              
if __name__=="__main__":
    app.run(debug=True)


   

