from cmath import inf
import requests

def sc_query(tourney_name, key):
    query = \
    f"""query EntrantsByTourney {{
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

def tourney_query(event_slug, key):
    page_num = 1
    num_pages = inf
    while True:
        if page_num > num_pages:
            return None
        query = f"""query EntrantsByTourney {{
                        event(slug:"{event_slug}") {{
                            numEntrants
                            entrants(query: {{perPage:50, page:{page_num}}}) {{
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
                    json={"query": query},
                    headers={"Authorization": "Bearer " + key})
        to_json = response.json()["data"]["event"]["entrants"]
        num_pages = to_json["pageInfo"]["totalPages"]
        yield to_json["nodes"]
        page_num += 1