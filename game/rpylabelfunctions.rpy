#region LABEL FUNCTIONS
label MoveTo(person, *args,dissolvetime=0.5): #if you can figure out how to pass by reference here, it might be better then have else: final x final y
    $ canMove = True
    $ renpy.block_rollback()
    hide expression "[person]" onlayer screens zorder -1 with Dissolve(dissolvetime)
    if len(args) > 0:
        while location != args[0]:
            $ renpy.pause()
        if len(args) > 1:
            show expression "[person]" onlayer screens zorder -1:
                function ondoor(to=args[1])
        pause(0.5)
        python:
            args = list(args)
            args.pop(0)
        call MoveTo(person, *tuple(args),dissolvetime=dissolvetime)
    else:
        $ canMove = False
        return
    return

label Battle:
    $ renpy.pause()
    $ renpy.block_rollback()
    jump Battle

label WaitUntil(to):
    $ canMove = True
    while location != to:
        $ renpy.pause()
        $ renpy.block_rollback()
    $ canMove = False
    return
#endregion