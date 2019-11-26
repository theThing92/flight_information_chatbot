import datetime
import operator

class FLightDataBase:
    def __init__(self, fileName):
        self.file = fileName

        #get the data saved in the file
        file1 = open(self.file,"r")
        rawData= file1.read()
        file1.close()

        #split the date at EOL sign to get rid of it and to get all lines in a list
        rawData= rawData.split("\n")
        rawData.pop()

        for i in range(0, len(rawData)):
            #and split the lines into its categories (start, goal...)
            rawData[i] = rawData[i].split(", ")
            for x in range(0, len(rawData[i])):
                #get rid of categorie names
                rawData[i][x]= rawData[i][x].split("= ")[1]
        #assign data to a calss variable
        self.data = rawData

    #this function returns a list with all elements that match the given criteria
    #note that the list will contain lists of strings
    #criteria can be left empty if the criteria is not important
    def GetFLights(self, start="", goal="" , date="", time="", changes="", duration="", cost=""):
        self.start= start
        self.goal=goal
        self.date=date
        self.time=time
        self.changes=changes
        self.duration= duration
        self.cost= cost
        #the data that will be returned
        returnData =[]

        #iterate once trough every object in the dataBase
        for i in range(0, len(self.data)):
            #if this variable is false, one of the criterias does not match
            returnable = True

            #check if the start is the correct one
            if start != "":
                found= False

                for x in start:
                    if self.data[i][0] == x:
                        found = True
                if not found:
                    returnable = False

            #check if the goal is the correct one
            if goal != "":
                found= False
                for x in goal:
                    if self.data[i][1] == x:
                        found = True
                if not found:
                    returnable = False

            swapped = False
            #check if the time at the date is correct
            if time != "":
                #split the string into hours minutes and seconds
                hms = self.data[i][3].split(":")
                #create a new datetime.time with the splited time
                flightTime=datetime.time(int(hms[0]),int(hms[1]))

                #define the tolerance in for the time
                #in this case it is hardcoded to +-2 hours
                timeborder1 = datetime.time((time.hour-2)%24,time.minute)
                timeborder2 = datetime.time((time.hour+2)%24,time.minute)

                #if the first border ist greater then the second border, the time is between 22 and 2 o'clock
                if timeborder1 > timeborder2:
                    swapped = True

                #time is not between 22 and 2 o'clock
                if swapped == False:
                    if flightTime< timeborder1 or flightTime> timeborder2:
                        returnable = False
                #time is between 22 and 2 o'clock
                else:
                    #if date is given, the management will be done in the date section
                    if date != "":
                        pass
                    #if no date is given, just swap the timeborders
                    if timeborder2 < flightTime and flightTime < timeborder1:
                        returnable = False


            #check if the date is correct
            if date != "":
                #means that time is given and it is between 22 and 2 o'clock
                if swapped == True:
                    #split the string into hours minutes and seconds
                    hms = self.data[i][3].split(":")
                    #create a new datetime.time with the splited time
                    flightTime=datetime.time(int(hms[0]),int(hms[1]))

                    #define the tolerance in for the time
                    #in this case it is hardcoded to +-2 hours
                    timeborder1 = datetime.time((time.hour-2)%24,time.minute)
                    timeborder2 = datetime.time((time.hour+2)%24,time.minute)

                    #after 0 o'clock
                    if time < timeborder1:
                        #get the date for the day before
                        dayBefore = datetime.datetime(date.year, date.month, date.day-1)
                        #you want every flight greater than timeborder1 for the previous day and every flight less than timeborder 2 on the given date
                        #so you want to mark every flight where that is not the case as not returnable
                        if  not(flightTime > timeborder1 and self.data[i][2] == dayBefore.strftime("%x")) and not(timeborder2 > flightTime and self.data[i][2] == date.strftime("%x")):
                            returnable = False
                    #before 0 o'clock
                    else:
                        #get the date for the day after
                        dayAfter = datetime.datetime(date.year, date.month, date.day+1)
                        #you want every flight greater than timeborder1 for the given day and every flight less than timeborder 2 on the date afterwards
                        #so you want to mark every flight where that is not the case as not returnable
                        if  not(timeborder2 > flightTime and self.data[i][2] == dayAfter.strftime("%x")) and not(flightTime > timeborder1 and self.data[i][2] == date.strftime("%x")):
                            returnable = False
                #no time is given or it isnt between 22 and 2 o'clock
                else:
                    if self.data[i][2] != date.strftime("%x"):
                        returnable = False

            #check if the number of changes is correct
            if changes != "":
                if int(self.data[i][4]) > changes:
                    returnable= False

            #check if the duration is correct
            if duration != "":
                if int(self.data[i][5]) > duration:
                    returnable= False

            #check if the cost is not oversteped
            if cost != "":
                if int(self.data[i][6]) > cost:
                    returnable= False

            #if after checking all the conditions returnable was not set to false, the current flight matches all the criteria
            if returnable:
                returnData.append(self.data[i])

        return returnData

    def SortList(self, listToSort, prefs):
            minPosDepartDiff = 10000
            maxPosDepartDiff = 0

            minNegDepartDiff = 10000
            maxNegDepartDiff = -10000

            minChanges = 10000
            maxChanges = 0

            minDuration= 10000
            maxDuration= 0

            minCost= 10000
            maxCost=0

            if self.time != "":
                givenIntTime= self.time.strftime("%X").split(":")

            #first get min and max of each column
            for i in range(len(listToSort)):
                if self.time != "":
                    #search for min and max posdepart time
                    #means that flight start before given time
                    currentIntTime = listToSort[i][3].split(":")
                    factor=0
                    if listToSort[i][2] != self.date.strftime("%x"):
                        curentDate = listToSort[i][2].split("/")
                        actualDate = datetime.datetime(int("20"+curentDate[2]),int(curentDate[0]),int(curentDate[1]))
                        if actualDate < self.date:
                            factor=1
                        else:
                            factor=-1

                    timeDiff=(int(givenIntTime[0])*60+int(givenIntTime[1])) - ((int(currentIntTime[0])*60+int(currentIntTime[1]))+factor*2400)
                    if ( timeDiff ) >0:
                        if timeDiff < minPosDepartDiff:
                            minPosDepartDiff = timeDiff
                        if timeDiff > maxPosDepartDiff:
                            maxPosDepartDiff = timeDiff
                    #search for min and max negdepart time
                    else:
                        timeDiff = timeDiff*-1
                        if timeDiff < minPosDepartDiff:
                            minPosDepartDiff = timeDiff
                        if timeDiff > maxPosDepartDiff:
                            maxPosDepartDiff = timeDiff

                if self.changes != "":
                    #search for min and max of changes
                    if int(listToSort[i][4]) < minChanges:
                        minChanges = int(listToSort[i][4])
                    if int(listToSort[i][4]) > maxChanges:
                        maxChanges = int(listToSort[i][4])

                if self.duration != "":
                    #ckeck for min and max of duration
                    if int(listToSort[i][5]) < minDuration:
                        minDuration = int(listToSort[i][5])
                    if int(listToSort[i][5]) > maxDuration:
                        maxDuration = int(listToSort[i][5])

                if self.cost != "":
                    #ckeck for min and max of cost
                    if int(listToSort[i][6]) < minCost:
                        minCost = int(listToSort[i][6])
                    if int(listToSort[i][6]) > maxCost:
                        maxCost = int(listToSort[i][6])


            #then apply a value to each row that indicates how good an entry is based on the given criteria
            for i in range(len(listToSort)):
                rating = 0
                if self.start != "":
                    #get rating for starting airport
                    for x in range(len(self.start)):
                        if listToSort[i][0] == self.start[x]:
                            rating = rating + prefs[0]*((len(self.start)-x)/len(self.start))

                if self.goal != "":
                    #get rating for target airport
                    for x in range(len(self.goal)):
                        if listToSort[i][1] == self.goal[x]:
                            rating = rating + prefs[1]*((len(self.goal)-1-x)/(len(self.goal)))

                if self.date != "":
                    #get rating for date
                    if listToSort[i][2] == self.date.strftime("%x"):
                        rating = rating + prefs[2]*(1)

                if self.time != "":
                    #get rating for time
                    #get currenttime diff
                    currentIntTime = listToSort[i][3].split(":")
                    factor=0
                    if listToSort[i][2] != self.date.strftime("%x"):
                        curentDate = listToSort[i][2].split("/")
                        actualDate = datetime.datetime(int("20"+curentDate[2]),int(curentDate[0]),int(curentDate[1]))
                        if actualDate < self.date:
                            factor=1
                        else:
                            factor=-1
                    timeDiff=(int(givenIntTime[0])*60+int(givenIntTime[1])) - ((int(currentIntTime[0])*60+int(currentIntTime[1]))+factor*2400)
                    
                    #if its positive apply an different formula
                    if ( timeDiff ) >0:
                        rating= rating+ prefs[3]*((maxPosDepartDiff - timeDiff) / (maxPosDepartDiff -minPosDepartDiff))
                    #if its negative applay an different formula
                    else:
                        timeDiff = timeDiff*-1
                        rating= rating+ prefs[3]*((maxPosDepartDiff - timeDiff) / (maxPosDepartDiff -minPosDepartDiff))

                if self.changes != "":
                    #get rating for changes
                    rating = rating + prefs[4]*((maxChanges - int(listToSort[i][4]))/(maxChanges-minChanges))

                if self.duration != "":
                    #get rating for Duration
                    rating = rating + prefs[5]*((maxDuration - int(listToSort[i][5]))/(maxDuration-minDuration))

                if self.cost != "":
                    #get rating for Cost
                    rating = rating + prefs[6]*((maxCost- int(listToSort[i][6]))/(maxCost-minCost))
                listToSort[i].append(rating)



            sorted_list = sorted(listToSort, key=operator.itemgetter(7))
            for i in sorted_list:
                i.pop()
            return sorted_list
