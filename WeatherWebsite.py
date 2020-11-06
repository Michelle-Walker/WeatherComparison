from flask import Flask, render_template, request, url_for
import requests
import json

from werkzeug.utils import redirect

app = Flask(__name__)


def city_check(city):
    # TODO: use this to get city info
    return city


@app.route("/", methods=["POST"])
def home():
    return render_template("index.html")


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
        if response1 and response2:
            city1 = r1["name"]
            city2 = r2["name"]
        else:
            return redirect(url_for("city_not_found"))

        weather_lst_one = weather_string(r1)
        weather_lst_two = weather_string(r2)
        return render_template("comparison.html", city1=city1, weather_string1=weather_lst_one, city2=city2, weather_string2=weather_lst_two)
        # return redirect(url_for("comparison", c1=city1, ws1=weather_lst_one, c2=city2, ws2=weather_lst_two))


@app.route("/cityNotFound", methods=["POST", "GET"])
def city_not_found():
    return render_template("cityNotFound.html")


def get_f_temp(response):
    k_temp = response
    f_temp = round((k_temp-273.15)*(9/5)+32, 1)
    return f_temp


def weather_string(response):
    main = response["main"]
    print(main)
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
    weather_list = []
    for each in weather_str:
        if each == "/":
            weather_list.append(place_holder)
            place_holder = ""
        else:
            place_holder += each
    print("weather_list: " + str(type(weather_list)))
    return weather_list


if __name__ == "__main__":
    app.run(debug=True)
