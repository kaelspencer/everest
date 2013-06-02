everest
=======

Everest is a REST API for EVE static data. To start with it only supports routes and jump counts.

Usage
-----
There are two API groups right now: `GET /route/` and `GET /jump/`

### Route
The route takes a source and destination and gives the shortest path between the two places. Route can take system names, system IDs, or any combination of the two.

    GET /route/Jita/Perimiter/

    {
      "count": 1,
      "route": [
      {
        "id": 30000142,
        "name": "Jita"
      },
      {
        "id": 30000144,
        "name": "Perimeter"
      }]
    }

Route can also take station names or IDs via `GET /route/station/<source>/<destination>/`

### Jump Count
In case you don't want the entire route and just want the jump count, `GET /jump/` is for you. Just like route, there is a station mode `GET /jump/station/`. Again, it can take any combination of names and IDs.

    GET /jump/Jita/Rens/

    {
      "jumps": 15
    }

### Batched Jump Count
If you need more than a few jump counts you should make use of the batched API. `POST /jump/batch/` accepts json data with one source and multiple destinations. Each location can be a system name or ID, or a station name or ID.

    POST /jump/batch/

    {
      "source": "Jita",
      "destinations": [
        "Rens",
        "Irjunen"
      ]
    }

The response to the request looks like this:

    {
      "source": "Jita",
      "destinations": [{
        "jumps": 15,
        "destination": "Rens"
      }, {
        "jumps": 6,
        "destination": "Irjunen"
      }]
    }

Configuration
-------------
To run this locally you'll need everyting in `requirements.txt`. You can either edit `config.py` directory or add a configuration file to your environment. For local development, I have a file called `debug.cfb`, and everest looks for that via EVEREST_CONFIG (so, `export EVEREST_CONFIG=debug.cfg`).

Unit Tests
----------
There are unit tests. They do, however, require the database to run. Run them via `python everest_test.py`.
