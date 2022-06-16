from flask import Flask, render_template, request, redirect, jsonify, url_for
from models import db, APIKeys, PublicItem
import json

app = Flask(__name__, template_folder="templates")
app.config.from_file("config.json", load=json.load)

db.init_app(app)
db.create_all(app=app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/")
def index():
    if 'CONTEST_MEMBER_ID' in app.config.keys(): member_id = app.config['CONTEST_MEMBER_ID']
    else: member_id = 'NULL'
    return render_template("index.html", member_id=member_id)

@app.route("/list_items")
def list_items():
    return render_template("list_items.html", items=PublicItem.query.all())

@app.route("/create_item", methods=["GET", "POST"])
def create_item():
    if request.method == "GET":
        return render_template("create_item.html")
    if request.method == "POST":
        attrs = request.form
        item = PublicItem(**attrs)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("list_items"))

@app.route("/delete/item/<id>", methods=["POST"])
def delete_item(id):
    item = PublicItem.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("list_items"))

@app.route("/api/list")
def api_list():
    list = [i.serialize for i in PublicItem.query.all()]
    return jsonify(list)

@app.route("/api/keys")
def api_keys():
    list = { i.serialize[0] : i.serialize[1] for i in APIKeys.query.all()}
    return jsonify(list)

if __name__ == "__main__":
    app.run()
