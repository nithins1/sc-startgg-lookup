import requests
import argparse

parser = argparse.ArgumentParser(description="Gets list of Santa Cruz players attending a specific event.")
parser.add_argument("-t", "--tourneys", type=int, metavar="tourneys", default=44, help="number of previous Santa Cruz tourneys to consider")

args = parser.parse_args()

with open('key.txt', 'r') as file:
    api_key = file.read()

sc_events = [f"11th-hour-smash"]


tourneys_query = """query SCTournaments($perPage: Int, $coordinates: String!, $radius: String!) {
  tournaments(query: {
    perPage: $perPage
    filter: {
      location: {
        distanceFrom: $coordinates,
        distance: $radius
      }
    }
  }) {
    nodes {
      id
      name
      city
    }
  }
}"""

tourneys_variables = f"""{{
  "perPage": {args.tourneys},
  "coordinates": "36.9741,-122.0308",
  "radius": "10mi"
}}"""

t = requests.post(url="https://api.start.gg/gql/alpha",
              json={"query": tourneys_query, "variables": tourneys_variables},
              headers={"Authorization": "Bearer " + api_key})

tourneys = t.json()["data"]["tournaments"]["nodes"]
tourney_ids = [t["id"] for t in tourneys]
print(tourney_ids)
