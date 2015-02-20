import time
import json
from flask import Flask,render_template,request
import markdown2
from db import *


app = Flask(__name__)
app.debug = True


@app.route('/')
def index():
    entries = list_blogs_meta()
    for entry in entries:
        entry["pretty_time"] = time.strftime("%m/%d/%y %M:%S",time.gmtime(entry["time"]))
    entries.sort()
    return render_template("index.html", entries=entries)

@app.route('/load_post', methods=["POST"])
def get_post():
    id = request.form["id"]
    r = get_blog_entry(id)
    r["id"] = id
    r["time"] = time.strftime("%m/%d/%y %M:%S",time.gmtime(r["time"]))
    return json.dumps(r)

@app.route('/view/<url>')
def get_blog_post(url):
    id = get_id(url)
    if id:
        blog = get_blog_entry(id)
        if blog["published"]=="true":
            return markdown2.markdown(blog["content"])
        else:
            return "not published yet!"
    else:
        return "404"


@app.route("/save_post", methods=["POST"])
def save_post():
    req = {}
    for k in request.form:

        req[k] = request.form[k]
    # print req
    # return ""
    #New post
    if req["id"]=="12345":
        req["time"] = time.time()
        db.save(req)
        return str(True)
    id = req["id"]
    req.pop("id")
    keys = []
    values = []
    for k in req:
        if k=="id":
            pass
        keys.append(k)
        values.append(req[k])

    update_values(keys, values, id)

    return str(True)

if __name__ == '__main__':
    app.run(port=666)
