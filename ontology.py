from owlready2 import *


class OntologyManager:

    def __init__(self, path_to_ontology="./data/flight_information_ontology.owl"):
        self.path_to_ontology = path_to_ontology
        self.ontology = self.load_ontology()
        # set to correct base iri to be able to correctly access ontology classes via ontology attribute
        self.ontology.base_iri = "flight_information_ontology.owl#"

    def load_ontology(self):
        try:
            onto = get_ontology("./data/flight_information_ontology.owl").load()
            return onto

        except (Exception, IOError) as e:
            raise e

    def get_valid_origin_airports(self):
        ontology_search_results = self.ontology.search(type=self.ontology.Flughafen, ist_gültiger_startflughafen_für_flugreise=True)

        return  OntologyManager._as_dict(ontology_search_results)

    def get_invalid_origin_airports(self):
        ontology_search_results = ontology_search_results = self.ontology.search(ist_gültiger_startflughafen_für_flugreise=False)

        return OntologyManager._as_dict(ontology_search_results)

    def get_valid_destination_airports(self):
        ontology_search_results = self.ontology.search(type= self.ontology.Flughafen, ist_gültiger_zielflughafen_für_flugreise=True)

        return OntologyManager._as_dict(ontology_search_results)

    def get_invalid_destination_airports(self):
        ontology_search_results = self.ontology.search(ist_gültiger_zielflughafen_für_flugreise=False)

        return OntologyManager._as_dict(ontology_search_results)

    @staticmethod
    def _as_dict(ontology_search_results):
        out = dict()

        names = list(map(lambda x: x.name,(ontology_search_results)))
        synonyms = list(map(lambda x: x.hat_synonyme,(ontology_search_results)))

        for k, v in zip(names, synonyms):
            out[k] = v

        return out


if __name__ == "__main__":
    from pprint import pprint

    onto_manager = OntologyManager()

    print("##############################################################")
    print("################# valid origin airports #################")
    print("##############################################################")
    pprint(onto_manager.get_valid_origin_airports())
    print()

    print("##############################################################")
    print("################# invalid origin airports #################")
    print("##############################################################")
    pprint(onto_manager.get_invalid_origin_airports())
    print()

    print("##############################################################")
    print("################# valid destination airports #################")
    print("##############################################################")
    pprint(onto_manager.get_valid_destination_airports())
    print()

    print("##############################################################")
    print("################# invalid destination airports #################")
    print("##############################################################")
    pprint(onto_manager.get_invalid_destination_airports())
    print()

