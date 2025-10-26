import obj
import shot
import place
import cores
import ilhas
import ponte
import pygame
import random
from pygame.locals import *

# variáveis globais
vel_y = 2
speed = 0
vidas = 1
n_eny = 5
gazlev = 0
pontos = 0
helice = 0
delay_y = 1
eny_box = 96
mover = False
sair = False
game = False
intro = False
gaz_level = 166
hitplane = False
screen_height = 480
s_gaz_alert = "gaz_full"
width, height = 800, 600

# inicialização
pygame.init()
win = pygame.display.set_mode((width, height))

# Sons
voo0 = pygame.mixer.Sound("sons/voo0.wav")
voo1 = pygame.mixer.Sound("sons/voo1.wav")
voo2 = pygame.mixer.Sound("sons/voo2.wav")
gaz1 = pygame.mixer.Sound("sons/gaz1.wav")
gaz0 = pygame.mixer.Sound("sons/gaz0.wav")
gaz1 = pygame.mixer.Sound("sons/gaz1.wav")
s_tiro = pygame.mixer.Sound("sons/tiro.wav")
gaz_end = pygame.mixer.Sound("sons/gaz_end.wav")
s_explode = pygame.mixer.Sound("sons/explode.wav")
gaz_alert = pygame.mixer.Sound("sons/gaz_alert.wav")
gaz_explode = pygame.mixer.Sound("sons/gaz_explode.wav")

# objetos
casa = [3]
ilha = [3]
terra = [3]
pontes = [3]
enemy = [n_eny]
data_casa = [3]
data_enemy = [n_eny]
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

for i in range(n_eny):
    enemy.append(i)
    enemy[i] = obj.Obj(win, 0, 0, 0, 0, 0, 0, 0)
    data_enemy.append(i)


def restart():
    global s_gaz_alert, pontos, vidas, mover, hitplane, data_ilha, data_enemy, data_terra, gaz_level, data_casa

    vidas = 3
    pontos = 0
    base.y = -100
    mover = False
    gaz_level = 166
    plane.out = True
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
    if base.y == 238 and game and intro:
        plane.out = False

    for e in pygame.event.get():
        if e.type == pygame.QUIT or e.type == KEYDOWN and e.key == K_ESCAPE:
            return True
        if (e.type == KEYDOWN) and e.key == K_F2:
            restart()
            game = True
        # Reiniciar com Enter quando o jogo acabou
        if (e.type == KEYDOWN) and e.key == K_RETURN and (not game or vidas <= 0):
            restart()
            game = True
        # Clique do mouse no botão de reiniciar (também quando vidas acabaram)
        if e.type == MOUSEBUTTONDOWN and (not game or vidas <= 0):
            mx, my = e.pos
            btn_w = 300
            btn_h = 60
            btn_x = width // 2 - btn_w // 2
            btn_y = screen_height // 2 - btn_h // 2
            if btn_x <= mx <= btn_x + btn_w and btn_y <= my <= btn_y + btn_h:
                restart()
                game = True
        if base.y == 238 and game and intro and (e.type == KEYDOWN):
            intro = False
            voo1.play(-1)

    return False


# Colisão
def colidir(a, b):
    return a.x + a.w > b.x and a.x < b.x + b.w and a.y + a.h > b.y and a.y < b.y + b.h


def hitcortest(obj, cor):
    cor = hex(cor)
    cor = cor.lstrip('0x')
    cor = tuple(int(cor[i:i + int(6 / 3)], 16) for i in range(0, 6, int(6 / 3)))

    if obj.x >= 0 and obj.x + obj.w <= width and obj.y >= 0 and obj.y + obj.h <= height:
        for i in range(int(obj.w)):
            for j in range(int(obj.h)):
                if (not i and (not j or j == int(obj.h) - 1)) or not j and i == int(obj.w) - 1:
                    if win.get_at((int(obj.x + i), int(obj.y + j))) == cor:
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


def hittest():
    global hitplane, gaz_level, mover, pontos, s_gaz_alert
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
            salvar_pos()
            hitplane = True
            pontos += 250
            pontes[2].out = True
            pontes[2].t_expl = t_expl

        # Tiro com a ponte da base
        if colidir(pontes[2], tiro) and not pontes[2].out and tiro.y >= 0:
            salvar_pos()
            pontes[2].t_expl = t_expl
            pontes[2].out = True
            pontos += 250
            s_tiro.stop()
            s_explode.play()
            tiro.y = -100

        # Pontos ao atingir inimigos
        if 2 < enehit < 7:     # helicoptero
            pontos += 80
        elif 6 < enehit < 9:   # navio
            pontos += 40
        elif 8 < enehit < 11:  # avião
            pontos += 120
        elif enehit == 11:     # Posto gaz
            pontos += 30


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
            # movimenta inimigos na vertical
            enemy[i].y += mover * vel_y

            # movimenta inimigos navios e helicópteros
            if 2 < enemy[i].ty < 9 and enemy[i].y > 200 and not enemy[i].out:
                enemy[i].x += enemy[i].dir

            # movimento dos aviões na horizontal
            if enemy[i].ty == 10 or enemy[i].ty == 9:
                if enemy[i].x > width and enemy[i].ty == 10:
                    enemy[i].x = 0
                if enemy[i].x < 0 and enemy[i].ty == 9:
                    enemy[i].x = width
                if not enemy[i].out and not plane.out:
                    enemy[i].x += enemy[i].dir

            # reposicionando inimigos
            if enemy[i].y == screen_height - eny_box / 3:
                enemy[i].y = 0
                if base.y < enemy[i].y < base.y + 400:
                    enemy[i].out = True
                else:
                    enemy[i].out = False

                # sorteia tipo de inimigos e posto
                enemys = [4, 6, 7, 8, 9, 10, 11]
                rnd = random.randint(0, 6)
                enemy[i].ty = enemys[rnd]
                if rnd == 0 or rnd == 1:
                    enemy[i].w = 42
                    enemy[i].h = 30
                elif rnd == 2 or rnd == 3:
                    enemy[i].w = 81
                    enemy[i].h = 24
                elif rnd == 4 or rnd == 5:
                    enemy[i].w = 48
                    enemy[i].h = 18
                elif rnd == 6:
                    enemy[i].w = 37
                    enemy[i].h = 72

                # Gerando posições aleatórias para os inimigos
                pos = True
                while pos:
                    enemy[i].x = random.randint(0, 8) * 84 + 23
                    pos = hitcortest(enemy[i], cor[2])

                enemy[i].y = -eny_box / 3

            if -370 <= base.y < 50 and enemy[i].y == screen_height + eny_box / 2:
                enemy[i].out = True

            if enemy[i].y == screen_height + eny_box / 2:
                enemy[i].y = -eny_box / 2

        enemy[i].show()

    # Retira gasolina
    if not intro and mover:
        gazlev += 1
        if gazlev > 100:
            gazlev = 0
            gaz_level -= 5
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
        if casa[i].y == screen_height:
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


def paint():
    # Rio
    if pontes[2].t_expl % 2:
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
    plane.show()

    # Painel
    win.fill(cor[7], rect=[0, screen_height, width, 130])
    win.fill(cor[14], rect=[0, height - 117, width, 112])

    # medidor de gasolina
    pygame.draw.rect(win, cor[7], [320, 515, 204, 44], 4)
    pygame.draw.rect(win, cor[7], [335, 515, 11, 13])
    pygame.draw.rect(win, cor[7], [422, 515, 5, 13])
    pygame.draw.rect(win, cor[7], [500, 515, 11, 13])

    textos()

    # Botão "Reiniciar Jogo" quando o jogo estiver encerrado (visível após game end ou vidas zeradas)
    # OBS: desenhamos em cima de tudo para garantir visibilidade
    if not game or vidas <= 0:
        btn_w = 340
        btn_h = 72
        btn_x = width // 2 - btn_w // 2
        btn_y = screen_height // 2 - btn_h // 2

        # helpers
        def hex2rgb(c):
            return ((c >> 16) & 255, (c >> 8) & 255, c & 255)

        mx, my = pygame.mouse.get_pos()
        hovered = (btn_x <= mx <= btn_x + btn_w) and (btn_y <= my <= btn_y + btn_h)
        pressed = pygame.mouse.get_pressed()[0] and hovered

        # overlay escuro local para destacar o botão
        overlay = pygame.Surface((btn_w + 24, btn_h + 24), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        win.blit(overlay, (btn_x - 12, btn_y - 12))

        # cores (fill e border)
        normal_fill = hex2rgb(cor[1])  # amarelo brilhante
        hover_fill = hex2rgb(cor[13])  # vermelho
        border_color = hex2rgb(cor[7])

        # efeito pressionado: escurece um pouco
        def darken(col, amt=0.7):
            return (int(col[0] * amt), int(col[1] * amt), int(col[2] * amt))

        if pressed:
            fill = darken(hover_fill)
        else:
            fill = hover_fill if hovered else normal_fill

        # botão
        pygame.draw.rect(win, fill, [btn_x, btn_y, btn_w, btn_h], border_radius=8)
        pygame.draw.rect(win, border_color, [btn_x, btn_y, btn_w, btn_h], 4, border_radius=8)

        # label com sombra
        font_b = pygame.font.SysFont("arial", 34, bold=True)
        label = "Reiniciar Jogo"
        txt_shadow = font_b.render(label, True, (0, 0, 0))
        txt = font_b.render(label, True, (255, 255, 255))
        text_x = btn_x + (btn_w - txt.get_width()) // 2
        text_y = btn_y + (btn_h - txt.get_height()) // 2
        win.blit(txt_shadow, (text_x + 2, text_y + 2))
        win.blit(txt, (text_x, text_y))

    # Reinicia Terras Base e Ilhas
    if ilha[2].y > screen_height:
        base.y = -400
        for i in range(3):
            terra[i].forma = random.randint(0, 7)
            ilha[i].forma = random.randint(0, 13)
    # atualiza a tela após tudo desenhado
    pygame.display.update()


def textos():
    # medidor
    font = pygame.font.SysFont("arial", 33)
    txt = font.render("E        " + chr(189) + "      F", 0, (0, 0, 0))
    win.blit(txt, (334, 524))
    pygame.draw.rect(win, cor[1], [335 + gaz_level, 529, 10, 27])

    # Vidas
    if vidas:
        font = pygame.font.SysFont("cooper Black", 34)
        txt = font.render(str(vidas), 0, (232, 232, 74))
        win.blit(txt, (290, 554))

    # Pontos
    if pontos:
        font = pygame.font.SysFont("cooper Black", 34)
        txt = font.render(str(pontos), 0, (232, 232, 74))
        win.blit(txt, (450, 474))

    # Texto
    if not game:
        font = pygame.font.SysFont("arial Black", 30)
        txt = font.render("Python", 0, (232, 232, 74))
        win.blit(txt, (364, 552))


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


restart()

while not sair:
    paint()
    sair = opned()











