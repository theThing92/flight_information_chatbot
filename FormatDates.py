#Diese Klasse kann in die Main importiert werden und soll aus Inputs zu
#Datum - getDate
#Zeit - getTime
#Budget - getBudget
#Umstiege - getChanges
#jeweils die Daten für die Suchamschien lesbar aufbereiten.
#Für jeden Case gibt es dafür eine eigene Methode, an die der ganze Input-String übergeben werden kann
import re

class Helper:
    #Datum
    #7. Januar, 7.1, 07.01.2020, 7/1
    def getDate(inputString):
        day = 0
        month = 0
        year = 2020 #Default

        inputString = inputString.lower()

        ###find the year
        yearNotChanged = True
        yearList = re.findall('20[0-9][0-9]', inputString)
        if len(yearList) == 1:
            year = int(yearList[0])
            yearNotChanged = False
        if len(yearList) > 1:
            year = int(input("Bitte geben Sie das Jahr spezifisch an:"))
            yearNotChanged = False

        ##find the Month&Day via Keyword
        months = {"januar":1, "februar":2, "märz":3, 
        "april":4, "mai":5, "juni":6, "juli":7, "august":8, 
        "september":9, "oktober":10, "november":11, "dezember":12}

        for mon in months.keys():
            if mon in inputString:
                month = months.get(mon)
                check = re.findall('[0-9][0-9]?\.\W*'+mon, inputString)
                if len(check) == 1:
                    day = re.findall('[0-9][0-9]?', check[0])
                    day = int(day[0])
        
        ##check for Patterns
        pointPattern = re.findall('[0-9][0-9]?[\.\/][0-9][0-9]?', inputString)
        if len(pointPattern) == 1:
            patt = pointPattern[0]
            patt = patt.replace(".", "/").split("/")
            day = int(patt[0])
            month = int (patt[1])
            newYear = re.findall('[0-9][0-9]?[\.\/][0-9][0-9]?[\.\/][0-9][0-9]', inputString)
            if len(newYear) == 1 & yearNotChanged:
                year = newYear[0]
                year = 2000 + int(year[-2:])

        date = [day,month,year]
        
        if day != 0 and month != 0:
            return date
        else:
            print ("Das habe ich nicht verstanden. Bitte geben Sie das Datum erneut ein")
            inp = input()
            return Helper.getDate(inp)


    
    #Zeit
    #17:30, 7:30, 17.30, 17 Uhr, 9
    def getTime(inputString):
        hour = -1
        minute = 0

        inputString = inputString.lower()

        #Check for first Pattern
        time = re.findall('[0-9][0-9]?[:\.][0-9][0-9]', inputString)

        if len(time) == 1:
            time = time[0].replace(".", ":").split(":")
            hour = int(time[0])
            minute = int (time[1])
        
        #Check for second pattern
        time = re.findall('[0-9][0-9]?\W*uhr', inputString)

        if len(time) == 1:
            time = time[0].split("uhr")
            hour = int(time[0])
        
        #check for single time
        if len(inputString) == 1 or len(inputString) == 2:
            hour = int(inputString)
        
        if hour != -1:
            time = [hour, minute]
            return time
        else:
            print ("Ich habe Sie nicht verstanden. Bitte geben Sie die Uhrzeit erneut ein:")
            inp = input()
            return Helper.getTime(inp)
    
    #Budget
    #300 Euro, 1$, 257000 €
    def getBudget(inputString):
        budget = -1

        inputString = inputString.lower()

        #check for pattern
        budg = re.findall('[0-9]+\W*[e,$,€]?',inputString)

        if len(budg) == 1:
            budg = budg[0].replace("e", " ").replace("€", " ").replace("$", " ").split(" ")
            budget = int (budg[0])
        
        if budget != -1:
            return budget
        else:
            print ("Das habe ich nicht verstanden. Bitte nur runde Zahlen eingeben:")
            inp = input()
            return Helper.getBudget(inp)

    #Umstiege
    #Zwei, 2, Keinen
    def getChanges(inputString):
        changes = -1

        inputString = inputString.lower()

        numbers = {"null":0,"ein":1, "zwei":2, "drei":3, "vier":4, "fünf":5, "sechs":6}

        #check for numbers
        chan = re.findall('[0-9]', inputString)

        if len(chan) == 1:
            changes = int(chan[0])
        else: #check for numbers in words
            for num in numbers.keys():
                if num in inputString:
                    if num == "ein" and "kein" in inputString:
                        changes = 0
                    else:
                        changes = numbers.get(num)
        
        if changes != -1:
            return changes
        else:
            print ("Das habe ich nicht verstanden. Bitte klarer ausdrücken")
            inp = input()
            return Helper.getChanges(inp)




        




