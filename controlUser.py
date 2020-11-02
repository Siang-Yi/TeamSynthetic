from mainPackage.tables import *

while True:
    while True:
        valid = ['w', 'a', 's', 'd', 'q']
        direction = input("Enter direction (w, a, s, d): (q for quit)")
        if direction in valid:
            break
    

    user = Visitor.query.filter(Visitor.username=="user").first()
    coor = user.coordinate[0]
    print("Before: " , coor.lat, coor.lng)
    if direction == 'w':
        coor.lat += 0.05
    elif direction == 'a':
        coor.lng -= 0.05
    elif direction == 's':
        coor.lat -= 0.05
    elif direction == 'd':
        coor.lng += 0.05
    else:
        break

    user.coor = coor
    db.session.add(user)
    db.session.commit()

    user = Visitor.query.filter(Visitor.username=="user").first()
    coor = user.coordinate[0]
    print("After: " , coor.lat, coor.lng)
