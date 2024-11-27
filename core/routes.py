import requests

from flask import Flask, render_template, request

from core.config import API
from core import app


def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        query_params = {"q": city, "appid": API, "units": "metric", "lang": "ru"}
        response = requests.get(url, params=query_params)
        data = response.json()

        weather_data = {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
        }
        return weather_data
    except requests.exceptions.RequestException as e:
        print(f"Ошибка API: {e}")
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            weather_data = get_weather(city)

    return render_template("index.html", weather_data=weather_data)
