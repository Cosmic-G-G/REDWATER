# region Python
init python:
    class CircularBar(renpy.Displayable):
        def __init__(self, center: tuple, dimension: tuple, color, angle, widthBorder, colorBorder=None, msg="", **kwargs): 
            super(CircularBar, self).__init__(**kwargs)
            self.box = pygame.rect.Rect(center[0]-dimension[0], center[1]-dimension[1], dimension[0], dimension[1])
            
            self.color = color
            self.angle = angle
            self.widthBorder = widthBorder
            self.colorBorder = self.color if colorBorder is None else colorBorder
            self.msg = msg
            ## To increase size, redraw with new dimensions
        
        def arc(self, surface, start_angle, stop_angle, segments=None):
            segments = max(20, int(abs(stop_angle-start_angle)*max(self.box.width,self.box.height)/2)) if segments is None else segments
            step = (stop_angle - start_angle) / segments
            for i in range(segments):
                x1 = self.box.centerx + self.box.width*math.cos(start_angle + step*i)/2
                y1 = self.box.centery + self.box.height*math.sin(start_angle + step*i)/2
                x2 = self.box.centerx + self.box.width*math.cos(start_angle + step*(i+1))/2
                y2 = self.box.centery + self.box.height*math.sin(start_angle + step*(i+1))/2
                pygame.draw.line(surface, self.color, (x1, y1), (x2, y2), self.widthBorder)

        def render(self, width, height, st, at):
            rv = renpy.Render(width, height)
            surface = renpy.display.pgrender.surface((width, height), True)
            text = Text(self.msg, size=min(self.box.width//2, self.box.height//2), color=self.color)
            txtrender = renpy.display.render.render(text, width, height, st, at)
            self.arc(surface, 0, self.angle)
            rv.blit(txtrender, (self.box.centerx-txtrender.width//2,self.box.centery-txtrender.height//2))
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
                    self.allies.append(c)
                    self.enemyTarget = c
                else:
                    self.enemies.append(c)
                    self.allyTarget = c
                #renpy.block_rollback()
        
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

    class Combatant():
        def __init__(self, name, hp, atk, bAlly = True, scale = 100):
            self.name = name
            self.hp = hp
            self.maxhp = hp
            self.atk = atk
            self._bAlly = bAlly
            self.scale = scale

            self.dSprites: dict = { }
            self.sprites = SpriteManager(update=self.Uupdate, event=self.Uevent)

            self.n: dict = { }
            self.s: dict = { }
            self._updateFrequency = 0.1
            self.target = combatManager.allyTarget if bAlly else combatManager.enemyTarget
            self.tookDamage = {"val": False, "cooldown": 0.5}
            
            self.initialImages()

        def initialImages(self): #Override this function in inherited classes if different styling
            with open(renpy.loader.transfn("combatant_styling.txt"), "r") as cstyle:
                reader = csv.reader(cstyle, delimiter = ':')
                for row in reader:
                    if row[0] == self.name:
                        self.n.update({
                            "color": tuple(map(int, (row[3], row[4], row[5], row[6]))),
                            "pos": (0,self.scale),
                            "dimension": (self.scale,self.scale),
                            "width": int(row[7]),
                            "angle": 0,
                            "maxtime": float(row[15]),
                            "ctime": float(row[15])
                        })
                        self.s.update({
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

                        self.dSprites["normalattack"] = self.sprites.create(row[2] + ".jpg")
                        self.dSprites["specialattack"] = self.sprites.create(row[8] + ".jpg")
                        self.dSprites["base"] = self.sprites.create(row[1] + ".jpg")
                        break
            cstyle.close()

            self.dSprites["base"].x , self.dSprites["base"].y = self.scale/2 , 0
            self.dSprites["normalattack"].x , self.dSprites["normalattack"].y = 0 , self.scale
            self.dSprites["specialattack"].x , self.dSprites["specialattack"].y = self.scale , self.scale

        def Uupdate(self, st):
            def updateFromCM(): #Maybe find a way to only update this when a change occurs may improve performance
                self.target = combatManager.allyTarget if self._bAlly else combatManager.enemyTarget

            def updateCBars(frequency):
                self.n["ctime"] -= frequency
                self.s["ctime"] -= frequency

                if self.n["ctime"] <= 0:
                    self.n["angle"] = 2*math.pi 
                    self.n["ctime"] = self.n["maxtime"]
                    self.normalattack()
                else:
                    self.n["angle"] = 2*math.pi - ( self.n["ctime"]/self.n["maxtime"] * 2*math.pi )
                
                if self.s["ctime"] <= 0:
                    self.s["allowSA"] = True
                    self.s["angle"] = 2*math.pi
                    self.s["ctime"] = self.s["maxtime"]
                elif self.s["ctime"] > 0 and not self.s["allowSA"]:
                    self.s["angle"] = 2*math.pi - ( self.s["ctime"]/self.s["maxtime"] * 2*math.pi )
                else:
                    self.s["ctime"] = self.s["maxtime"]

            def updateHealth(frequency):
                self.tookDamage["cooldown"] -= frequency
                if self.tookDamage["cooldown"] <= 0:
                    self.tookDamage["cooldown"] = 0.5
                    self.tookDamage["value"] = False

                if self.hp <= 0:
                    combatManager.remove(self)
                    self.hp = self.maxhp
                    combatManager.eNextTarget() if self._bAlly else combatManager.aNextTarget()

            updateFromCM()
            updateCBars(self._updateFrequency)
            updateHealth(self._updateFrequency)
            return self._updateFrequency

        def Uevent(self, ev, x, y, st):
            if ev.type == 768:
                #print(self.s["allowSA"], ev.__dict__["unicode"], self.s["key"])
                if self.s["allowSA"] and ev.__dict__["unicode"] == self.s["key"]:
                    self.s["allowSA"] = False
                    self.specialattack()
        
        def specialattack(self):
            # Should be overwritten
            pass

        def normalattack(self):
            if self.target is not None:
                self.target.hp -= self.atk
                self.target.tookDamage["val"] = True
        
        @property
        def bAlly(self):
            return self._bAlly

        @bAlly.setter
        def bAlly(self, value):
            self._bAlly = value
            self.target = combatManager.allyTarget if value else combatManager.enemyTarget

    class MikaylaFighter(Combatant):
        def __init__(self, name, hp, atk, bAlly = True, scale = 100):
            super().__init__(name, hp, atk, bAlly, scale)

        def specialattack(self):
            if self.target is not None:
                self.target.hp -= self.atk * round(random.uniform(1.5, 3.0), 2)
                self.target.tookDamage["val"] = True

    class MizuFighter(Combatant):
        def __init__(self, name, hp, atk, bAlly = True, scale = 100):
            super().__init__(name, hp, atk, bAlly, scale)
        
        def specialattack(self):
            if combatManager.enemyTarget is not None:
                combatManager.enemyTarget.hp += self.atk
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
        add CircularBar((ally.scale*0.5, ally.scale*1.5), (ally.scale-ally.n["width"], ally.scale-ally.n["width"]), ally.n["color"], ally.n["angle"], ally.n["width"]):
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        add CircularBar((ally.scale*1.5, ally.scale*1.5), (ally.scale-ally.n["width"], ally.scale-ally.n["width"]), ally.s["color"], ally.s["angle"], ally.s["width"], msg=ally.s["key"]):
            pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
        if ally.tookDamage["val"]:
                bar value ally.hp range ally.maxhp:
                    xmaximum 2*ally.scale
                    pos ( i / ( len(combatManager.allies) + 1 ) , 0.6)
    
    for i, enemy in enumerate(combatManager.enemies , 1):
        add enemy.sprites:
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        add CircularBar((enemy.scale*0.5, enemy.scale*1.5), (enemy.scale-enemy.n["width"], enemy.scale-enemy.n["width"]), enemy.n["color"], enemy.n["angle"], enemy.n["width"]):
            pos ( i / ( len(combatManager.enemies) + 1 ) , 0.2)
        add CircularBar((enemy.scale*1.5, enemy.scale*1.5), (enemy.scale-enemy.n["width"], enemy.scale-enemy.n["width"]), enemy.s["color"], enemy.s["angle"], enemy.s["width"]):
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