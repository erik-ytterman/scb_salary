import requests
import json
import codecs
import re

request_string = """
{
  "query": [
    {
      "code": "Region",
      "selection": {
        "filter": "vs:RegionKommun07EjAggr",
        "values": [
          "0180"
        ]
      }
    },
    {
      "code": "Kon",
      "selection": {
        "filter": "item",
        "values": [
          "1",
          "2"
        ]
      }
    },
    {
      "code": "Alder",
      "selection": {
        "filter": "vs:ÅlderInk",
        "values": [
          "16",
          "17",
          "18",
          "19",
          "20",
          "21",
          "22",
          "23",
          "24",
          "25",
          "26",
          "27",
          "28",
          "29",
          "30",
          "31",
          "32",
          "33",
          "34",
          "35",
          "36",
          "37",
          "38",
          "39",
          "40",
          "41",
          "42",
          "43",
          "44",
          "45",
          "46",
          "47",
          "48",
          "49",
          "50",
          "51",
          "52",
          "53",
          "54",
          "55",
          "56",
          "57",
          "58",
          "59",
          "60",
          "61",
          "62",
          "63",
          "64",
          "65",
          "66",
          "67",
          "68",
          "69",
          "70",
          "71",
          "72",
          "73",
          "74",
          "75",
          "76",
          "77",
          "78",
          "79",
          "80",
          "81",
          "82",
          "83",
          "84",
          "85",
          "86",
          "87",
          "88",
          "89",
          "90",
          "91",
          "92",
          "93",
          "94",
          "95",
          "96",
          "97",
          "98",
          "99"
        ]
      }
    },
    {
      "code": "ContentsCode",
      "selection": {
        "filter": "item",
        "values": [
          "000001OR",
          "000001ON",
          "000001OQ"
        ]
      }
    },
    {
      "code": "Tid",
      "selection": {
        "filter": "item",
        "values": [
          "2015"
        ]
      }
    }
  ],
  "response": {
    "format": "json"
  }
}
"""

# Create generator for region tuples with correct string data
def parse_regions(source, debug=False, delimiter=','):
    # Prepare regex matchers for every field
    matchers = {
        1 : ('rid'  , re.compile('^[0-9]{4,4}$')         ),
        2 : ('name' , re.compile('^[\w\-åäöÅÄÖ\ ]{1,30}$') )
    }

    # Foe every line read from source
    for linenr, line in enumerate(source, 1):
        # Split line @delimiter
        kid, name = line.strip('\t\n\r').split(delimiter)
        values = (kid, name) 
        
        # Check for error in every field, logging errors
        errors = []
        for fieldnr, value in enumerate(values, 1):
            fieldname, matcher = matchers[fieldnr]
            if (matcher.match(value) == None): errors.append((fieldnr, fieldname, value))
                
        # Select actions
        selector = (len(errors) == 0, debug)
        if(selector == (True , False)) : yield(((kid,), (name,)))
        if(selector == (True , True )) : yield(((kid,), (name,)))
        if(selector == (False, False)) : pass
        if(selector == (False, True )) : print("Error(s) in line: " + str(linenr) + " : " + str(values) + " -> " + str(errors)) 

# Load salaries from SCB 
def get_salaries():
    json_data    = json.loads(request_string)
    api_endpoint = r'http://api.scb.se/OV0104/v1/doris/sv/ssd/START/HE/HE0110/HE0110A/NetInk02'

    json_text    = requests.post(url=api_endpoint, json=json_data)
    json_data    = json.loads(codecs.decode(json_text.content, 'utf-8-sig'))
    source       = json_data["data"]

    for datum in source:
        kid, gender, age, year = datum['key']
        average, median, count = datum['values']

        try:
            key    = (kid, int(gender), int(age), int(year))
            values = (float(average), float(median), int(count))
            yield(key, values)
        except ValueError:
            pass


