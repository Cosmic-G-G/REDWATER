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
                        #endregion