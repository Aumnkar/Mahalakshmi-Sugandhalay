from flask import Flask, render_template, request, jsonify
import csv, os
app = Flask(__name__)

# Put your WhatsApp number here (country code + number, no plus sign). Example: 9199XXXXXXXX
WHATSAPP_NUMBER = "9224297407"

# Simple product list (no DB). Edit prices/descriptions as you like.
products = [
    {"id": 1, "name": "A2 Desi Cow Ghee 1kg", "price": "₹1200", "image": "ghee.jpg",
     "description": "Small-batch A2 desi cow ghee from our family farm."},
    {"id": 2, "name": "Organic Jaggery (1kg)", "price": "₹120", "image": "jaggery.jpg",
     "description": "Chemical-free jaggery, traditional processing."},
    {"id": 3, "name": "Safflower Cold Pressed Oil (1L)", "price": "₹460", "image": "oil.jpg",
     "description": "Wood-pressed cold oil, no heat, full nutrients."},
    {"id": 4, "name": "Natural Agarbatti (pack)", "price": "₹140", "image": "agarbatti.jpg",
     "description": "Hand-rolled agarbatti made with natural ingredients."}
]

# Home page
@app.route("/")
def index():
    return render_template("index.html", products=products, whatsapp=WHATSAPP_NUMBER)

# Product detail page
@app.route("/product/<int:product_id>")
def product_page(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return "Product not found", 404
    return render_template("product.html", product=product, whatsapp=WHATSAPP_NUMBER)

# Simple lead endpoint: saves to leads.csv
@app.route("/lead", methods=["POST"])
def save_lead():
    data = request.get_json() or request.form
    name = data.get("name", "")
    phone = data.get("phone", "")
    message = data.get("message", "")
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "leads.csv")
    new_row = [name, phone, message]
    write_header = not os.path.exists(file_path)
    with open(file_path, "a", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["name", "phone", "message"])
        writer.writerow(new_row)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
