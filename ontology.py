"""
TODO: add doc
"""
from data import textgen
from owlready2 import *
from levenshtein import levenshtein

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

    def get_individuals_for_levenshtein(self):
        return OntologyManager._as_list_1d(list(self.ontology.individuals()))

    def get_most_likely_individual(self, query, distance=3):
        individuals = self.get_individuals_for_levenshtein()
        out = None

        for element in individuals:
            if levenshtein(query, element) <= distance:
                out = element
        return out

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
        ontology_search_results.extend(self.ontology.search(type=self.ontology.Sehenswürdigkeit, ist_sehenswürdigkeit_von_stadt=self.ontology.search_one(iri="flight_information_ontology.owl#New York")))

        return ontology_search_results

    def query_ontology(self, query, context, distance=1):
        """
        TODO: add doc
        :param entity_name: str
        :param context: str
        :return: str
        """
        query = self.get_most_likely_individual(query=query, distance=distance)

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
        destination_bundesland_invalid = self.get_valid_origin_state_germany()

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
            if OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_flughafen_valid)):
                print(textgen.origin_flughafen_valid.format(query))
                return query, True

            # valid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_stadt_valid)):
                flughafen = origin_flughafen_valid[0].name

                print(textgen.origin_stadt_valid.format(query, query, flughafen))
                return query, False

            # valid land
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_land_valid)):
                airport = origin_flughafen_valid[0].name

                print(textgen.origin_land_valid.format(query, query, airport))
                return query, False

            # valid bundesland
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_bundesland_valid)):
                airport = origin_flughafen_valid[0].name

                print(textgen.origin_bundesland_valid.format(query, query, airport))
                return query, False

            # valid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_sehenswürdigkeit_valid)):
                airport = origin_flughafen_valid[0].name

                print(textgen.origin_sehenswürdigkeiten_valid.format(query, query, airport))
                return query, False

            # invalid flughafen
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_flughafen_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                print(textgen.origin_flughafen_invalid.format(query, city, country, state, airport))
                return query, False

            # invalid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_stadt_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                print(textgen.origin_stadt_invalid.format(query, city, country, state, airport))
                return query, False

            # invalid bundesland
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_bundesland_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                print(textgen.origin_bundesland_invalid.format(query, city, country, state, airport))
                return query, False

            # invalid bundesstaat
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_bundesstaat_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                print(textgen.origin_bundesstaat_invalid.format(query, city, country, state, airport))
                return query,False

            # invalid svz
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_svz_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                print(textgen.origin_svz_invalid.format(query, city, country, state, airport))
                return query,False

            # invalid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(origin_sehenswürdigkeit_invalid)):
                airport = origin_flughafen_valid[0].name
                city = origin_stadt_valid[0].name
                country = origin_land_valid[0].name
                state = origin_bundesland_valid[0].name

                print(textgen.origin_sehenswürdigkeiten_invalid.format(query, city, country, state, airport))
                return query,False
            else:
                print(textgen.unknown)
                return query,False

        elif context == "destination":
            # valid flughafen
            if OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_flughafen_valid)):
                print(textgen.destination_flughafen_valid.format(query))
                return query,True

            # valid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_stadt_valid)):
                index = None
                valid_cities_list = OntologyManager._as_list_2d(destination_stadt_valid)

                for i,val in enumerate(valid_cities_list):
                    for j in val:
                        if query == j:
                            index = i

                valid_destination_airports = []


                for airport in destination_flughafen_valid:
                    if airport.ist_flughafen_von[0] == destination_stadt_valid[index]:
                        valid_destination_airports.append(airport)

                valid_destination_airports = str(valid_destination_airports).replace("flight_information_ontology.","").replace("[","").replace("]","")


                print(textgen.destination_stadt_valid.format(query, query, valid_destination_airports))
                return query, False

            # valid land
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_land_valid)):
                index = None
                valid_countries_list = OntologyManager._as_list_2d(destination_land_valid)

                for i,val in enumerate(valid_countries_list):
                    for j in val:
                        if query == j:
                            index = i

                # america
                try:
                    destination_land_valid[index].besteht_aus_bundesstaaten
                    valid_destination_airports = list(set(destination_flughafen_valid).intersection(destination_stadt_valid[0].hat_flughäfen))


                except Exception as e:
                    pass

                # china
                try:
                    destination_land_valid[index].besteht_aus_sonderverwaltungszonen
                    valid_destination_airports = list(set(destination_flughafen_valid).intersection(set(destination_stadt_valid[1].hat_flughäfen)))

                except Exception as e:
                    pass

                valid_destination_airports = str(valid_destination_airports).replace("flight_information_ontology.","").replace("[","").replace("]","")


                print(textgen.destination_land_valid.format(query, query, valid_destination_airports))
                return query, False

            # valid bundesstaat
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_bundesstaat_valid)):
                index = None
                valid_state_america_list = OntologyManager._as_list_2d(destination_bundesstaat_valid)

                for i,val in enumerate(valid_state_america_list):
                    for j in val:
                        if query == j:
                            index = i

                valid_destination_airports = list(
                    set(destination_flughafen_valid).intersection(set(destination_bundesstaat_valid[index].hat_flughäfen)))

                valid_destination_airports = str(valid_destination_airports).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                print(textgen.destination_bundesstaat_valid.format(query, query, valid_destination_airports))
                return query, False

            # valid svz
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_svz_valid)):
                index = None
                valid_sar_list = OntologyManager._as_list_2d(destination_svz_valid)

                for i,val in enumerate(valid_sar_list):
                    for j in val:
                        if query == j:
                            index = i

                valid_destination_airports = list(
                    set(destination_flughafen_valid).intersection(set(destination_svz_valid[index].hat_flughäfen)))

                valid_destination_airports = str(valid_destination_airports).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                print(textgen.destination_svz_valid.format(query, query, valid_destination_airports))
                return query, False

            # valid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_sehenswürdigkeit_valid)):
                index = None
                valid_sight_list = OntologyManager._as_list_2d(destination_sehenswürdigkeit_valid)

                for i,val in enumerate(valid_sight_list):
                    for j in val:
                        if query == j:
                            index = i
                valid_destination_airports = list(
                    set(destination_flughafen_valid).intersection(set(
                        destination_sehenswürdigkeit_valid[index].ist_sehenswürdigkeit_von_stadt.hat_flughäfen)))

                valid_destination_airports = str(valid_destination_airports).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                print(textgen.destination_sehenswürdigkeiten_valid.format(query, query, valid_destination_airports))
                return query, False

            # invalid flughafen
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_flughafen_valid)):

                airports_new_york = str(destination_flughafen_valid[:2]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                airports_hongkong = str(destination_flughafen_valid[2:]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                city_new_york = str(destination_stadt_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                city_hongkong = str(destination_stadt_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                state_new_york = str(destination_bundesstaat_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                sar_hongkong = str(destination_svz_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                country_china = str(destination_land_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                country_america = str(destination_land_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")


                print(textgen.destination_flughafen_invalid.format(query, city_new_york, country_america, state_new_york, city_hongkong, country_china, sar_hongkong, airports_new_york, airports_hongkong))
                return query, False

            # invalid stadt
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_stadt_invalid)):

                airports_new_york = str(destination_flughafen_valid[:2]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                airports_hongkong = str(destination_flughafen_valid[2:]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                city_new_york = str(destination_stadt_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                city_hongkong = str(destination_stadt_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                state_new_york = str(destination_bundesstaat_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                sar_hongkong = str(destination_svz_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                country_china = str(destination_land_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                country_america = str(destination_land_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")


                print(textgen.destination_stadt_invalid.format(query, city_new_york, country_america, state_new_york, city_hongkong, country_china, sar_hongkong, airports_new_york, airports_hongkong))
                return query, False

            # invalid bundesland
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_bundesland_invalid)):

                airports_new_york = str(destination_flughafen_valid[:2]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                airports_hongkong = str(destination_flughafen_valid[2:]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                city_new_york = str(destination_stadt_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                city_hongkong = str(destination_stadt_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                state_new_york = str(destination_bundesstaat_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                sar_hongkong = str(destination_svz_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                country_china = str(destination_land_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                country_america = str(destination_land_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")


                print(textgen.destination_bundesland_invalid.format(query, city_new_york, country_america, state_new_york, city_hongkong, country_china, sar_hongkong, airports_new_york, airports_hongkong))
                return query, False


            # invalid bundesstaat
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_bundesstaat_invalid)):

                airports_new_york = str(destination_flughafen_valid[:2]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                airports_hongkong = str(destination_flughafen_valid[2:]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                city_new_york = str(destination_stadt_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                city_hongkong = str(destination_stadt_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                state_new_york = str(destination_bundesstaat_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                sar_hongkong = str(destination_svz_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                country_china = str(destination_land_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                country_america = str(destination_land_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")


                print(textgen.destination_bundesstaat_invalid.format(query, city_new_york, country_america, state_new_york, city_hongkong, country_china, sar_hongkong, airports_new_york, airports_hongkong))
                return query, False


            # invalid svz
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_svz_invalid)):

                airports_new_york = str(destination_flughafen_valid[:2]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                airports_hongkong = str(destination_flughafen_valid[2:]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                city_new_york = str(destination_stadt_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                city_hongkong = str(destination_stadt_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                state_new_york = str(destination_bundesstaat_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                sar_hongkong = str(destination_svz_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                country_china = str(destination_land_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                country_america = str(destination_land_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")


                print(textgen.destination_svz_invalid.format(query, city_new_york, country_america, state_new_york, city_hongkong, country_china, sar_hongkong, airports_new_york, airports_hongkong))
                return query, False


            # invalid sehenswürdigkeit
            elif OntologyManager.__get_exact_match(query, OntologyManager._as_list_2d(destination_sehenswürdigkeit_invalid)):

                airports_new_york = str(destination_flughafen_valid[:2]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                airports_hongkong = str(destination_flughafen_valid[2:]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                city_new_york = str(destination_stadt_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                city_hongkong = str(destination_stadt_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                state_new_york = str(destination_bundesstaat_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                sar_hongkong = str(destination_svz_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")

                country_china = str(destination_land_valid[0]).replace("flight_information_ontology.","").replace("[", "").replace("]","")
                country_america = str(destination_land_valid[1]).replace("flight_information_ontology.","").replace("[", "").replace("]","")


                print(textgen.destination_sehenswürdigkeiten_invalid.format(query, city_new_york, country_america, state_new_york, city_hongkong, country_china, sar_hongkong, airports_new_york, airports_hongkong))
                return query, False


            else:
                print(textgen.unknown)
                return query, False

    def get_synonym_airport_mapping(self):
        out = dict()

        airports_origin = OntologyManager._as_dict(self.get_invalid_destination_airport()).items()
        airports_destination = OntologyManager._as_dict(self.get_valid_destination_airport()).items()

        for i in [airports_destination, airports_origin]:
            for k, v in i:
                for syn in v:
                    out[syn] = k
                out[k] = k

        return out


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
    def _as_list_2d(ontology_search_results):
        """
        TODO: add doc
        :param ontology_search_results:
        :return out: list
        """
        out = list()

        for k,v in OntologyManager._as_dict(ontology_search_results).items():
            out.append([k] + v)

        return out

    @staticmethod
    def _as_list_1d(ontology_search_results):
        d2 = OntologyManager._as_list_2d(ontology_search_results)
        d1 = []

        for i in d2:
            for j in i:
                d1.append(j)

        return d1



if __name__ == "__main__":
    onto_manager = OntologyManager()

    print(onto_manager.query_ontology("Honggong", "destination", 1))
    print(onto_manager.query_ontology("Freiheitsstatuse", "destination"))
    print(onto_manager.query_ontology("Freiheitsstatuse", "origin"))

