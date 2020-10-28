from mainPackage.tables import *
from random import uniform

# ground floor
counter = 0
for i in range(30):
    counter += 1
    lat = uniform(0.1, 2.15)
    lng = uniform(0.1, 1)
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
    lat = uniform(0.1, 2.15)
    lng = uniform(2.1, 3)
    name = "visitor" + str(counter)
    email = name + "@gmail.com"
    visitor = Visitor(email=email, firstName=name, lastName=name, username=name, password=name)
    db.session.add(visitor)
    db.session.commit()
    coor = Coordinate(lat=lat, lng=lng, visitor=visitor)
    db.session.add(coor)
    db.session.commit()