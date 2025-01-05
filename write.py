"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    with open(filename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(fieldnames)
        for r in results:
            
            row_to_write = (r.time_str,r.distance,r.velocity,r._designation,r.neo.name,r.neo.diameter,r.neo.hazardous)
            writer.writerow(row_to_write)
    outfile.close()

def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    #Write the results to a JSON file, following the specification in the instructions.
    #{
    #"datetime_utc": "2025-11-30 02:18",
    #"distance_au": 0.397647483265833,
    #"velocity_km_s": 3.72885069167641,
    #"neo": {
    #  "designation": "433",
    #  "name": "Eros",
    #  "diameter_km": 16.84,
    #  "potentially_hazardous": false
    #}
    f= open(filename, 'w')
    r_out = [approach.get_obj() for approach in results]
    json.dump(r_out,f,indent =2)
    f.close()