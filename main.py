from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import hypixel
from mojang import MojangAPI
from hypixelapi import hypixelapi
import hypixel

app = Flask(__name__)

keys = ['e6a09aab-befc-4f53-b668-7fd3fe2a585d', 'e6a09aab-befc-4f53-b668-7fd3fe2a585d']
hypixel.setKeys(keys)


@app.route('/search')
def search_user():
    username = request.form['username']
    uuid = MojangAPI.get_uuid(username)

    if not uuid:
        search_user()
    else:
        session['logged_in'] = True
    return home()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('home.html')
    else:
        return profile()


@app.route('/discord')
def discord():
    return redirect('https://discord.gg/K92sX47')


@app.route('/profile/')
def profile():
    # key = 'e6a09aab-befc-4f53-b668-7fd3fe2a585d'
    api = hypixelapi.HypixelAPI('e6a09aab-befc-4f53-b668-7fd3fe2a585d')
    raw_username = request.args.get('username')
    uuid = MojangAPI.get_uuid(raw_username)
    player = api.get_player(uuid)
    name = MojangAPI.get_profile(uuid).name
    network_rank = hypixel.Player(raw_username).getRank()['rank']
    network_level = player.get_level()
    network_exp = str(player.get_exp())
    if not uuid:
        session['logged_in'] = False
    else:
        return render_template('profile.html', username=name, network_rank=network_rank, uuid=uuid,
                               network_level=network_level, network_exp=network_exp)
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8080)
