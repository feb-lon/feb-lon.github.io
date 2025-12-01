from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
pokemons = pd.read_csv(app_dir / "Pokemon.csv", keep_default_na=False)
types = pd.read_csv(app_dir / "type_effectiveness.csv")
moves = pd.read_csv(app_dir / "Moves.csv")
type_priority = [
    "Normal",
    "Fire",
    "Water",
    "Electric",
    "Grass",
    "Ice",
    "Fighting",
    "Poison",
    "Ground",
    "Flying",
    "Psychic",
    "Bug",
    "Rock",
    "Ghost",
    "Dragon",
    "Dark",
    "Steel"
]
