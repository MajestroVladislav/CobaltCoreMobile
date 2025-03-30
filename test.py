from pygame import *
from pygame.locals import *
import random
# import os
import time as t

# Установка режима полноэкранного
sc = display.set_mode((0, 0), FULLSCREEN)
info = display.Info()
screenWidth = info.current_w
screenHeight = info.current_h

if screenWidth == 1920:
    scale = 4
    font.init()
    font = font.Font(None, 40)
else:
    scale=2.55
    font.init()
    font = font.Font(None, 27)

def loads(path):
    im = image.load(path)
    # Масштабируем изображение
    scaled_width = min(im.get_width(), screenWidth)
    scaled_height = min(im.get_height(), screenHeight)
    return transform.scale(im, (int(scaled_width*scale), int(scaled_height*scale)))

def button(img, x, y):
    mouse_pos = mouse.get_pos()
    button_rect = img.get_rect(topleft=(
        int(x * scale) + screenWidth // 2 - img.get_width() // 2,
        int(y * scale) + screenHeight // 2 - img.get_height() // 2
    ))
    return button_rect.collidepoint(mouse_pos)

def pixi(img, x, y, current=sc):
    if img is not None:
        current.blit(img, (int(x * scale) + current.get_width() // 2 - img.get_width() // 2,
                           int(y * scale) + current.get_height() // 2 - img.get_height() // 2))


def recolor(img):
    filter_color = (52, 78, 186)  # RGB для #344eba
    filter_surface = Surface(img.get_size())
    filter_surface.fill(filter_color)
    filtered_image = img.copy()
    filtered_image.blit(filter_surface, (0, 0), special_flags=BLEND_RGBA_MULT)
    return filtered_image

dizzy = loads("sprites/cards/dizzy.png")
border_dizzy = loads("sprites/cards/border_dizzy.png")

def ee(**k):
    f={"Урон":[],"Усиление":["",0],"Движ":-666,"Ото":[""],"Щит":[0,0],"Вщит":[0,0],"Выпуск":[" ",0],"Разд":[0,0],"Дебаф":["",0],"ЭфУрон":[0,0,"",0]}
    for key,v in k.items():
        f[key]=v
    return f
def ene(name,h=0,ef={"🔶":0},midl=[],sdwig=0,sship=[]):
    if name == "CCD-19 Cicada":
        if h!=0:
            if h % 2 == 1:
                return ee(Урон=[2 + ef["🔶"], 0])
            if h % 2 == 0:
                return ee(Усиление=["🔶", 1], Щит=[2, 3], Движ=0)
        return {"Имя": "Беспилотник Цикада", "Кабина": [1], "Отсек": [3], "Пушка": [2], "Остальное": [0, 4],
                "Твёрд": [0, 1, 2, 3, 4], "Броня": [], "Уязвимость": [], "Трещина": [],
                "Спрайты": (chassis_cicada, wing_cicada, missiles_cicada, cannon_cicada, cockpit_cicada,  wing_cicada_mir), "Корпус": 8, "Щит": 4}


class card:
    def __init__(self, **k):
        f = {"имя": "", "выпуск": " ", "манёвр": 0, "вщит": 0, "щит": 0, "урон": -1, "цена": 1, "перс": "", "доп": "",
             "статус": {"🔶": 0, "🥾": 0, "⭐": 0, "↩": 0, "↪": 0, "🚘": 0, "🌈": 0, "🫧": 0, "💾": 0, "🩸": 0, "📗": 0, "🧧": 0,
                        "<🟢>": 0, "🔫": 0, "⚡": 0, "⏰": 0, "🛑": 0, "🔥": 0, "🛡": 0, "🅿": 0, "🚀": 0, "🦠": 0, "": 0, "♦": 0,
                        "⇫": 0, "⊥": 0, "🥇": 0, "🧱": 0, "🪨": 0, "😇": 0, "✈": 0, "🕸": 0, "▩": 0, "🪑": 0, "⌚": 0,
                        "Добор": 0},
             "встатус": {"🔶": 0, "🥾": 0, "⭐": 0, "↩": 0, "↪": 0, "🚘": 0, "🌈": 0, "🫧": 0, "💾": 0, "🩸": 0, "📗": 0, "🧧": 0,
                         "<🟢>": 0, "🔫": 0, "⚡": 0, "⏰": 0, "🛑": 0, "🔥": 0, "🛡": 0, "🅿": 0, "🚀": 0, "🦠": 0, "": 0,
                         "♦": 0, "⇫": 0, "⊥": 0, "🥇": 0, "🧱": 0, "🪨": 0, "😇": 0, "✈": 0, "🕸": 0, "▩": 0, "🪑": 0,
                         "⌚": 0}}
        for key, v in k.items():
            f[key] = v
        self.имя = f["имя"]
        self.урон = f["урон"]
        self.щит = f["щит"]
        self.манёвр = f["манёвр"]
        self.вщит = f["вщит"]
        self.выпуск = f["выпуск"]
        self.цена = f["цена"]
        self.статус = f["статус"]
        self.встатус = f["встатус"]
        self.доп = f["доп"]
        self.перс = f["перс"]

    def show(self, x, y, e=None):
        if e is None:
            e = {"🔶": 0, "🥾": 0, "⭐": 0, "↩": 0, "↪": 0, "🚘": 0, "🌈": 0, "🫧": 0, "💾": 0, "🩸": 0, "📗": 0, "🧧": 0,
                 "<🟢>": 0, "🔫": 0, "⚡": 0, "⏰": 0, "🛑": 0, "🔥": 0, "🛡": 0, "🅿": 0, "🚀": 0, "🦠": 0, "": 0, "♦": 0,
                 "⇫": 0, "⊥": 0, "🥇": 0, "🧱": 0, "🪨": 0, "😇": 0, "✈": 0, "🕸": 0, "▩": 0, "🪑": 0, "⌚": 0,
                 "Добор": 0}
        t = {"Урон": None, "Щит": None, "Манёвр": None, "Вщит": None, "Выпуск": None, "🔶": None, "🥾": None, "⭐": None,
             "↩": None, "↪": None, "🚘": None, "🌈": None, "🫧": None, "💾": None, "🩸": None, "📗": None, "🧧": None,
             "<🟢>": None, "🔫": None, "⚡": None, "⏰": None, "🛑": None, "🔥": None, "🛡": None, "🅿": None, "🚀": None,
             "🦠": None, "♦": None, "⇫": None, "⊥": None, "🥇": None, "🧱": None, "🪨": None, "😇": None, "✈": None,
             "🕸": None, "▩": None, "🪑": None, "⌚": None, "Добор": None, "Доп": None}
        if self.урон > -1:
            t["Урон"]=self.урон + e["🔶"] + e["♦"]
        if self.щит > 0:
            t["Щит"] = self.щит
        if self.манёвр > 0:
            t["Манёвр"] = self.манёвр
        if self.вщит > 0:
            t["Вщит"] = self.вщит
        if self.выпуск != " ":
            t += str(self.выпуск)
        for key, v in self.статус.items():
            if v != 0:
                t[key] = v
        for key, v in self.встатус.items():
            if v != 0:
                t[key] = v
        if self.доп != "":
            t["Доп"] = self.доп
        a = 0
        for key, v in t.items():
            if t[key] is not None:
                a += 1

        if self.перс == "Диззи" or True:
            cr = Surface(border_dizzy.get_size())
            pixi(dizzy,0,0,cr)
            pixi(border_dizzy, 0, 0, cr)

        q = 1
        text=self.имя.split()
        for i in range(len(text)):
            if i!=len(text)-1:
                if len(text[i+1])+len(text[i])<12:
                    namec = font.render(text[i]+" "+text[i+1], True, (0, 0, 0))
                    cr.blit(namec,(7,5))
                    i+=1
                else:
                    namec = font.render(text[i], True, (0, 0, 0))
                    cr.blit(namec, (7, 5))
                    namec = font.render(text[i+1], True, (0, 0, 0))
                    cr.blit(namec, (7, 30))
        for key, v in t.items():
            if t[key] is not None and key != "Доп":
                # Проверка, что kartinka[key] загружен
                if kartinka[key] is not None:
                    pixi(kartinka[key], -4, 12 * q - a*6//2 - a*2, cr)
                    namec = font.render(str(t[key]), True, (255, 255, 255))
                    pixi(namec, 4, 12 * q - a * 6 // 2 - a * 2, cr)
                    q += 1
        cr.blit(font.render(str(self.цена), True, (255, 255, 255)), (20, 80))
        pixi(cr, x, y)

cards=(card(перс="Киса",имя="Базовый выстрел",урон=1,статус={"🔶":1}),card(перс="Киса",имя="Базовый щит",щит=1,урон=1,манёвр=1,вщит=1),card(перс="Киса",имя="Базовый манёвр",манёвр=1),card(перс="Диззи",имя="Большой щит",щит=3,цена=2,статус={"♦":1}),card(перс="Диззи",имя="Блокирующий выстрел",урон=1,вщит=1))

mock_zone_first = loads("sprites/mock_zone_first.png")
cockpit = loads("sprites/cockpit.png")

chassis_boxy = loads("sprites/chassis_boxy.png")
cannon_artemis = loads("sprites/cannon_artemis.png")
cockpit_artemis = loads("sprites/cockpit_artemis.png")
missiles_artemis = loads("sprites/missiles_artemis.png")
wing_player = loads("sprites/wing_player.png")
wing_player_mir = loads("sprites/wing_player_mir.png")

startCombat = loads("sprites/icons/startCombat.png")
shield = loads("sprites/icons/shield.png")
evade = loads("sprites/icons/evade.png")
tempShield=loads("sprites/icons/tempShield.png")
powerdrive=loads("sprites/icons/powerdrive.png")
overdrive=loads("sprites/icons/overdrive.png")
ace=loads("sprites/icons/ace.png")
hermes=loads("sprites/icons/hermes.png")
autododgeLeft=loads("sprites/icons/autododgeLeft.png")
autododgeRight=loads("sprites/icons/autododgeRight.png")
heat=loads("sprites/icons/heat.png")
loseEvadeNextTurn=loads("sprites/icons/loseEvadeNextTurn.png")
payback=loads("sprites/icons/payback.png")
tempPayback=loads("sprites/icons/tempPayback.png")
boost=loads("sprites/icons/boost.png")
backwardsMissiles=loads("sprites/icons/backwardsMissiles.png")
corrode=loads("sprites/icons/corrode.png")
endlessMagazine=loads("sprites/icons/endlessMagazine.png")
energyLessNextTurn=loads("sprites/icons/energyLessNextTurn.png")
energyNextTurn=loads("sprites/icons/energyNextTurn.png")
drawLessNextTurn=loads("sprites/icons/drawLessNextTurn.png")
drawNextTurn=loads("sprites/icons/drawNextTurn.png")
drawCard=loads("sprites/icons/drawCard.png")
autopilot=loads("sprites/icons/autopilot.png")
bubbleShield=loads("sprites/icons/bubbleShield.png")
mitosis=loads("sprites/icons/mitosis.png")
quarry=loads("sprites/icons/quarry.png")
serenity=loads("sprites/icons/serenity.png")
stunCharge=loads("sprites/icons/stunCharge.png")
stunSource=loads("sprites/icons/stunSource.png")
tableFlip=loads("sprites/icons/tableFlip.png")
timeStop=loads("sprites/icons/timeStop.png")
engineStall=loads("sprites/icons/engineStall.png")
strafe=loads("sprites/icons/strafe.png")
cleanExhaust=loads("sprites/icons/cleanExhaust.png")
libra=loads("sprites/icons/libra.png")
droneShift=loads("sprites/icons/droneShift.png")
perfectShield=loads("sprites/icons/perfectShield.png")
rockFactory=loads("sprites/icons/rockFactory.png")
hurtBlockable=loads("sprites/icons/hurtBlockable.png")

status_bg=loads("sprites/icons/status_bg.png")

m_r = loads("sprites/move_right.png")
lif = loads("sprites/life.png")
lif_cr = loads("sprites/life_corner_r.png")
lif_cl = loads("sprites/life_corner_l.png")
lif_net = loads("sprites/life_net.png")
shild = loads("sprites/shild.png")
shild_net = loads("sprites/shild_net.png")
shild_corner = loads("sprites/shild_corner.png")
vshild = loads("sprites/vshild.png")

cannon_cicada = loads("sprites/ememy/cannon_cicada.png")
chassis_cicada = loads("sprites/ememy/chassis_cicada.png")
cockpit_cicada = loads("sprites/ememy/cockpit_cicada.png")
wing_cicada = loads("sprites/ememy/wing_cicada.png")
wing_cicada_mir = loads("sprites/ememy/wing_cicada_mir.png")
missiles_cicada = loads("sprites/ememy/missiles_artemis.png")

energy = loads("sprites/energy.png")
deck = loads("sprites/deck.png")
exhaust = loads("sprites/exhaust.png")
base_gray = loads("sprites/base_gray.png")
menu_menu = loads("sprites/menu.png")
char_dizzy = loads("sprites/char_dizzy.png")
char_compOffline_mini = loads("sprites/char_compOffline_mini.png")
char_enemy = loads("sprites/char_enemy.png")
enemy_ship_name = loads("sprites/enemy_ship_name.png")

dizzy_neutral = loads("sprites/dizzy_neutral_0.png")
scrap_neutral = loads("sprites/scrap_neutral_0.png")
comp_mini = loads("sprites/comp_mini_0.png")

hint_shield=loads("sprites/hints/hint_shield.png")

kartinka = {"Урон": startCombat, "Щит": shield, "Манёвр": evade, "Вщит": tempShield, "Выпуск": None, "🔶": powerdrive, "🥾": hermes, "⭐": ace,
             "↩": autododgeRight, "↪": autododgeLeft, "🚘": autopilot, "🌈": boost, "🫧": bubbleShield, "💾": cleanExhaust, "🩸": corrode, "📗": drawNextTurn, "🧧": drawLessNextTurn,
             "<🟢>": droneShift, "🔫": endlessMagazine, "⚡": energyNextTurn, "⏰": energyLessNextTurn, "🛑": engineStall, "🔥": heat, "🛡": libra, "🅿": loseEvadeNextTurn, "🚀": backwardsMissiles,
             "🦠": mitosis, "♦": overdrive, "⇫": tempPayback, "⊥": payback, "🥇": perfectShield, "🧱": hurtBlockable, "🪨": rockFactory, "😇": serenity, "✈": strafe,
             "🕸": stunCharge, "▩": stunSource, "🪑": tableFlip, "⌚": timeStop, "Добор": drawCard, "Доп": None}

def battle(sship,life,mlife,colod,razm,nam,mdefe,defe,re):
    FPS = 60
    clock = time.Clock()

    hod = 0
    mener = 3

    sdwig = 0

    vs = ene(nam)
    enemy_ship = vs["Спрайты"]
    hp = mhp = vs["Корпус"]
    bron = mbron = vs["Щит"]

    r = razm
    ha = []
    sbros = []
    burn = []
    vta = colod.copy()
    vustrel_flag = 0
    s = 999

    ef={"🔶": 0, "🥾": 0, "⭐": 0, "↩": 0, "↪": 0, "🚘": 0, "🌈": 0, "🫧": 0, "💾": 0, "🩸": 0, "📗": 0, "🧧": 0,
        "<🟢>": 0, "🔫": 0, "⚡": 0, "⏰": 0, "🛑": 0, "🔥": 0, "🛡": 0, "🅿": 0, "🚀": 0, "🦠": 0, "": 0, "♦": 0,
        "⇫": 0, "⊥": 0, "🥇": 0, "🧱": 0, "🪨": 0, "😇": 0, "✈": 0, "🕸": 0, "▩": 0, "🪑": 0, "⌚": 0, "Добор": 0}
    manevr=0

    fon = Surface(sc.get_size())
    fon.fill((255, 255, 255))
    pixi(mock_zone_first, 0, 0, fon)
    pixi(recolor(cockpit), 0, 0, fon)
    pixi(energy, -220, 110, fon)
    pixi(deck, -185, 110, fon)
    pixi(recolor(base_gray), 205, 115, fon)
    pixi(font.render("Конец хода", True, (255, 255, 255)), 205, 114, fon)
    pixi(deck, 221, 78, fon)
    pixi(exhaust, 190, 84, fon)
    pixi(chassis_boxy, -1, 35, fon)
    pixi(cannon_artemis, 0, 10, fon)
    pixi(cockpit_artemis, 16, 10, fon)
    pixi(missiles_artemis, -16, 10, fon)
    pixi(wing_player, -32, 10, fon)
    pixi(transform.flip(wing_player, True, False), 32, 10, fon)
    pixi(m_r, 64, 10, fon)
    pixi(transform.flip(m_r, True, False), -64, 10, fon)
    pixi(menu_menu, -215, -125, fon)
    pixi(char_dizzy, -204, 50, fon)
    pixi(dizzy_neutral, -204, 50, fon)
    pixi(font.render("Диззи", True, (255, 255, 255)), -204-15, 50-24, fon)
    pixi(char_dizzy, -204, -10, fon)
    pixi(dizzy_neutral, -204, -10, fon)
    pixi(font.render("Диззи", True, (255, 255, 255)), -204-15, -10-24, fon)
    pixi(char_dizzy, -204, -70, fon)
    pixi(dizzy_neutral, -204, -70, fon)
    pixi(font.render("Диззи", True, (255, 255, 255)), -204-15, -70-24, fon)
    pixi(char_compOffline_mini, -160, -120, fon)
    pixi(comp_mini, -129, -104, fon)
    pixi(font.render("Cat.exe", True, (255, 255, 255)), -160, -120-11, fon)
    pixi(char_enemy, 203, -84, fon)
    pixi(scrap_neutral, 203, -84, fon)
    pixi(font.render("X.09", True, (200, 0, 0)), 203-20, -84-24, fon)
    pixi(enemy_ship_name, 204, -120, fon)
    pixi(font.render(nam, True, (255, 255, 255)), 202, -120, fon)


    while (hp>0 and life>0):
        ener = mener
        hod += 1
        vdefe = 0
        random.shuffle(vta)
        random.shuffle(sbros)
        if len(vta) < r:
            for i in range(len(vta)):
                ha.append(vta.pop(0))
            vta.extend(sbros)
            sbros = []
            while len(ha) < r and len(vta) != 0:
                ha.append(vta.pop(0))
        else:
            for i in range(r):
                ha.append(vta.pop(0))
        end = True
        while (hp>0 and life>0 and end):
            pixi(fon, 0, 0)
            pixi(font.render(str(ener), True, (255, 255, 255)), -220, 110)
            pixi(font.render(str(len(sbros)), True, (255, 255, 255)), 212, 89)
            pixi(font.render(str(len(vta)), True, (255, 255, 255)), -194, 121)
            pixi(font.render(str(len(burn)), True, (255, 255, 255)), 185, 89)

            twerd = []
            for i in vs["Твёрд"]:
                twerd.append(-(len(vs["Твёрд"])-1)*8 + i * 16 + sdwig * 16)

            for i in range(len(enemy_ship)):
                if i == 0:
                    pixi(enemy_ship[0], -1 - sdwig * 16, -105)
                else:
                    pixi(enemy_ship[i], -(len(enemy_ship))*8 + i * 16 - sdwig * 16, -75)

            for i in range(len(ene(nam,hod)["Урон"])//2):
                alpha_surface = Surface(sc.get_size(), SRCALPHA)
                x = vs["Пушка"][ene(nam,hod)["Урон"][2*i+1]] * 16 - (len(enemy_ship)-2)*8 + i * 16 - sdwig * 16
                y = -5
                if (vs["Пушка"][ene(nam,hod)["Урон"][2*i+1]] - sdwig - 2) in range(-2,3):
                    mimo = 0
                else:
                    mimo = 55
                draw.lines(alpha_surface,(200,20,0,150),True,((int(x * scale) + screenWidth//2, int((y-55) * scale) + screenHeight//2),
                                                              (int(x * scale) + screenWidth//2, int((y+mimo) * scale) + screenHeight//2)), int(16 * scale))
                pixi(alpha_surface, 0, 0)
                pixi(font.render(str(ene(nam,hod)["Урон"][2*i]), True, (230, 10, 0)),x,y-42)
            if ene(nam, hod)["Щит"]!=[0,0]:
                for qqq in range(len(ene(nam, hod)["Щит"])//2):
                    pixi(hint_shield, -(len(enemy_ship))*8 + (ene(nam, hod)["Щит"][2 * qqq + 1]+1) * 16 - sdwig * 16, -75)

            statusOtstup=0
            statusk=0

            for key, v in ef.items():
                if v!=0:
                    statusOtstup+=1
            if manevr>0:
                statusOtstup += 1
            for key, v in ef.items():
                if v != 0:
                    statusk+=1
                    pixi(status_bg,- 6.5 - 8.5*statusOtstup + 17*statusk - statusOtstup,36)
                    pixi(kartinka[key],-2 - 6.5 - 8.5*statusOtstup + 17*statusk - statusOtstup,36)
                    pixi(font.render(str(v), True, (255, 255, 255)), 4 - 6.5 - 8.5*statusOtstup + 17*statusk - statusOtstup, 36)
            if manevr>0:
                statusk += 1
                pixi(status_bg,- 6.5 - 8.5*statusOtstup + 17*statusk - statusOtstup, 36)
                pixi(evade,-2 - 6.5 - 8.5*statusOtstup + 17*statusk - statusOtstup,36)
                pixi(font.render(str(manevr), True, (255, 255, 255)),4 - 6.5 - 8.5*statusOtstup + 17*statusk - statusOtstup,36)

            j = 0  # Отрисовка хп врага
            while j < hp:
                pixi(lif, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                if j == 0:
                    pixi(lif_cl, - 3 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                    pixi(lif_cr, (mhp - 1) * 4 - (mhp + mbron - 1) * 2 + 2 - sdwig * 16, -96)
                j += 1
            while j < mhp:
                pixi(lif_net, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                j = j + 1
            while j < mhp + bron:
                pixi(shild, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                j = j + 1
            while j < mhp + mbron:
                pixi(shild_net, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                j = j + 1
            while j < mhp + mbron + vbron:
                pixi(vshild, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                j = j + 1
            if mbron > 0 or vdefe > 0:
                pixi(shild_corner, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16 - 2, -96)

            j = 0  # Отрисовка хп
            while j < life:
                pixi(lif, j * 4 - (mlife + mdefe - 1) * 2, 26)
                if j == 0:
                    pixi(lif_cl, - 3 - (mlife + mdefe - 1) * 2, 26)
                    pixi(lif_cr, (mlife - 1) * 4 - (mlife + mdefe - 1) * 2 + 2, 26)
                j = j + 1
            while j < mlife:
                pixi(lif_net, j * 4 - (mlife + mdefe - 1) * 2, 26)
                j = j + 1
            while j < mlife + defe:
                pixi(shild, j * 4 - (mlife + mdefe - 1) * 2, 26)
                j = j + 1
            while j < mlife + mdefe:
                pixi(shild_net, j * 4 - (mlife + mdefe - 1) * 2, 26)
                j = j + 1
            while j < mlife + mdefe + vdefe:
                pixi(vshild, j * 4 - (mlife + mdefe - 1) * 2, 26)
                j = j + 1
            if mdefe > 0 or vdefe > 0:
                pixi(shild_corner, j * 4 - (mlife + mdefe - 1) * 2 - 2, 26)

            for i in range(len(ha)):
                if len(ha) < 6:
                    mom = 60
                if len(ha) == 6:
                    mom = 55 - 1
                if len(ha) == 7:
                    mom = 50 - 2
                if len(ha) == 8:
                    mom = 45 - 3
                if len(ha) == 9:
                    mom = 40 - 4
                if len(ha) == 10:
                    mom = 35 - 5
                ha[i].show(i * mom - (len(ha) - 1) * mom / 2, 90)

            for eve in event.get():
                if eve.type == QUIT or (eve.type == KEYDOWN and eve.key == K_ESCAPE):
                    exit()
                elif eve.type == MOUSEBUTTONDOWN:
                    if button(m_r, 64, 10):
                        sdwig += 1
                    if button(m_r, -64, 10):
                        sdwig -= 1
                    if button(base_gray, 205, 115):
                        end = False
                        break
                    for i in range(len(ha)):
                        if button(dizzy, i * mom - (len(ha) - 1) * mom / 2, 90) and ha[i].цена <= ener:
                            ener -= ha[i].цена
                            do=ha[i]
                            if do.урон!=-1:
                                vustrel_flag = do.урон
                                s = 0
                            if do.щит > 0:
                                defe += do.щит
                                if defe > mdefe:
                                    defe = mdefe
                            if do.вщит > 0:
                                vdefe += do.вщит
                            if do.манёвр > 0:
                                manevr+=do.манёвр
                            for key, v in do.статус.items():
                                if v != 0:
                                    ef[key] += v
                            sbros.append(ha.pop(i))

            if vustrel_flag:
                if s < 8:
                    x=0
                    y=-32 - s*15
                    draw.line(sc, (255, 255, 255), (int(x * scale) + screenWidth // 2,
                           int(y * scale) + screenHeight // 2), (int(x * scale) + screenWidth // 2,
                           int((y+20) * scale) + screenHeight // 2), 4)
                    s += 1
                    if 25 - s * 20 < -50 + 20:
                        for i in range(len(twerd)):
                            if twerd[i] == 0:
                                s = 8
                                vbron = vbron - vustrel_flag - ef["♦"] - ef["🔶"]
                                if vbron < 0:
                                    bron = bron + vbron
                                    vbron = 0
                                    if bron < 0:
                                        hp = hp + bron
                                        bron = 0
                else:
                    vustrel_flag = 0

            display.update()
            clock.tick(FPS)

        while len(ha) > 0:
            sbros.append(ha.pop(0))
        # Ход врага
        vbron = 0
        if (hp > 0 and life > 0):
            for qqq in range(len(ene(nam, hod)["Урон"]) // 2):
                x = vs["Пушка"][ene(nam, hod)["Урон"][2 * qqq + 1]] * 16 - (len(enemy_ship) - 2) * 8 + qqq * 16 - sdwig * 16
                s = 0
                while s < 13:
                    pixi(fon, 0, 0)
                    pixi(font.render(str(ener), True, (255, 255, 255)), -220, 110)
                    pixi(font.render(str(len(sbros)), True, (255, 255, 255)), 212, 89)
                    pixi(font.render(str(len(vta)), True, (255, 255, 255)), -194, 121)
                    pixi(font.render(str(len(burn)), True, (255, 255, 255)), 185, 89)

                    statusOtstup = 0
                    statusk = 0

                    for key, v in ef.items():
                        if v != 0:
                            statusOtstup += 1
                    if manevr > 0:
                        statusOtstup += 1
                    for key, v in ef.items():
                        if v != 0:
                            statusk += 1
                            pixi(status_bg, - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                            pixi(kartinka[key], -2 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                            pixi(font.render(str(v), True, (255, 255, 255)),
                                 4 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                    if manevr > 0:
                        statusk += 1
                        pixi(status_bg, - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                        pixi(evade, -2 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                        pixi(font.render(str(manevr), True, (255, 255, 255)),
                             4 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)

                    j = 0  # Отрисовка хп врага
                    while j < hp:
                        pixi(lif, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        if j == 0:
                            pixi(lif_cl, - 3 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                            pixi(lif_cr, (mhp - 1) * 4 - (mhp + mbron - 1) * 2 + 2 - sdwig * 16, -96)
                        j += 1
                    while j < mhp:
                        pixi(lif_net, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    while j < mhp + bron:
                        pixi(shild, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    while j < mhp + mbron:
                        pixi(shild_net, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    while j < mhp + mbron + vbron:
                        pixi(vshild, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    if mbron > 0 or vdefe > 0:
                        pixi(shild_corner, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16 - 2, -96)

                    j = 0  # Отрисовка хп
                    while j < life:
                        pixi(lif, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        if j == 0:
                            pixi(lif_cl, - 3 - (mlife + mdefe - 1) * 2, 26)
                            pixi(lif_cr, (mlife - 1) * 4 - (mlife + mdefe - 1) * 2 + 2, 26)
                        j = j + 1
                    while j < mlife:
                        pixi(lif_net, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    while j < mlife + defe:
                        pixi(shild, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    while j < mlife + mdefe:
                        pixi(shild_net, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    while j < mlife + mdefe + vdefe:
                        pixi(vshild, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    if mdefe > 0 or vdefe > 0:
                        pixi(shild_corner, j * 4 - (mlife + mdefe - 1) * 2 - 2, 26)

                    twerd = []
                    for i in vs["Твёрд"]:
                        twerd.append(-(len(vs["Твёрд"]) - 1) * 8 + i * 16 + sdwig * 16)

                    for i in range(len(enemy_ship)):
                        if i == 0:
                            pixi(enemy_ship[0], -1 - sdwig * 16, -105)
                        else:
                            pixi(enemy_ship[i], -(len(enemy_ship)) * 8 + i * 16 - sdwig * 16, -75)

                    if s == 3 and (vs["Пушка"][ene(nam, hod)["Урон"][2 * qqq + 1]] - sdwig - 2) in range(-2, 3):
                        break
                    y=-55+s*15
                    draw.line(sc, (255, 255, 255), (int(x * scale) + screenWidth // 2, int(y * scale) + screenHeight // 2),
                              (int(x * scale) + screenWidth // 2,int((y+20) * scale) + screenHeight // 2), 4)
                    s += 1
                    display.update()
                    clock.tick(FPS)

                if (vs["Пушка"][ene(nam, hod)["Урон"][2 * qqq + 1]] - sdwig - 2) in range(-2, 3):
                    vdefe = vdefe - ene(nam, hod)["Урон"][2 * qqq]
                    if vdefe < 0:
                        defe = defe + vdefe
                        vdefe = 0
                        if defe < 0:
                            life = life + defe
                            defe = 0
            if ene(nam, hod)["Щит"]!=[0,0]:
                for qqq in range(len(ene(nam, hod)["Щит"])//2):
                    bron+=ene(nam, hod)["Щит"][2*qqq]
                    if bron>mbron:
                        bron=mbron
            if ene(nam, hod)["Усиление"]!=["",0]:
                0==0
            if ene(nam, hod)["Движ"] == -666:
                if vs["Пушка"] != []:
                    k = -sdwig - vs["Пушка"][len(vs["Пушка"]) // 4] + random.randint(0, len(enemy_ship) - 1)
                else:
                    k = -sdwig - vs["Отсек"][len(vs["Отсек"]) // 4] + random.randint(0, len(enemy_ship) - 1)
                for qqq in range(abs(k)):
                    sdwig += k // abs(k)
                    pixi(fon, 0, 0)
                    pixi(font.render(str(ener), True, (255, 255, 255)), -220, 110)
                    pixi(font.render(str(len(sbros)), True, (255, 255, 255)), 212, 89)
                    pixi(font.render(str(len(vta)), True, (255, 255, 255)), -194, 121)
                    pixi(font.render(str(len(burn)), True, (255, 255, 255)), 185, 89)

                    statusOtstup = 0
                    statusk = 0

                    for key, v in ef.items():
                        if v != 0:
                            statusOtstup += 1
                    if manevr > 0:
                        statusOtstup += 1
                    for key, v in ef.items():
                        if v != 0:
                            statusk += 1
                            pixi(status_bg, - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                            pixi(kartinka[key], -2 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                            pixi(font.render(str(v), True, (255, 255, 255)),
                                 4 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                    if manevr > 0:
                        statusk += 1
                        pixi(status_bg, - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                        pixi(evade, -2 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)
                        pixi(font.render(str(manevr), True, (255, 255, 255)),
                             4 - 6.5 - 8.5 * statusOtstup + 17 * statusk - statusOtstup, 36)

                    for i in range(len(enemy_ship)):
                        if i == 0:
                            pixi(enemy_ship[0], -1 - sdwig * 16, -105)
                        else:
                            pixi(enemy_ship[i], -(len(enemy_ship)) * 8 + i * 16 - sdwig * 16, -75)

                    j = 0  # Отрисовка хп врага
                    while j < hp:
                        pixi(lif, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        if j == 0:
                            pixi(lif_cl, - 3 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                            pixi(lif_cr, (mhp - 1) * 4 - (mhp + mbron - 1) * 2 + 2 - sdwig * 16, -96)
                        j += 1
                    while j < mhp:
                        pixi(lif_net, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    while j < mhp + bron:
                        pixi(shild, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    while j < mhp + mbron:
                        pixi(shild_net, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    while j < mhp + mbron + vbron:
                        pixi(vshild, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16, -96)
                        j = j + 1
                    if mbron > 0 or vdefe > 0:
                        pixi(shild_corner, j * 4 - (mhp + mbron - 1) * 2 - sdwig * 16 - 2, -96)

                    j = 0  # Отрисовка хп
                    while j < life:
                        pixi(lif, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        if j == 0:
                            pixi(lif_cl, - 3 - (mlife + mdefe - 1) * 2, 26)
                            pixi(lif_cr, (mlife - 1) * 4 - (mlife + mdefe - 1) * 2 + 2, 26)
                        j = j + 1
                    while j < mlife:
                        pixi(lif_net, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    while j < mlife + defe:
                        pixi(shild, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    while j < mlife + mdefe:
                        pixi(shild_net, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    while j < mlife + mdefe + vdefe:
                        pixi(vshild, j * 4 - (mlife + mdefe - 1) * 2, 26)
                        j = j + 1
                    if mdefe > 0 or vdefe > 0:
                        pixi(shild_corner, j * 4 - (mlife + mdefe - 1) * 2 - 2, 26)

                    display.update()
                    clock.tick(3)




battle([],10,10,[cards[0], cards[1], cards[2], cards[3], cards[4]],5,"CCD-19 Cicada",4,0,[])