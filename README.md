# Protótipo de Jogo 2D em Python (Estilo Pokémon)

## Requisitos
- Python 3.8 ou superior
- Instalar o pygame:
```
pip install pygame
```

## Como rodar
1. Extraia o projeto.
2. Abra o terminal na pasta extraída.
3. Execute:
```
python main.py
```

## Controles
- **WASD ou Setas** → mover
- **E** → Interagir com NPC
- **↑/↓** → Navegar nas opções
- **Enter** → Confirmar resposta

## O que vem pronto
✔ Player com movimento  
✔ NPC com pergunta  
✔ Sistema de escolhas  
✔ Tilemap 8-bit  
✔ Tileset incluído em: `/assets/tileset_16x16.png`  

## Estrutura
- `main.py` — Loop principal  
- `engine/` — Player, NPC, diálogo, tilemap, gerenciador de cenas  
- `assets/` — Tileset  
- `data/perguntas.json` — Perguntas do jogo  

---
Agora você só precisa personalizar perguntas, sprites e fases 🔥
