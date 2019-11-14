import random
import datetime
class FLightGenerator:
    def __init__(self, fileName, numberOfFlights):
        self.file=fileName
        self.flights = numberOfFlights

    def generate(self):
        file1 = open(self.file,"w")
        towns = [["Düsseldorf"], ["Hong Kong i airport", "2"], ["JFK", "NewArk"]]

        for i in range(0, self.flights):
            #get starttown
            startTown = towns[random.randint(0,len(towns)-1)]
            flight ="Start= "+ startTown[random.randint(0,len(startTown)-1)]

            #get goaltown that is different from starttown
            goalTown = towns[random.randint(0,len(towns)-1)]
            while goalTown == startTown:
                goalTown = towns[random.randint(0,len(towns)-1)]
            flight= flight + ", Goal= "+ goalTown[random.randint(0,len(goalTown)-1)]
            #get date and time
            date = datetime.datetime(2019, 11, 7+(i//(self.flights// 10)), random.randint(0,23), random.randint(0,59))
            flight = flight + ", Date= "+ date.strftime("%x")+ ", Time= "+ date.strftime("%X")
            #get the number of plane changes
            planeChanges = random.randint(0,5)
            flight = flight + ", Changes= " + str(planeChanges)

            #get the flight duration
            flightDuration = random.randint(7,9) + random.randint(1,3)*planeChanges
            flight = flight + ", Duration= "+ str(flightDuration)

            #get the cost
            cost = random.randint(500,700) - random.randint(50,100)*planeChanges
            flight = flight + ", Cost= " + str(cost) + "\n"

            file1.write(flight)

        file1.close()
