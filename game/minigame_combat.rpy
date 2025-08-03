# region Python
init python:
    class CircularBar(renpy.Displayable):
        def __init__(self, color, center: tuple, dimension: tuple, barWidth, angle, colorBorder = 0, widthBorder = 0, **kwargs): #TODO priority-low: colorBorder widthBorder
            super(CircularBar, self).__init__(**kwargs)
            self.center = center
            self.dimension = dimension
            self.barWidth = barWidth

            self.angle = angle

            self.color = color
            self.colorBorder = colorBorder
            self.widthBorder = widthBorder
        
        def arc(self, surface, color, rect, angle_start, angle_stop, width=1): #TODO priority-mid: Make into module
            x = rect.x
            y = rect.y
            radius1 = rect.w
            radius2 = rect.h

            if (radius1 < radius2):
                if radius1 < 1.0e-4:
                    aStep = 1.0
                else:
                    aStep = math.asin(2.0 / radius1)
            else:
                if radius2 < 1.0e-4:
                    aStep = 1.0
                else:
                    aStep = math.asin(2.0 / radius2)
            
            if (aStep < 0.05):
                aStep = 0.05
            
            x_last = int( x + math.cos(angle_start) * radius1)
            y_last = int( y - math.sin(angle_start) * radius2)

            a = float ( angle_start + aStep )
            while a < aStep + angle_stop:
                a += aStep

                points = [0,0,0,0]
                x_next = int ( x + math.cos(min(a, angle_stop)) * radius1)
                y_next = int ( y - math.sin(min(a, angle_stop)) * radius2)
                points[0] = x_last
                points[1] = y_last
                points[2] = x_next
                points[3] = y_next

                pygame.draw.line(surface, color, (points[0], points[1]), (points[2], points[3]), width)
                x_last = x_next
                y_last = y_next

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            surface = renpy.display.pgrender.surface((width, height), True)

            self.arc(surface, self.color, pygame.rect.Rect(*self.center, *self.dimension), 0, self.angle, width = self.barWidth)
            rv.blit(surface, (0,0))

            return rv  

    class CombatManager():
        def __init__(self):
            self.allies: list = [ ]
            self.enemies: list = [ ]
            self.returnLabel = "ilikeyourstylebrat.doneBattle" #This just needs to be one that does exist to prevent screen prediction bugs
            self.outcome = None
            self.allyTarget = None
            self.enemyTarget = None

        def add(self, *combatants):
            for c in combatants:
                if c.bAlly:
                    self.allies.append ( c )
                    self.enemyTarget = c
                else:
                    self.enemies.append ( c )
                    self.allyTarget = c
                renpy.block_rollback()
        
        def remove(self, *combatants):
            if combatants == ("all",):
                self.allies.clear()
                self.enemies.clear()
                return

            for combatant in combatants:
                try:
                    self.allies.remove(combatant)
                except:
                    self.enemies.remove(combatant)

        def aNextTarget(self):
            try:
                self.allyTarget = next(self.enemies)
            except:
                self.allyTarget = self.enemies[0] if self.enemies else None
        
        def eNextTarget(self):
            try:
                self.enemyTarget = next(self.allies)
            except:
                self.enemyTarget = self.allies[0] if self.allies else None
        
        def __str__():
            return "for debugging"

    class Combatant():
        def __init__(self, name, hp, atk, bAlly = True, scale = 100):
            self.name = name
            self.hp = hp
            self.atk = atk
            self.bAlly = bAlly
            self.scale = scale

            self._dSprites: dict = { }
            self._lspriteManager = SpriteManager(update=self.Uupdate, event=self.Uevent)
            self._naBar: dict = { }
            self._saBar: dict = { }
            self._updateFrequency = 0.1
            self._target = combatManager.allyTarget if bAlly else combatManager.enemyTarget
            self._maxhp = hp
            self._tookDamage = {"val": False, "cooldown": 0.5}
            
            self.initialImages()

        def initialImages(self): #Override this function in inherited classes if different styling
            with open(renpy.loader.transfn("combatant_styling.txt"), "r") as cstyle:
                reader = csv.reader(cstyle, delimiter = ':')
                for row in reader:
                    #print(row)
                    if row[0] == self.name:
                        self._naBar.update({
                            "color": tuple(map(int, (row[3], row[4], row[5], row[6]))),
                            "pos": (0,self.scale),
                            "dimension": (self.scale,self.scale),
                            "width": int(row[7]),
                            "angle": 0,
                            "maxtime": float(row[15]),
                            "ctime": float(row[15])
                        })
                        self._saBar.update({
                            "color": tuple(map(int, (row[9], row[10], row[11], row[12]))),
                            "pos": (self.scale,self.scale),
                            "dimension": (self.scale,self.scale),
                            "width": int(row[13]),
                            "angle": 2*math.pi,
                            "maxtime": float(row[16]),
                            "ctime": float(row[16]),
                            "key": row[14],
                            "allowSA": True
                        })

                        self._dSprites["normalattack"] = self._lspriteManager.create(row[2] + ".jpg")
                        self._dSprites["specialattack"] = self._lspriteManager.create(row[8] + ".jpg")
                        self._dSprites["base"] = self._lspriteManager.create(row[1] + ".jpg")
                        break
            cstyle.close()

            self._dSprites["base"].x , self._dSprites["base"].y = self.scale/2 , 0
            self._dSprites["normalattack"].x , self._dSprites["normalattack"].y = 0 , self.scale
            self._dSprites["specialattack"].x , self._dSprites["specialattack"].y = self.scale , self.scale

        def Uupdate(self, st):
            def updateFromCM(): #Maybe find a way to only update this when a change occurs may improve performance
                self._target = combatManager.allyTarget if self.bAlly else combatManager.enemyTarget

            def updateCBars(frequency):
                self._naBar["ctime"] -= frequency
                self._saBar["ctime"] -= frequency

                if self._naBar["ctime"] <= 0:
                    self._naBar["angle"] = 2*math.pi 
                    self._naBar["ctime"] = self._naBar["maxtime"]
                    self.normalattack()
                else:
                    self._naBar["angle"] = 2*math.pi - ( self._naBar["ctime"]/self._naBar["maxtime"] * 2*math.pi )
                
                if self._saBar["ctime"] <= 0:
                    self._saBar["allowSA"] = True
                    self._saBar["angle"] = 2*math.pi
                    self._saBar["ctime"] = self._saBar["maxtime"]
                elif self._saBar["ctime"] > 0 and not self._saBar["allowSA"]:
                    self._saBar["angle"] = 2*math.pi - ( self._saBar["ctime"]/self._saBar["maxtime"] * 2*math.pi )
                else:
                    self._saBar["ctime"] = self._saBar["maxtime"]

            def updateHealth(frequency):
                self._tookDamage["cooldown"] -= frequency
                if self._tookDamage["cooldown"] <= 0:
                    self._tookDamage["cooldown"] = 0.5
                    self._tookDamage["value"] = False

                if self.hp <= 0:
                    combatManager.remove(self)
                    self.hp = self._maxhp

                    combatManager.eNextTarget() if self.bAlly else combatManager.aNextTarget()

            updateFromCM()
            updateCBars(self._updateFrequency)
            updateHealth(self._updateFrequency)
            return self._updateFrequency

        def Uevent(self, ev, x, y, st):
            if ev.type == 768:
                #print(self._saBar["allowSA"], ev.__dict__["unicode"], self._saBar["key"])
                if self._saBar["allowSA"] and ev.__dict__["unicode"] == self._saBar["key"]:
                    self._saBar["allowSA"] = False
                    self.specialattack()
        
        def specialattack(self):
            # Should be overwritten
            pass

        def normalattack(self):
            if self._target is not None:
                self._target.hp -= self.atk
                self._target.tookDamage["val"] = True
        
        def safechange(self, bAlly = None):
            self.bAlly = not self.bAlly if bAlly == None or bAlly != self.bAlly else self.bAlly
            self._target = combatManager.allyTarget if bAlly else combatManager.enemyTarget

        @property
        def sprites(self):
            return self._lspriteManager
        @property
        def n(self):
            return self._naBar
        @property
        def s(self):
            return self._saBar
        @property
        def maxhp(self):
            return self._maxhp
        @property
        def tookDamage(self):
            return self._tookDamage

    class MikaylaFighter(Combatant):
        def __init__(self, name, hp, atk, bAlly = True, scale = 100):
            super().__init__(name, hp, atk, bAlly, scale)

        def specialattack(self):
            if self._target is not None:
                self._target.hp -= self.atk * round(random.uniform(1.5, 3.0), 2)
                self._target.tookDamage["val"] = True

    class MizuFighter(Combatant):
        def __init__(self, name, hp, atk, bAlly = True, scale = 100):
            super().__init__(name, hp, atk, bAlly, scale)
        
        def specialattack(self):
            if combatManager.enemyTarget is not None:
                combatManager.enemyTarget.hp += self.atk
    
    class Journal():
        def __init__(self, entry = []):
            self.entry = []

        def addEntry(self, newEntry):
            self.entry.append(newEntry)
        
        def getEntry(self):
            fullEntry = " ".join(self.entry)
            return fullEntry
# endregion

# region Ren'py

default combatManager = CombatManager()
default user = Combatant("Player", 300, 30)
default mikaylaFighter = MikaylaFighter("Mikayla", 400, 100)
default mizuFighter = MizuFighter("Mizu", 350, 40)
default enemy = Combatant("Player", 1500, 30, bAlly = False)

label Battle:
    $ renpy.pause()
    $ renpy.block_rollback()
    jump Battle

screen combat():
    tag combat
    timer 0.1 repeat True action Show("combat")
    on "hide" action Hide("combat")
    add color("00000088")

    for i, ally in enumerate(combatManager.allies, 1):
        add ally.sprites:
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        add CircularBar(ally.n["color"], (ally.scale*0.5, ally.scale*1.5), (ally.scale*0.5-ally.n["width"], ally.scale*0.5-ally.n["width"]), ally.n["width"], ally.n["angle"]):
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        add CircularBar(ally.s["color"], (ally.scale*1.5, ally.scale*1.5), (ally.scale*0.5-ally.n["width"], ally.scale*0.5-ally.n["width"]), ally.s["width"], ally.s["angle"]):
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        if ally.tookDamage["val"]:
                bar value ally.hp range ally.maxhp:
                    xmaximum 2*ally.scale
                    pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
    
    for i, enemy in enumerate(combatManager.enemies , 1):
        add enemy.sprites:
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        add CircularBar(enemy.n["color"], (enemy.scale*0.5, enemy.scale*1.5), (enemy.scale*0.5-enemy.n["width"], enemy.scale*0.5-enemy.n["width"]), enemy.n["width"], enemy.n["angle"]):
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        add CircularBar(enemy.s["color"], (enemy.scale*1.5, enemy.scale*1.5), (enemy.scale*0.5-enemy.n["width"], enemy.scale*0.5-enemy.n["width"]), enemy.s["width"], enemy.s["angle"]):
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        if enemy.tookDamage["val"]:
            bar value enemy.hp range enemy.maxhp:
                xmaximum 2*enemy.scale
                pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
    python:
        if combatManager.allies == [] or combatManager.enemies == []:
            renpy.hide_screen("combat")
            ui.close()
            renpy.jump(combatManager.returnLabel)
#endregion