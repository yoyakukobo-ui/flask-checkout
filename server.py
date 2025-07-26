from flask import Flask, request, jsonify
import stripe
import os
from flask_cors import CORS  # ←追加

stripe.api_key = os.getenv("STRIPE_KEY")

app = Flask(__name__)
CORS(app)

@app.route("/create-checkout", methods=["POST"])
def create_checkout():
    data = request.get_json()

    email = data.get("login_id")
    item_id = data.get("_id")
    class_name = data.get("class", "").lower()

    price_map = {
        "p2p3kaikin": 4500,
        "p2p3cancel": 7000,
        "p2p3sale": 2000
    }
    unit_price = price_map.get(class_name, 4500)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=[{
            "price_data": {
                "currency": "jpy",
                "product_data": {
                    "name": f"羽田空港駐車場予約代行（{class_name}）"
                },
                "unit_amount": unit_price,
            },
            "quantity": 1
        }],
        customer_email=email,
        metadata={
            "itemId": item_id,
            "class": class_name
        },
        success_url="https://www.yoyakukobo.com/thankskaikin?rc=test-site",
        cancel_url="https://www.yoyakukobo.com/blank?rc=test-site"
    )

    return jsonify({ "checkout_url": session.url })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
