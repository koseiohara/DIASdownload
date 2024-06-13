import datetime
from dateutil.relativedelta import relativedelta
import os

INI = datetime.datetime(1947, 9,  1,  0)
FIN = datetime.datetime(2024, 5, 31, 18)
#INI = datetime.datetime(1947, 9,  1,  0)
#FIN = datetime.datetime(1949, 5, 31, 18)

years  = FIN.year  - INI.year
months = FIN.month - INI.month

delta = years*12 + months + 1

#print(delta)

PRESENT = INI

WHERE = "/mnt/jet12/JRA3Q/Daily/fcst_phyp125/"

for t in range(0, delta):
    DIR = datetime.datetime.strftime(PRESENT, '%Y%m')
    FULL = WHERE + DIR
    print(FULL)
    os.mkdir(FULL)

    PRESENT = PRESENT + relativedelta(months=1)

