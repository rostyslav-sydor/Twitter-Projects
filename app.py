"""
Program is designed to get list of somebody's twitter friends 
and generate map showing their locations.
"""
from flask import Flask, render_template, request, redirect
from geopy import Nominatim
from geopy.exc import GeocoderUnavailable
import folium
import json
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/redirect', methods = ["GET", "POST"])
def redirection():
    tag = request.form.get('tag')
    if len(tag) == 0:
        return render_template('index.html')
    main(tag)
    return redirect('/map')

@app.route('/map')
def karta():
    return render_template('map.html')

def findCoords(lst: list):
    """
    Finds latitude and longitude using address.
    >>> findCoords([('Bill Clinton', 'New York, NY')])
    [('Bill Clinton', (40.7127281, -74.0060152), 'New York, NY')]
    """
    good_friends = []
    for elem in lst:
        if len(good_friends) < 15:
            address = Nominatim(user_agent="friends-map").geocode(elem[1])
            try:
                good_friends.append((elem[0], (address.latitude, address.longitude), elem[1]))
            except (AttributeError, GeocoderUnavailable):
                pass
    return good_friends

def main(name: str) -> None:
    """
    Main function
    """
    with open('lab2/templates/map.html', mode='w') as karta:
        karta.write('')
    params = {"cursor": '-1', "screen_name": name, "count": 20}
    headers = {"Authorization": "Bearer AAAAAAAAAAAAAAAAAAAAABu4MwEAAAAAAD2jcKqtXF%2FNpsK9ci73Dk6gU5U%3DpaFqLuGKQPpWbzdoezJFm6q5snSDbhUbhs6P6Kqe6ucgz76kPy", "user-Agent": "my-app"}
    re = requests.get("https://api.twitter.com/1.1/friends/list.json", headers=headers, params=params).json()
    friends = []
    print(re)
    for user in re['users']:
        if user['location'] != '':
            name = user['name']
            address = user['location']
            friends.append((name, address))
    print(friends)
    friends = findCoords(friends)
    karta = folium.Map()
    groups = {}
    for friend in friends:
        if friend[2] not in groups:
            groups[friend[2]] = folium.FeatureGroup(name = friend[2])
        groups[friend[2]].add_child(folium.Marker(location=[friend[1][0], friend[1][1]], popup = friend[0]))
        karta.add_child(groups[friend[2]])
    karta.save('lab2/templates/map.html')

if __name__ == "__main__":
    app.run(debug=True)