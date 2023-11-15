from flask import Flask, render_template, request, url_for
from part1 import find_stop_near, get_weather


app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/nearest_mbta', methods=['POST'])
def nearest_mbta():
    place_name = request.form.get('Location')
    if not place_name:
        return render_template('error.html', error_message="Please enter a location.", url_for_home=url_for('index'))
    try:
        result, accessible = find_stop_near(place_name)
        weather_info = get_weather(place_name)
        return render_template("mbta_station.html", result=result, accessible=accessible, weather_info=weather_info)
    except Exception as e:
        print(e)
        return render_template("error.html", error_message="An error occured.", url_for_home=url_for('index'))

@app.route('/error')
def error():
    return render_template("error.html", error_message="An error occured.", url_for_home=url_for('index'))
    

if __name__ == '__main__':
    app.run(debug=True)
