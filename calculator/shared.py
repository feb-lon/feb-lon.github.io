from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
pokemons = pd.read_csv(app_dir / "Pokemon.csv")
types = pd.read_csv(app_dir / "type_effectiveness.csv")
moves = pd.read_csv(app_dir / "Moves.csv")
