# Overview

There are three API groups right now: `/route/`, `/jump/`, and `/industry/`.

## Route
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

### Security Avoidance
Route can also be configured to avoid certain systems with a given sec status. For instance, to avoid all null and high sec systems, append `/highonly/` to the request. To avoid high sec, append `/nohigh/`. This will result in routes that contain no entries of the given security status. If the start or end points fall in the avoidance list, everest will return an empty set.

## Jump Count
In case you don't want the entire route and just want the jump count, `GET /jump/` is for you. Just like route, there is a station mode `GET /jump/station/`. Again, it can take any combination of names and IDs. It also support security avoidance like the route API and is used in the same manner.

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

#### Security Avoidance
Batched jump counts also supports security avoidance. It has slightly different nomenclature than the GET requests. A top level key `avoidance` supports three options: `high`, `highonly`, and `none`. This key is optional and defaults to none. A value `high` is equivalent to `nohigh` in the GET requests where all of high sec is avoided. `highonly` is the same as GET and will return jump counts that stay in high sec. `none` disables the avoidance list.

## Industry
The industry API is used to fetch T2 blueprint details. There are two modes for retrieving these: getting all blueprints by category (or just all of them) and then pulling information for a specific item.

### Result Set
A lot of data comes back as a result.
  * __categoryName__: The category the item belongs to. This is from invCategories.
  * __chance__: Base chance for invention.
  * __datacores__: A list of datacores required to invent this item. This is an array of the following objects:
    * __quantity__: Number required of this type.
    * __typeID__: The typeID of the datacore.
    * __typeName__: The name of the datacore.
  * __decryptor_category__: The category ID of the decryptor. Apologies for the naming inconsistency. It will be one of the following:
    * __728__: Occult (Amarr)
    * __729__: Cryptic (Minmatar)
    * __730__: Incognito (Gallente)
    * __731__: Esoteric (Caldari)
  * __maxProductionLimit__: The max production limit for the T1 BPO. This informs how many items you'll get as a result of invention.
  * __perfectMaterials__: This is the material list for an ME 0 T2 BPC. The list is coalesced so there is no split from regular materials and extra materials. A flag indicates where waste needs to be applied.
    * __dmg__: The damage factor as a percentage.
    * __name__: The name.
    * __quanity__: How many you need.
    * __typeID__: Type ID of the material.
    * __wasteME__: Whether material efficiency waste needs to be applied to this material. Since types are coalesced, this will be true for items in extra materials that are also in normal materials, but false otherwise.
    * __wastePE__: Whether production efficiency waste applies to this material. Note: this skill is now called "Material Efficiency" which is confusing because there is a separate material efficiency/material level (ME) for the blueprint itself.
  * __productionTime__: Time in seconds for this PE 0 blueprint.
  * __productivityModifier__: Used in the total production time calculation.
  * __t1bpo__: Details about the T1 BPO used as a source for invention.
    * __blueprintTypeID__: Type ID of the BPO.
    * __maxProductionLimit__: The max production limit of this blueprint.
    * __researchCopyTime__: Time in seconds. This is a strange number. It is the copy time for half of the maxProductionLimit. The copy time for a max run blueprint is twice this value.
    * __typeID__: Type ID of the item this blueprint produces.
    * __typeName__: The name of the item this BPO produces.
  * __typeID__: Type ID of the T2 item.
  * __typeName__: Type name of the T2 item.
  * __wasteFactor__: Waste factor of the T2 BPC.

### Calling the API.
There are two ways to get a list of inventable items.

#### GET
The first one is retrieving a single category (or all) `/industry/<categoryid>/`. This will return a list of all inventable items in that category. `/industry/<categoryid>/nogrigs/` will return all items in that category that are not rigs. This is only useful for modules and all; the other options won't return rigs anyway. These are the category options:
  * __0__: All Inventable Items
  * __6__: Ships
  * __7__: Modules
  * __8__: Charges
  * __18__: Drones
  * __22__: Deployable

This URL can be modified to return type names as well. `/names/` can be mixed and matched with `/norigs/`. Possibilities:
  * `/industry/<categoryid>/`
  * `/industry/<categoryid>/names/`
  * `/industry/<categoryid>/norigs/`
  * `/industry/<categoryid>/names/norigs/`
  * `/industry/<categoryid>/norigs/names/`

#### POST
The second option for calling the API allows you to retrieve items from multiple categories instead of single or all. `POST /industry/` with a valid request object. The request object supports three parameters:
  * __categories__: Required. This is an array of ints. Each value must be in (0, 6, 7, 8, 18, 22). Passing in all (0) trumps other categories.
  * __rigs__: Optional. A boolean that indicates whether rigs should be included in the result set.
  * __names__: Optional. A boolean that indicates whether the results should have names.

Here is a sample.

    POST /industry/

    {
      "categories": [7, 18],
      "rigs": false,
      "names": true
    }

See the detail section for a sample result.

### Item Detail
To get detailed information about a specific item, pass in the T2 item id to the `/industry/detail/<itemid>/`. This can also have names: `/industry/detail/<itemid>/names/`. Here is a sample. Note that all `/industry/` APIs return a list with detail returning a single element list.

    GET /industry/detail/12735/names/

    {
      "items": {
        "12735": {
          "categoryName": "Ship",
          "chance": 0.25,
          "datacores": [
            {
              "quantity": 8,
              "typeID": 20172,
              "typeName": "Datacore - Minmatar Starship Engineering"
            },
            {
              "quantity": 8,
              "typeID": 20424,
              "typeName": "Datacore - Mechanical Engineering"
            }
          ],
          "decryptor_category": 729,
          "maxProductionLimit": 10,
          "perfectMaterials": [
            {
              "dmg": 1.0,
              "name": "Tritanium",
              "quantity": 79620.0,
              "typeID": 34,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Pyerite",
              "quantity": 21970.0,
              "typeID": 35,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Isogen",
              "quantity": 1593.0,
              "typeID": 37,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Nocxium",
              "quantity": 258.0,
              "typeID": 38,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Megacyte",
              "quantity": 26.0,
              "typeID": 40,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Construction Blocks",
              "quantity": 75.0,
              "typeID": 3828,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Morphite",
              "quantity": 40.0,
              "typeID": 11399,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Plasma Thruster",
              "quantity": 75.0,
              "typeID": 11530,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Ladar Sensor Cluster",
              "quantity": 60.0,
              "typeID": 11536,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Nanomechanical Microprocessor",
              "quantity": 800.0,
              "typeID": 11538,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Fernite Carbide Composite Armor Plate",
              "quantity": 2000.0,
              "typeID": 11542,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Nuclear Reactor Unit",
              "quantity": 25.0,
              "typeID": 11548,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Electrolytic Capacitor Unit",
              "quantity": 150.0,
              "typeID": 11551,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Deflection Shield Emitter",
              "quantity": 100.0,
              "typeID": 11555,
              "wasteME": true,
              "wastePE": true
            },
            {
              "dmg": 1.0,
              "name": "Wreathe",
              "quantity": 1.0,
              "typeID": 653,
              "wasteME": false,
              "wastePE": false
            },
            {
              "dmg": 0.95,
              "name": "R.A.M.- Starship Tech",
              "quantity": 7.0,
              "typeID": 11478,
              "wasteME": false,
              "wastePE": false
            }
          ],
          "productionTime": 80000,
          "productivityModifier": 16000,
          "t1bpo": {
            "blueprintTypeID": 988,
            "maxProductionLimit": 15,
            "researchCopyTime": 240000,
            "typeID": 653,
            "typeName": "Wreathe"
          },
          "typeID": 12735,
          "typeName": "Prowler",
          "wasteFactor": 10
        }
      }
    }
