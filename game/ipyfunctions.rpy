init python:
                    #region FUNCTIONS
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
                if row[0] == location and row[1] == to:
                    trans.xcenter = float(row[4])
                    trans.yalign =1.0
                    doors.close()
                    return None
        doors.close()
        return None
    ondoor = renpy.curry(uncurried_ondoor)

    def uncurried_fstorebuy(drop, drags, citems):
        drags[0].draggable = False
        citems.remove(drags[0].drag_name)
        dbg.latest = drags[0].drag_name

        if drop.drag_name == "cart":
            print(drags[0].drag_name)
            inventory.append(drags[0].drag_name)

        if not citems:
            renpy.hide_screen("screenbuy")
        
        renpy.restart_interaction()
        return
    fstorebuy = renpy.curry(uncurried_fstorebuy)
                        #endregion