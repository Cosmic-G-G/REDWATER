init:
                        #region TRANSFORMS
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