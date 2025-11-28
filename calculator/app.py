from math import floor

import faicons as fa
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data and compute static values
from shared import app_dir, pokemons, types, moves

from shiny import App, Inputs, Outputs, Session, reactive, render, ui

def simplified_page():
    return ui.nav_panel(
        "Simplified",
        ui.layout_columns(
            ui.card(
                ui.input_numeric("enemy_level_simplified", "Enemy Level:", 8, min=1, max=100),
                ui.input_numeric("move_power", "Move Power:", 50, step=5),
                ui.input_numeric("own_defense", "Own Defense:", 20),
                ui.input_numeric("damage_received", "Damage Received:", 5),
            ),
            ui.card(
                ui.output_plot("calculate_offense_simplified"),
            ),
            col_widths = (3, 9),
        )
    )

def advanced_page():
    return ui.nav_panel(
        "Advanced",
        ui.page_sidebar(
            ui.sidebar(
                "Own Pokemon:",
                ui.navset_card_tab(
                    ui.nav_panel("Pokemon",
                                 ui.input_selectize("pokemon", "Select your Pokemon", pokemons["Pokemon"]),
                                 ),
                    ui.nav_panel("Type",
                                 ui.input_selectize("types", "Select types:", types["Type"], multiple=True)
                                 ),
                    id="input_type",
                ),
                ui.input_numeric("def_spd", "Own DEF/SPD:", 20, min=4),
                ui.input_numeric("def_spd_stage", "Own DEF/SPD Stage:", 0, min=-6, max=6),
                ui.input_switch("reflect_lightscreen", "Reflect / Lightscreen:"),
                ui.input_switch("def_spd_badge", "DEF/SPD Badge:"),
                ui.input_switch("thick_fat", "Thick Fat:"),
                ui.include_css(app_dir / "styles.css"),
            ),
            ui.page_fluid(
                ui.layout_columns(
                    ui.card(
                        ui.input_numeric("enemy_level_advanced", "Enemy Level:", 8, min=1, max=100),
                        ui.input_selectize("enemy_move", "EnemyMove", ["Tackle", "Pound"]),
                        ui.input_switch("enemy_stab", "Move gets STAB bonus:"),
                        ui.input_numeric("atk_spa_stage", "Enemy ATK/SPA Stage:", 0, min=-6, max=6),
                        ui.input_switch("crit", "Move gets STAB bonus:"),
                        ui.input_switch("burned", "Enemy is burned:"),
                        ui.input_switch("ff_active", "Enemy gets bonus from Flashfire"),
                        ui.input_switch("dd_charge", "Damage is doubled or Charge bonus active:"),
                        ui.input_select("weather", "The current Weather:",
                                        ["Increases Damage", "is Neutral", "Decreases Damage"],
                                        selected="is Neutral"),
                    ),
                    ui.card(
                        ui.input_text("test", label="test"),
                        px.scatter(title="1", x=pokemons["Pokemon"], y=pokemons["Exp."]),
                    ),
                    col_widths=(3, 9),
                ),
            ),
        ),
    )


app_ui = \
    ui.page_fluid(
        ui.navset_tab(
            ui.nav_spacer(),
            simplified_page(),
            advanced_page(),
            id="mode"
        )
    )


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.effect
    @reactive.event(input.input_type, input.types, input.pokemon)
    def _():
        if f"{input.input_type()}" == "Type":
            ui.update_text("test", value=f"{input.types()}")
        else:
            ui.update_text("test", value=f"{input.pokemon()}")

    @render.plot
    def calculate_offense_simplified():
        fig, ax = plt.subplots()
        ax.set_title("Attack Value Likelihood")
        dmg = []
        enemy_level = int(input.enemy_level_simplified())
        move_power = int(input.move_power())
        own_defense = int(input.own_defense())
        damage_received = int(input.damage_received())

        min_offense_guess = max(1, int(floor(((damage_received-2)*50)*own_defense/move_power/floor(enemy_level*2/5+2)))-3)
        max_offense_guess = min(600, int(np.ceil((np.ceil((np.ceil(damage_received/0.75)-2)*50+49)*own_defense+own_defense-1)/move_power/floor(enemy_level*2/5+2)))+3)

        minOffense = -1
        maxOffense = -1

        for x in range(min_offense_guess, max_offense_guess+1):
            dmg.append(0)
            dmg100 = floor(floor(floor(enemy_level * 2 / 5 + 2) * move_power * x / own_defense) / 50 + 2)
            for y in range(16):
                if floor(dmg100 * (y + 85) / 100) == damage_received:
                    dmg[x-min_offense_guess] += 1
                    maxOffense = x
                    if minOffense == -1:
                        minOffense = x

        dmg = dmg[(minOffense - min_offense_guess) : (maxOffense - min_offense_guess + 1)]

        ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])
        ax.set_ylim(0, 16)
        ax.set_xticks(range(minOffense, maxOffense + 1))
        ax.bar(range(minOffense, maxOffense + 1), dmg)
        return fig


app = App(app_ui, server)
