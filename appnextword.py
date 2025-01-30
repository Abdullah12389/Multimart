from flask import Flask, render_template, request, jsonify
import algorithms as alg
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("products.html")
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    input_text = data.get("text", "")
    sugg=alg.pred_next(input_text,1)
    return jsonify({"suggestions": [sugg]})
if __name__ == "__main__":
    app.run(debug=True)

