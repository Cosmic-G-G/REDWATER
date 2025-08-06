# region Python

init python:
    def uncurried_ondoor(trans, st, at, to):
        with open(renpy.loader.transfn("doors.txt"), "r") as doors:
            reader = csv.reader(doors, delimiter = '\t')
            for row in reader:
                if row[0] == Player.location and row[1] == to:
                    trans.xcenter = float(row[4])
                    trans.yalign =1.0
                    doors.close()
                    return None
        doors.close()
        return None
    ondoor = renpy.curry(uncurried_ondoor)

# end region

# region Ren'Py

init:
    transform bounce (height, seconds = 0.1, bwait = 0.0, afwait = 0.0):
        pause(bwait)
        linear seconds/2.0 yoffset -height
        linear seconds/2.0 yoffset height
        pause(afwait)

    transform left_right(screenpos, seconds = 1.0, bwait = 0.0, afwait = 0.0):
        pause(bwait)
        linear seconds xalign screenpos
        pause(afwait)

    transform top_bottom(screenpos, seconds = 1.0, bwait = 0.0, afwait = 0.0):
        pause(bwait)
        linear seconds yalign screenpos
        pause(afwait)

#endregion