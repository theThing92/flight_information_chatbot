
class OntologyManager:

    def __init__(self, path_to_ontology="./data/flight_information_ontology.owl"):
        self.path_to_ontology = path_to_ontology
        self.ontology = self.load_ontology()
        # set to correct base iri to be able to correctly access ontology classes via ontology attribute
        self.ontology.base_iri = "flight_information_ontology.owl#"
        self.dictionary = self.as_dict()

    def load_ontology(self):
        try:
            onto = get_ontology("./data/flight_information_ontology.owl").load()
            return onto

        except (Exception, IOError) as e:
            raise e

    def as_dict(self, ontology):

        out = dict()

        list_flugreisen = ontology.search(type=onto.Flugreise)

        for f in list_flugreisen:
            name = f.name
            props = f.get_properties()

            for p in props:
                name = p.name

        pass


    def get_valid_origin_airports(self):
        pass

    def get_valid_destination_airports(self):
        pass




if __name__ == "__main__":
    from owlready2 import *

    onto = get_ontology("./data/flight_information_ontology.owl").load()
    # set to correct base iri to be able to correctly access ontology classes via ontology attribute
    onto.base_iri = "flight_information_ontology.owl#"
