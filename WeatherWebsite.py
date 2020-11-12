from flask import Flask, render_template, request, url_for
import requests
import json
from werkzeug.utils import redirect
from models.WeatherInfo import WeatherInfo

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


def get_response(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    payload1 = {
        'q': city,
        'appid': "2f086cf6129c094ad1c057393633cd53"
    }
    response = requests.request("POST", url, params=payload1)
    return response


@app.route("/none", methods=["GET"])
def none():
    return render_template("none.html")


@app.route("/comparetrial", methods=["POST"])
def comparetrial():
    c1 = request.form["city1"]
    c2 = request.form["city2"]
    if c1 == "" or c2 == "":
        return redirect(url_for("none"))
    if c1 is not None and c2 is not None:
        response1 = get_response(c1)
        response2 = get_response(c2)  # weather API call

        r1 = json.loads(response1.text)
        r2 = json.loads(response2.text)  # takes API response and returns json object

        if not response1:  # check if city is found
            return redirect(url_for("city_not_found", city=c1))
        elif not response2:
            return redirect(url_for("city_not_found", city=c2))
        else:
            city1 = r1["name"]
            city2 = r2["name"]

        return render_template("comparison.html", city1=city1, weather1=weather_obj(r1), city2=city2, weather2=weather_obj(r2))


@app.route("/cityNotFound/<city>", methods=["GET"])
def city_not_found(city):
    return render_template("cityNotFound.html", city=city)


def weather_obj(response):  # turns weather info from API into object
    main = response["main"]
    weather = json.loads(json.dumps(main, indent=2), object_hook=lambda d: WeatherInfo(**d))
    weather.description = response["weather"][0]["main"]
    return weather


if __name__ == "__main__":
    app.run(debug=True)
