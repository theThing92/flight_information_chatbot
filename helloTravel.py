#### Dialogsysteme WS2019

#### Intro ####
# Wir arbeiten mit einem frame-basierten Systemen
# dh wir haben frames mit leeren slots, die  gefüllt werden müssen
# die slots werden in der interaktion mit den antworten des users gefüllt
# unsere slots bestehen aus basis informationen, die sich direkt auf den Flug beziehen und angegeben werden müssen
# und slots, die sich auf persönliche präferenzen des users beziehen und optional sind, also auch leer bleiben können
# die präferenzen könnten aber auch von anfang an sinnvolle default werte haben, die genutzt werden, falls der user
# keine weiteren präferenzen angibt


#### Skript ####
# im skript sind wie folgt erst die slots aufgelistet, im moment in form einer (zwei) dictionaries
# darauf folgen die einzelnen funktionen und ideen für mögliche weitere
# als letztes der eigentliche abruf des chatprograms mit einbettung der funktionen

#### To Do ####
# Flug Suggestion: sind sie zufrieden? rekurisv
# Präferenzen : Frage auslagern, verschiedene Optionen
# getFlights() + filterFlights()
# eine validate um alle keywords zu erkennen? implikation für store??
# -> keyword matching + ausführen der passenden store funktion
# Keyword Erkennung aller Slots bei jeder Frage möglich machen
# Exit Keyword # if schleife nach jeder funktion in startChat?

from FormatDates import Helper
from flightgenerator import FLightGenerator
from flightDataBase import FLightDataBase
import datetime
from ontology import OntologyManager
import nltk
from copy import deepcopy

### TODO: check if global declaration necessary
global storage
global stopwords
global tokenizer
global ontology_manager

ontology_manager = OntologyManager()

stopwords = nltk.corpus.stopwords.words("german")
stopwords += ["fliegen"]
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

storage = {
    'start': ["Flughafen Düsseldorf"],      #basic need-to-know
    'ziel':  ["John F. Kennedy Airport"],      #basic need-to-know
    'dep-date': [7, 11, 2019],   #basic need-to-know
    'dep-time': [12, 0],   #basic need-to-know
    'budget': 500,         # optional nice-to-know
    'sort-by-time': 500,  # optional nice-to-know
    'max-stops': 4,      # optional nice-to-know
    # Default Settings?
}
# alternative speicherung der präferenzen als nested dictionary:
# preferences = {'lay-over-time': {'value': None, 'importance': 0},
#               'budget': {value: None, 'importance': 0}
#               ..... }


def greeting():
    print('Hallo! Wilkommen beim DS Travel Assitant! Ich freue mich Ihnen zu helfen.')

def askForStart(distance=2):


    data = str(input("Von wo aus möchten Sie abfliegen? "))

    data = remove_stopwords_interpunctuation(data)

    if data == "":
        return None


    output, valid = extractInfo(data, "origin", distance=distance)
    while True:
        if valid:
            normalized = ontology_manager.get_synonym_airport_mapping()

            storage['start'] = [normalized[output]]
            break
        else:
            print("Bitte spezifizieren Sie den Startflughafen oder überprüfen Sie Ihre Eingabe.")
            data = str(input("Von wo aus möchten Sie abfliegen? "))

            data = remove_stopwords_interpunctuation(data)

            if data == "":
                break

            output, valid = extractInfo(data, "origin", distance=distance)

        # Bestätigung der Eingabe? zB
        # User: " Ich möchte die Freiheitsstatue sehen"
        # Bot : " Wollen Sie nach New York?"

def askForDestination(distance=2):
    data = str(input("Wo möchten Sie hinfliegen? "))

    data = remove_stopwords_interpunctuation(data)

    if data == "":
        return None

    output, valid = extractInfo(data, "destination", distance=distance)
    while True:
        if valid:
            normalized = ontology_manager.get_synonym_airport_mapping()

            storage['ziel']= [normalized[output]]
            break
        else:
            print("Bitte spezifizieren Sie den Zielflughafen oder überprüfen Sie Ihre Eingabe.")
            data = str(input("Wo möchten Sie hinfliegen? "))

            data = remove_stopwords_interpunctuation(data)

            if data == "":
                break

            output, valid = extractInfo(data, "destination", distance=distance)



def askForDate():
    data = str(input("An welchem Tag möchten Sie fliegen? "))

    if data == "":
        return None

    else:
        output = Helper.getDate(data)
        store({'dep-date':output})
        if output == None:
            print("Tut mir leid, das habe ich nicht verstanden. Können Sie bitte noch einmal wiederholen?")
            askForDate()

def askForTime():
    data = str(input("Möchten Sie zu einer bestimmten Uhrzeit abfliegen? "))

    if data == "":
        return None

    else:
        output = Helper.getTime(data)
        store({'dep-time':output})
        if output == None:
            print("Tut mir leid, das habe ich nicht verstanden. Können Sie bitte noch einmal wiederholen?")
            askForTime()

def askForPreference():
    print("Haben Sie noch weitere Präferenzen, z.B. ein Budget, eine Höchstanzahl an Umstiegen oder eine maximale Flugdauer? ")
    data = str(input())
    pref = Helper.getPreference(data)

    if data in ["","nein","ne","nö","keine"]:
        return None

    else:
        if pref == "changes":
            output = Helper.getChanges(data)
            store({'max-stops': output})
        elif pref == "budget":
            output = Helper.getBudget(data)
            store({'budget':output})
        elif pref == "duration":
            # TODO: write helper function to get max duration
            output = Helper.getBudget(data)
            store({'sort-by-time':output})
        else:
            print("Entschuldigung, ich habe Ihre Präferenz nicht verstanden. Könnten Sie das noch einmal anders formulieren?")
            askForPreference()

        print ("Alles klar, haben Sie noch weitere Präferenzen?")
        answer = str(input())
        if answer.lower() in ["ja", "absolut", "klar"]:
            askForPreference()

        if answer.lower() in ["nein","ne","nö","keine"]:
            return None

def extractInfo(data, context, distance):
    # Die usereingabe wird überprüft, keywörter extrahiert und eine dictionary zurückgegeben
    # -> die dictionary enthält key und value paare
    # ontologie und levenstein funktion werden benutzt

    out, valid_input = ontology_manager.query_ontology(query=data,context=context, distance=distance)

    return out,valid_input

def store(output):
    # output kann mehrere key und values enthalten
    for key, value in output.items():
        storage[key] = value
        # Für was für ein system entscheiden wir uns bei der 'importance'?
        # werden 'storage', also basis infos, und präfernzen in 2 getrennten dicts gespeichert?

def flightQuery():
    print("Ihre Flüge werden gesucht, bitte warten...")

    try:
        flights = dataBase.GetFLights(start= storage["start"], goal =storage["ziel"], date = datetime.datetime(storage["dep-date"][2],storage["dep-date"][1],storage["dep-date"][0]),
        time= datetime.time(storage["dep-time"][1],storage["dep-time"][0]), changes = storage["max-stops"], duration = storage["sort-by-time"], cost = storage["budget"])
        preferences=[1,1,1,1,1,1,1]
        bestFlights= dataBase.SortList(flights, preferences)
        return bestFlights

    except Exception as e:
        raise e

def filterQuery():
    # sortieren der Flüge aus der Query nach Präferenzen
    return {}

def flightSuggestion(flights,index=0):
    proposed_flight = deepcopy(flights[index])

    # add keys for proposed flight
    proposed_flight[0] = "Start: "+proposed_flight[0]
    proposed_flight[1] = "Ziel: "+proposed_flight[1]
    proposed_flight[2] = "Datum: " +proposed_flight[2]
    proposed_flight[3] = "Uhrzeit: " +proposed_flight[3]
    proposed_flight[4] = "Umstiege: " +proposed_flight[4]
    proposed_flight[5] = "Flugdauer (in Std.): " +proposed_flight[5]
    proposed_flight[6] = "Preis (in €): " +proposed_flight[6]

    proposed_flight = ", ".join(proposed_flight)


    data = str(input('Was halten Sie von diesem Flug? Möchten Sie ihn buchen?\n' + proposed_flight))
    output = extractFlightSuggestionInfo(data, flights, index)

    # Usercase 1. Wenn der output "Ja" ist wird der Flug gebucht und das Programm beendet
        #bookFlight()
    # Usercase 2. Wenn der output "Nein" ist wird der 2ten Flug aus dem Filter vorgeschlagen?
    #if output == 'nein':
        # 2. Flug aus liste vorschlagen?
        #data = str(input('Ist dieser Flug besser?' + flights[1] ))
    # Usercase 3. Wenn der output Präferenzen beinhaltet, wird ein neuer Filter ausgelöst -> neue Query anfrage?
    # Usercase 4. Ganz von vorne starten
    # Variation der Frage? Set von Fragen aus den mit Random eine Frage ausgesucht wird
    # Wie Loop zurück zum Query?

def extractFlightSuggestionInfo(data, flights, index):
    # Verarbeitet ja/nein und sowas wie später/früher
    # beinhaltet extractInfo() -> falls Präfernezn geändert/hinzugefügt werden

    if data.lower() in ["ja", "absolut", "klar"]:
        bookFlight()

    ## TODO: add re-prompt for query
    elif data.lower() in ["nein","ne","nö","nicht"]:
        print("Der nächstbeste Flug wird vorgeschlagen.")
        flightSuggestion(flights, index+1)


def bookFlight():
    print('Ihr Flug wurde gebucht!')

def startChat():
    greeting()
    askForStart()
    askForDestination()
    askForDate()
    askForTime()
    askForPreference()
    flights = flightQuery()
    flightSuggestion(flights, 0)



def remove_stopwords_interpunctuation(input_string):
    no_interpunctuation = tokenizer.tokenize(input_string)

    only_content_words = " ".join([w for w in no_interpunctuation if w.lower() not in stopwords])

    return only_content_words




if __name__ == "__main__":
    dataBase = FLightDataBase("flights.txt")

    startChat()