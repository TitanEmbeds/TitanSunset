from flask import Flask, abort, request, redirect, render_template, url_for
import os

app = Flask(__name__)

def is_crawler(): # So we don't get a screwed up SEO
    agent = request.headers.get('User-Agent', "").lower()
    return "bot" in agent or "crawl" in agent or "slurp" in agent or "spider" in agent or "mediapartners" in agent

@app.route("/api/<path:path>", methods=["GET", "POST", "DELETE"]) # Tell the API that it doesn't exists no more
def api(path):
    abort(404)

@app.route("/embed/<path:path>")
def embed(path):
    if is_crawler():
        return redirect(url_for("index"), code=301)
    return render_template("embed.html.j2")

@app.route('/',)
def index():
    return render_template("index.html.j2")

@app.route('/<path:path>')
def catch_all(path):
    return redirect(url_for("index"), code=301)

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 3000)), debug=True)