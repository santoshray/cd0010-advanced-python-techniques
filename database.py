"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches


        # TODO: What additional auxiliary data structures will be useful?
        # loop through all close approaches objects and create a dictionary.
        #  {
        #     "pdes1":[ca11,ca12 ..], 
        #     "pdes2":[ca21,ca211 ...]
        #     . . .
        #     "pdesN":[caN1,caN2, . . . ]
        #  } 
        pdes_ca_dict = {}
        neo_name_dict= {}

        for ca in approaches:
            if ca._designation not in pdes_ca_dict.keys():
                pdes_ca_dict[ca._designation] = []
            pdes_ca_dict[ca._designation].append(ca)
        
        for neo in neos:
            if neo.designation in pdes_ca_dict.keys():
                # Assign all the close approaches list to neo.approaches 
                neo.approaches = pdes_ca_dict[neo.designation]

                #For all the Close appraches for the neo associate the neo to each close approach
                for ca in neo.approaches:
                    ca.neo = neo 
            
            if neo.name != None :
                neo_name_dict[neo.name] = neo
    
        self.neo_ca_dict =   pdes_ca_dict
        self.neo_name_dict = neo_name_dict

        return  
    
    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        # TODO: Fetch an NEO by its primary designation.
        if designation in self.neo_ca_dict.keys():
            neo_by_designation = self.neo_ca_dict[designation][0].neo
        else:
            neo_by_designation =None 

        return neo_by_designation

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        # TODO: Fetch an NEO by its name.
        try:
            neo = self.neo_name_dict[name]
        except:
            neo =None
    
        return neo


    def query(self, filters=[]):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # TODO: Generate `CloseApproach` objects that match all of the filters.
        for approach in self._approaches:
            if check_filter_condition(approach,filters):
                yield approach
        
@staticmethod
def check_filter_condition(approach,filters):
    flag = True
    for f in filters:
        if  f(approach) == False:
            return False
    return flag

