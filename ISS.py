import discord
from discord.ext import commands , tasks
import json
import urllib.request
from geopy.geocoders import Nominatim
import config

TOKEN = config.TOKEN

bot = commands.Bot(command_prefix='/')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('---------------')
    print(bot.user.name)
    print('---------------')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the space"))

@bot.command()
async def info(ctx):
    async with ctx.typing():
        geolocator = Nominatim(user_agent="ISS_information")
        url_people = "http://api.open-notify.org/astros.json"
        url_pos = "http://api.open-notify.org/iss-now.json"
        data_people = urllib.request.urlopen(url_people)
        data_pos = urllib.request.urlopen(url_pos)
        resultat_people = json.loads(data_people.read())
        resultat_pos = json.loads(data_pos.read())

        number_people = resultat_people['number']
        people_in = resultat_people['people']

        pos_ISS = resultat_pos['iss_position']
        lat = str(pos_ISS['latitude'])
        lon = str(pos_ISS['longitude'])
        try:
            location = geolocator.reverse(f"{lat},{lon}")
            if location != None:
                address = location.raw['address']
                city = address.get('city', '')
                state = address.get('state', '')
                country = address.get('country', '')
        except:
            location = "error"
        f = open("data.txt", "w")
        f.write("")
        f.close()

        f = open("data.txt", "a")

        f.write("------- In the ISS -------\n")
        f.write(f"Number of people in the ISS: {number_people} \n\n")
        for p in people_in:
            f.write(f"{p['name']}\n")

        f.write('\n------- Location -------\n')

        if location != None:
            if city != "":
                f.write(f"City: {city}\n")
            if state != "":
                f.write(f"State: {state}\n")
            if country != "":
                f.write(f"Country: {country}\n")
        elif location == "error":
            f.write("|| GeoPy currently has a problem. ||")
        else:
            f.write("The ISS is above the ocean.\n")

        f.write(f"\nThe coordinate is: {lat}, {lon}\n")
        f.write(f"Url: https://www.latlong.net/c/?lat={lat}&long={lon}")
        f.close()

        f = open("data.txt", "r")
    await ctx.send(f.read())

bot.run(TOKEN)
