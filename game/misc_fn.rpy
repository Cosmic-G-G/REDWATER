# Random code
#python:
    #    for c in [Mizu, Laela, Mirai, Mikayla, Chishiki]:
    #        label_name = f"{c.name}_story_{c.progress}"
    #        renpy.jump(label_name) if renpy.has_label(label_name) else None

#region FUNCTIONS
init python:
    def has_exited(event, interact=True, targetbg = None, **kwargs):
        if not interact:
            return

        if event == "show":
            #print(targetbg, Player.location)
            if Player.location != targetbg:
                renpy.return_statement()
    
    def default(event, interact=True, **kwargs):
        return

    def numpy_clip(value, minimum, maximum):
            if value > maximum:
                return maximum
            elif value < minimum:
                return minimum
            else:
                return value

    def pygame_draw_arc(surface, color, rect, start_angle, stop_angle, width=1, segments=None):
            segments = max(20, int(abs(stop_angle-start_angle)*max(rect.width,rect.height)/2)) if segments is None else segments
            step = (stop_angle - start_angle) / segments
            for i in range(segments):
                x1 = rect.centerx + rect.width*math.cos(start_angle + step*i)/2
                y1 = rect.centery + rect.height*math.sin(start_angle + step*i)/2
                x2 = rect.centerx + rect.width*math.cos(start_angle + step*(i+1))/2
                y2 = rect.centery + rect.height*math.sin(start_angle + step*(i+1))/2
                pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)
            return rect
#endregion