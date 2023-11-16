#region LOCATIONS
screen bg_beach():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetoforest",from_current=False) sensitive canMove xcenter 0.5 ycenter 0.5

label changetobeach(transition = None):
    $ location = 'beach'
    if 'beach' not in locationsvisited: 
        $ locationsvisited.append('beach') 
    scene beach with transition
    show screen bg_beach
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
    scene forest with transition
    show screen bg_forest
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
    scene town with transition
    show screen bg_town
    return

screen bg_store():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetotown",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5

label changetostore(transition = None):
    $ location = 'store'
    if 'store' not in locationsvisited:
        $ locationsvisited.append('store')
    scene store with transition
    show screen bg_store
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
    scene school with transition
    show screen bg_school
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
    scene hallway with transition
    show screen bg_hallway
    return

screen bg_classroom():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call("changetohallway",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5

label changetoclassroom(transition = None):
    $ location = 'classroom'
    if 'classroom' not in locationsvisited:
        $ locationsvisited.append('classroom')
    scene classroom with transition
    show screen bg_classroom
    return

screen bg_park():
    tag current
    zorder -2
    imagebutton auto "door_%s.png" action Call ("changetoschool",from_current=False) sensitive canMove xcenter 0.1 ycenter 0.5

label changetopark(transition = None):
    $ location = 'park'
    if 'park' not in locationsvisited:
        $ locationsvisited.append('park')
    scene park with transition
    show screen bg_park
    return
#endregion