from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import hypixel
from mojang import MojangAPI
from hypixelapi import hypixelapi
import hypixel
import requests
import time
import datetime

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
            if str(is_online) == "True":
                is_online_gameType = player.get_status()['gameType']
                is_online_mode = player.get_status()['mode']
                if is_online_gameType == "SKYBLOCK":
                    is_online_gameType = "SkyBlock"
                    if is_online_mode == 'dynamic':
                        is_online_mode = 'their Island'
                    elif is_online_mode == 'hub':
                        is_online_mode = 'the Hub'
                    elif is_online_mode == 'combat_1':
                        is_online_mode = "the Spider's Den"
                    elif is_online_mode == 'combat_2':
                        is_online_mode = 'the Blazing Fortress'
                    elif is_online_mode == 'combat_3':
                        is_online_mode = 'the End'
                    elif is_online_mode == 'foraging_1':
                        is_online_mode = 'the Park'
                    elif is_online_mode == 'farming_1':
                        is_online_mode = 'the Barn'
                    elif is_online_mode == 'farming_2':
                        is_online_mode = 'the Mushroom Dessert'
                    elif is_online_mode == 'mining_1':
                        is_online_mode = 'the Gold Mine'
                    elif is_online_mode == 'mining_2':
                        is_online_mode = 'the Deep Caverns'
                    elif is_online_mode == 'dungeon_hub':
                        is_online_mode = 'the Dungeon Hub'
                    else:
                        is_online_mode = is_online_mode
                else:
                    is_online_gameType = "is_online_gameType"
                    is_online_mode = "is_online_mode"
            else:
                is_online_gameType = "is_online_gameType"
                is_online_mode = "is_online_mode"

            skyblock_number_of_profiles = hypixel.Player(raw_username).getPlayerInfo()
            print(skyblock_number_of_profiles)

            black = '#000000'
            dark_blue = '#0000AA'
            dark_green = '#00AA00'
            dark_aqua = '#00AAAA'
            dark_red = '#AA0000'
            dark_purple = '#AA00AA'
            gold = '#FFAA00'
            gray = '#AAAAAA'
            dark_gray = '#555555'
            blue = '#5555FF'
            green = '#55FF55'
            aqua = '#55FFFF'
            red = '#FF5555'
            light_purple = '#FF55FF'
            yellow = '#FFFF55'
            white = '#FFFFFF'

            rpc = requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()['rank_plus_color']
            if str(rpc) == "&0":
                rank_plus_color = black
            elif str(rpc) == "&1":
                rank_plus_color = dark_blue
            elif str(rpc) == "&2":
                rank_plus_color = dark_green
            elif str(rpc) == "&3":
                rank_plus_color = dark_aqua
            elif str(rpc) == "&4":
                rank_plus_color = dark_red
            elif str(rpc) == "&5":
                rank_plus_color = dark_purple
            elif str(rpc) == "&6":
                rank_plus_color = gold
            elif str(rpc) == "&7":
                rank_plus_color = gray
            elif str(rpc) == "&8":
                rank_plus_color = dark_gray
            elif str(rpc) == "&9":
                rank_plus_color = blue
            elif str(rpc) == "&a":
                rank_plus_color = green
            elif str(rpc) == "&b":
                rank_plus_color = aqua
            elif str(rpc) == "&c":
                rank_plus_color = red
            elif str(rpc) == "&d":
                rank_plus_color = light_purple
            elif str(rpc) == "&e":
                rank_plus_color = yellow
            elif str(rpc) == "&f":
                rank_plus_color = white

            return render_template('profile.html', username=name, network_rank=network_rank, uuid=uuid,
                                   network_level=network_level, network_exp=network_exp,
                                   network_linked_socialmedia_number=network_linked_socialmedia_number,
                                   TWITTER=TWITTER, TWITCH=TWITCH, YOUTUBE=YOUTUBE, INSTAGRAM=INSTAGRAM,
                                   DISCORD=DISCORD, HYPIXEL=HYPIXEL, is_online=is_online,
                                   rank_plus_color=rank_plus_color, is_online_gameType=is_online_gameType,
                                   is_online_mode=is_online_mode)

        except hypixel.PlayerNotFoundException:
            return home()
    else:
        return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8080)
