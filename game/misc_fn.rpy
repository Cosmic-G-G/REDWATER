#region FUNCTIONS
init python:
    def has_exited(event, interact=True, targetbg = None, **kwargs):
        if not interact:
            return

        if event == "show":
            #print(targetbg, PlayerVariables.location)
            if PlayerVariables.location != targetbg:
                renpy.return_statement()
    
    def default(event, interact=True, **kwargs):
            return

    def get_open_stories():
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
#endregion