from flask import Flask, render_template, request
import requests
from core.config import API, URL
from core import app


@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            try:
                response = requests.get(
                    URL,
                    params={
                        "q": city,
                        "appid": API,
                        "units": "metric",
                        "lang": "ru",
                    },
                )
                data = response.json()

                if data.get("cod") != 200:
                    error_message = data.get("message", "Ошибка при получении данных")
                else:
                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "description": data["weather"][0]["description"],
                        "icon": data["weather"][0]["icon"],
                    }
            except requests.RequestException:
                error_message = "Ошибка сети или подключения к API"

    return render_template(
        "index.html", weather_data=weather_data, error_message=error_message
    )
