from flask import (
    Flask,
    render_template,
    send_from_directory,
    redirect,
    url_for,
    request,
)
from datetime import datetime
from math import floor
import json
import os

from tinydb import TinyDB, Query

app = Flask(__name__)

name_to_full_name = {
    "tantra": "Tantra",
    "bbc": "BBC",
    "vc": "Vindhya Canteen",
    "bakul": "Bakul Nivas",
    "parijaat": "Parijaat Nivas",
    "obh": "Old Boys Hostel",
}


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "favicon.ico",
        mimetype="image/vdn.microsoft.icon",
    )


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/canteen/<name>")
def canteen(name: str) -> str:
    with app.open_resource(f"static/menu/{name}.json", "r") as f:
        menu_list = json.load(f)

    print(menu_list)
    return render_template(
        "canteen.html", name=name_to_full_name[name], menu_list=menu_list
    )


@app.route("/orders/accepted")
def accepted():
    print("accepted")
    orders = table.search(Order.status == "accepted")
    tantra_orders = []
    bbc_orders = []
    vc_orders = []

    for order in orders:
        order_time = datetime.strptime(order["time"], "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.now()
        delta = current_time - order_time
        delta_minutes = floor(delta.total_seconds() / 60)

        order["delta_minutes"] = delta_minutes
        if order["hostel"] in name_to_full_name:
            order["hostel"] = name_to_full_name[order["hostel"]]
        if order["canteen"] == "Tantra":
            tantra_orders.append(order)
        elif order["canteen"] == "BBC":
            bbc_orders.append(order)
        elif order["canteen"] == "Vindhya Canteen":
            vc_orders.append(order)

    return render_template(
        "accepted_orders.html",
        all_canteens={
            "Tantra": tantra_orders,
            "BBC": bbc_orders,
            "Vindhya Canteen": vc_orders,
        },
    )


@app.route("/orders/pending")
def pending():
    orders = table.search(Order.status == "pending")
    tantra_orders = []
    bbc_orders = []
    vc_orders = []

    for order in orders:
        if order["hostel"] in name_to_full_name:
            order["hostel"] = name_to_full_name[order["hostel"]]
        order_time = datetime.strptime(order["time"], "%Y-%m-%d %H:%M:%S.%f")
        current_time = datetime.now()
        delta = current_time - order_time
        delta_minutes = floor(delta.total_seconds() / 60)

        order["delta_minutes"] = delta_minutes
        if order["canteen"] == "Tantra":
            tantra_orders.append(order)
        elif order["canteen"] == "BBC":
            bbc_orders.append(order)
        elif order["canteen"] == "Vindhya Canteen":
            vc_orders.append(order)

    return render_template(
        "pending_orders.html",
        all_canteens={
            "Tantra": tantra_orders,
            "BBC": bbc_orders,
            "Vindhya Canteen": vc_orders,
        },
    )


@app.route("/api/addOrder", methods=["POST"])
def addOrder():
    data = {
        "name": request.form.get("name"),
        "hostel": request.form.get("hostel"),
        "room-number": request.form.get("room-number"),
        "phone-number": request.form.get("phone-number"),
        "travel-cost": request.form.get("travel-cost"),
        "food-cost": request.form.get("food-cost"),
        "total-cost": request.form.get("total-cost"),
        "canteen": request.form.get("canteen"),
        "time": str(datetime.now()),
        "status": "pending",
        "orders": [],
    }
    for k, v in request.form.items():
        if k == "name":
            break
        if v == "0":
            continue
        else:
            data["orders"].append((k, v))

    table.insert(data)
    return redirect("/orders/pending")


@app.route("/api/acceptOrder", methods=["POST"])
def acceptOrder():
    data = request.json
    table.update(
        {
            "status": "accepted",
            "accepted-by": data["name"],
            "contact": data["number"],
            "code": data["code"],
        },
        Order.time == str(data["timestamp"]),
    )

    print("updated table")

    return {"status": 200}


@app.route("/api/deliverOrder", methods=["POST"])
def deliverOrder():
    data = request.json
    res = table.search(Order.time == str(data["timestamp"]))[0]
    code = str(res["code"])

    auth = code == data["code"]

    if not auth:
        return {"status": 401}

    table.remove(Order.time == str(data["timestamp"]))
    return {"status": 20}


if __name__ == "__main__":
    db = TinyDB("db.json")
    table = db.table("orders")
    Order = Query()
    app.run(debug=True)
