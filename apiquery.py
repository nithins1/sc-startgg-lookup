def sc_query(tourney_name):
    return f"""query EntrantsByTourney {{
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

def tourney_query(event_slug):
    return