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
            return

    def uncurried_ondoor(trans, st, at, to):
        with open(renpy.loader.transfn("doors.txt"), "r") as doors:
            reader = csv.reader(doors, delimiter = '\t')
            for row in reader:
                #print(row[0]+ ","+location+","+row[1]+","+to)
                if row[0] == location and row[1] == to:
                    trans.xcenter = float(row[4])
                    trans.yalign =1.0
                    doors.close()
                    return None
        doors.close()
        return None
    ondoor = renpy.curry(uncurried_ondoor)

init:
                        #OVERRIDE
    screen choice(items):
        style_prefix "choice"

        vbox:
            for i in items:
                if i.caption[:3] == "<L>":
                    textbutton i.caption[3:] action None
                else:
                    textbutton i.caption action i.action
    
                        #TRANSFORMS
    transform bounce (height, seconds = 0.1, bwait = 0.0, afwait = 0.0):
        pause(bwait)
        linear seconds/2.0 yoffset -height
        linear seconds/2.0 yoffset height
        pause(afwait)

    transform left_right(screenpos, seconds = 1.0, bwait = 0.0, afwait = 0.0):
        pause(bwait)
        linear seconds xalign screenpos
        pause(afwait)

#START
label start:
                            #FLAGS
    $ hour = 0                                  # counter for each loop to not repeat stories
    $ canMove = False                           # disables movement
    $ locationsvisited = []
    $ mProgress = 0
    $ lProgress = 0
    $ miProgress = 0
    $ mirProgress = 0

                            #INTRO SCENE
    call intro
    call changetobeach(transition = Fade(0.1,1.0,0.5,color="#000"))
    pause(1.0)

                            #MAIN GAME LOOP
    while True:
        if location == 'beach' and mProgress == 0: 
            call mizuIntro
            #if exit or block the exit with mizu
        if location == 'school' and lProgress == 0:
            call laelaIntro

        if location == "classroom" and mirProgress == 0:
            call miraiIntro
        
        $ renpy.pause()
        $ renpy.block_rollback()

    return

#FUNCTIONS
label MoveTo(person, *args, finalxcenter=0.5, finalyalign=1.0,dissolvetime=0.5):
    $ canMove = True
    $ renpy.block_rollback()
    if len(args) > 0:
        hide person onlayer screens zorder -1 with Dissolve(dissolvetime)
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
        call MoveTo(person, *tuple(args),finalxcenter=finalxcenter,finalyalign=finalyalign,dissolvetime=dissolvetime)
    else:
        hide person onlayer screens zorder -1 with Dissolve(dissolvetime)
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
    imagebutton auto "door_%s.png" action Call("changetohallway",from_current=False) sensitive canMove xcenter 0.9 ycenter 0.5

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

#MAP
screen map():
    zorder 2
    image "map.jpg"
    imagebutton idle "door_idle.png" action [Hide("map"), Call("changetobeach")] sensitive ("beach" in locationsvisited and canMove) xcenter 0.1 ycenter 0.5
    key "m" action Hide("map")

screen mapicon():
    zorder 1
    imagebutton idle "map icon_idle.webp" action Show("map") xcenter 0.8 yalign 0.0

#TIMER
screen timer(step, tolabel):
    zorder 2
    timer step repeat If(time > 0, true=True, false=False) action If(time >= step, true=SetVariable('time',time-step), false=Jump(tolabel))
    text "{ctime:.2f}".format(ctime = time) size 100



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
    "Woah!"
    scene cabin window:
        fit "scale-up"                          #image cabin window = im.FactorScale("cabin window.jpg", 2)
    #Show tentacle
    "What the heck is that?"
    #Tentacle approaching
    "Oh... {nw}"
    #Tentacle approaching faster
    "Oh...{fast}no...{nw}"
    #Tentacle approaches closer
    "Oh...no...{fast}{w=0.5}That can't be good"
    #Tentacle breaking window
    "Oh sh--!"

    return

label mizuIntro:
    $ m = Character("mizu") #callback=functools.partial(has_exited, targetbg = '') or callback=default
    
    show mizu onlayer screens zorder -1:
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
    $ mProgress += 1
    return

label laelaIntro:
    $ l = Character("Laela")
    $ canMove = False

    hide screen bg_school with Dissolve(0.5)
    show school: # This type of transition is simple enough that does not need a function
        linear 2.0 zoom 2.0
        left_right(0.2, 1.0, 0.5)
        left_right(0.8, 1.0, 0.5)
    pause(5.0)
    "... Is that a person over there?"

    # maybe hide her behind a rock or something
    show laela onlayer screens zorder -1 with dissolve:
        xysize (247,341)
        align (0.6, 0.8)

        # should change expression when she sees you to flustered
        bounce(50, afwait=0.5)
        left_right(0.35, 0.5, 0.5)
        left_right(0.7, 0.5)
    
    "Timid girl" "awawawawawa..."

    #show laela sighing
    pause(1.0)
    hide laela onlayer screens zorder -1 with dissolve

    show school:
        linear 0.4 zoom 1.0
        pause(0.2)
    show screen bg_school with Dissolve(0.2)

    show laela onlayer screens zorder -1 with Dissolve(0.2)

    "Timid girl" "hello...{w}{cps=2}...{/cps}"
    # her eyes shift
    "Timid girl" "{cps=2}......."

    $ c1, c2 = False, False
    menu laelaMeeting01:
        "...And you are?" if not c1:
            if c2:
                $ l = Character("Laela")
            
            "Timid girl" "Um...{w=0.2}{nw}"
            # show blush, embarassed
            "Timid girl" "{cps=50}Y-you first!"
            # hide blush
            "I was just asking your name?"
            "{i}Precious{/i}" "I'm great, thanks for asking!{w=1.0}"
            # eyes shift
            # Show blush
            # show sweet smile
            l "No wait!! I'm pleasure, it's a Laela to make your acquantance."
            $ c1 = True
            jump laelaMeeting01
        "<L>...And you are?" if c1:
            pass

        "I was told to come to the school to investigate..." if not c2:
            if not c1:
                $ l = "Timid girl"

            "{cps=30}I was told to come to the school to investigate how to get off this island. A woman named Mizu told me there was{nw}"
            # show dizzy
            extend " a broadcasting station in this school and I was wondering if you could help me reach it. {nw}"
            "I wanted to contact the nearest municipality or nearest governor of this prefecture. Would you happen to know?"
            l "Governor..? No... I'm an engineer. Though, if you're trying to find Mizu, I could probably help."
            "Um... nevermind. {w}Let's talk about you."
            "You know mizu?"
            # Brightens up
            l "Yes! {w}Mizu is super nice{cps=5}...{/cps}{nw}"
            # eyes lower
            extend "{size=*0.5} Even to someone like me..."
            # eyes look back up
            l "We were best friends! She, her and my dear sister..."
            l "{cps=10}I wish we could go back to those days..."
            $ c2 = True
            jump laelaMeeting01
        "<L>I was told to come to the school to investigate..." if c2:
            pass

        "<L>???" if not c1 or not c2:
            pass
        "So... did something happen between you and Mizu?" if c1 and c2: #Final choice
            l "My sister was really kind and caring, with a bright smile and demeanour whose light would rival the sun."
            #Show sister silouette (BLOND btw)
            l"""
            I think... Because of me, because of something I did... I hurt my sister and well,

            Mizu abhored what I did and it's pretty obvious that she never forgave me for what I did... 
            
            That's what caused our fallout, I think.

            Anyways, I'd rather not depress you with my sad story. \"Let's focus on what we can do right now\", that's what she used to say.

            Except finding the broadcasting station, I can't help you with that. {w}Or the governor... 
            """
            # show eyes shift, mouth flat
            extend "And I don't really know if it is even possible to leave this island."
            "Um... Is there anything you {i}could{/i} do for me?"
            # show sad smile

    l "I always do this don't I?"
    l "I'm sorry for being so useless!"

    pause(0.5)
    show laela onlayer screens zorder -1:
        linear 0.5 xcenter 0.1
    l "I'm sorry, {size=*0.8}I'm sorry, {size=*0.6}I'm sorry, {size=*0.4}I'm sorry, {size=*0.2}I'm sorry,"
    hide laela onlayer screens zorder -1

    "Hey wait!"
    pause(0.5)
    l "I'm just a water flea!"
    pause(1.0)
    
    $ time = 15.00
    show screen timer(0.1,'laelaIntro.endtimegame')
    
    call MoveTo("laela","town", "store", "town", "forest","beach","forest","town","school","hallway","classroom",finalxcenter = -1.0, finalyalign = 1.0, dissolvetime=0.1)
    hide laela onlayer screens zorder -
    if time > 0.0 and location == "classroom":
        call laelaIntro.endtimegame

    $ hour += 1
    $ lProgress += 1
    return
label .endtimegame:
    hide screen timer
    $ time = -1.0
    if location == "classroom":
        "Dang... she's fast. Where did she go?"
    else:
        "Lost her... Maybe, I should head back to the {color=#0000ffff}school{/color} and keep exploring. Hopefully I can run into her there. "
    return

label mikaylaIntro:

    $ hour += 1
    $ miProgress += 1
    return

label miraiIntro:
    $ m = Character("???")
    
    show mirai onlayer screens zorder -1:
        function ondoor(to="hallway")

    "{i}You walk stumble into the abandoned classroom, falling onto the floor, and as you look up you're met with the cool gaze of the girl standing by the window.{/i}"

    m "What business do you have with me?"

    "Sorry for the intrusion, I was searching for Laela. Welp, I'll be on my way then."

    m "W-wait! I don't remember seeing you around here. Who are you?"

    menu: 
        "I'm an individual lost to the unpredictable forces of the sea.":
            m "I'm sorry to hear that."
        "I'm here for you.":
            m "But you were just about to leave."

    "Well there's no point dwelling on the past. Nice to meet you."

    m "I'm Mirai, nice to meet you too."

    $ m = Character("Mirai")

    "Would you happen to know how I can get off this island? I have places i need to be."

    m "It seems you've met some of the others already. More company is always welcome to our town. Why dpn't you stay a bit and meet the rest of the other?"

    menu: 
        "I'd prefer to get out of here as soon as possible.":
            m "What's the rush? I'm sure you're tired after the shipwreck. Why not stay a while first?"

            "...You're right. I guess I could stay for a while."

            m "Well I'd like to stay and talk but I've got places I need to be."

        "If the others are like you, I wouldn't be against the idea.":
            "{i}She averts her eye contact.{/i}"

            m "W-well excuse me, but I've got things to do. I'll see you later."

    "Sure, but before that I'm a bit famished. Any idea where I could get some food?"

    m "Yes! I think the convenience store might have some food. Since the town is quite small, they're quite willing to help newcomers out."

    m "Be careful with the store clerk though. {fast}{nw}"

    hide mirai onlayer screens with dissolve

    "Wait what do you mean?{nw}"

    "{i}She rushes out the classroom before you can finish your thought. She must have urgent matters to attend to.{/i}}"

    $ hour += 1
    $ mirProgress += 1
    return