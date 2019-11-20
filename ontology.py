"""
TODO: add doc
"""
import textgen
from owlready2 import *


class OntologyManager:
    """
    TODO: add doc
    """

    def __init__(self, path_to_ontology="./data/flight_information_ontology.owl"):
        self.path_to_ontology = path_to_ontology
        self.ontology = self.load_ontology()
        # set to correct base iri to be able to correctly access ontology classes via ontology attribute
        self.ontology.base_iri = "flight_information_ontology.owl#"

    def __repr__(self):
        return f"OntologyManger @{id(self)}"

    def load_ontology(self):
        """
        TODO: add doc
        """
        try:
            onto = get_ontology("./data/flight_information_ontology.owl").load()
            return onto

        except (Exception, IOError) as e:
            raise e

    #############################################
    ########### origin & destination  ###########
    #############################################
    def get_valid_origin_airport(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Flughafen, ist_gültiger_startflughafen_für_flugreise=True)

        return ontology_search_results

    def get_invalid_origin_airport(self):
        ontology_search_results = self.ontology.search(type=self.ontology.Flughafen, ist_gültiger_startflughafen_für_flugreise=False)

        return ontology_search_results

    def get_valid_destination_airport(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Flughafen, ist_gültiger_zielflughafen_für_flugreise=True)

        return ontology_search_results

    def get_invalid_destination_airport(self):
        ontology_search_results = self.ontology.search(type=self.ontology.Flughafen, ist_gültiger_zielflughafen_für_flugreise=False)

        return ontology_search_results

    def get_valid_origin_city(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Stadt)

        out = list()
        for o in ontology_search_results:
            try:
                if o.ist_startort_von.name == "Flugreise1":
                    out.append(o)

            except Exception as e:
                pass

        return out

    def get_invalid_origin_city(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Stadt)

        out=list()
        for o in ontology_search_results:
            try:
                if o.ist_zielort_von.name in ["Flugreise1","Flugreise2"]:
                    out.append(o)

            except Exception as e:
                pass

        return out

    def get_valid_origin_state_germany(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Bundesland, iri="flight_information_ontology.owl#Nord-Rhein-Westphalen")

        return ontology_search_results

    def get_invalid_origin_state_germany(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Bundesland, iri="^(flight_information_ontology.owl#Nord-Rhein-Westphalen)")

        return ontology_search_results


    def get_valid_origin_state_america(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Bundesstaat, iri="^(flight_information_ontology.owl#New York)")

        return ontology_search_results

    def get_invalid_origin_state_america(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Bundesstaat, iri="flight_information_ontology.owl#New York")

        return ontology_search_results


    def get_valid_origin_sar(self):
        """
        TODO: add doc
        :return: list
        """
        # empty list
        ontology_search_results = self.ontology.search(type=self.ontology.Sonderverwaltungszone, iri="^(flight_information_ontology.owl#Hongkong)")

        return ontology_search_results

    def get_invalid_origin_sar(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Sonderverwaltungszone, iri="flight_information_ontology.owl#Hongkong")

        return ontology_search_results

    def get_valid_origin_country(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Land, iri="flight_information_ontology.owl#Deutschland")

        return ontology_search_results

    def get_invalid_origin_country(self):
        """
        TODO: add doc
        :return: list
        """
        ontology_search_results = self.ontology.search(type=self.ontology.Land, iri="flight_information_ontology.owl#China")
        ontology_search_results.extend(self.ontology.search(type=self.ontology.Land, iri="flight_information_ontology.owl#Amerika"))

        return ontology_search_results


    def get_valid_origin_sight(self):
        ontology_search_results = self.ontology.search(type=self.ontology.Sehenswürdigkeit, ist_sehenswürdigkeit_von_stadt=self.ontology.Düsseldorf)

        return ontology_search_results

    def get_invalid_origin_sight(self):
        ontology_search_results = self.ontology.search(type=self.ontology.Sehenswürdigkeit, ist_sehenswürdigkeit_von_stadt=self.ontology.Hongkong)
        ontology_search_results.extend(self.ontology.search(type=self.ontology.Sehenswürdigkeit, ist_sehenswürdigkeit_von_stadt="*New York"))

        return ontology_search_results

    def query_ontology(self, query, context):
        """
        TODO: add doc
        :param entity_name: str
        :param context: str
        :return: str
        """
        # valid & invalid origin and destination airports
        origin_flughafen_valid = self.get_valid_origin_airport()
        origin_flughafen_invalid = self.get_invalid_origin_airport()
        destination_flughafen_valid = self.get_valid_destination_airport()
        destination_flughafen_invalid = self.get_invalid_destination_airport()

        # valid & invalid origin and destination country
        origin_land_valid = self.get_valid_origin_country()
        origin_land_invalid = self.get_invalid_origin_country()
        destination_land_valid = self.get_invalid_origin_country()
        destination_land_invalid = self.get_valid_origin_country()

        # valid & invalid origin and destination state germany
        origin_bundesland_valid = self.get_valid_origin_state_germany()
        origin_bundesland_invalid = self.get_invalid_origin_state_germany()
        destination_bundesland_valid = self.get_invalid_origin_state_germany()
        destination_origin_bundesland_invalid = self.get_valid_origin_state_germany()

        # valid & invalid origin and destination state america
        origin_bundesstaat_valid = self.get_valid_origin_state_america()
        origin_bundesstaat_invalid = self.get_invalid_origin_state_america()
        destination_bundesstaat_valid = self.get_invalid_origin_state_america()
        destination_bundesstaat_invalid = self.get_valid_origin_state_america()

        # valid & invalid origin and destination sar
        origin_svz_valid = self.get_valid_origin_sar()
        origin_svz_invalid = self.get_invalid_origin_sar()
        destination_svz_valid = self.get_invalid_origin_sar()
        destination_svz_invalid = self.get_valid_origin_sar()

        # valid & invalid origin and destination city
        origin_stadt_valid =  self.get_valid_origin_city()
        origin_stadt_invalid = self.get_invalid_origin_city()
        destination_stadt_valid = self.get_invalid_origin_city()
        destination_stadt_invalid = self.get_valid_origin_city()

        # valid & invalid origin and destination sight
        origin_sehenswürdigkeit_valid = self.get_valid_origin_sight()
        origin_sehenswürdigkeit_invalid = self.get_invalid_origin_sight()
        destination_sehenswürdigkeit_valid = self.get_invalid_origin_sight()
        destination_sehenswürdigkeit_invalid = self.get_valid_origin_sight()

        if context == "origin":
            # valid flughafen
            if OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_flughafen_valid)):
                return textgen.origin_flughafen_valid.format(query)

            # valid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_stadt_valid)):
                flughafen = origin_flughafen_valid[0].name

                return textgen.origin_stadt_valid.format(query, query, flughafen)

            # valid land
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_land_valid)):
                airport = origin_flughafen_valid[0].name

                return textgen.origin_land_valid.format(query, query, airport)

            # valid bundesland
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_bundesland_valid)):
                airport = origin_flughafen_valid[0].name

                return textgen.origin_bundesland_valid.format(query, query, airport)

            # valid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_sehenswürdigkeit_valid)):
                airport = origin_flughafen_valid[0].name

                return textgen.origin_sehenswürdigkeiten_valid.format(query, query, airport)

            # invalid flughafen
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_flughafen_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_flughafen_invalid.format(query, city, country, state, airport)

            # invalid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_stadt_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_stadt_invalid.format(query, city, country, state, airport)

            # invalid bundesland
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_bundesland_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_bundesland_invalid.format(query, city, country, state, airport)

            # invalid bundesstaat
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_bundesstaat_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_bundesstaat_invalid.format(query, city, country, state, airport)

            # invalid svz
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_svz_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_svz_invalid.format(query, city, country, state, airport)

            # invalid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_sehenswürdigkeit_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_sehenswürdigkeiten_invalid.format(query, city, country, state, airport)

            else:
                return textgen.unknown

        elif context == "destination":
            # valid flughafen
            if OntologyManager.__get_exact_match(query, OntologyManager._as_list(destination_flughafen_valid)):
                return textgen.destination_flughafen_valid.format(query)

            # valid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(destination_stadt_valid)):
                ## TODO: add disambiguation for China + USA
                flughafen = destination_flughafen_valid[0].name

                return textgen.origin_stadt_valid.format(query, query, flughafen)

            # valid land
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(destination_land_valid)):
                ## TODO: add disambiguation for China + USA
                airport = destination_flughafen_valid[0].name

                return textgen.destination_land_valid.format(query, query, airport)

            # valid bundesstaat
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(destination_bundesstaat_valid)):
                ## TODO: add disambiguation for China + USA
                airport = destination_flughafen_valid[0].name

                return textgen.destination_bundesstaat_valid.format(query, query, airport)

            # valid svz
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(destination_svz_valid)):
                ## TODO: add disambiguation for China + USA
                airport = origin_flughafen_valid[0].name

                return textgen.destination_svz_valid.format(query, query, airport)

            # valid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(destination_sehenswürdigkeit_valid)):
                # TODO: add disambiguation for China + USA
                airport = origin_flughafen_valid[0].name

                return textgen.destination_sehenswürdigkeiten_valid.format(query, query, airport)

            ### TODO: disambiguate invalid  dest path corretly
            # invalid flughafen
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_flughafen_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_flughafen_invalid.format(query, city, country, state, airport)

            # invalid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_stadt_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_stadt_invalid.format(query, city, country, state, airport)

            # invalid bundesland
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_bundesland_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_bundesland_invalid.format(query, city, country, state, airport)

            # invalid bundesstaat
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_bundesstaat_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_bundesstaat_invalid.format(query, city, country, state, airport)

            # invalid svz
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_svz_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_svz_invalid.format(query, city, country, state, airport)

            # invalid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list(origin_sehenswürdigkeit_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                return textgen.origin_sehenswürdigkeiten_invalid.format(query, city, country, state, airport)

            else:
                return textgen.unknown


    @staticmethod
    def __get_exact_match(query,ontology_query_results):
        match = ""

        for l in ontology_query_results:
            for s in l:
                if query == s:
                    match = s

        return match

    @staticmethod
    def _as_dict(ontology_search_results):
        """
        TODO: add doc
        :param ontology_search_results:
        :return: dict
        """
        out = dict()

        names = list(map(lambda x: x.name,(ontology_search_results)))
        synonyms = list(map(lambda x: x.hat_synonyme,(ontology_search_results)))

        for k, v in zip(names, synonyms):
            out[k] = v

        return out

    @staticmethod
    def _as_list(ontology_search_results):
        """
        TODO: add doc
        :param ontology_search_results:
        :return out: list
        """
        out = list()

        for k,v in OntologyManager._as_dict(ontology_search_results).items():
            out.append([k] + v)

        return out



if __name__ == "__main__":
    from pprint import pprint

    onto_manager = OntologyManager()

    onto_manager.query_ontology(1,2)

