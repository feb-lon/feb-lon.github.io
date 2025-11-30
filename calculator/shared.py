from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
pokemons = pd.read_csv(app_dir / "Pokemon.csv")
types = pd.read_csv(app_dir / "type_effectiveness.csv")
moves = pd.read_csv(app_dir / "Moves.csv")
type_priority = {
    "Normal": 0,
    "Fire": 1,
    "Water": 2,
    "Electric": 3,
    "Grass": 4,
    "Ice": 5,
    "Fighting": 6,
    "Poison": 7,
    "Ground": 8,
    "Flying": 9,
    "Psychic": 10,
    "Bug": 11,
    "Rock": 12,
    "Ghost": 13,
    "Dragon": 14,
    "Dark": 15,
    "Steel": 16
}
