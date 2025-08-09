init python:
    class UCharacter(ADVCharacter): # May need to check if persistent data is saved
        def __init__(self, name, kind=None, **properties):
            self.name = name
            super().__init__(self.name, kind, **properties)

            self.progress = 0
            self.affection = 0
            self.location = ""

    class PlayerVariables:
        def __init__(self):
            self.day = 0                                  # counter for each loop to not repeat stories
            self.canMove = False                          # disables movement
            self.inventory = []
            self.visited = set()
            self.showStoreBackDoor = False

    def get_open_stories_from_file():
        ret = dict()
        with open(renpy.loader.transfn("story_flags.txt"), "r") as stories:
            reader = csv.reader(stories, delimiter = ',')
            
            for row in reader:
                ret[row[0]] = row[1] #{"label_name": "location"}
                for item in row[2:]:
                    obj = item.split('=')[0].split('.')[0]
                    attr = item.split('=')[0].split('.')[1]
                    value = item.split('=')[1]
                    if (str(getattr(globals()[obj], attr)) != value):
                        ret.pop(row[0])
                        break
        stories.close()
        return ret
    
    def get_open_stories():
        ret = dict() 
        ret['Mizu_story_0'] = 'beach' if Mizu.progress == 0 else None #if exit or block the exit with mizu
        ret['Laela_story_0'] = 'school' if Laela.progress == 0 else None #No call stack local jump
        ret['Mirai_story_0'] = 'classroom' if Mirai.progress == 0 else None
        ret['Mikayla_story_0'] = 'store' if Mikayla.progress == 0 and Laela.progress > 0 else None
        ret['Mikayla_story_1'] = 'forest' if Mikayla.progress == 1 else None
        ret['Chishiki_story_0'] = 'park' if Chishiki.progress == 0 and (0 not in (Laela.progress, Mirai.progress, Mizu.progress)) and Mikayla.progress == 2 else None
        ret['endOfDay'] = 'beach' if Player.day == 0 and (0 not in (Laela.progress, Mirai.progress, Mizu.progress)) and Mikayla.progress == 2 else None
        ret['Laela_story_1'] = 'beach' if Player.day == 1 and Laela.progress == 1 else None
        return ret

default Mizu = UCharacter("Mizu")
default Laela = UCharacter("Laela")
default Mirai = UCharacter("Mirai")
default Mikayla = UCharacter("Mikayla")
default Chishiki = UCharacter("Chishiki")
default Player = PlayerVariables()

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