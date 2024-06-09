# ------------------------------------------ Imports -------------------------------------------
import os
import time
from flask import *
import re
import json
import hmac
import hashlib
import logging
import traceback

# --------------------------------------- Flask Init ---------------------------------------------

app = Flask(__name__)

# ------------------------------------- Variables --------------------------------------------------

SECRET_KEY = b'' # Put your sellix webhook secret
WHITELISTED_IP = '99.81.24.41' # Ip adress of sellix
DEPLOY = False # Keep that to false if you do not want to deploy it (will only work on local host)

# ------------------------------------- Endpoints --------------------------------------------------

@app.route("/")
def home():
    json_data = {
    "message": "Welcome to Cyberious API",
    "version": "1.0",
    "docs": "None Yet",
    "author": "https://cyberious.xyz",
    "status": "Down & under construction",
}
    return json_data

@app.route("/hwid")
def get_hwid_status():
    hwid = request.args.get('hwid')
    if not hwid:
        return jsonify({"error": "No hardware ID provided"}), 400

    with open(os.path.join("data", "whwid.json"), "r") as whwid_file:
        whwid_data = eval(whwid_file.read().replace('null', 'None'))

    with open(os.path.join("data", "bhwid.json"), "r") as bhwid_file:
        bhwid_data = eval(bhwid_file.read().replace('null', 'None'))

    if hwid in bhwid_data:
        expiry = bhwid_data[hwid]
        if expiry is None:
            expiry = "permanent"
        else:
            expiry = time.ctime(expiry)
        return jsonify({"blacklisted": True, "expiry": expiry})

    if hwid in whwid_data:
        expiry = time.ctime(whwid_data[hwid])
        return jsonify({"whitelisted": True, "expiry": expiry})

    return jsonify({"error": "Hardware ID not found"}), 404

# OPTIONAL SELLIX ORDER INTEGRATION

@app.route("/sellix", methods=["POST"])
def sellix_webhook():
    if request.remote_addr != WHITELISTED_IP:
        return jsonify({"error": "Request not from whitelisted IP"}), 401
    payload = request.get_data()
    header_signature = request.headers.get('X-Sellix-Signature')
    if not header_signature:
        return jsonify({"error": "Missing X-Sellix-Signature header"}), 400

    calculated_signature = hmac.new(SECRET_KEY, payload, hashlib.sha512).hexdigest()

    if hmac.compare_digest(calculated_signature, header_signature):
        data = request.get_json()
        product_title = data.get("data", {}).get("product_title")
        order_uniqid = data.get("data", {}).get("uniqid")

        if not product_title or not order_uniqid:
            return jsonify({"error": "Missing product title or order uniqid"}), 400

        product_title = product_title.lower()

        if (
            "discord account creator" in product_title # Add your title here
            or "discord token gen" in product_title # Add your alternative title here
            or "token gen" in product_title # Add your alternative title here
        ):
            durations = {
                "1 week": 7, # Add more as you wish. The time should be in days
                "1 month": 30,
                "lifetime": 999999,
            }
            duration_str = re.search(r"\[(\d+ \w+)\]", product_title).group(1) if re.search(r"\[(\d+ \w+)\]", product_title) else None
            if duration_str:
                duration = durations.get(duration_str)
                if duration:
                    order_data = {order_uniqid: duration}

                    with open(os.path.join("data", "u_orders.json"), "r") as orders_file:
                        orders_data = json.load(orders_file)

                    orders_data.update(order_data)

                    with open(os.path.join("data", "u_orders.json"), "w") as orders_file:
                        json.dump(orders_data, orders_file)
                    return jsonify({"success": f"Order {order_uniqid} saved with duration {duration}"})
        return jsonify({"error": "Unsupported product or invalid duration"}), 400
    else:
        print("Someone Tried To send a request without a valid X-Sellix-Signature.")
        return jsonify({"error": "Invalid X-Sellix-Signature"}), 401

@app.route("/verify_user", methods=['GET'])
def verify_user():

    with open(os.path.join("data", "users.json"), 'r') as f:
        users = json.load(f)

    hwid = request.headers.get('hwid')

    if hwid in users:
        return users[hwid]
    else:
        return 'User not found', 404

@app.route("/check_if_paused", methods=['GET'])
def check_if_paused():
    hwid = request.headers.get('hwid')

    with open(os.path.join("data", "status.json"), "r") as status_file:
        status_data = json.load(status_file)

    if hwid in status_data:
        is_paused = status_data[hwid]
        return is_paused
    else:
        return jsonify({"error": "Hardware ID not found"}), 404 

from flask import jsonify

@app.route("/check_user_expiry", methods=['GET'])
def check_user_expiry():
    hwid = request.headers.get('hwid')

    with open(os.path.join("data", "expire.json"), "r") as expire_file:
        expire_data = json.load(expire_file)

    if hwid in expire_data:
        expiry_timestamp = expire_data[hwid]
        # convert the expiry timestamp to a string and return it as a JSON object
        return jsonify({"timestamp": str(expiry_timestamp)})
    else:
        return jsonify({"error": "Hardware ID not found"}), 404

    
@app.route("/register", methods=['POST'])
def register():
    logging.basicConfig(level=logging.DEBUG)

    hwid = request.headers.get('hwid')
    user = request.headers.get('user')
    order = request.headers.get('order')

    logging.debug(f"Received request with hwid: {hwid}, user: {user}, order: {order}")

    if not hwid or not user or not order:
        logging.error("Missing required headers")
        return jsonify({"error": "Missing required headers"}), 400

    try:
        with open(os.path.join("data", "u_orders.json"), "r") as u_orders_file:
            u_orders_data = json.load(u_orders_file)
    except Exception as e:
        logging.error(f"Error loading u_orders.json: {e}")
        return jsonify({"error": "Error loading u_orders.json"}), 500

    if order not in u_orders_data:
        logging.error("Order not found in the database")
        return jsonify({"error": "You are not in the databse, stop trying to cheat"}), 400
    duration = u_orders_data[order]

    try:
        with open(os.path.join("data", "c_orders.json"), "r") as c_orders_file:
            c_orders_data = json.load(c_orders_file)
    except Exception as e:
        logging.error(f"Error loading c_orders.json: {e}")
        return jsonify({"error": "Error loading c_orders.json"}), 500

    expiry_timestamp = int(time.time()) + duration * 24 * 60 * 60

    order_data = {
        "order_id": order,
        "expiry": expiry_timestamp,
        "timestamp": int(time.time()),
        "hwid": hwid
    }
    c_orders_data[order] = order_data

    try:
        with open(os.path.join("data", "c_orders.json"), "w") as c_orders_file:
            json.dump(c_orders_data, c_orders_file, indent=4)
    except Exception as e:
        logging.error(f"Error writing to c_orders.json: {e}")
        return jsonify({"error": "Error writing to c_orders.json"}), 500

    del u_orders_data[order]

    try:
        with open(os.path.join("data", "u_orders.json"), "w") as u_orders_file:
            json.dump(u_orders_data, u_orders_file)
    except Exception as e:
        logging.error(f"Error writing to u_orders.json: {e}")
        return jsonify({"error": "Error writing to u_orders.json"}), 500

    try:
        with open(os.path.join("data", "users.json"), "r") as users_file:
            users_data = json.load(users_file)
    except Exception as e:
        logging.error(f"Error loading users.json: {e}")
        return jsonify({"error": "Error loading users.json"}), 500

    users_data[hwid] = user

    try:
        with open(os.path.join("data", "users.json"), "w") as users_file:
            json.dump(users_data, users_file)
    except Exception as e:
        logging.error(f"Error writing to users.json: {e}")
        return jsonify({"error": "Error writing to users.json"}), 500

    try:
        with open(os.path.join("data", "status.json"), "r") as status_file:
            status_data = json.load(status_file)
    except Exception as e:
        logging.error(f"Error loading status.json: {e}")
        return jsonify({"error": "Error loading status.json"}), 500

    status_data[hwid] = False

    try:
        with open(os.path.join("data", "status.json"), "w") as status_file:
            json.dump(status_data, status_file)
    except Exception as e:
        logging.error(f"Error writing to status.json: {e}")
        return jsonify({"error": "Error writing to status.json"}), 500

    try:
        with open(os.path.join("data", "whwid.json"), "r") as whwid_file:
            whwid_data = json.load(whwid_file)
    except Exception as e:
        logging.error(f"Error loading whwid.json: {e}")
        return jsonify({"error": "Error loading whwid.json"}), 500

    whwid_data[hwid] = expiry_timestamp

    try:
        with open(os.path.join("data", "whwid.json"), "w") as whwid_file:
            json.dump(whwid_data, whwid_file)
    except Exception as e:
        logging.error(f"Error writing to whwid.json: {e}")
        return jsonify({"error": "Error writing to whwid.json"}), 500
    try:
        with open(os.path.join("data", "expire.json"), "r") as expire_file:
            expire_data = json.load(expire_file)
    except Exception as e:
        logging.error(f"Error loading expire.json: {e}")
        expire_data = {}

    expire_data[hwid] = expiry_timestamp

    try:
        with open(os.path.join("data", "expire.json"), "w") as expire_file:
            json.dump(expire_data, expire_file)
    except Exception as e:
        logging.error(f"Error writing to expire.json: {e}")
        return jsonify({"error": "Error writing to expire.json"}), 500
    logging.debug("Registration successful")
    return jsonify({"message": "Registration successful"}), 200

@app.route("/get_latest", methods=['GET'])
def get_latest_version():
    with open(os.path.join("data", "version.json"), "r") as version_file:
        version_data = json.load(version_file)

        return version_data['version']

@app.route("/download/launcher")
def download_launcher():
    return send_from_directory("storage", "launcher.txt", as_attachment=True)

@app.route("/download/cyberious")
def download_cyberious():
    hwid = request.args.get('hwid')
    if not hwid:
        return jsonify({"error": "Missing hwid parameter"}), 400 

    whwid_path = os.path.join("data", "whwid.json")
    if not os.path.exists(whwid_path):
        return jsonify({"error": "File not found"}), 404

    with open(whwid_path, "r") as whwid_file:
        whwid_data = json.load(whwid_file)

    if hwid not in whwid_data:
        return jsonify({"error": "Unauthorized"}), 401
    expiry_timestamp = whwid_data[hwid]
    if time.time() > expiry_timestamp:
        return jsonify({"error": "License expired"}), 401

    return send_from_directory("storage", "launcher.txt", as_attachment=True)

if not DEPLOY:
    if __name__ == "__main__":
        app.run(debug=True)
