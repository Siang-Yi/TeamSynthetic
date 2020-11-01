from mainPackage.tables import *
from random import uniform
from math import sqrt

coordinates = []
# ground floor
counter = 0
for i in range(30):
    counter += 1
    lat = uniform(0.1, 1)
    lng = uniform(0.1, 2.1)
    coordinates.append([lat, lng])
    no_add = False
    for coor in coordinates:
        dist = sqrt((coor[0] - lat)**2 + (coor[1] - lng) ** 2)
        if dist < 0.01 and dist > 0:
            no_add = True
            break
    if not no_add:
        name = "visitor" + str(counter)
        email = name + "@gmail.com"
        visitor = Visitor(email=email, firstName=name, lastName=name, username=name, password=name)
        db.session.add(visitor)
        db.session.commit()
        coor = Coordinate(lat=lat, lng=lng, visitor=visitor)
        db.session.add(coor)
        db.session.commit()

# first floor
for i in range(30):
    counter += 1
    lat = uniform(2.1, 3)
    lng = uniform(0, 2.1)
    name = "visitor" + str(counter)
    email = name + "@gmail.com"
    visitor = Visitor(email=email, firstName=name, lastName=name, username=name, password=name)
    db.session.add(visitor)
    db.session.commit()
    coor = Coordinate(lat=lat, lng=lng, visitor=visitor)
    db.session.add(coor)
    db.session.commit()