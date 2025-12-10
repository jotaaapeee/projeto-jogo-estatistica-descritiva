"""
Script para gerar arquivos JSON de mapas automaticamente.
Use o visualizador de tiles (debug_tileset_viewer.py) para descobrir os índices dos tiles.
"""
import json
import os

def criar_mapa_simples(map_index, nome):
    """Cria um mapa simples retangular"""
    width = 30
    height = 18
    
    # Tiles (ajuste conforme seu tileset)
    WALL_TOP_LEFT = 75
    WALL_TOP_RIGHT = 77
    WALL_TOP = 76
    WALL_BOTTOM_LEFT = 100
    WALL_BOTTOM_RIGHT = 102
    WALL_BOTTOM = 101
    WALL_LEFT = 129
    WALL_RIGHT = 128
    FLOOR = 30
    
    map_data = []
    for y in range(height):
        row = []
        for x in range(width):
            if y == 0:
                if x == 0:
                    tile = WALL_TOP_LEFT
                elif x == width - 1:
                    tile = WALL_TOP_RIGHT
                else:
                    tile = WALL_TOP
            elif y == height - 1:
                if x == 0:
                    tile = WALL_BOTTOM_LEFT
                elif x == width - 1:
                    tile = WALL_BOTTOM_RIGHT
                else:
                    tile = WALL_BOTTOM
            else:
                if x == 0:
                    tile = WALL_LEFT
                elif x == width - 1:
                    tile = WALL_RIGHT
                else:
                    tile = FLOOR
            row.append(tile)
        map_data.append(row)
    
    return {
        "name": nome,
        "description": f"Mapa {map_index + 1} gerado automaticamente",
        "map_data": map_data
    }

def salvar_mapa(map_data, map_index):
    """Salva um mapa em arquivo JSON"""
    os.makedirs("data/maps", exist_ok=True)
    path = f"data/maps/map_{map_index}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(map_data, f, indent=2, ensure_ascii=False)
    print(f"✓ Mapa salvo em {path}")

def main():
    print("Gerando 6 mapas básicos...")
    
    nomes = [
        "Sala Simples",
        "Sala com Pilares",
        "Sala com Corredor",
        "Sala Central",
        "Sala Dividida",
        "Sala com Grid"
    ]
    
    for i in range(6):
        mapa = criar_mapa_simples(i, nomes[i])
        salvar_mapa(mapa, i)
    
    print("\n✓ Todos os mapas foram gerados!")
    print("\nPara personalizar os mapas:")
    print("1. Use debug_tileset_viewer.py para ver os índices dos tiles")
    print("2. Edite os arquivos em data/maps/map_X.json")
    print("3. Ou modifique este script para criar mapas mais complexos")

if __name__ == "__main__":
    main()

