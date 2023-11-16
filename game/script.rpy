init python:
    import functools
    import csv
    import pygame
    import math

#START
label start:
                            #FLAGS
    $ hour = 0                                  # counter for each loop to not repeat stories
    $ canMove = False                           # disables movement
    $ locationsvisited = []
    $ inventory = []

                            #INTRO SCENE
    call intro
    call changetobeach(transition = Fade(0.1,1.0,0.5,color="#000"))
    pause(1.0)

                            #MAIN GAME LOOP
    while True:
        if location == 'beach' and Mizu.progress == 0: 
            call mizuIntro
            #if exit or block the exit with mizu
        if location == 'school' and Laela.progress == 0:
            call laelaIntro
        if location == "classroom" and Mirai.progress == 0:
            call miraiIntro
        if location == "store" and Mikayla.progress == 0 and Laela.progress > 0:
            call mikaylaIntro
        if location == "forest" and Mikayla.progress == 1:
            call mikaylaStory1
        if location == "park" and Chishiki.progress == 0:
            call chishikiIntro

        if location == "beach" and hour >= 4:
            call endOfDay

        $ canMove = True
        $ renpy.pause()
        $ renpy.block_rollback()

    return

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
    $ m = Mizu
    # $ m = Character("mizu") #callback=functools.partial(has_exited, targetbg = '') or callback=default
    
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

    call MoveTo("mizu", "forest","town","store")    # May need to change canMove in function (William)
    
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

    m """
    ...I.. have to complete something.
    
    You can around the city to see if you can find a way to contact the nearest municipality. I think there is a broadcasting station in the {color=#0000ffff}school{/color}.
    
    Here is the lightrail map. I have to go now. Bye.
    """
    show screen mapicon

    $ canMove = True
    hide mizu onlayer screens zorder -1

    $ hour += 1
    $ Mizu.progress += 1
    return

label laelaIntro:
    $ l = Laela
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
                $ l = Laela
            
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
    
    call MoveTo("laela","town", "store", "town", "forest","beach","forest","town","school","hallway","classroom", dissolvetime=0.1)
    if time > 0.0 and location == "classroom":
        call laelaIntro.endtimegame

    $ hour += 1
    $ Laela.progress += 1
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
    $ canMove = False
    $ m = "Punk"
    
    show store:
        linear 2.0 zoom 1.5
        top_bottom(0.9)
    
    show mikayla onlayer screens zorder -1: 
        xalign 0.5 yalign 3.0
        top_bottom(1.0)

    # mean face
    m "What're you gawkin' at punk? Never seen a cute girl before?"

    menu:
        "My breath was simply stolen by your beauty, my dear. ":
            "My sincerest apologies my dearest, my breath was simply stolen by your beauty."
            #show her disgusted
            m "Gross..."
            m "What the hell d'ya want?"
            "Your name, milady"
            #roll eyes
            $ m = Mikayla
            m "Mikayla. No need to remember it."
            # Eyes shift
            m "I guess the gang needs water-fetchers{cps=10}........"
            # Eyes shift back
            m """
            Heya pal, I'm offerin' ya a once in a lifetime opportunity to be my personal slave{cps=10}........{/cps}

            Actually I ain't offerin', I'm tellin'

            Forest. Shrine. There'll be a showdown. Bring water 'n bandages. Get me somethin' good too. 

            Be there or be square.
            """
            jump dontlikeyourstyle
        
        "You got a problem? You can take it up with my fists!":
            #show surprised, then smile
            m "I like your style brat."
            $ m = Mikayla
            
            $ combatManager.returnLabel = "ilikeyourstylebrat.doneBattle" #IDK screen prediction is supppppeeerrr weird -> declare combat parameters ~3 pauses before the combat may *potentially* show
            $ combatManager.add(User)
            $ combatManager.add(Enemy)

            m "I'm Mikayla. How about you become my underling and we'll paint the town red!"
            jump ilikeyourstylebrat

    menu ilikeyourstylebrat:
        "How about you prove your strength first?":
            m "Alright big shot. Think you can take me? Let's go."
            show screen combat onlayer screens
            jump Battle

            label ilikeyourstylebrat.doneBattle:
                m "Not bad kiddo. You've got guts."
                #Thinking
                m """
                I think you've got what it takes{cps=10}.........{/cps} Yea I ain't losin' a talent like yourself.
                
                Alright I got one more person in mind for my big plan.

                Meet me at the forest shrine. If we're lucky we'll have a third member for our posse soon. 

                There'll be a fight you don't wanna miss. Bring some food 'n water just in case. 
                """
        
        "How about you prove your merit first?":
            # Smug eyes closed
            m "The name \'Yellow Oni\' ring any bells?"
            "{cps=10}.......{/cps}"
            # open eyes blue top of head - worried look
            m "You {i}have{/i} heard of me{cps=10}...{/cps} right?"
            m "Y'know, that demon gang led by that terrible dilenquent?"
            "{cps=10}.......{/cps}"
            # back to smug
            m """
            Well, I promise I'm a big deal! 
            
            My mission is to uncover the truth and expose the dark conspiracies of this world. 

            It goes without saying that any bad guys who stand on the side of darkness get beaten up!
            """
            #looks down, maybe a bit embarassed
            m "But uhh... {w}Seems like my squad disbanded a while ago when I started {size=17}prea{size=15}chin' {size=12}'em {size=10}these {size=5}ideas..."
            show mikayla onlayer screens zorder -1:
                bounce(50)
            # maybe show like smug or happy
            m "I mean! {w=0.5}I just so happen to have an opening that fits your particular set of skills."
            m "In fact, I know just one more person who might agree to be our partner in crime..."
            # Big toothy smile
            m "Meet me at the forest shrine and we'll have a nice friendly 'negotiation' with her."
            pause(1.0)
            m "You might wanna bring some bandages"

    label dontlikeyourstyle:
        "What a character..."
        "Whatever.. I guess I'll get her things..."

    $ ilst = ["waterbottle","greentea","melonpan","onigiri","bandage"]
    $ rlst = [(renpy.random.random()*0.7+0.1, renpy.random.random()*0.7+0.1) for x in range(len(ilst))]
    show screen storebuy(ilst, rlst)

    hide mikayla onlayer screens zorder -1

    $ canMove = True
    $ hour += 1
    $ Mikayla.progress += 1
    return

label mikaylaStory1:
    $ canMove = False
    $ m = "Mikayla"

    show mikayla onlayer screens zorder -1
    # looks at you, becomes happy

    $ hour += 1
    $ Mikayla.progress += 1
    return


label miraiIntro:
    $ m = "Girl by the window"
    
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

    $ m = Mirai

    "Would you happen to know how I can get off this island? I have places I need to be."

    m "It seems you've met some of the others already. More company is always welcome to our town. Why don't you stay a bit and meet the rest of the others?"

    menu: 
        "I'd prefer to get out of here as soon as possible.":
            m "What's the rush? I'm sure you're tired after the shipwreck. Why not stay a while first?"

            "...You're right. I guess I could stay for a while."

            m "Well I'd like to stay and talk but I've got places I need to be."

        "If the others are like you, I wouldn't be against the idea.":
            "{i}She averts her eyes.{/i}"

            m "W-well excuse me, but I've got things to do. I'll see you later."

    "Sure, but before that I'm a bit famished. Any idea where I could get some food?"

    m "Yes! I think the convenience store might have some food. Since the town is quite small, they're quite willing to help those in need."

    m "Be careful with the store clerk though."

    hide mirai onlayer screens with dissolve

    "Wait what do you mean?{w=0.1}"

    "{i}She rushes out the classroom before you can finish your thought. She must have urgent matters to attend to.{/i}}"

    $ hour += 1
    $ Mirai.progress += 1
    return

label chishikiIntro:
    show chishiki onlayer screens zorder -1:
    $ c = "Girl reading in the park"

    "{i}You arrive at the park and notice a girl reading to herself. All ambient noises have suddenly ceased. {/i}"
    "{i}You take in the calmness of the scene before you. {/i}"
    "{i}You start to slowly walk away, making as little noise as possible as to not disturb the serenity. {/i}"

    c "Aren't you gonna talk to me?"

    "{i}She startles you, as you jump back around to face her. {/i}"

    menu:
        "Sorry, I didn't see you there.":
            c "Hey, lying isn't very nice."
        "How did you know I was here?":
            c "There are few things I don't know."
        
    c "I know you fell off the ship right?"
    "Yes... I presume you heard from the others?"
    c "Sure. Let's got with that."
    "Uhh...ok..."
    "What's your name?"
    c "I'm Chishiki. Nice to meet you."

    $ c = Chishiki

    "Nice to meet you too. What are you doing out here all by yourself? Why aren't you with the others?"
    c "You'll see in due time. I'll see you again soon..."
    
    hide chishiki onlayer screens with dissolve

    "Huh? Wait!"
    "{i}How peculiar. I wonder what her deal is.{/i}"
    "{i}I should probably hurry and return to the shrine.{/i}"

    $ Chishiki.progress += 1
    return

label endOfDay:
    "{i}I should document my daily events in case I need to refer to them.{/i}"
    show journal onlayer screens zorder -1:

    $ day1Entry = Journal()

    "{i}Day 1: Today I _____.{/i}"
    menu: 
        "fell off a boat and met strange people inhabiting this island.":
            $ day1Entry.addEntry("Today I fell off a boat and met strange people inhabiting this island.")
        "fell off a boat and met a handful of maidens. I think I like them.":
            $ day1Entry.addEntry("Today I fell off a boat and met a handful of maidens.")
    "{i}I think it will take time before I can _____.{/i}"
    menu:
        "get off this island and return home.":
            $ day1Entry.addEntry("I think it will take time before I can get off this island and return home.")
        "get closer to the people on this island.":
            $ day1Entry.addEntry("I think it will take time before I can get closer to the people on this island.")
    "{i}I think tomorrow, I will try to get closer to _____.{/i}"
    menu:
        "Mizu.":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Mizu.")
        "Laela":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Laela.")
        "Mirai":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Mirai.")
        "Mikayla":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Mikayla.")
        "Chishiki":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Chishiki.")
    
    screen displayJournal:

        text "[day1Entry.getEntry()]": 
            xcenter 0.5
            ycenter 0.3 
    show screen displayJournal         