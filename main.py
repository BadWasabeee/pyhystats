from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import hypixel
from mojang import MojangAPI
from hypixelapi import hypixelapi
import hypixel
import requests


app = Flask(__name__)

keys = ['e6a09aab-befc-4f53-b668-7fd3fe2a585d', 'e6a09aab-befc-4f53-b668-7fd3fe2a585d']
hypixel.setKeys(keys)


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
    raw_username = request.args.get('username')
    uuid = MojangAPI.get_uuid(raw_username)
    if uuid:
        try:
            api = hypixelapi.HypixelAPI('e6a09aab-befc-4f53-b668-7fd3fe2a585d')
            player = api.get_player(uuid)
            name = MojangAPI.get_profile(uuid).name
            network_rank = hypixel.Player(raw_username).getRank()['rank']
            network_level = player.get_level()
            network_exp = int(player.get_exp())
            links = requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()['links']

            network_linked_socialmedia_number = 0
            for SocialMedias in links:
                Social = links[SocialMedias]
                if not str(Social) == "None":
                    network_linked_socialmedia_number = network_linked_socialmedia_number + 1

            TWITTER = links['TWITTER']
            YOUTUBE = links['YOUTUBE']
            INSTAGRAM = links['INSTAGRAM']
            TWITCH = links['TWITCH']
            DISCORD = links['DISCORD']
            HYPIXEL = links['HYPIXEL']

            is_online = player.get_status()['online']
            # if str(is_online) == "True":
            #     is_online_gameType = player.get_status()['gameType']
            #     is_online_mode = player.get_status()['mode']

            print(requests.get('https://api.slothpixel.me/api/players/' + raw_username).json())

            return render_template('profile.html', username=name, network_rank=network_rank, uuid=uuid,
                                   network_level=network_level, network_exp=network_exp,
                                   network_linked_socialmedia_number=network_linked_socialmedia_number,
                                   TWITTER=TWITTER, TWITCH=TWITCH, YOUTUBE=YOUTUBE, INSTAGRAM=INSTAGRAM,
                                   DISCORD=DISCORD, HYPIXEL=HYPIXEL, is_online=is_online)

        except hypixel.PlayerNotFoundException:
            return home()
    else:
        return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8080)
