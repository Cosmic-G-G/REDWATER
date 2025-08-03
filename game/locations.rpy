#region Locations
screen map():
    zorder 2
    image "map.jpg"
    imagebutton idle "door_idle.png" action [Hide("map"), Call("changeto", "beach")] sensitive ("beach" in PlayerVariables.visited and PlayerVariables.canMove) xcenter 0.1 ycenter 0.5
    key "m" action Hide("map")

screen mapicon():
    zorder 1
    imagebutton idle "map icon_idle.webp" action Show("map") xcenter 0.8 yalign 0.0

screen bg_beach():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call("changeto","forest",from_current=False) sensitive PlayerVariables.canMove xcenter 0.5 ycenter 0.5

screen bg_forest():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call("changeto","beach",from_current=False) sensitive PlayerVariables.canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changeto","town",from_current=False) sensitive PlayerVariables.canMove xcenter 0.9 ycenter 0.5

screen bg_town():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call("changeto","forest",from_current=False) sensitive PlayerVariables.canMove xcenter 0.5 ycenter 1.0
    imagebutton auto "door_%s.png" action Call("changeto","store",from_current=False) sensitive PlayerVariables.canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changeto","school",from_current=False) sensitive PlayerVariables.canMove xcenter 0.5 ycenter 0.5

screen bg_store():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call("changeto","town",from_current=False) sensitive PlayerVariables.canMove xcenter 0.1 ycenter 0.5
    if PlayerVariables.showStoreBackDoor:
        imagebutton auto "door_%s.png" action [SetVariable("PlayerVariables.location","backstore"), Return()] sensitive PlayerVariables.canMove xcenter 0.5 ycenter 0.5

screen bg_backstore:
    layer "master"
    tag current
    add "freezer.jpg"

screen bg_school():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call("changeto","town",from_current=False) sensitive PlayerVariables.canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changeto","hallway",from_current=False) sensitive PlayerVariables.canMove xcenter 0.5 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changeto","park",from_current=False) sensitive PlayerVariables.canMove xcenter 0.9 ycenter 0.5

screen bg_hallway():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call("changeto","school",from_current=False) sensitive PlayerVariables.canMove xcenter 0.1 ycenter 0.5
    imagebutton auto "door_%s.png" action Call("changeto","classroom",from_current=False) sensitive PlayerVariables.canMove xcenter 0.9 ycenter 0.5

screen bg_classroom():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call("changeto","hallway",from_current=False) sensitive PlayerVariables.canMove xcenter 0.1 ycenter 0.5

screen bg_park():
    layer "master"
    tag current
    imagebutton auto "door_%s.png" action Call ("changeto","school",from_current=False) sensitive PlayerVariables.canMove xcenter 0.1 ycenter 0.5
# endregion

#region movement functions
label changeto(place, transition = None):
    $ PlayerVariables.visited.add(place)
    $ PlayerVariables.location = place
    scene expression "[PlayerVariables.location]" zorder -200 with transition
    show screen expression "bg_" + PlayerVariables.location onlayer master zorder -100
    #$ renpy.show_screen(f"bg_{PlayerVariables.location}", zorder=-100)
    return

label MoveTo(person, *locations, transition=None):
    ## Please hide sprite before using MoveTo, and show sprite after
    $ PlayerVariables.canMove = True
    while PlayerVariables.location != locations[0]:
        $ renpy.pause()
    if len(locations) > 1:
        show expression "[person]" as moving_person:
            function ondoor(to=locations[1])
        pause 0.01
        hide moving_person with Dissolve(0.5)
        call MoveTo(person, *tuple(locations[1:]), transition=transition)
    return

label WaitUntil(*to):
    $ PlayerVariables.canMove = True
    while PlayerVariables.location not in to:
        $ renpy.pause()
        $ renpy.block_rollback()
    $ PlayerVariables.canMove = False
    return
#endregion