# River Raid Cover

Cover jogável do clássico River Raid, em Python com Pygame. Você pilota um avião no rio, desvia das margens, atira em helicópteros, navios e jatos, e segura o combustível até a ponte da base. Cada ponte destruída abre a fase seguinte.

## Linux

Na pasta `River_Raid` (onde está `RiverRaid.py`):

```bash
cd River_Raid
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python RiverRaid.py
```

O `requirements.txt` pede `pygame-ce`. No Python 3.14 o pacote `pygame` clássico não tem wheel e tenta compilar SDL. O `pygame-ce` instala pronto e o jogo continua fazendo `import pygame`.

Os sons são carregados a partir da pasta deste arquivo, então o comando também funciona se você chamar `python River_Raid/RiverRaid.py` de outro diretório.

## Controles

- Setas esquerda e direita: mover o avião
- Seta para cima: acelerar
- Seta para baixo: reduzir
- Espaço: atirar
- F2 ou o botão Jogar: começar (ou jogar de novo)
- Na pista, qualquer tecla solta o avião
- ESC: sair

O botão fica no centro da capa. Passe o mouse para o hover e clique.

## Fases

1. Rio clássico. Helicóptero, navio, jato e posto, do jeito do cover original.
2. Garganta. Margens estreitas, mais navio, e uma boia que pisca como posto e some no toque sem encher o tanque.
3. Neblina. Um feixe varre o rio. Fora dele o inimigo não aparece, mas a colisão continua.
4. Comboio. Rajada de jatos, combustível mais lento, e uma sombra que cruza no sentido contrário sem pontuar e sem colidir.
5. Temporal. Chuva, relâmpago que esconde o medidor e um vento que empurra o avião. A ponte seguinte volta para a fase 1, com a velocidade já acumulada (teto de 4 pixels).

## Arquivos

- `RiverRaid.py` — loop, capa, fases e HUD
- `obj.py` — avião, inimigos, posto, explosão
- `place.py` — margens e base
- `ilhas.py` — ilhas
- `ponte.py` — pontes
- `shot.py` — tiro
- `cores.py` — paleta
- `sons/` — efeitos
- `requirements.txt` — dependência

São 3 vidas. Sem combustível ou batendo na margem, no inimigo ou na ponte, o avião explode. Destruir a ponte da base vale 250 pontos e troca a fase.
