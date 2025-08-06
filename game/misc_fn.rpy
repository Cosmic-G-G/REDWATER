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
#endregion