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

    def csvRepr(self):
        return f"{self.shiftDate};{self.shiftType};{self.numRides};{self.numRestHours}"

def randomDate(dateFrom: date, dateTo: date) -> date:
    '''generates a random date'''

    dateList = [dateFrom]
    # loop to get each date till end date
    while dateList[-1] != dateTo:
        dateList.append(dateList[-1] + timedelta(days=1))
    # return one choice of the list
    return random.choice(dateList)

def randomShift() -> shift:

    x = np.arange(0,14) # numRides
    y = -(12/14)*x + 12 # numRestHours

    res = random.choice([val for val in zip(x,y)])

    return shift(shiftDate=randomDate(dateFrom=date(2015,1,1), dateTo=date(2023,7,1)),
                 shiftType=random.choice(["TD", "ND"]),
                 numRides=res[0],
                 numRestHours=round(res[1]/0.5)*0.5)


if __name__ == '__main__':
    for _ in range(500):
        print(randomShift())