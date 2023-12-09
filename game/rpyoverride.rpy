init:
                        #region OVERRIDE
    screen choice(items):
        style_prefix "choice"

        vbox:
            for i in items:
                if i.caption[:3] == "<L>":
                    textbutton i.caption[3:] action None
                else:
                    textbutton i.caption action i.action
    
    screen mundanechoice(items, cd):
        timer cd repeat False action Return(None)
        style_prefix "choice"

        vbox:
            for i in items:
                textbutton i hovered Return(i) action NullAction()
                        #endregion