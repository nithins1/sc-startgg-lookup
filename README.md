# Santa Cruz Start.GG Player Lookup

### What it does:
* Paste in a start.gg event link
* The list of Santa Cruz players attending that event will be listed

### Requirements:
* start.gg API key
  * Go to start.gg -> Developer Settings -> Create new token
  * Paste token into local file `key.txt`
* Python
  * Install Python 3
  * Install dependencies (`pip install -r requirements.txt`)

### Running the program:
Usage:
```
python lookupplayers.py [-h] [-m MIN_TOURNEYS] [-n]

optional arguments:
  -h, --help                                    show this help message and exit
  -m MIN_TOURNEYS, --min MIN_TOURNEYS           minimum number of tourneys required to be added to list
  -n, --nocache                                 discard cache of Santa Cruz players

Be sure to enter a link to an event on start.gg, such as start.gg/tournament/XXXXX/event/ultimate-singles, not just start.gg/tournament/XXXXX
```

### How it works:
* API Queries
  * Make GraphQL API requests to Start.GG API to get a list of players at each Santa Cruz tournament
  * Cross reference those lists, creating attendance counts for each player
* Santa Cruz players list
  * Defined as players who entered at least `m` tournaments in Santa Cruz
  * Cached in `players.cache` so future searches are faster
  * `m` can be specified on the command line to make this list more or less strict (use `-m` flag)
  * Force cache discard with `-n` flag