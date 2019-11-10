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


storage = {
    'start': None,      #basic need-to-know
    'ziel':  None,      #basic need-to-know
    'dep-date': None,   #basic need-to-know
    'dep-time': None,   #basic need-to-know
    'budget': None,         # optional nice-to-know
    'lay-over-time': None,  # optional nice-to-know
    'max-stops': None,      # optional nice-to-know
    'eco-friendly': None,   # optional nice-to-know
    'importance': None      # optional nice-to-know
    # Default Settings?
}
# alternative speicherung der präferenzen als nested dictionary:
# preferences = {'lay-over-time': {'value': None, 'importance': 0}, 
#               'budget': {value: None, 'importance': 0}
#               ..... }


def greeting():
    print('Hallo! Wilkommen beim DS Travel Assitant! Ich freue mich Ihnen zu helfen.')

def askForStart():
    data = str(input("Von wo aus möchten Sie abfliegen? "))
    output = extractInfo(data)
    store(output)
    if output['start'] == None:
        print("Tut mir leid, das habe ich nicht verstanden. Können Sie bitte noch einmal wiederholen?")
        askForStart()
    # Bestätigung der Eingabe? zB
    # User: " Ich möchte die Freiheitsstatue sehen"
    # Bot : " Wollen Sie nach New York?"

def askForDestination():
    data = str(input("Wo möchten Sie hinfliegen? "))
    output = extractInfo(data)
    store(output)
    if output['ziel'] == None:
        print("Tut mir leid, das habe ich nicht verstanden. Können Sie bitte noch einmal wiederholen?")
        askForDestination()

def askForDate():
    data = str(input("An welchem Tag möchten Sie fliegen? "))
    output = Helper.getDate(data)
    store(output)
    if output['dep-date'] == None:
        print("Tut mir leid, das habe ich nicht verstanden. Können Sie bitte noch einmal wiederholen?")
        askForDate()

def askForTime():
    data = str(input("Möchten Sie zu einer bestimmten Uhrzeit abfliegen? "))
    output = Helper.getTime(data)
    store(output)
    if output['dep-time'] == None:
        print("Tut mir leid, das habe ich nicht verstanden. Können Sie bitte noch einmal wiederholen?")
        askForTime()

def askForPreference():
    print("Haben Sie noch weitere Präferenzen, z.B. ein Budget oder eine Höchstanzahl an Umstiegen? ")
    data = str(input())
    # validatePreference():
    # 1. keywordsearch um spezifische präferenzen zu identifizieren, zB 'Budget'
    # 2. erkennung des wertes der präferenzen, zB '300'

    # data = 'Mein budget liegt bei 300 euro'
    # gewünschter output = {'budget': 300}

    # data = "Der Preis darf nicht über 100 Euro liegen und ich möchte nur 2 mal umsteigen"
    # gewünschter output =  {'budget': 100, 'max stops': 2}

    # Wenn nur Budget gesagt wird dann {'budget': min} 
    # es wird dann bei der Flugssuche nach den niedrigsten Kosten sortiert

    # data = "blablablaba"
    # validatePreference = False, bzw output = {}, dann bleiben die präferenzen leer oder im default
    output = extractInfo(data)
    store(output)
    

def extractInfo(data):
    # Die usereingabe wird überprüft, keywörter extrahiert und eine dictionary zurückgegeben    
    # -> die dictionary enthält key und value paare
    # ontologie und levenstein funktion werden benutzt
    return {}

def store(output):
    # output kann mehrere key und values enthalten
    for key, value in output.items():
        storage[key] = value
        # Für was für ein system entscheiden wir uns bei der 'importance'?
        # werden 'storage', also basis infos, und präfernzen in 2 getrennten dicts gespeichert?

def flightQuery():
    flights = getFlights() # sucht nach Flügen
    bestFlights = filterQuery(flights) # Flüge filtern
    # bestFlights = Liste von festgesetzter Menge an Flügen ? 
    return bestFlights

def filterQuery():
    # sortieren der Flüge aus der Query nach Präferenzen
    return {}

def flightSuggestion():
    flights = flightQuery()
    data = str(input('Was halten Sie von diesem Flug? Möchten Sie ihn buchen?' + flights[0] ))
    output = extractFlightSuggestionInfo(data)
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

def extractFlightSuggestionInfo(data):
    # Verarbeitet ja/nein und sowas wie später/früher
    # beinhaltet extractInfo() -> falls Präfernezn geändert/hinzugefügt werden
    return {}

def bookFlight():
    print('Ihr Flug wurde gebucht!')
    return 

def startChat():
    # Exit?
    greeting()
    askForStart()
    if storage['ziel'] == None:
        askForDestination()
    if storage['date'] == None:
        askForDate()
    if storage['time'] == None:
        askForTime()

    askForPreference()
    flightQuery()
    flightSuggestion()

    # return

