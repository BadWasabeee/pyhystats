from flask import Flask, flash, redirect, render_template, request, session
import os
import hypixel
from mojang import MojangAPI
from hypixelapi import hypixelapi
import requests
import datetime
import json

app = Flask(__name__)

keys = json.load(open("keys.json"))['api_keys']
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
            api_key = json.load(open("keys.json"))['api_keys']
            api = hypixelapi.HypixelAPI(api_key[0])
            player = api.get_player(uuid)
            name = MojangAPI.get_profile(uuid).name
            network_rank = hypixel.Player(raw_username).getRank()['rank']

            def format_dates(long_number):
                format_long_number = datetime.datetime.fromtimestamp(long_number // 1000.0)
                difference_of_number = datetime.datetime.now() - format_long_number

                number_from_now_days = divmod(difference_of_number.total_seconds(), 86400)
                number_from_now_hours = divmod(number_from_now_days[1], 3600)
                number_from_now_mins = divmod(number_from_now_hours[1], 60)
                number_from_now_secs = divmod(number_from_now_mins[1], 1)

                if number_from_now_days[0] < 1 and number_from_now_hours[0] > 1:
                    return (str(int(round(number_from_now_hours[0], 0))) + " hours " + str(int(round(
                        number_from_now_mins[0], 0))) + " minutes " + str(int(round(number_from_now_secs[0], 0)))
                            + " seconds ")

                elif number_from_now_hours[0] < 1 and number_from_now_days[0] < 1:
                    return (str(int(round(number_from_now_mins[0], 0))) + " minutes " + str(int(round(
                        number_from_now_secs[0], 0))) + " seconds ")

                elif number_from_now_mins[0] < 1 and number_from_now_days[0] < 1 and number_from_now_hours[0] < 1:
                    return (str(int(round(number_from_now_secs[0], 0))) + " seconds ")

                else:
                    return (str(int(round(number_from_now_days[0], 0))) + " days " + str(int(round(
                        number_from_now_hours[0], 0))) + " hours " + str(
                        int(round(number_from_now_mins[0], 0))) +
                            " minutes " + str(int(round(number_from_now_secs[0], 0))) + " seconds ")

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
                last_login_long = requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()[
                    'last_login']
                if not str(last_login_long) == "None":
                    last_login_from_now = format_dates(last_login_long)
                else:
                    last_login_from_now = "null"
                last_logout_from_now = 'Online'
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
                elif is_online_gameType == "PROTOTYPE":
                    is_online_gameType = "Prototype lobby"
                elif is_online_gameType == "MAIN":
                    is_online_gameType = "Main Lobby"
                elif is_online_gameType == "BEDWARS":
                    is_online_gameType = "BedWars"
                    if is_online_mode == "LOBBY":
                        is_online_mode = "the Lobby"
                    elif is_online_mode == "EIGHT_ONE":
                        is_online_mode = "Solos"
                    elif is_online_mode == "EIGHT_TWO":
                        is_online_mode = "Duos"
                    elif is_online_mode == "FOUR_THREE":
                        is_online_mode = "3v3v3v3"
                    elif is_online_mode == "FOUR_FOUR":
                        is_online_mode = "4v4v4v4"
                    else:
                        is_online_mode = is_online_mode
                else:
                    is_online_gameType = is_online_gameType
                    is_online_mode = is_online_mode
            elif str(requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()[
                         'last_logout']).lower() == "none":

                last_logout_from_now = "disabled"
                is_online_gameType = "disabled"
                is_online_mode = "disabled"
                last_login_from_now = "disabled"
            else:
                last_logout_long = requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()[
                    'last_logout']
                last_logout_from_now = format_dates(last_logout_long)
                is_online_gameType = "Offline"
                is_online_mode = "Offline"
                last_login_from_now = "Offline"

            rpc = requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()['rank_plus_color']
            if str(rpc) == "&0":
                rank_plus_color = 'mc-black'
            elif str(rpc) == "&1":
                rank_plus_color = 'mc-dark_blue'
            elif str(rpc) == "&2":
                rank_plus_color = 'mc-dark_green'
            elif str(rpc) == "&3":
                rank_plus_color = 'mc-dark_aqua'
            elif str(rpc) == "&4":
                rank_plus_color = 'mc-dark_red'
            elif str(rpc) == "&5":
                rank_plus_color = 'mc-dark_purple'
            elif str(rpc) == "&6":
                rank_plus_color = 'mc-gold'
            elif str(rpc) == "&7":
                rank_plus_color = 'mc-gray'
            elif str(rpc) == "&8":
                rank_plus_color = 'mc-dark_gray'
            elif str(rpc) == "&9":
                rank_plus_color = 'mc-blue'
            elif str(rpc) == "&a":
                rank_plus_color = 'mc-green'
            elif str(rpc) == "&b":
                rank_plus_color = 'mc-aqua'
            elif str(rpc) == "&c":
                rank_plus_color = 'mc-red'
            elif str(rpc) == "&d":
                rank_plus_color = 'mc-light_purple'
            elif str(rpc) == "&e":
                rank_plus_color = 'mc-yellow'
            elif str(rpc) == "&f":
                rank_plus_color = 'mc-white'

            if 'SkyBlock' in str(player.get_stats()):
                profile_id = requests.get('https://api.slothpixel.me/api/skyblock/profile/' + name).json()['id']
                profile = requests.get('https://api.slothpixel.me/api/skyblock/profile/' + name + "/" + profile_id).json()
                profile_name = player.get_stats()['SkyBlock']['profiles'][profile_id]['cute_name']
                profile_attributes = profile['members'][uuid]['attributes']
                profile_skills = profile['members'][uuid]['skills']

                def human_format(num):
                    num = float('{:.3g}'.format(num))
                    magnitude = 0
                    while abs(num) >= 1000:
                        magnitude += 1
                        num /= 1000.0
                    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'),
                                         ['', 'K', 'M', 'B', 'T'][magnitude])

                if 'taming' in str(profile_skills):
                    skill_info_api_check = 'enabled'
                else:
                    skill_info_api_check = 'disabled'

            else:
                flash("Player has no SkyBlock profiles.")
                return home()

            return render_template('profile.html', username=name, network_rank=network_rank, uuid=uuid,
                                   network_linked_socialmedia_number=network_linked_socialmedia_number,
                                   TWITTER=TWITTER, TWITCH=TWITCH, YOUTUBE=YOUTUBE, INSTAGRAM=INSTAGRAM,
                                   DISCORD=DISCORD, HYPIXEL=HYPIXEL, is_online=is_online,
                                   rank_plus_color=rank_plus_color, is_online_gameType=is_online_gameType,
                                   last_logout_from_now=last_logout_from_now, last_login_from_now=last_login_from_now,
                                   human_format=human_format, skill_info_api_check=skill_info_api_check, profile=profile,
                                   profile_name=profile_name, profile_attributes=profile_attributes,
                                   profile_skills=profile_skills)

        except hypixel.PlayerNotFoundException:
            flash("The user has not played Hypixel.")
            return home()
    else:
        flash("No user with the name '" + raw_username + "' was found.")
        return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8080)
