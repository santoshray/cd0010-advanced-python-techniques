"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self,designation,name,diameter, hazardous, *approaches, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `designation`, `name`, `diameter`, and `hazardous`.
        # You should coerce these values to their appropriate data type and
        # handle any edge cases, such as a empty name being represented by `None`
        # and a missing diameter being represented by `float('nan')`.
        #print("designation={},name={},diameter={}, hazardous={}".format(designation,name,diameter, hazardous))
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = None

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return self.designation + self.name

    def __str__(self):
        """Return `str(self)`."""
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        #"NEO 433 (Eros) has a diameter of 16.840 km and is not potentially hazardous."
        isharzardous =""
        if self.hazardous == True:
            isharzardous = ""
        else:
            isharzardous = "not"
        return f"NEO {self.designation} ({self.name}) has a diameter of {self.diameter} km" \
               f" and is {isharzardous} potentially hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self,pdes,time,distance,velocity,neo=None, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        # Assign information from the arguments passed to the constructor
        # onto attributes named `_designation`, `time`, `distance`, and `velocity`.
        # You should coerce these values to their appropriate data type and handle any edge cases.
        # The `cd_to_datetime` function will be useful.
        #print("pdes={},time={},distance={},velocity={}".format(pdes,time,distance,velocity))

        self._designation = pdes
        self.time = cd_to_datetime(time)  # Use the cd_to_datetime function for this attribute.
        self.distance = float(distance)
        self.velocity = float(velocity)
        # Create an attribute for the referenced NEO, originally None.
        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        # Use this object's `.time` attribute and the `datetime_to_str` function to
        # build a formatted representation of the approach time.
        # Use self.designation and self.name to build a fullname for this object.
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        # NEO 1910-05-20 12:49, '1P (Halley)' approaches Earth at a distance of 0.15 au and a velocity of 70.56 km/s.
        # Use this object's attributes to return a human-readable string representation.
        # The project instructions include one possibility. Peek at the __repr__
        # method for examples of advanced string formatting.
        return f"On {self.time_str} ,' {self.neo.designation} {self.neo.name}' approaches Earth at a "  \
                f"distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def get_obj(self):
        """Return json formatted CloseApproach object."""
        obj = {}
        obj["datetime_utc"] = self.time_str
        obj["distance_au"] = self.distance
        obj["velocity_km_s"] = self.velocity
        obj["neo"] = {}

        obj["neo"]["designation"]=self.neo.designation
        if self.neo.name != None :
            obj["neo"]["name"]= self.neo.name 
        else:
            obj["neo"]["name"] = ""
            print(type(self.neo.diameter))
        if self.neo.diameter == float('nan'):
            obj["neo"]["diameter_km"]= ""
        else:
            obj["neo"]["diameter_km"]= self.neo.diameter

        obj["neo"]["potentially_hazardous"]= self.neo.hazardous

        return obj