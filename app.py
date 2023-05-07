from flask import Flask, render_template, send_from_directory
import json
import os

app = Flask(__name__)

name_to_full_name = {
    "tantra": "Tantra",
    "bbc": "BBC",
    "vc": "Vindhya Canteen",
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


if __name__ == "__main__":
    app.run(debug=True)
