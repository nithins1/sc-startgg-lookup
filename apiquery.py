import requests

def sc_query(tourney_name, key):
    query = f"""query EntrantsByTourney {{
      event(slug:"tournament/{tourney_name}/event/ultimate-singles") {{
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

    return requests.post(url="https://api.start.gg/gql/alpha",
                    json={"query": query},
                    headers={"Authorization": "Bearer " + key})

def tourney_query(event_slug, api_key):
    query = f"""query EntrantsByTourney {{
      event(slug:"{event_slug}") {{
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