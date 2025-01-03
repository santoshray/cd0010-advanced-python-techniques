"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neo_list = []
    f = open(neo_csv_path ,'r')
    reader = csv.DictReader(f)
    for row in reader:
        pdes = row['pdes']
        name = row['name']
        if name == "":
            name = None
        if (row['diameter']==""):
            diameter = float("nan")
        else:
            diameter = float(row['diameter'])
        hazardous = row['pha']
        if (hazardous == 'Y' ):
            b_hazardous = True
        else:
            b_hazardous = False

        neo = NearEarthObject(pdes,name,diameter,b_hazardous)
        neo_list.append(neo)
    return (neo_list)


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    # TODO: Load close approach data from the given JSON file.
    f=open(cad_json_path,"r")
    data = json.load(f)
    cad_list = data["data"]
    close_approach_list = []
    for cad in cad_list:
        cd_time = cad[3]
        pdes = cad[0]
        distance = cad[4]
        velocity = cad[7]
        ca = CloseApproach(pdes,cd_time,distance,velocity,neo=None)    
        close_approach_list.append(ca)

    return (close_approach_list)
