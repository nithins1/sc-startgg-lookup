import requests


with open('key.txt', 'r') as file:
    api_key = file.read()

query = """query EventEntrants($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    entrants(query: {
      page: $page
      perPage: $perPage
    }) {
      pageInfo {
        total
        totalPages
      }
      nodes {
        id
        participants {
          id
          gamerTag
        }
      }
    }
  }
}
"""

variables = """{
  "eventId": 121970,
  "page": 1,
  "perPage": 2
}"""

x = requests.post(url="https://api.start.gg/gql/alpha",
              json={"query": query, "variables": variables},
              headers={"Authorization": "Bearer " + api_key})

print(x.text)