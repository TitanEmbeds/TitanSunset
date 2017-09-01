from flask import Flask, abort, request, redirect, render_template
import os

app = Flask(__name__)

def is_crawler(): # So we don't get a screwed up SEO
    agent = request.headers.get('User-Agent').lower()
    return "bot" in agent or "crawl" in agent or "slurp" in agent or "spider" in agent or "mediapartners" in agent

@app.route("/api/<path:path>", methods=["GET", "POST", "DELETE"]) # Tell the API that it doesn't exists no more
def api(path):
    abort(404)

@app.route("/embed/<path:path>")
def embed(path):
    arguments = ""
    if len(request.args) > 0:
        arguments += "?"
        for key, val in request.args.items():
            arguments += "{0}={1}&".format(key, val)
        arguments = arguments[:len(arguments) - 1]
    url = "https://titanembeds.com/embed/" + path + arguments
    if is_crawler():
        return redirect(url, code=301)
    return render_template("embed.html.j2", url=url)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if is_crawler():
        return redirect("https://titanembeds.com/", code=301)
    return render_template("redirect.html.j2")

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), debug=True)