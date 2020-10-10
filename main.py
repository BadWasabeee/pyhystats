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
            '''
            All essential variables to make the other code run properly
            '''
            api = hypixelapi.HypixelAPI('e6a09aab-befc-4f53-b668-7fd3fe2a585d')
            player = api.get_player(uuid)
            name = MojangAPI.get_profile(uuid).name
            network_rank = hypixel.Player(raw_username).getRank()['rank']
            network_level = player.get_level()
            network_exp = int(player.get_exp())
            '''
            Social media of player.
            '''
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

            '''
            Beautifying the players location and more... Adding more soon.
            Have to run this 'if' statement to not get errors.
            '''
            is_online = player.get_status()['online']
            if str(is_online) == "True":
                last_logout_from_now_formatted = 'Online'
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
                    is_online_gameType = is_online_gameType
                    is_online_mode = is_online_mode
            elif str(requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()[
                         'last_logout']).lower() == "none":
                player_api_settings = "disabled"
                last_logout_from_now_formatted = "disabled"
                is_online_gameType = "disabled"
                is_online_mode = "disabled"
            else:
                last_logout = requests.get('https://api.slothpixel.me/api/players/' + raw_username).json()[
                    'last_logout']
                last_logout = datetime.datetime.fromtimestamp(requests.get('https://api.slothpixel.me/api/players/' +
                                                                           raw_username).json()[
                                                                  'last_logout'] // 1000.0)
                last_logout_from_now = datetime.datetime.now() - last_logout
                last_logout_from_now_for = divmod(last_logout_from_now.total_seconds(), 60)
                last_logout_from_now_formatted = (str(int(round(last_logout_from_now_for[0], 1))) + " minutes " +
                                                  str(int(round(last_logout_from_now_for[1], 0))) + " seconds ago")

            '''
            Just identifying variables for html color
            '''
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

            '''
            Making sure for people who have MVP+ & higher get their correct plus color casted to them.
            '''
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

            '''
            Setting up for choosing different profiles.
            '''
            if 'SkyBlock' in str(player.get_stats()):

                profiles = player.get_stats()['SkyBlock']['profiles']
                x = 0
                profile_id = []
                cute_name = []
                for profile in profiles:
                    x = x + 1
                    profile_id.append(str(profile))
                    cute_name.append(str(profiles[profile]['cute_name']))
                # print(profile_id[1], cute_name[1])
                '''
                Grabbing variables
                '''
                last_played_profile = requests.get('https://api.slothpixel.me/api/skyblock/profile/' + name).json()
                last_played_profile_id = requests.get('https://api.slothpixel.me/api/skyblock/profile/' + name).json()[
                    'id']
                last_played_profile_name = profiles[last_played_profile_id]['cute_name']
                last_played_profile_stats = last_played_profile['members'][uuid]['attributes']
                last_played_profile_stats_health = last_played_profile_stats['health']
                last_played_profile_stats_defense = last_played_profile_stats['defense']
                last_played_profile_stats_strength = last_played_profile_stats['strength']
                last_played_profile_stats_speed = last_played_profile_stats['speed']
                last_played_profile_stats_crit_chance = last_played_profile_stats['crit_chance']
                last_played_profile_stats_crit_damage = last_played_profile_stats['crit_damage']
                last_played_profile_stats_bonus_attack_speed = last_played_profile_stats['bonus_attack_speed']
                last_played_profile_stats_intelligence = last_played_profile_stats['intelligence']
                last_played_profile_stats_sea_creature_chance = last_played_profile_stats['sea_creature_chance']
                last_played_profile_stats_magic_find = last_played_profile_stats['magic_find']
                last_played_profile_stats_pet_luck = last_played_profile_stats['pet_luck']

                '''
                Rendering html template
                '''
                print(player.get_stats()['SkyBlock'])
            else:
                flash("Player has no SkyBlock profiles.")
                return home()

            return render_template('profile.html', username=name, network_rank=network_rank, uuid=uuid,
                                   network_level=network_level, network_exp=network_exp,
                                   network_linked_socialmedia_number=network_linked_socialmedia_number,
                                   TWITTER=TWITTER, TWITCH=TWITCH, YOUTUBE=YOUTUBE, INSTAGRAM=INSTAGRAM,
                                   DISCORD=DISCORD, HYPIXEL=HYPIXEL, is_online=is_online,
                                   rank_plus_color=rank_plus_color, is_online_gameType=is_online_gameType,
                                   is_online_mode=is_online_mode, last_played_profile_name=last_played_profile_name,
                                   last_played_profile_stats_health=last_played_profile_stats_health,
                                   last_played_profile_stats_strength=last_played_profile_stats_strength,
                                   last_played_profile_stats_speed=last_played_profile_stats_speed,
                                   last_played_profile_stats_crit_chance=last_played_profile_stats_crit_chance,
                                   last_played_profile_stats_crit_damage=last_played_profile_stats_crit_damage,
                                   last_played_profile_stats_bonus_attack_speed=last_played_profile_stats_bonus_attack_speed,
                                   last_played_profile_stats_intelligence=last_played_profile_stats_intelligence,
                                   last_played_profile_stats_sea_creature_chance=last_played_profile_stats_sea_creature_chance,
                                   last_played_profile_stats_magic_find=last_played_profile_stats_magic_find,
                                   last_played_profile_stats_pet_luck=last_played_profile_stats_pet_luck,
                                   last_played_profile_stats_defense=last_played_profile_stats_defense,
                                   last_logout_from_now_formatted=last_logout_from_now_formatted)

        except hypixel.PlayerNotFoundException:
            '''
            Catching if a player has not joined the server.
            Returning them to the home page if so...
            '''
            flash("The user has not played Hypixel.")
            return home()
    else:
        '''
        Catching if a player name is not authentic.
        Using MojangAPI to see if the uuid exists
        '''
        flash("No user with the name '" + raw_username + "' was found.")
        return home()


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, port=8080)
