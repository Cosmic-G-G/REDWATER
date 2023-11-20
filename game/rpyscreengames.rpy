#region SCREEN MINIGAMES
screen storebuy(items, rlst): #randomize items before calling, rlist is a list of [(rx,ry)1, (rx,ry)2] of length of items
    default citems = items.copy()
    tag storebuy
    zorder 10
    on "hide" action Hide("storebuy")

    showif citems:
        add "black"
        draggroup:
            drag:
                xycenter (0.1, 0.9)
                child "cart"
                drag_name "cart"
                draggable False
                droppable True
                dropped fstorebuy(citems = citems)
            drag:
                xycenter (0.9, 0.9)
                child "bin"
                drag_name "bin"
                draggable False
                droppable True
                dropped fstorebuy(citems = citems)
            for i, item in enumerate(items):
                if item in citems:
                    drag:
                        xycenter (rlst[i][0], rlst[i][1])
                        child item
                        drag_name item
                        draggable True
                        droppable False
    python:
        if dbg.latest in citems:
            citems.remove(dbg.latest)
            dbg.latest = None
            renpy.restart_interaction()

screen combat():
    tag combat
    timer 0.1 repeat True action Show("combat")
    on "hide" action Hide("combat")
    add color("00000088")

    for i, ally in enumerate(combatManager.allies, 1):
        add ally.sprites:
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        add CircularBar(ally.n["color"], (ally.scale*0.5, ally.scale*1.5), (ally.scale*0.5-ally.n["width"], ally.scale*0.5-ally.n["width"]), ally.n["width"], ally.n["angle"]):
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        add CircularBar(ally.s["color"], (ally.scale*1.5, ally.scale*1.5), (ally.scale*0.5-ally.n["width"], ally.scale*0.5-ally.n["width"]), ally.s["width"], ally.s["angle"]):
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        if ally.tookDamage["val"]:
                bar value ally.hp range ally.maxhp:
                    xmaximum 2*ally.scale
                    pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
    
    for i, enemy in enumerate(combatManager.enemies , 1):
        add enemy.sprites:
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        add CircularBar(enemy.n["color"], (enemy.scale*0.5, enemy.scale*1.5), (enemy.scale*0.5-enemy.n["width"], enemy.scale*0.5-enemy.n["width"]), enemy.n["width"], enemy.n["angle"]):
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        add CircularBar(enemy.s["color"], (enemy.scale*1.5, enemy.scale*1.5), (enemy.scale*0.5-enemy.n["width"], enemy.scale*0.5-enemy.n["width"]), enemy.s["width"], enemy.s["angle"]):
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        if enemy.tookDamage["val"]:
            bar value enemy.hp range enemy.maxhp:
                xmaximum 2*enemy.scale
                pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
    python:
        if combatManager.allies == [] or combatManager.enemies == []:
            renpy.hide_screen("combat")
            ui.close()
            renpy.jump(combatManager.returnLabel)
#endregion