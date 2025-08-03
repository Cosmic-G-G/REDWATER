init python:
    def uncurried_fstorebuy(drop, drags, item_dict):
        drags[0].draggable = False
        item_dict.pop(drags[0].drag_name)

        if drop.drag_name == "cart":
            #print(drags[0].drag_name)
            PlayerVariables.inventory.append(drags[0].drag_name)

        if not item_dict:
            renpy.hide_screen("screenbuy")
        
        renpy.restart_interaction()
        return
    fstorebuy = renpy.curry(uncurried_fstorebuy)

screen storebuy(item_dict): 
    tag storebuy
    zorder 10
    on "hide" action Hide("storebuy")

    showif item_dict:
        add "black"
        draggroup:
            drag:
                xycenter (0.1, 0.9)
                child "cart"
                drag_name "cart"
                draggable False
                droppable True
                dropped fstorebuy(item_dict = item_dict)
            drag:
                xycenter (0.9, 0.9)
                child "bin"
                drag_name "bin"
                draggable False
                droppable True
                dropped fstorebuy(item_dict = item_dict)
            for item, (x, y) in item_dict.items():
                drag:
                    xycenter (x, y)
                    child item
                    drag_name item
                    draggable True
                    droppable False