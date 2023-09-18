init python:
    import functools
    import csv

                        #FUNCTIONS
    def has_exited(event, interact=True, targetbg = None, **kwargs):
        if not interact:
            return

        if event == "show":
            print(targetbg, location)
            if location != targetbg:
                renpy.return_statement()
    
    def default(event, interact=True, **kwargs):
        if not interact:
            return

    def uncurried_ondoor(trans, st, at, to):
        with open(renpy.loader.transfn("doors.csv"), "r") as doors:
            reader = csv.reader(doors, delimiter = '\t')
            for row in reader:
                print(row[0]+ ","+location+","+row[1]+","+to)
                if row[0] == location and row[1] == to:
                    trans.xcenter = float(row[4])
                    trans.yalign =1.0
                    doors.close()
                    return None
        doors.close()
        return None
    ondoor = renpy.curry(uncurried_ondoor)

                        #FLAGS
    hour = 0                                  # counter for each loop to not repeat stories
    canMove = False                           # disables movement
    locationsvisited = []

#START
label start:
    call intro
    
    call changetobeach(transition = Fade(0.1,1.0,0.5,color="#000"))
    pause(1.0)

    while True:
        $ renpy.pause()
        if location == 'beach' and hour == 0: 
            call mizuIntro
            #if exit or block the exit with mizu

        $ renpy.block_rollback()

    return

#FUNCTIONS
label MoveTo(person, *args, finalxcenter=0.5, finalyalign=1.0):
    $ canMove = True
    $ renpy.block_rollback()
    if len(args) > 0:
        hide person onlayer screens zorder -1 with dissolve
        while location != args[0]:
            $ renpy.pause()
        if len(args) > 1:
            show expression "[person]" as person onlayer screens zorder -1:
                function ondoor(to=args[1])
        else:                                                                                   # Even though whatever is shown here will be hidden, needed for the split second before the function returns.
            show expression "[person]" as person onlayer screens zorder -1:
                xcenter finalxcenter
                yalign finalyalign
        pause(0.5)
        python:
            args = list(args)
            args.pop(0)
        call MoveTo(person, *tuple(args))
    else:
        hide person onlayer screens zorder -1
        $ canMove = False
        return
    return

##LOCATIONS
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

#MAP
screen map():
    zorder 2
    image "map.jpg"
    imagebutton idle "door_idle.png" action [Hide("map"), Call("changetobeach")] sensitive ("beach" in locationsvisited and canMove) xcenter 0.1 ycenter 0.5
    key "m" action Hide("map")

screen mapicon():
    zorder 1
    imagebutton idle "map icon_idle.webp" action Show("map") xcenter 0.8 yalign 0.0

#Characters
layeredimage mizu:
    attribute only null

    group standing multiple variant "standing": #Anything layered onto the standing pose (weapons, accessories etc)
        #Furthest
        attribute pose1 default if_not "pose2"                                                             
        attribute pose2                                                                            #mizu_standing_pose2 <=> show mizu standing pose2 or show mizu pose2 until sitting/other implemented

        attribute robes default if_not "only"                                                      #show mizu (robes) mizu sweater (robes+sweater) mizu sweater only (sweater)
        attribute sweater pos(100,0)
    
    #group sitting multiple:
    #    attribute robes

    group face auto:
        pos(50,50)
        attribute neutral default                                                                   #mizu_face_neutral
    

##STORIES
label intro:
                    #INTRO SCENE
    scene cabin
    pause(0.5)
    scene cabin with Fade(0.1,0.0,0.5,color="#fff")
    "{size=+20}BLAM" with vpunch
    "Crap! Oh crap oh crap oh crap!"
    scene cabin window:
        fit "scale-up"                          #image cabin window = im.FactorScale("cabin window.jpg", 2)
    #Show tentacle
    "What the heck is that?"
    #Tentacle break window ciniematic
    return

label mizuIntro:
    $ m = Character("mizu") #callback=functools.partial(has_exited, targetbg = '') or callback=default
    
    show mizu onlayer screens zorder -1 with fade:
        function ondoor(to="forest")

    m "...You're sure that's all you remember?"
    m "You are indeed very far from home."

    menu: 
        "How do I leave?":
            "How do I-- {nw}"
            "How do I-- {fast}{w=0.5}{i}Growwwlll{/i}"

    m "Heh.. We must first sate the appetite of that monster in your belly!" #FORESHADOWING???? crazy
    m "Follow me!"
    
    window hide
    hide mizu onlayer screens with dissolve         # Please hide sprite before using MoveTo, and show sprite after (the sprite used in MoveTo is nonreferencable outside MoveTo)

    call MoveTo("mizu", "forest","town","store")    # name, locations in order, finalxcenter, finalyalign for last pos. May need to change canMove in function (William)
    
    show mizu onlayer screens zorder -1

    m "Here we are! Take anything you want... after all..."

    menu:
        "I noticed on the way here...":
            pass
        "Where is everyone?":
            pass
    
    m "..."
    m "{cps=20}Oh! This onigiri brand is super delish, have some!"

    "Thanks. So anyway, where is everyone?"

    m "{cps=40}This instant noodle is also one of my favorites,{nw}"
    menu:
        extend "{cps=60} it's got a great sauce and little chunks of fish! But in my opinion, the best part is the price! 
        Whether you're a broke college student or just hurtin' for some cash you can't beat this deal!"

        "Is there a reason why you're not answering my questions":
            m "..."
    
    "Why are you the only person I've seen on this island?"

    m "...I.. have to complete something."
    m "You can around the city to see if you can find a way to contact the nearest municipality. I think there is a broadcasting station in the {color=#0000ffff}school{/color}."
    m "Here is the lightrail map. I have to go now. Bye."
    show screen mapicon

    $ canMove = True
    hide mizu onlayer screens zorder -1
    $ hour += 1