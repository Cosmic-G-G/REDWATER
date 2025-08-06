init python:
    import functools
    import csv
    import pygame
    import math
    import random

label start:
                            #INTRO SCENE
    
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

    call changeto("beach", transition=Fade(0.1,1.0,0.5))
    pause(1.0)
    jump MGL #MAIN GAME LOOP

label MGL:
    $ open_stories = get_open_stories()         # {"label_name": location}
    call WaitUntil(*tuple(open_stories.values())) # Wait until at start Player.location of story
    $ story_name = next(k for k, v in open_stories.items() if v == Player.location)
    $ renpy.jump(story_name) if renpy.has_label(story_name) else None


    $ Player.canMove = True
    $ renpy.pause()
    $ renpy.block_rollback()
    jump MGL

##STORIES
label Mizu_story_0:
    # $ m = Character("mizu") #callback=functools.partial(has_exited, targetbg = '') or callback=default
    $ m = Mizu

    show mizu:
        function ondoor(to="forest")
    with Fade(0.5,1.0,0.5)

    #Concerned
    m "...So that's all you can remember?"

    "Yes. That monster was the last thing I saw before I blacked out."

    "If we're not too far from the mainland, maybe someone can find me?"

    #Sad
    m "You are{cps=2}...{cps=40} {i}very{/i} far from home."

    menu: 
        "Then, how do I leave?":
            "Then, how do I leave? {w=1.5}{nw}"
            "Then, how do I-- {fast}{w=1}{size=+20}{i}Growwwlll{/i}"

    #Laugh
    m "Hehe.." 
    m "We must first sate the appetite of that monster in your belly!" #FORESHADOWING???? crazy
    m "Follow me!"
    
    window hide
    hide mizu with dissolve
    call MoveTo("mizu", "forest", "town", "store")
    show mizu with dissolve

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
    
    You can go around the city to see if you can find a way to contact the nearest municipality. I think there is a broadcasting station in the {color=#0000ffff}school{/color}.
    
    Here is the lightrail map. I have to go now. Bye.
    """
    show screen mapicon

    hide mizu

    $ Mizu.progress = 1
    jump MGL

label Laela_story_0:
    $ l = Laela
    $ Player.canMove = False

    hide screen bg_school with Dissolve(0.5)
    show school: # This type of transition is simple enough that does not need a function
        anchor (0.5, 0.75) align (0.5, 0.75) 
        linear 2.0 zoom 2.0
        left_right(0.2, 1.0, 0.5)
        left_right(0.8, 1.0, 0.5)
    pause(5.0)
    "... Is that a person over there?"

    # maybe hide her behind a rock or something
    show laela with dissolve:
        xysize (247,341)
        align (0.6, 0.8)

        # should change expression when she sees you to flustered
        bounce(50, afwait=0.5)
        left_right(0.35, 0.5, 0.5)
        left_right(0.7, 0.5)
    
    "Timid girl" "awawawawawa..."

    #show laela sighing
    pause(1.0)
    hide laela with dissolve

    show school:
        linear 0.4 zoom 1.0
        pause(0.2)
    show screen bg_school with Dissolve(0.2)

    show laela with Dissolve(0.2)

    "Timid girl" "H-hello...{w}{cps=2}...{/cps}"
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
            l "No wait!! I'm pleasure, it's a Laela to make your acquaintance."
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
            "You know Mizu?"
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
            I think... because of me, because of something I did... I hurt my sister and well,

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
    show laela:
        linear 0.5 xcenter 0.1
    l "I'm sorry, {size=*0.8}I'm sorry, {size=*0.6}I'm sorry, {size=*0.4}I'm sorry, {size=*0.2}I'm sorry,"
    hide laela

    "Hey wait!"
    pause(0.5)
    l "I'm just a water flea!"
    pause(1.0)
    
    $ time = 15.00
    show screen timer(0.1,'Laela_story_0.endtimegame')
    
    call MoveTo("laela","town", "store", "town", "forest","beach","forest","town","school","hallway","classroom", transition=Dissolve(0.2))

    if time > 0.0 and Player.location == "classroom":
        jump Laela_story_0.endtimegame
    jump MGL #Should not be here
label .endtimegame:
    $ renpy.block_rollback()
    hide screen timer
    hide expression "[person]"  with Dissolve(0.1)
    $ time = -1.0
    if Player.location == "classroom":
        "Dang... she's fast. Where did she go?"
    else:
        "Lost her... Maybe, I should head back to the {color=#0000ffff}school{/color} and keep exploring. Hopefully I can run into her there. "
    $ Laela.progress = 1
    jump MGL

label Laela_story_1:
    $ Player.canMove = False
    $ l = "Laela"
    $ a = "Asahi"
    $ m = "Mikayla"
    if Chishiki.progress == 1:
        $ c = "Chishiki"
    else:
        $ c = "???"
    #Maybe show Player.inventory, chishiki's timepiece is lost
    
    hide beach_night
    show laela:
        align (0.5,0.5)
        blur 100.0
    with Fade(0.5,2.0,0.5)
    pause(2.0)
    show asahi with Fade(0.5,1.0,0.5):
        align (0.5, 0.5)
        blur 100.0
        ease 3.0 blur 0
    "???" "Hello down there~ Hellooo~"
    hide laela 
    
    menu:
        "Ack.. So bright...": 
            "..." "Sunshine as usual."
            #show confused
            "???" "Is that a... compliment?"
            "..." "..."
            #Smile
            "???" "I appreciate it boss!"
        "Laela... or was that...":
            "..." "Mizu..?"
            "???" "No-pe! Guess again!"

    menu:
        "Then... who?":
            "..." "Ugh, my head... What happened?"

    #Salute
    a "Sir! Major Asahi Laurent reporting in!"
    a "We found you lying on the beach and thought you would appreciate warm soup and a hot shower!"

    menu:
        "Good work Major. Lead me to your encampment.":
            #Smile
            a "This way, sir!"
        
        "What are you doing?":
            #pout
            a "Come on, play along a little!"
    
    #Background hand passing through other hand
    "But as you reach for the girl's outstreched hand, your fingertips are only met with the chilling ocean breeze."

    "What the..?"

    show laela at right
    show asahi:
        ease 0.5 xalign 0.0
    with moveinbottom

    l "Five more minutes... doesn't matter anyways."

    a "Laela Laurent, you wake up right now! We've got a big day ahead; lots of neighbours to greet and people that need our help!"

    #Smile
    l "Okay sis, I'll be right there. {size=15}Don't ever change.{/size}"

    #smile
    a "Attagirl! Today's the day everything changes, I promise."

    l "Sure will."

    hide laela 
    hide asahi 
    with dissolve

    $ Player.canMove = True
    while Player.location != 'forest':
        $ renpy.pause()
        $ renpy.block_rollback()
    $ Player.canMove = False
    
    show villager at right
    show asahi:
        align (0.4, 1.0)
    show laela  zorder -2 at left

    "Villager" "Why if it isn't little Asahi. {w=1.0}As well as the other Laurent! {w=1.0}So nice to see you, Asahi."

    a "G'morning Jane!"

    #show laela shy, blush

    extend " Sis and I were wondering if you need any extra hands?"

    "Villager" "Eagar to help as always, dear. Well thanks to your visit the other day, most of the chores have already been taken care of {cps=10}...{/cps}"
    "Villager" "If you'd like, could you deliver this letter to my son? He's teaching at the {color=#0000ffff}school classroom{/color}."

    a "You got it! Here, can you hold it sis? I'm pretty clumsy with important things."

    hide asahi  with dissolve

    "Villager" "Try not to lose it or damage it."
    l "..."

    hide laela 
    hide villager 
    with dissolve

    a "But first, let's get you that hot shower, sis..." #fanservice scene

    call changeto("classroom")

    show villager_teacher at left
    show asahi:
        xalign 0.6
    show laela  zorder -2 at right
    with Fade(0.5,1.0,0.5)

    a "Heya Jon, got a letter here from your ma."

    "Jon" "Asahi does delivery service now? Well thanks, I'll be sure to leave a good review."

    a "Asahi and Laela Express! Come rain or snow, we'll get your package where it needs to be. 24/7 no shipping costs!"

    a "Jokes aside, anything you need help with Jon?"

    "Jon" "Hmmm... I'm having a hard time with these two students..."

    a "Remedial classes? Fret not, XXXX Valedictorian Laela and her trusty assistant Asahi are on the case!"

    "Jon" "You're a lifesaver, Asahi."

    hide villager_teacher  with dissolve

    show asahi:
        ease 0.8 xalign 0.4
    show laela  zorder -2:
        ease 0.8 xalign 0.0
    
    pause(0.8)
    show villager_youngstudent at right

    show asahi:
        left_right(0.4, 0.7)

    #show grossed
    a "Ughhh maths... Math master Laela, I request thy wisdom..."

    "Young student" "Big sis Asahi! Are you here to play with me?"

    a "Haha, we can play together, but only after you finish your homework!"

    "Young student" "Ehhhh... But I'm stuck on this question..."

    menu:
        "Solve the differential equation x'-x+3=0"

        "a) x(t)=ln(x-3)+C":
            a "This one, obviously! (total guess)"

            l "Uhh. Maybe the correct answer is b..?"

            l "I'm sorry..."
        
        "b) x(t)=Aexp(t)+3":
            l "If you differentiate this and plug it back into the equation, you will arrive at zero."

            $ Laela.affection += 1

        "c) x(t)=Ax+B":
            a "Well if you count the number of c's its probably this one."

            l "Sister... maybe we shouldn't encourage that behavior..."

            l "The answer probably includes a natural exponential component since they equal themselves when differentiated..."

            l "...sorry..."

    "Young student" "..."

    a "Well, you heard it here from the master engineer herself, my most trust worthy study buddy!"

    "Young student" "Well, if you say so Asahi, then I believe you."

    "Young student" "Thanks Asahi! Let's play tomorrow, I think my mom is waiting for me at home."

    a "Toodles!"

    a "One more to go!"

    hide villager_youngstudent  with dissolve
    
    show asahi:
        ease 0.8 xalign 0.4
    show laela  zorder -2:
        ease 0.8 xalign 0.0
    
    pause(0.8)
    show mikayla_young at right with dissolve

    "Girl" "So you gonna help me or just gonna stare?"

    "Clearly Mikayla" "{fast}So you gonna help me or just gonna stare?"

    a "Ah! Sorry! Please listen to Laela, she knows more than me."

    m "Sure, I don't care."

    show laela

    l "R-really? Everyone seems to have... reservations."

    m "Just lemme outa here. Stupid four-eyes can't see a prodigy when she's right in front of him. "

    m "'Sides, I always notice you here from late at night to early morning. In the garage 'n chem lab, making... things."

    l "Wow, aren't you a very observant child{cps=10}... {/cps} Wait shouldn't you be sleeping at that time?"

    m "Nevermind, just help me out."

    show laela:
        left_right(0.7)
    # show laela like toriel suspicious face
    pause(1.0)

    l "I don't think 'cuz the sea collectin debts, ya see' is a grammatically correct sentence{cps=10}... {/cps} What the heck is this report even on?"

    #show mikayla frustrated, maybe with a bounce or someting, or vpunch
    show mikayla_young  zorder -3 with vpunch
    m "AHHHH I DON'T FRIGGIN CARE ABOUT THIS STUPID ESSAY!"

    show laela:
        left_right(0.55, 0.1)
    m "THAT FOUR EYES CAN TAKE MY PAPER AND SHOVE IT NEXT TO THE STICK UP HIS A----"

    hide mikayla_young  with moveoutleft

    a "WOAH...Hey!!! Haha... sorry Jon, no luck... Should we chase her?"

    "Jon" "No use... That child is a dead end. Thanks anyways Asahi. Take care now."

    hide laela 
    hide asahi 
    with dissolve

    call WaitUntil("hallway")

    show chishiki

    c "We're running out of time..."

    if Chishiki.progress < 1:
        "Who are you?"

        $ c = "Chishiki"
        # show frustrated
        c "Chishiki... We don't have time for this..."

    $ items = ("What's going on?", "Why can't anyone see me?", "Where am I?", "Why is Mikayla a child?", "What are you hiding?", "How do I go home?")
    call screen mundanechoice(items, 5.0)

    if not _return:
        c "I know you have plenty of burning questions, but we must progress this story. "
    elif _return == "What's going on?":
        c "Your duty is to play the part of the 'hero.'"
    elif _return  == "Why can't anyone see me?":
        c "Indeed, an ironic contradiction of reality."
    elif _return == "Where am I?":
        c "A place that should not exist."
    elif _return == "Why is Mikayla a child?":
        c "Perhaps you've realized this is not the same time dimension you are from."
    elif _return == "What are you hiding?":
        c "All will be revealed in time."
    elif _return == "How do I go home?":
        c "I apologize, but your story is not yet finished."

    $ renpy.block_rollback()

    "As you are about to speak, the air in your lungs is forcibly taken away."

    $ gt = renpy.get_game_runtime()
    c "Though only [gt] minutes have passed for you, this world has waited far too long for a savior."

    c "My power is weakening. I will not be able to suspend the catastrophe for much longer.."

    c "Take my pocket watch; it will help you to return to the 'present.'"

    pause (1.5)

    c "Oh, and... Please take care of them, okay?"

    "Hey wait!!"

    hide chishiki  with dissolve
    call changeto("forest")

    show mizu at left
    show asahi
    show laela  zorder -2 at right
    with Fade(0.5,1.0,0.5)

    $ m = "Mizu"

    m "... and so that's what's happened today. What about you girls?"

    a "Well... about the usual. We went around trying to help everyone in town, but it seems like everyone is still hesitant to accept Laela."

    l "Hesistant is an understatement... But it's okay. As long as I've got you and dear sister Asahi, I don't need anything else."

    m "Now, now."

    a "But Laela has so many good qualities. I'm a little upset that no one appreciates her."

    l "It's because you outshine me in every way; and I'm happy about that."

    a "This entire day has been Asahi this, Asahi that. But who's the smartest engineer in town? Who's the one that always fixes all of the cars and troubleshoots all of our electricity problems?"

    m "True. Laela is amazingly smart, yet humble. Hardworking even without recognition."

    l "P-please... don't get so worked up over my sake... But I'm very happy you think so."

    m "..."

    m "Fine... I guess we'll leave it there for now. By the way Asahi, are you still planning to go to that party?"

    a "Yeah. I mean, it is my send-off party after all, arranged specifically for me."

    #show mizu disappointed

    m "Your always helping them. What have they ever done for you?"

    m "You'd really rather spend your last few days with strangers than us?"

    a "Come on it's not like that... You know I love you guys. But if I stay with you any longer, I don't think I'll have the courage to leave."

    l "...I also don't want you to go... There has to be another way. If you just wait a little..."

    a "Dear Laela... I'm sure we will see each other again after all of this is over. "

    a """
    Laela... There will certainly come a day when your talents and hard work are appreciated and rewarded. I already know you will one day be heralded as a hero, standing heads and shoulders above others.

    They will look towards you for your leadership and you will certainly help them with a smile on your face.

    Mizu... Thank you for your friendship towards Laela and myself over these past few years. I'm sure it has been tough to be friends with Laela when she is so wrongfully ostracized, but it really means the world to us.

    Your work here is not yet finished. Even though I may be leaving, I'm sure you will find many more capable partners to take my place.

    Please look after Laela during my absence.
    """
    #Show cry

    a "I-I love you guys a-a lot... "

    #Show happy
    a "I can't be crying now... I should go now. Take care now."
    
    hide asahi  with dissolve

    hide mizu 
    hide laela 
    call changeto("town")

    show villager at right
    show asahi at left 
    with Fade(0.5,1.0,0.5)
    # sad asahi

    "Villager" "Why so glum Asahi? You're doing a great thing, something to be proud of!"

    a "Aha... Sorry Marle... You even went through the trouble of organizing this party for me."

    "Villager" "You're doing a great service for this small town. That being said{cps=10}... {/cps} I think many people here, myself included, will miss you dearly."

    "Rowdy voice" "Hey Asahi! I think someone's looking for you in the convience store!"

    a "Oh? I'll be there right away."

    "Villager" "Still helping others even now, huh Asahi?"

    hide asahi 
    hide villager 
    with dissolve

    call WaitUntil("store")

    show asahi
    
    a "Hello..? Is anyone here..?"

    show asahi:
        left_right(0.3, 0.5)
        left_right(0.7,0.5)
        ease 0.5 xalign 0.5

    a "Maybe in the back..?"

    hide asahi  with dissolve

    "{i}click...{/i}"

    a "Huh..? Door's locked..."

    a "Feeling a bit woozy..."

    a "No... stop... my... clothes..."

    menu:
        "Stop right there!":
            $ secretVariables.showStoreBackDoor = True
            $ renpy.restart_interaction()

    call WaitUntil("backstore")

    show screen bg_backstore
    show laela 
    with Fade(0.5,0.5,0.5)

    "{cps=10}L-Laela...?"

    c "We're out of time. Sending you back."

    call changeto("beach", transition = Fade(0.5,0.7,0.5))
    $ secretVariables.showStoreBackDoor = False

    "{i}You wake up to the familiar scent of salt carried by the wind. It's cold, other than Chishiki's pocket watch in you hand emitting a strange warmth. "
    $ Laela.progress = 2
    jump MGL

label Mikayla_story_0:
    $ Player.canMove = False
    $ m = "Punk"
    
    #A background That just goes from top to bottom i think is better
    show store:
        anchor (0.5, 0.6) align (0.5, 0.6)
        linear 2.0 zoom 1.5
        top_bottom(0.9)
    
    show mikayla: 
        xalign 0.5 yalign 3.0
        top_bottom(1.0)

    show screen bg_store with Dissolve(0.2)

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
            $ combatManager.remove("all")
            $ combatManager.add(user)
            $ mikaylaFighter.safechange()
            $ combatManager.add(mikaylaFighter)

            m "I'm Mikayla. How about you become my underling and we'll paint the town red!"
            jump ilikeyourstylebrat

    menu ilikeyourstylebrat:
        "How about you prove your strength first?":
            m "Alright big shot. Think you can take me? Let's go."
            show screen combat 
            jump Battle

            label ilikeyourstylebrat.doneBattle:
                $ mikaylaFighter.safechange()
                $ combatManager.remove("all")
                m "Not bad kiddo. You've got guts."
                #Thinking
                m """
                I think you've got what it takes{cps=10}.........{/cps} Yea I ain't losin' a talent like yourself.
                
                Alright I got one more person in mind for my big plan.

                Meet me at the forest shrine. If we're lucky we'll have a third member for our posse soon. 

                There'll be a fight you don't wanna miss. Bring some food 'n water just in case. 
                """
                hide mikayla
        
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
            show mikayla:
                bounce(50)
            # maybe show like smug or happy
            m "I mean! {w=0.5}I just so happen to have an opening that fits your particular set of skills."
            m "In fact, I know just one more person who might agree to be our partner in crime..."
            # Big toothy smile
            m "Meet me at the forest shrine and we'll have a nice friendly 'negotiation' with her."
            pause(1.0)
            m "You... might wanna bring some bandages."
            hide mikayla

    label dontlikeyourstyle:
        "What a character..."
        "Whatever.. I guess I'll get her things..."

    $ item_dict = dict(zip(
        ["waterbottle","greentea","melonpan","onigiri","bandage"],
        [(renpy.random.random()*0.7+0.1, renpy.random.random()*0.7+0.1) for _ in range(5)]
    ))
    show screen storebuy(item_dict)

    hide mikayla

    $ Player.canMove = True
    $ Mikayla.progress = 1
    jump MGL

label Mikayla_story_1:
    $ Player.canMove = False
    $ m = "Mikayla"
    $ M = "Mizu"

    show mikayla
    # looks at you, becomes happy
    m "You made it!"
    # smug, with hand wiping nose
    m "I knew you'd come. "

    "So I guess the person you were talking about was Mizu?"
    #Neutral happy
    m "Ya guessed correctly!"

    $ c2 = False
    $ c1 = "So how d'ya want to go about this?"
    menu negotiations:
        m "[c1]"

        "Storm the front gates!":
            #eyes open, then wait
            #Really cute laugh
            m """
            Hahahaha! You're pretty awesome!

            Allllriggghtt! Let's get this show started!
            """
            jump afterNegotiation
        
        "Apply diplomatic pressure." if not c2:
            m "Nice thinkin'"

            m "Mizu ya home, best?"

            m "Found ourselves fresh meat. Real tough cookie."

            "..."

            #looks at you, then smiles

            m "Not bad lookin either."

            pause(1.0)

            #sad, desperate expression

            m """
            Hey, com'on dude... ya still mad about {i}that{/i}? {size=10}Said I was sorry already...

            How long are ya plannin' on givin' me the cold shoulder? It'll be different this time I promise!

            I won't lose. I can't lose again.   

            This time I'l-- no, {i}we'll{/i} win, together. 

            ...

            Any other ideas?
            """
            $ c1 = "Any other ideas?"
            $ c2 = True
            jump negotiations
        "<L>Apply diplomatic pressure." if c2:
            pass
    
    label afterNegotiation:
        m "'ight, time to show ya how strong I've really become over these past years.."

        show mikayla with vpunch #maybe angry

        m "Nuff of this. Get out here ya wuss. Said it was time for a rematch." # would like to use the p-wordussy here
    
    show mizu at left
    show mikayla at right

    M "Oh hello, it's you. I hope you've found your way around?"

    "Me?"

    M "Why, who else would I be talkin', I mean {i}talking{/i} to?"

    m "This b-"

    "Suddenly Mikayla lashes forward and all you can see is the arch in her body as her fist hurtles through the air... and stops less than an inch before Mizu, who remains unflinched." #Maybe a background would be better here

    M "Why the silence? Are you feeling unwell?"

    # Mikayla very sad
    m "Mizu... I'm really sorry. I shouldn've done that without tellin' ya. But I've never once regretted what I've done 'n would do it again in a heartbeat."

    m "Ya didn't deserve then to be hurtin' alone and you don't now. {size=17}Please...{size=15} Don't ignore me anymore..."

    M "..."

    "..."

    show mikayla with vpunch # also darken her forhead and hide eyes (you know the anime face)
    pause(0.5)
    show mikayla with moveoutright
    hide mikayla 
    
    $ inventorylist = [(item, item) for item in Player.inventory if item is not "bandage"] # screen prediction smh

    M "Well I appreciate the visit, but if you're just here to see me, I'm afraid I don't have much hospitality to offer you."

    menu:
        "Why are you so cold to her?":
            #Confused
            M "Huh?"
            menu:
                "Nevermind.":
                    M "...Well, I have a few chores to do around the temple. Feel free to sit and enjoy the nice weather."
    
    show mizu with moveoutleft
    hide mizu 

    show mikayla with moveinright #should be poofy eyed

    menu:
        "Hey, I'm really sorry...":
            #show smile
            m "Nah... I knew it would turn out like this..."

        "Never yield. Those who surrender have already lost the battle of heart!":
            #show smile
            m "Damn right!"
            m "Don't worry about it. I knew it would turn out like this..."
    
    $ narrator("Give her...", interact=False)

    if inventorylist:
        $ present = renpy.display_menu(inventorylist)

        # Surprised, sweet smile
        m "Thanks ya really know just what do to get my spirits up huh?"
        $ Mikayla.affection += 1
        $ Player.inventory.remove(present)

        if "bandage" in Player.inventory:
            m "Haha... you even brought bandages. Don't worry, only my heart hurts a little."
            $ Mikayla.affection += 1
    else:
        m "Well, ya know what always helps when you're down? A good meal!"

        "..."

        #Looks at you

        m "Uhh... nevermind."
    
    #Wistful
    m "Would you believe me if I said Mizu once had short hair?"

    #Sad laugh
    m """
    We all thought she would be a pathetic little pushover. After all, what sane person would openly defy the Yellow Oni gang when they claimed their stomping grounds.

    After all, nobody ever comes way out here in the sticks and her Pa was gone most of the time.

    All alone, she could but acquiesce to the power in front of her.

    So then, after she returned wither her head hung low. I leaned over her, real close...

    'Heya girlie, just wonderin' what'cha guys were doin' with all our offerins over these years. Surely ya haven't been wastin around all day?'

    Thought I'd play with her a bit... ruffle her feathers.

    'Guess you could say we've come to collect our rightful dues.'

    But before I could finish, she tilted her delicate face back and stared right through me. Then she landed a headbutt right on my shnoz.

    Stumbled back n' realized-- my nose was bleedin'!

    N' so we fought, all of us gang members 'gainst a little maiden... and got our asses handed to us on a silver platter!

    ...My crewmates dropped one by one. But I never retreated. 

    Every day I'd return for a rematch... and every day I'd get walloped!

    Little by little, I'd learn more about Mizu. Her likes, her dislikes and her story.

    I learned what she was fighting for... and I learned I didn't want her to fight alone.

    That was when I vowed I'd get stronger for her sake. 

    Then, on the day she determined would be her last, I decided I would fight on her behalf.

    I just... just wanted to protect her. After all that training, I never thought I'd... d-

    """ #background while leaning in
    
    "You'd...?"

    #Scared
    m "What... is that?"
    
    hide mikayla  with moveoutbottom
    show leviathan with vpunch

    $ combatManager.returnLabel = "Mikayla_story_1.doneBattle"
    $ combatManager.remove("all")
    $ combatManager.add(user,mikaylaFighter,mizuFighter,enemy)

    "{size=80}{i}GRROOOOAAAARRRR{/i}{/size}"

    M "OUT OF THE WAY!"

    show mizu at left
    M "I'll hold it off."

    show mikayla at right
    m "Never again. We'll fight together."

    show screen combat 
    jump Battle
    return
label .doneBattle: #You must win this battle -> configure health such that you always win even by doing nothing
        $ combatManager.remove(("all"))
        "Sea monster" "{size=80}{i}SCREEECHHH{/i}{/size}"
        hide leviathan  with dissolve

        m "Hah.. hah...I was... pretty good, don't'cha think?"
        M "Looks like we fought it off, for now"
        # mizu concerned
        m "Come on... at least give me a little credit!"

        M "I... need to check something immediately."

        M "If you've already finished everything you need to do for today, head to the {color=#0000ffff}beach{/color}. I pitched a campsite there for you."

        M "I'm sorry. I need to leave."

        hide mizu  with dissolve

        m "Hey, sorry, but catch ya later?"

        hide mikayla  with dissolve

        $ Player.canMove = True
        $ Mikayla.progress = 2
        jump MGL

label Mirai_story_0:
    $ Player.canMove = False
    $ m = "Girl by the window"
    
    show mirai:
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

    m "Be careful in that area though."

    hide mirai  with dissolve

    "Wait what do you mean?{w=0.1}"

    "{i}She rushes out the classroom before you can finish your thought. She must have urgent matters to attend to.{/i}"

    $ Mirai.progress = 1
    jump MGL

label Chishiki_story_0:
    $ Player.canMove = False
    show chishiki
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
    
    hide chishiki  with dissolve

    "Huh? Wait!"
    "{i}How peculiar. I wonder what her deal is.{/i}"
    "{i}I should probably hurry and return to the beach.{/i}"

    $ Chishiki.progress = 1
    jump MGL

label endOfDay:
    $ Player.day = 1
    $ Player.canMove = False
    show beach_night
    "{i}I should document my daily events in case I need to refer to them.{/i}"

    $ day1Entry = Journal()

    "{i}Day 1: Today I _____.{/i}"
    menu: 
        "fell off a boat and met strange people inhabiting this island.":
            $ day1Entry.addEntry("Day1: Today I fell off a boat and met strange people inhabiting this island.")
        "fell off a boat and met a handful of maidens. I think I like them.":
            $ day1Entry.addEntry("Day 1: Today I fell off a boat and met a handful of maidens.")
    "{i}I think it will take time before I can _____.{/i}"
    menu:
        "get off this island and return home.":
            $ day1Entry.addEntry("I think it will take time before I can get off this island and return home.")
        "get closer to the people on this island.":
            $ day1Entry.addEntry("I think it will take time before I can get closer to the people on this island.")
    "{i}I think tomorrow, I will try to get closer to _____.{/i}"
    menu:
        "Mizu":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Mizu.")
        "Laela":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Laela.")
        "Mirai":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Mirai.")
        "Mikayla":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Mikayla.")
        "Chishiki":
            $ day1Entry.addEntry("I think tomorrow, I will try to get closer to Chishiki.")
    
    $ displayText = day1Entry.getEntry()

    screen displayJournal:
        frame:
            xpadding 20
            ypadding 20
            xalign 0.5
            yalign 0.5
            xsize 500
            background "journal.jpg"
            vbox:
                text "{color=#000000} [displayText] {/color}" 

    show screen displayJournal
    
    "Guess I'm getting a little sleepy. I'll just... doze off here..."
    hide screen displayJournal
    jump MGL