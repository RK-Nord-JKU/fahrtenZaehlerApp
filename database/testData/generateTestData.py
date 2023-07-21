import csv
import random
from datetime import date, timedelta
import calendar
import locale
import numpy as np
from dataclasses import dataclass

@dataclass
class shift:
    '''class for representation of a shift input'''
    shiftDate: date
    shiftType: str
    numRides: int
    numRestHours: float

    def dateRepr(self) -> str:
        locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
        weekDay = self.shiftDate.strftime('%A')
        monthName = calendar.month_name[self.shiftDate.month]
                                        
        return f"{weekDay}-{self.shiftDate.day}.{monthName}.{self.shiftDate.year}"

    def __repr__(self) -> str:
        return ("-----------------------------------\n"
                f"{self.dateRepr()}\n"
                f"Dienstart: {self.shiftType}\n"
                f"Ausfahrten: {self.numRides}\n"
                f"Ruhestunden: {self.numRestHours}h")

    def listRepr(self) -> list:
        return [self.shiftDate,self.shiftType,self.numRides,self.numRestHours]

def testDataGeneration(dateFrom: date, dateTo: date, n: float) -> list[shift]:
    '''generates a list with N number of random shifts'''

    # generate date list
    dateList = [dateFrom]
    while dateList[-1] != dateTo: # loop to get each date till end date
        dateList.append(dateList[-1] + timedelta(days=1))
    dateList = list(np.repeat(dateList, 2))
    N = len(dateList)

    # get N random dates
    dateList = sorted(random.sample(dateList, int(N*n)))

    # iterate over N samples and generate shift entry
    x = np.arange(0,14) # numRides
    y = -(12/14)*x + 12 # numRestHours

    data = list()
    dateDuplicates = True
    for d in dateList:
        if dateList.count(d) == 1:
            shiftType = random.choice(["TD", "ND"])
        elif dateDuplicates: # first occurence
            dateDuplicates = False
            shiftType = "TD"
        else:
            dateDuplicates = True # reset variable
            shiftType = "ND"
            
        
        res = random.choice([val for val in zip(x,y)])
        s = shift(shiftDate = d,
                 shiftType = shiftType,
                 numRides = res[0],
                 numRestHours = round(res[1]/0.5)*0.5)
        data.append(s)
    
    return data




if __name__ == '__main__':
    randShifts = testDataGeneration(dateFrom=date(2020,1,1), dateTo=date(2023,7,16), n=0.6)
    # for s in randShifts:
    #     print(s)
    with open("rides_test.csv", 'w', newline='') as f:
        writer = csv.writer(f)
        for s in randShifts:
            writer.writerow(s.listRepr())
    
    print('-'*20)
    print(f"Anzahl Dienste = {len(randShifts)}")