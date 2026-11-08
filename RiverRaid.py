import obj
import shot
import place
import cores
import ilhas
import ponte
import pygame
import random
from pathlib import Path
from pygame.locals import *

ROOT = Path(__file__).resolve().parent

# variáveis globais
vel_y = 2
speed = 0
vidas = 1
n_eny = 6
fase = 1
gazlev = 0
pontos = 0
helice = 0
delay_y = 1
eny_box = 96
mover = False
sair = False
game = False
intro = False
partidas = 0
flash = 0
beam_y = 0
chuva = 0
gaz_level = 166
hitplane = False
screen_height = 480
s_gaz_alert = "gaz_full"
width, height = 800, 600

# nome, margens, ilhas, tráfego, ritmo do combustível
FASES = {
    1: {"nome": "rio clássico", "terra": (0, 7), "ilha": (0, 13),
        "pool": ("heli", "heli", "ship", "ship", "jet", "jet", "fuel"),
        "cada": 100, "gasto": 5},
    2: {"nome": "garganta", "terra": (4, 6), "ilha": (8, 13),
        "pool": ("ship", "ship", "ship", "heli", "jet", "decoy", "fuel"),
        "cada": 100, "gasto": 5},
    3: {"nome": "neblina", "terra": (0, 7), "ilha": (0, 13),
        "pool": ("heli", "heli", "heli", "ship", "jet", "fuel", "fuel"),
        "cada": 100, "gasto": 5},
    4: {"nome": "comboio", "terra": (0, 7), "ilha": (0, 13),
        "pool": ("jet", "jet", "jet", "jet", "shadow", "heli", "fuel"),
        "cada": 170, "gasto": 3},
    5: {"nome": "temporal", "terra": (0, 7), "ilha": (0, 13),
        "pool": ("heli", "ship", "jet", "fuel", "decoy", "shadow"),
        "cada": 90, "gasto": 6},
}

LETRAS = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "I": ("11111", "00100", "00100", "00100", "00100", "00100", "11111"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
}

# inicialização
pygame.display.init()
pygame.font.init()
audio_ok = False
try:
    pygame.mixer.init()
    audio_ok = True
except pygame.error:
    audio_ok = False

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("River Raid")


class Silencio:
    def play(self, *args, **kwargs):
        return None

    def stop(self):
        return None


def carregar_som(nome):
    if not audio_ok:
        return Silencio()
    try:
        return pygame.mixer.Sound(str(ROOT / "sons" / nome))
    except pygame.error:
        return Silencio()


# Sons. O caminho parte do arquivo, não da pasta em que o comando foi chamado.
voo0 = carregar_som("voo0.wav")
voo1 = carregar_som("voo1.wav")
voo2 = carregar_som("voo2.wav")
gaz1 = carregar_som("gaz1.wav")
gaz0 = carregar_som("gaz0.wav")
s_tiro = carregar_som("tiro.wav")
gaz_end = carregar_som("gaz_end.wav")
s_explode = carregar_som("explode.wav")
gaz_alert = carregar_som("gaz_alert.wav")
gaz_explode = carregar_som("gaz_explode.wav")

# objetos
casa = [3]
ilha = [3]
terra = [3]
pontes = [3]
data_casa = [3]
data_enemy = [[0, 0, 0, 0, 0, 1] for _ in range(n_eny)]
data_ilha = [3, 3, 3]
data_terra = [3, 3, 3]

cor = cores.cor
tiro = shot.Shot(win, 1, 0, 1)
base = place.Place(win, width, 8, -100)
plane = obj.Obj(win, 370, 420, 49, 42, 0, 0, 0)

for i in range(3):
    data_casa.append(i)
    casa.append(i)
    casa[i] = obj.Obj(win, -100, 0, 85, 56, 14, 0, 0)

    ilha.append(i)
    ilha[i] = ilhas.Ilhas(win, width, 1, 0)

    terra.append(i)
    terra[i] = place.Place(win, width, 3, - i * 336 - 100)

    pontes.append(i)
    pontes[i] = ponte.Ponte(win, i * 485, -screen_height, 316, 77, 0, 0, 0)

terra_intro = place.Place(win, width, 0, 0)
pontes[2].ty = 1
pontes[2].x = 312
pontes[2].out = 1
pontes[2].h = 68
pontes[2].w = 175

enemy = [obj.Obj(win, 0, 0, 0, 0, 0, 0, 0) for _ in range(n_eny)]


def limites_fase():
    return 6 if fase == 5 else 5


def aplicar_terreno():
    terra_faixa = FASES[fase]["terra"]
    ilha_faixa = FASES[fase]["ilha"]
    for i in range(3):
        terra[i].forma = random.randint(terra_faixa[0], terra_faixa[1])
        ilha[i].forma = random.randint(ilha_faixa[0], ilha_faixa[1])


def avancar_fase():
    global fase, vel_y
    fase = 1 if fase >= 5 else fase + 1
    vel_y = min(4, vel_y + 1)
    aplicar_terreno()
    if fase == 5:
        enemy[5].out = False
        enemy[5].y = -eny_box
        enemy[5].decoy = False
    else:
        enemy[5].out = True
        enemy[5].y = -400


def restart():
    global s_gaz_alert, pontos, vidas, mover, hitplane, data_ilha, data_enemy, data_terra, gaz_level, data_casa
    global fase, vel_y, flash, beam_y, intro

    vidas = 3
    pontos = 0
    fase = 1
    vel_y = 2
    flash = 0
    beam_y = 0
    intro = True
    base.y = -100
    mover = False
    gaz_level = 166
    plane.out = True
    plane.decoy = False
    plane.hide = False
    hitplane = False
    pontes[2].out = True
    s_gaz_alert = "gaz_full"

    # Parando os sons
    voo0.stop()
    voo1.stop()
    voo2.stop()
    gaz_alert.stop()

    for i in range(3):
        terra[i].forma = 3
        data_terra[i] = 3
        terra[i].y = -i * 336 - 100
        casa[i].x = 80
        data_casa[i] = [80, False]
        ilha[i].y = -1600
        data_ilha[i] = 13

    data_casa[1][1] = True
    terra_intro.y = 100

    for i in range(n_eny):
        data_enemy[i] = [100, i * eny_box - screen_height, 42, 30, 6, 1, 0]
    data_enemy[4] = [350, -96, 81, 24, 8, 0]
    data_enemy[3] = [450, -192, 42, 30, 6, 0]
    data_enemy[1] = [500, -384, 37, 72, 11, 0]
    data_enemy[5] = [120, -400, 42, 30, 6, 1]
    for i in range(n_eny):
        enemy[i].decoy = False
        enemy[i].hide = False


def botao_rect():
    btn_w, btn_h = 300, 60
    return (width // 2 - btn_w // 2, screen_height // 2 - btn_h // 2, btn_w, btn_h)


def comecar():
    global game, partidas
    restart()
    game = True
    partidas += 1


def opned():
    global game, intro, vidas, gaz_level

    if base.y < 238 and not game:
        intro = True
        base.y += 1
        for i in range(n_eny):
            enemy[i].y += 1
            if i < 3:
                casa[i].y += 1
                ilha[i].y += 1
                terra[i].y += 1

    if base.y == -100 and plane.out:
        ler_pos()

    if base.y < 238 and game and intro:
        base.y += 1
        for i in range(n_eny):
            #  Espaço entre a base e os inimigos
            if enemy[i].y > base.y + 4:
                enemy[i].out = True
            enemy[i].y += 1
            if i < 3:
                casa[i].y += 1
                ilha[i].y += 1
                terra[i].y += 1

    if plane.out and not plane.t_expl and game and vidas > 0 and not intro:
        intro = True
        pontes[2].out = True
        gaz_level = 166
        plane.x = 370
        plane.ty = 0
        base.y = -100
        vidas -= 1
    if plane.out and not plane.t_expl and game and vidas <= 0 and not intro:
        game = False
    if base.y == 238 and game and intro:
        plane.out = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            return True
        if (e.type == KEYDOWN) and e.key == K_F2:
            comecar()
        # Clique do mouse no botão de jogar (também quando vidas acabaram)
        if e.type == MOUSEBUTTONDOWN and not game:
            mx, my = e.pos
            btn_x, btn_y, btn_w, btn_h = botao_rect()
            if btn_x <= mx <= btn_x + btn_w and btn_y <= my <= btn_y + btn_h:
                comecar()
        if base.y == 238 and game and intro and (e.type == KEYDOWN):
            intro = False
            voo1.play(-1)

    return False


# Colisão
def colidir(a, b):
    return a.x + a.w > b.x and a.x < b.x + b.w and a.y + a.h > b.y and a.y < b.y + b.h


def hitcortest(obj, cor_alvo):
    alvo = cor_alvo[:3]
    if obj.x >= 0 and obj.x + obj.w <= width and obj.y >= 0 and obj.y + obj.h <= height:
        for i in range(int(obj.w)):
            for j in range(int(obj.h)):
                if (not i and (not j or j == int(obj.h) - 1)) or not j and i == int(obj.w) - 1:
                    pix = win.get_at((int(obj.x + i), int(obj.y + j)))
                    if pix[0] == alvo[0] and pix[1] == alvo[1] and pix[2] == alvo[2]:
                        return True
    return False


def salvar_pos():
    global data_enemy, data_casa, data_ilha, data_terra
    for i in range(n_eny):
        data_enemy[i][0] = enemy[i].x
        data_enemy[i][1] = enemy[i].y
        data_enemy[i][2] = enemy[i].w
        data_enemy[i][3] = enemy[i].h
        data_enemy[i][4] = enemy[i].ty
        data_enemy[i][5] = enemy[i].out
        if i < 3:
            data_terra[i] = terra[i].forma
            data_ilha[i] = ilha[i].forma
            data_casa[i][0] = casa[i].x
            data_casa[i][1] = casa[i].y


def ler_pos():
    global game, data_ilha, data_terra, data_enemy, data_casa
    if vidas < 0:
        game = False

    for i in range(n_eny):
        enemy[i].x = data_enemy[i][0]
        enemy[i].y = data_enemy[i][1]
        enemy[i].w = data_enemy[i][2]
        enemy[i].h = data_enemy[i][3]
        enemy[i].ty = data_enemy[i][4]
        enemy[i].out = data_enemy[i][5]

    for i in range(3):
        casa[i].x = data_casa[i][0]
        casa[i].out = data_casa[i][1]
        terra[i].forma = data_terra[i]
        ilha[i].forma = data_ilha[i]
        casa[i].x = 80
        casa[i].y = -i * 350

    terra[0].y = 100
    terra_intro.y = 100


def quebrar_ponte(pelo_tiro):
    global pontos, hitplane
    if pontes[2].out:
        return
    salvar_pos()
    pontes[2].t_expl = 40
    pontes[2].out = True
    pontos += 250
    if pelo_tiro:
        s_tiro.stop()
        s_explode.play()
        tiro.y = -100
    else:
        hitplane = True
    avancar_fase()


def hittest():
    global hitplane, gaz_level, mover, pontos, s_gaz_alert
    if not game:
        return
    t_expl = 40
    # Tiro colide com paredes
    if hitcortest(tiro, cor[2]):
        tiro.y = -tiro.h

    # Avião com paredes
    if(hitcortest(plane, cor[2]) or hitplane or not gaz_level) and not plane.out:
        voo0.stop()
        voo1.stop()
        voo2.stop()
        mover = False
        hitplane = False
        plane.out = True
        gaz_alert.stop()
        plane.t_expl = 80
        s_gaz_alert = "gaz_full"
        if gaz_level:
            s_explode.play()
        else:
            gaz_explode.play()

    enehit = 0
    for i in range(n_eny):
        # movimenta aviões no eixo x
        if enemy[i].ty == 5 or enemy[i].ty == 6 or enemy[i].ty == 8 or enemy[i].ty == 9:
            enemy[i].dir = -1
        else:
            enemy[i].dir = 1

        if enemy[i].decoy:
            if colidir(plane, enemy[i]) and not enemy[i].out and not plane.out:
                enemy[i].out = True
            continue

        hit = enemy[i].w
        enemy[i].w = hit/2
        if hitcortest(enemy[i], cor[2]):
            if enemy[i].ty == 5 or enemy[i].ty == 6:
                enemy[i].ty = 4
                enemy[i].x += 2
            if enemy[i].ty == 8:
                enemy[i].x += 2
                enemy[i].ty = 7

        enemy[i].x += hit/2
        if hitcortest(enemy[i], cor[2]):
            if enemy[i].ty == 4 or enemy[i].ty == 3:
                enemy[i].x -= 2
                enemy[i].ty = 6
            if enemy[i].ty == 7:
                enemy[i].x -= 2
                enemy[i].ty = 8
        enemy[i].x -= hit/2
        enemy[i].w = hit

        # Tiro colide com objetos
        if colidir(tiro, enemy[i]) and not enemy[i].out and tiro.y >= 0:
            enemy[i].t_expl = t_expl
            enemy[i].out = True
            enehit = enemy[i].ty
            s_tiro.stop()
            s_explode.play()
            tiro.y = -tiro.h

        # Avião com inimigos
        if colidir(plane, enemy[i]) and enemy[i].ty < 11 and not enemy[i].out:
            enemy[i].t_expl = t_expl
            enemy[i].out = True
            enehit = enemy[i].ty
            s_tiro.stop()
            hitplane = True

        # Avião com gasolina
        if colidir(plane, enemy[i]) and enemy[i].ty == 11 and not enemy[i].out and not plane.out:
            if gaz_level < 165:
                gaz0.play()
                gaz_level += 0.3
            else:
                gaz1.play()

        # Avião com pontes
        if (colidir(plane, pontes[0]) or colidir(plane, pontes[1])) and not plane.out:
            hitplane = True

        # Avião com ponte base
        if colidir(plane, pontes[2]) and not pontes[2].out:
            quebrar_ponte(False)

        # Tiro com a ponte da base
        if colidir(pontes[2], tiro) and not pontes[2].out and tiro.y >= 0:
            quebrar_ponte(True)

        # Pontos ao atingir inimigos
        if 2 < enehit < 7:     # helicoptero
            pontos += 80
        elif 6 < enehit < 9:   # navio
            pontos += 40
        elif 8 < enehit < 11:  # avião
            pontos += 120
        elif enehit == 11:     # Posto gaz
            pontos += 30


def sortear_inimigo(alvo):
    kind = random.choice(FASES[fase]["pool"])
    alvo.decoy = kind in ("decoy", "shadow")
    if kind == "heli":
        alvo.ty = random.choice((4, 6))
        alvo.w, alvo.h = 42, 30
    elif kind == "ship":
        alvo.ty = random.choice((7, 8))
        alvo.w, alvo.h = 81, 24
    elif kind in ("jet", "shadow"):
        alvo.ty = random.choice((9, 10))
        alvo.w, alvo.h = 48, 18
    else:
        alvo.ty = 11
        alvo.w, alvo.h = 37, 72


def inimigos():
    global helice, gaz_level, gazlev, s_gaz_alert

    helice = not helice
    hittest()
    for i in range(n_eny):
        # anima helice dos Helicopteros
        if helice and enemy[i].ty == 3 or enemy[i].ty == 5:
            enemy[i].ty += 1
        elif enemy[i].ty == 4 or enemy[i].ty == 6:
            enemy[i].ty -= 1
    
        if game and not intro:
            if i >= limites_fase():
                enemy[i].out = True
                enemy[i].y = -400
            else:
                # movimenta inimigos na vertical
                enemy[i].y += mover * vel_y

                # movimenta inimigos navios e helicópteros
                if 2 < enemy[i].ty < 9 and enemy[i].y > 200 and not enemy[i].out:
                    enemy[i].x += enemy[i].dir

                # movimento dos aviões na horizontal; a sombra vai no sentido contrário
                if enemy[i].ty == 10 or enemy[i].ty == 9:
                    passo = -enemy[i].dir if enemy[i].decoy else enemy[i].dir
                    if enemy[i].x > width and passo > 0:
                        enemy[i].x = 0
                    if enemy[i].x < 0 and passo < 0:
                        enemy[i].x = width
                    if not enemy[i].out and not plane.out:
                        enemy[i].x += passo

                # reposicionando inimigos; >= evita pular o pixel quando vel_y > 1
                baixo = screen_height + eny_box / 2
                limite = screen_height - eny_box / 3
                if enemy[i].y >= baixo:
                    if -370 <= base.y < 50:
                        enemy[i].out = True
                    enemy[i].y = -eny_box / 2
                elif enemy[i].y >= limite:
                    enemy[i].y = 0
                    if base.y < enemy[i].y < base.y + 400:
                        enemy[i].out = True
                    else:
                        enemy[i].out = False
                    sortear_inimigo(enemy[i])
                    for _ in range(12):
                        enemy[i].x = random.randint(0, 8) * 84 + 23
                        if not hitcortest(enemy[i], cor[2]):
                            break
                    else:
                        enemy[i].out = True
                    enemy[i].y = -eny_box / 3

        pisca = enemy[i].decoy and enemy[i].ty == 11 and (pygame.time.get_ticks() // 180) % 2 == 0
        fora = False
        if fase == 3 and game and not enemy[i].t_expl:
            cy = enemy[i].y + enemy[i].h / 2
            fora = not (beam_y - 46 <= cy <= beam_y + 46)
        enemy[i].hide = (pisca or fora) and not enemy[i].t_expl
        enemy[i].show()

    # Retira gasolina
    if not intro and mover:
        gazlev += 1
        if gazlev > FASES[fase]["cada"]:
            gazlev = 0
            gaz_level -= FASES[fase]["gasto"]
        if gaz_level < 0:
            gaz_level = 0

    # Aviso de gasolina acabando
    if gaz_level <= 70 and s_gaz_alert == "gaz_full":
        s_gaz_alert = "gaz_alert"
        gaz_alert.play(-1)
    if gaz_level <= 5 and gazlev > 80 and s_gaz_alert == "gaz_alert":
        s_gaz_alert = "gaz_end"
        gaz_alert.stop()
        gaz_end.play()

    if s_gaz_alert != "gaz_full" and gaz_level > 70:
        s_gaz_alert = "gaz_full"
        gaz_end.stop()
        gaz_alert.stop()


def lands():
    # mover a base
    if game and not intro and not plane.t_expl:
        base.y += mover * vel_y

    for i in range(3):
        ilha[i].y = base.y - (2000+i*246)
        terra[i].y = base.y - (330+i*300)
        if intro:
            terra_intro.show()

        if terra[i].y < screen_height:
            terra[i].show()

        if ilha[i].y < screen_height:
            ilha[i].show()

    terra_intro.y = base.y + 210

    for i in range(3):
        # movimenta casa e base em y
        casa[i].y += mover * vel_y

        # posiciona casinhas aleatóreamente
        if casa[i].y >= screen_height:
            casa[i].y = 0
            rnd_casa = [0, 1, 2, 3, 4, 5, 6, 7, 8]
            random.shuffle(rnd_casa)  # embaralha array
            for j in range(0, 8):
                casa[i].x = rnd_casa[j] * casa[i].w + 25
                if hitcortest(casa[i], cor[3]) or pontes[2].t_expl or colidir(casa[i], pontes[0]) or colidir(casa[i], pontes[1]) or colidir(casa[i], pontes[2]):
                    casa[i].out = True
                else:
                    casa[i].out = False
                    break

        if casa[i].y < screen_height:
            casa[i].show()

        # Pontes
        pontes[i].y = base.y + 164
        if -screen_height < base.y < screen_height:
            pontes[i].show()
    pontes[2].y = base.y + 169

    # Regenera a ponte
    if base.y > screen_height and not intro:
        pontes[2].out = False


def distrair():
    global beam_y, flash, chuva
    beam_y = (beam_y + 4) % (screen_height + 120)
    chuva = (chuva + 9) % screen_height
    if not game or fase != 5:
        return
    if flash > 0:
        flash -= 1
        return
    if random.randint(0, 200) == 0 and not plane.out:
        flash = 10
        sopro = random.choice((-4, 4))
        plane.x = max(10, min(734, plane.x + sopro))


def texto_pixel(texto, x, y, escala):
    for ch in texto:
        glifo = LETRAS.get(ch, LETRAS[" "])
        for ly, linha in enumerate(glifo):
            for lx, bit in enumerate(linha):
                if bit == "1":
                    pygame.draw.rect(win, cor[1], (x + lx * escala, y + ly * escala, escala - 1, escala - 1))
        x += 6 * escala


def neblina():
    by = int(beam_y) % (screen_height + 80) - 40
    fog = pygame.Surface((width, screen_height), pygame.SRCALPHA)
    if by > 0:
        fog.fill((0, 0, 20, 160), (0, 0, width, by))
    baixo = by + 92
    if baixo < screen_height:
        fog.fill((0, 0, 20, 160), (0, baixo, width, screen_height - baixo))
    win.blit(fog, (0, 0))


def chuva_na_tela():
    for k in range(36):
        x = (k * 47 + chuva * 2) % width
        y = (k * 61 + chuva * 3) % screen_height
        pygame.draw.line(win, (190, 190, 230), (x, y), (x - 3, y + 14), 1)


def paint():
    distrair()
    # Rio. O temporal reusa o pisca da explosão da ponte.
    if pontes[2].t_expl % 2 or (fase == 5 and game and flash % 2):
        win.fill(cor[8])
    else:
        win.fill(cor[3])

    # Liberando controle
    if not plane.out and not intro:
        control()

    tiro.show(plane.x + plane.w/2, plane.y + plane.h/2)

    # Fundo
    win.fill(cor[2], rect=[0, 0, 20, height])
    win.fill(cor[2], rect=[width - 20, 0, 20, height])

    if -screen_height < base.y < screen_height:
        base.show()

    lands()
    inimigos()
    if fase == 3 and game:
        neblina()
    if not game:
        plane.out = False
        plane.t_expl = 0
        plane.hide = False
        plane.x = 370
        plane.y = 390
        plane.ty = 0
    plane.show()
    if fase == 5 and game:
        chuva_na_tela()

    # Painel
    win.fill(cor[7], rect=[0, screen_height, width, 130])
    win.fill(cor[14], rect=[0, height - 117, width, 112])

    # medidor de gasolina. Some no relâmpago da fase 5.
    if not (fase == 5 and game and flash):
        pygame.draw.rect(win, cor[7], [320, 515, 204, 44], 4)
        pygame.draw.rect(win, cor[7], [335, 515, 11, 13])
        pygame.draw.rect(win, cor[7], [422, 515, 5, 13])
        pygame.draw.rect(win, cor[7], [500, 515, 11, 13])

    textos()

    if not game:
        texto_pixel("RIVER RAID", 250, 28, 5)
        font_s = pygame.font.SysFont("monospace", 22)
        sub = font_s.render("cover    fase 1  —  rio clássico", True, cor[1])
        win.blit(sub, ((width - sub.get_width()) // 2, 78))
        dica = font_s.render("na pista, aperte uma tecla para decolar", True, cor[13])
        win.blit(dica, ((width - dica.get_width()) // 2, 168))
        btn_x, btn_y, btn_w, btn_h = botao_rect()
        mx, my = pygame.mouse.get_pos()
        hovered = (btn_x <= mx <= btn_x + btn_w) and (btn_y <= my <= btn_y + btn_h)
        btn_color = cor[13] if not hovered else cor[1]
        win.fill(btn_color, rect=[btn_x, btn_y, btn_w, btn_h])
        pygame.draw.rect(win, cor[7], [btn_x, btn_y, btn_w, btn_h], 4)
        rotulo = "Jogar de novo" if partidas else "Jogar"
        font_b = pygame.font.SysFont("monospace", 30, bold=True)
        txt_b = font_b.render(rotulo, True, (0, 0, 0))
        win.blit(txt_b, (btn_x + (btn_w - txt_b.get_width()) // 2, btn_y + (btn_h - txt_b.get_height()) // 2))

    # Reinicia Terras Base e Ilhas
    if ilha[2].y > screen_height:
        base.y = -400
        aplicar_terreno()
    # atualiza a tela após tudo desenhado
    pygame.display.update()


def textos():
    if not (fase == 5 and game and flash):
        pygame.draw.rect(win, cor[1], [335 + gaz_level, 529, 10, 27])
        font = pygame.font.SysFont("monospace", 22, bold=True)
        for texto, x in (("E", 338), (chr(189), 410), ("F", 500)):
            txt = font.render(texto, True, (0, 0, 0))
            win.blit(txt, (x, 526))

    if vidas:
        font = pygame.font.SysFont("monospace", 34, bold=True)
        txt = font.render(str(vidas), True, (232, 232, 74))
        win.blit(txt, (290, 554))

    if game:
        font = pygame.font.SysFont("monospace", 22)
        txt = font.render("Fase %d  %s" % (fase, FASES[fase]["nome"]), True, (232, 232, 74))
        win.blit(txt, (16, 474))
        pts = font.render(str(pontos), True, (232, 232, 74))
        win.blit(pts, (620, 474))

    if not game:
        font = pygame.font.SysFont("monospace", 16)
        linhas = ("Setas: mover e acelerar", "Espaco: atirar    F2: jogar", "ESC: sair")
        for n, linha in enumerate(linhas):
            txt = font.render(linha, True, (232, 232, 74))
            win.blit(txt, (18, 496 + n * 22))


def control():
    global delay_y, speed, mover

    # velocidade do jogo
    if game and not intro:
        speed += 1
        if speed > delay_y:
            mover = True
            speed = 0
        else:
            mover = False

    # Controlando a direção
    plane.ty = 0
    key = pygame.key.get_pressed()
    if key[K_LEFT] and plane.x > 10:
        plane.x -= 1
        plane.ty = 1
    if key[K_RIGHT] and plane.x < 734:
        plane.x += 1
        plane.ty = 2

    # controlando a velocidade
    if key[K_UP]:
        if delay_y > 0:
            voo0.stop()
            voo1.stop()
            voo2.play(-1)
        delay_y = 0
    elif key[K_DOWN]:
        if delay_y < 2:
            voo1.stop()
            voo2.stop()
            voo0.play(-1)
        delay_y = 2
    else:
        if delay_y != 1:
            voo0.stop()
            voo2.stop()
            voo1.play(-1)
        delay_y = 1

    # Atirando
    if key[K_SPACE]:
        tiro.shoting = True
        if tiro.y == plane.y - 15:
            s_tiro.stop()
            s_tiro.play()


def main():
    global sair
    restart()
    while not sair:
        paint()
        sair = opned()


if __name__ == "__main__":
    main()











