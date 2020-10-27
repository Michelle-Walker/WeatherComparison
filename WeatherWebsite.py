# TODO: First, learn how to get user input

from flask import Flask, render_template, request, url_for
import requests
import json

from werkzeug.utils import redirect

app = Flask(__name__)


def city_check(city):
    # TODO: use this to get city info
    return city


@app.route("/")
def home():
    # TODO: get cities from user
    return render_template("index.html")

'''
@app.route("/nice", methods=["POST"])
def nice():
    city1 = request.form["city1"]
    return f"<h1> {city1} is nice </h1>"
'''


@app.route("/Compare", methods=["POST"])
def city_comparison():
    # TODO: display city comparison
    c1 = request.form["city1"]
    c2 = request.form["city2"]
    if "c1" in request.args:
        c1 = request.args["c1"]
    if "c2" in request.args:
        c2 = request.args["c2"]
    if c1 is not None and c2 is not None:
        return f"Check out {c1} and {c2}!"


@app.route("/checkagain", methods=["POST"])
def check():
    url = "http://api.openweathermap.org/data/2.5/weather"
    c1 = request.form["city1"]
    if "c1" in request.args:
        c1 = request.args["c1"]
    payload = {
        'lat': c1,
        'lon': "139",
        'appid': "2f086cf6129c094ad1c057393633cd53"
    }
    response = requests.request("GET", url, params=payload)
    # return f"check out lat {c1} and lon"
    return response.text


@app.route("/comparetrial", methods=["POST"])
def comparetrial():
    url = "http://api.openweathermap.org/data/2.5/weather"
    c1 = request.form["city1"]
    c2 = request.form["city2"]
    if "c1" in request.args:
        c1 = request.args["c1"]
    if "c2" in request.args:
        c2 = request.args["c2"]
    if c1 is not None and c2 is not None:
        payload1 = {
            'q': c1,
            'appid': "2f086cf6129c094ad1c057393633cd53"
        }
        response1 = requests.request("POST", url, params=payload1)
        payload2 = {
            'q': c2,
            'appid': "2f086cf6129c094ad1c057393633cd53"
        }
        response2 = requests.request("POST", url, params=payload2)
        r1 = json.loads(response1.text)
        r2 = json.loads(response2.text)
        city1 = r1["name"]
        city2 = r2["name"]
        weather1 = r1["weather"]
        weather2 = r2["weather"]
        main1 = r1["main"]
        main2 = r2["main"]
        print(type(main2))
        print(main2["temp"])
        return redirect(url_for("comparison", c1=str(city1), m1=main1["temp"], w1=weather1[0]["main"], d1=weather1[0]["description"], c2=str(city2), m2=main2["temp"], w2=weather2[0]["main"], d2=weather2[0]["description"]))


@app.route("/comparison/<c1>/<m1>/<w1>/<d1>/<c2>/<m2>/<w2>/<d2>", methods=["GET", "POST"])
def comparison(c1, m1, w1, d1, c2, m2, w2, d2):
    # return f"<h1>{c1}</h1>"
    return render_template("comparison.html", city1=c1, main1=m1, weather1=w1, description1=d1, city2=c2, main2=m2, weather2=w2, description2=d2)



if __name__ == "__main__":
    app.run(debug=True)
