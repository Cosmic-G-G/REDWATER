#region LOCATIONS
screen bg_beach():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetoforest",from_current=False) sensitive canMove xcenter 0.5 ycenter 0.5

label changetobeach(transition = None):
    $ location = 'beach'
    if 'beach' not in locationsvisited: 
        $ locationsvisited.append('beach') 
    if transition == None:
        scene beach
        show screen bg_beach
    else:
        scene beach
        show screen bg_beach
        with transition
    return

screen bg_forest():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetobeach",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changetotown",from_current=False) sensitive canMove xcenter 0.9 ycenter 0.5

label changetoforest(transition = None):
    $ location = 'forest'
    if 'forest' not in locationsvisited:
        $ locationsvisited.append('forest')
    if transition == None:
        scene forest
        show screen bg_forest
    else:
        scene forest
        show screen bg_forest
        with transition
    return

screen bg_town():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetoforest",from_current=False) sensitive canMove xcenter 0.5 ycenter 1.0
    imagebutton auto "door_%s.png" action Call("changetostore",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changetoschool",from_current=False) sensitive canMove xcenter 0.5 ycenter 0.5

label changetotown(transition = None):
    $ location = 'town'
    if 'town' not in locationsvisited:
        $ locationsvisited.append('town')
    if transition == None:
        scene town
        show screen bg_town
    else:
        scene town
        show screen bg_town
        with transition
    return

screen bg_store():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetotown",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5

label changetostore(transition = None):
    $ location = 'store'
    if 'store' not in locationsvisited:
        $ locationsvisited.append('store')
    if transition == None:
        scene store
        show screen bg_store
    else:
        scene store
        show screen bg_store
        with transition
    return

screen bg_school():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetotown",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changetohallway",from_current=False) sensitive canMove xcenter 0.5 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changetopark",from_current=False) sensitive canMove xcenter 0.9 ycenter 0.5

label changetoschool(transition = None):
    $ location = 'school'
    if 'school' not in locationsvisited:
        $ locationsvisited.append('school')
    if transition == None:
        scene school
        show screen bg_school
    else:
        scene school
        show screen bg_school
        with transition
    return

screen bg_hallway():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetoschool",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changetoclassroom",from_current=False) sensitive canMove xcenter 0.9 ycenter 0.5

label changetohallway(transition = None):
    $ location = 'hallway'
    if 'hallway' not in locationsvisited:
        $ locationsvisited.append('hallway')
    if transition == None:
        scene hallway
        show screen bg_hallway
    else:
        scene hallway
        show screen bg_hallway
        with transition
    return

screen bg_classroom():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetohallway",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5

label changetoclassroom(transition = None):
    $ location = 'classroom'
    if 'classroom' not in locationsvisited:
        $ locationsvisited.append('classroom')
    if transition == None:
        scene classroom
        show screen bg_classroom
    else:
        scene classroom
        show screen bg_classroom
        with transition
    return

screen bg_park():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call ("changetoschool",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5

label changetopark(transition = None):
    $ location = 'park'
    if 'park' not in locationsvisited:
        $ locationsvisited.append('park')
    if transition == None:
        scene park
        show screen bg_park
    else:
        scene park
        show screen bg_park
        with transition
    return
#endregion