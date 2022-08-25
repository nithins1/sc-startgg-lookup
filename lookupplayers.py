import collections
import argparse
import os
import re
import apiquery


parser = argparse.ArgumentParser(description="Gets list of Santa Cruz players attending a specific event.",
                                 epilog="Be sure to enter a link to an event on start.gg, such as "
                                 "start.gg/tournament/XXXXX/event/ultimate-singles, "
                                 "not just start.gg/tournament/XXXXX")
parser.add_argument("-m", "--min", type=int, dest="min_tourneys", default=3, help="minimum number of tourneys required to be added to list")
parser.add_argument("-n", "--nocache", action="store_true", help="discard cache of Santa Cruz players")

args = parser.parse_args()


if not os.path.exists("key.txt"):
    open("key.txt", "a").close() # Create empty file
    print("You need a Start.GG API key to use this tool.")
    print("Go to Start.GG -> Developer Settings -> Create new token")
    print("Copy the code, then paste it into the local file `key.txt`")
    exit(1)

input_url = ""
pattern = re.compile("(start|smash)\.gg\/tournament\/[\w-]+\/event/[\w-]+")
while not input_url:
    input_url = pattern.search(input("Enter event URL: "))

input_url = input_url[0] # Get full regex match from Match object

with open('key.txt', 'r') as file:
    api_key = file.read()

if args.nocache or not os.path.exists("players.cache"):
    tourney_names = [f"11th-hour-smash-{i}" for i in range(1, 28)]
    # Add irregular tourney names
    tourney_names[0] = "11th-hour-smash-the-return"
    tourney_names[7] = "11th-hour-smash-8-50-prize-pot-free-to-enter"

    player_counts = collections.Counter()

    for name in tourney_names:
        response = apiquery.sc_query(name, api_key)
        if response.status_code == 400:
            print("Your API key was invalid. Try generating a new one.")
            exit(1)
        elif response.status_code == 429:
            pass #TODO
        elif response.status_code > 400:
            print("Error occured while making start.gg API requests.")
            exit(1)

        to_json = response.json()
        if to_json["data"]["event"]:
            for d in to_json["data"]["event"]["entrants"]["nodes"]:
                player_counts[d["name"]] += 1

    sc_players = {name for name in player_counts if player_counts[name] >= args.min_tourneys}

    cache_file = open("players.cache", "w")
    cache_file.write("\n".join(sc_players))
else:
    sc_players = set()
    with open("players.cache") as cache_file:
        for line in cache_file:
            sc_players.add(line.rstrip())


input_slug = input_url[len("start.gg/"):]
output_list = []
for page in apiquery.tourney_query(input_slug, api_key):
    for node in page:
        if node["name"] in sc_players:
            output_list.append(node["name"])

print("Santa Cruz players in attendance:")
print("\n".join(output_list))