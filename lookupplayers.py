import collections
import requests
import argparse
import os


parser = argparse.ArgumentParser(description="Gets list of Santa Cruz players attending a specific event.")
parser.add_argument("-m", "--min", type=int, dest="min_tourneys", default=3, help="minimum number of tourneys required to be added to list")
parser.add_argument("-n", "--nocache", action="store_true", help="discard cache of Santa Cruz players")

args = parser.parse_args()


if not os.path.exists("key.txt"):
  open("key.txt", "a").close()
  print("You need a Start.GG API key to use this tool.")
  print("Go to Start.GG -> Developer Settings -> Create new token")
  print("Copy the code, then paste it into the local file key.txt")
  exit(1)

input_url = input("Enter tournament URL: ")

with open('key.txt', 'r') as file:
    api_key = file.read()

if args.nocache or not os.path.exists("players.cache"):
  tourney_names = [f"11th-hour-smash-{i}" for i in range(1, 28)]
  tourney_names[0] = "11th-hour-smash-the-return"
  tourney_names[7] = "11th-hour-smash-8-50-prize-pot-free-to-enter"

  #print(tourney_names)

  player_counts = collections.Counter()

  for name in tourney_names:
    players_query = f"""query EntrantsByTourney {{
      event(slug:"tournament/{name}/event/ultimate-singles") {{
        numEntrants
        entrants(query: {{perPage:64, page:1}}) {{
          pageInfo {{
            totalPages
          }}
          nodes {{
            name
          }}
        }}
      }}
    }}"""

    response = requests.post(url="https://api.start.gg/gql/alpha",
                json={"query": players_query},
                headers={"Authorization": "Bearer " + api_key})
    
    to_json = response.json()
    #print(to_json)
    if to_json["data"]["event"]:
      #print(to_json["data"]["event"]["entrants"]["nodes"])
      for d in to_json["data"]["event"]["entrants"]["nodes"]:
        player_counts[d["name"]] += 1
    
  print(player_counts)


  sc_players = {name for name in player_counts if player_counts[name] >= args.min_tourneys}
  print(sc_players)

  cache_file = open("players.cache", "w")
  cache_file.write("\n".join(sc_players))
else:
  sc_players = set()
  with open("players.cache") as cache_file:
    for line in cache_file:
      sc_players.add(line.rstrip())
  print(sc_players)