from flask import Flask,render_template
import json
app=Flask(__name__)
@app.route("/",methods=["GET"])
def niche():
    with open("products.json") as f:
        data=json.load(f)
    products=data.values()
    return render_template("products.html",products=products)
@app.route("/sign_up",methods=["GET"])
def sign_up():
    return render_template("Signup.html")
if __name__=="__main__":
    app.run(debug=True)
