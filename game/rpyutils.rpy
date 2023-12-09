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