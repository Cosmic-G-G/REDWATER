init python:

    class UCharacter(ADVCharacter): # May need to check if persistent data is saved
        def __init__(self, name, kind=None, **properties):
            self.name = name
            super().__init__(self.name, kind, **properties)

            self.progress = 0
            self.affection = 0
            self.location = ""

    class PlayerVariables():
        def __init__(self):
            self.day = 0                                  # counter for each loop to not repeat stories
            self.canMove = False                          # disables movement
            self.inventory = []
            self.visited = set()
            self.showStoreBackDoor = False

default Mizu = UCharacter("Mizu")
default Laela = UCharacter("Laela")
default Mirai = UCharacter("Mirai")
default Mikayla = UCharacter("Mikayla")
default Chishiki = UCharacter("Chishiki")
default PlayerVariables = PlayerVariables()

layeredimage mizu:
    attribute only null

    group standing multiple variant "standing": #Anything layered onto the standing pose (weapons, accessories etc)
        #Furthest
        attribute pose1 default if_not "pose2"                                                             
        attribute pose2                                                                            #mizu_standing_pose2 <=> show mizu standing pose2 or show mizu pose2 until sitting/other implemented

        attribute robes default if_not "only"                                                      #show mizu (robes) mizu sweater (robes+sweater) mizu sweater only (sweater)
        attribute sweater pos(100,0)
    
    #group sitting multiple:
    #    attribute robes

    group face auto:
        pos(50,50)
        attribute neutral default                                                                   #mizu_face_neutral