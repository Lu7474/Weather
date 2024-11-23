from flask import Flask, render_template, request
import requests
from core.config import API
from core import app


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric&lang=ru"
            response = requests.get(url)
            data = response.json()

            weather_data = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
            }

    return render_template("index.html", weather_data=weather_data)
