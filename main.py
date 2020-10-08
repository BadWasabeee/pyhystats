from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import hypixel
from mojang import MojangAPI
from hypixelapi import hypixelapi


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
    rank = player.get_rank()
    level = player.get_level()
    number_of_profiles = player.get_stats(hypixelapi.GameType.SKYBLOCK)['profiles'][uuid]['cute_name']
    x = 0
    for number_of_profiles in player.get_stats(hypixelapi.GameType.SKYBLOCK)['profiles']:
        print(number_of_profiles)
        x = x + 1
    if not uuid:
        session['logged_in'] = False
    else:
        if str(rank).lower() == 'youtube':
            rank_color = '#FF5555'
        elif str(rank).lower() == "admin":
            rank_color = '#FF5555'
        elif str(rank).lower() == "mod":
            rank_color = '#00AA00'
        elif str(rank).lower() == "helper":
            rank_color = '#5555FF'
        elif str(rank).lower() == "Superstar":
            rank_color = '#FFAA00'
        elif str(rank).lower() == "mvp_plus":
            rank_color = '#55FFFF'
        elif str(rank).lower() == "mvp":
            rank_color = '#55FFFF'
        elif str(rank).lower() == "vip_plus":
            rank_color = '#55FF55'
        elif str(rank).lower() == "vip":
            rank_color = '#55FF55'
        elif str(rank).lower() == "none":
            rank_color = '#AAAAAA'

        if not str(rank).lower() == 'none':
            rank_tag = str('[' + str(rank) + ']').upper()
        else:
            rank_tag = ''

        return render_template('profile.html', username=name, rank=rank, ranktag=rank_tag, uuid=uuid, level=level,
                               rankcolor=rank_color, x=x)
    return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8080)
