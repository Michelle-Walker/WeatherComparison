from flask import Flask, render_template, request, url_for
import requests
import json
from werkzeug.utils import redirect

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

        if not response1:
            return redirect(url_for("city_not_found", city=c1))
        elif not response2:
            return redirect(url_for("city_not_found", city=c2))
        else:
            city1 = r1["name"]
            city2 = r2["name"]

        weather_lst_one = weather_list(r1)
        weather_lst_two = weather_list(r2)
        return render_template("comparison.html", city1=city1, weather_string1=weather_lst_one, city2=city2, weather_string2=weather_lst_two)


@app.route("/cityNotFound/<city>", methods=["GET"])
def city_not_found(city):
    # TODO: more descriptive error message here
    return render_template("cityNotFound.html", city=city)


def get_f_temp(response):  # converts from K to deg F
    k_temp = response
    f_temp = round((k_temp-273.15)*(9/5)+32, 1)
    return f_temp


def weather_list(response):  # turns weather info into list
    main = response["main"]
    temp = get_f_temp(main["temp"])
    feels_like = get_f_temp(main["feels_like"])
    min_temp = get_f_temp(main["temp_min"])
    max_temp = get_f_temp(main["temp_max"])
    humidity = main["humidity"]
    weather = response["weather"]
    description = weather[0]
    w_des = description["main"]
    weather_str = "Description: " + w_des + "/ Temperature: " + str(temp) + str(" degrees F") + "/ Feels like: " + str(feels_like) + str(" degrees F") + "/ Minimum Temperature: " + str(min_temp) + str(" degrees F") + "/ Maximum Temperature: " + str(max_temp) + str(" degrees F") + "/ Humidity: " + str(humidity) + "%/"

    place_holder = ""
    weather_lst = []
    for each in weather_str:
        if each == "/":
            weather_lst.append(place_holder)
            place_holder = ""
        else:
            place_holder += each
    return weather_lst


if __name__ == "__main__":
    app.run(debug=True)
