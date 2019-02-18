from flask import Flask, render_template, request, redirect
import json
import urllib.request, urllib.parse, urllib.error
import twurl
import json
import folium
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="specify_your_app_name_here", timeout=100)
from geopy.extra.rate_limiter import RateLimiter
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)


from create_map import inform_friends, get_data_map, geodata, layer_loc_friends


app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/register", methods=["POST"])
# def map():
#     # if not request.form.get("name"):
#     #     return render_template("failure.html")
#     acct = request.form.get("name")
#     err = layer_loc_friends(acct)
#     layer_loc_friends(acct)
#     # print(err)
#     # if err == "Error":
#     #     return render_template("failure.html")
#     return render_template("Main_map.html")


@app.route("/register", methods=["POST"])
def map():
    if not request.form.get("name"):
        return render_template("failure.html")
    acct = request.form.get("name")
    map_html = layer_loc_friends(acct)
    return map_html

if __name__ == '__main__':
    app.run(debug=True)