# River Raid Cover

Este é um clone do clássico jogo **River Raid**, desenvolvido em Python utilizando a biblioteca **Pygame**. O objetivo do jogo é controlar um avião, desviar de obstáculos, destruir inimigos e gerenciar o nível de combustível para alcançar a maior pontuação possível.

## 🎮 Como Jogar

- **F12**: Inicia o jogo.
- **Seta para a Esquerda/Direita**: Move o avião para os lados.
- **Seta para Cima**: Aumenta a velocidade.
- **Seta para Baixo**: Diminui a velocidade.
- **Espaço**: Atira.

Evite colidir com obstáculos e inimigos, e colete combustível para continuar voando!

## 🛠️ Instalação

1. Certifique-se de ter o Python 3.8+ instalado em sua máquina.
2. Clone este repositório:
   ```bash
   git clone https://github.com/Jetsetjedi/River-Raid-cover.git
   cd river-raid-cover
3. Crie um ambiente virtual e instale as dependencias:
    python -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    pip install pygame
4. Execute o jogo:
    python RiverRaid.py

 📂 Estrutura do Projeto

 River_Raid/
├── [cores.py](http://_vscodecontentref_/0)          # Definição de cores usadas no jogo
├── [ilhas.py](http://_vscodecontentref_/1)          # Implementação das ilhas
├── [obj.py](http://_vscodecontentref_/2)            # Implementação de objetos (aviões, helicópteros, etc.)
├── [place.py](http://_vscodecontentref_/3)          # Implementação de terrenos
├── [ponte.py](http://_vscodecontentref_/4)          # Implementação das pontes
├── [shot.py](http://_vscodecontentref_/5)           # Implementação do tiro
├── [RiverRaid.py](http://_vscodecontentref_/6)      # Arquivo principal do jogo
├── sons/             # Sons usados no jogo
│   ├── explode.wav
│   ├── gaz_alert.wav
│   ├── ...
└── [REDAME.md](http://_vscodecontentref_/7)         # Este arquivo   
# River Raid - Cover (Python / Pygame)

Clone / cover do clássico River Raid implementado em Python com Pygame.

## Descrição
Você controla um avião, deve desviar de obstáculos, destruir inimigos e gerenciar combustível para sobreviver o máximo possível.

## Dependências
- Python 3.8+
- pygame

Instalação rápida (Windows PowerShell):

```powershell
python -m venv venv
venv\Scripts\activate
pip install pygame
```

## Como executar
Na pasta do projeto (onde está `RiverRaid.py`):

```powershell
python RiverRaid.py
```

## Controles
- Seta Esquerda: mover avião para a esquerda
- Seta Direita: mover avião para a direita
- Seta Cima: acelerar (aumenta velocidade do mapa)
- Seta Baixo: reduzir velocidade
- Espaço: atirar
- F2: reiniciar / começar o jogo (também há botão reiniciar quando o jogo acabar)
- ESC: sair
- Clique do mouse (botão esquerdo): clicar no botão "Reiniciar Jogo" que aparece no centro da tela quando a partida termina

Observação: ao terminar a partida (`game == False`) o botão "Reiniciar Jogo" aparece no centro do mapa. Passe o mouse sobre o botão para ver o efeito de hover e clique para reiniciar.

## Estrutura do projeto
- `RiverRaid.py` - arquivo principal do jogo
- `obj.py` - definição de objetos (aviões, inimigos, explosões)
- `place.py` - terrenos e base
- `shot.py` - lógica do tiro
- `cores.py` - paleta de cores utilizada
- `sons/` - pasta com os efeitos sonoros

## Observações e dicas
- Se o avião não aparecer ao abrir o jogo, pressione `F2` ou espere a tela mostrar o botão de reinício e clique nele.
- Para desenvolver: mantenha o Pygame atualizado e use um ambiente virtual para evitar conflitos.

## Como contribuir
1. Faça um fork
2. Crie uma branch: `git checkout -b minha-feature`
3. Commit e push
4. Abra um Pull Request

---
Feito com carinho para brincar com o clássico River Raid. Boa diversão! :)
