import datetime

a = datetime.datetime.strptime('26-04-1997','%d-%m-%Y').date()
b = datetime.date.today()

print(a.year - b.year)