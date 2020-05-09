from .models import Calendar, Pair
from datetime import time

def pair_filling():

    times={1: [time(hour=7, minute=30), time(hour=9,minute=5)],
        2: [time(hour=9, minute=20), time(hour=10,minute=55)],
        3: [time(hour=11, minute=10), time(hour=12,minute=45)],
        4: [time(hour=13, minute=15), time(hour=14,minute=50)],
        5: [time(hour=15), time(hour=16,minute=35)],
        6: [time(hour=16, minute=45), time(hour=18,minute=20)],
        7: [time(hour=18, minute=30), time(hour=20,minute=5)],}

    for i in range(1,8):
        if not Pair.objects.filter(pk=i):
            new_instance=Pair(i,times.get(i)[0], times.get(i)[1])
            new_instance.save()
            #Pair.objects.create(times.get(i)[0],times.get(i)[1])

def calendar_filling():

    type_={1:'чн', 2: 'нч'}
    days={1:'пон',
        2:'вт',
        3:'ср',
        4: 'чет',
        5: 'пят',
        6: 'суб',
        7:'вос',}

    for k1,v1 in type_.items():
        for k2,v2 in days.items():
            if not Calendar.objects.filter(TypeOfWeek=v1, DayOfWeek=v2):
                id=k1 if k1==1 else k2+7
                Calendar.objects.create(Id=id,TypeOfWeek=v1, DayOfWeek=v2)
