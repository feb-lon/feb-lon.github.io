from math import floor, ceil

import faicons as fa
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data and compute static values
from shared import app_dir, pokemons, types, moves, type_priority

from shiny import App, Inputs, Outputs, Session, reactive, render, ui, render_plot


def simplified_page():
    return ui.nav_panel(
        "Simplified",
        ui.layout_columns(
            ui.card(
                ui.input_numeric("enemy_level_simplified", "Enemy Level:", 8, min=1, max=100),
                ui.input_numeric("move_power_simplified", "Move Power:", 50, step=5),
                ui.input_numeric("own_defense_simplified", "Own Defense:", 20),
                ui.input_numeric("damage_received_simplified", "Damage Received:", 5),
            ),
            ui.card(
                ui.output_plot("calculate_offense_simplified"),
            ),
            col_widths=(3, 9),
        )
    )


def advanced_page():
    return ui.nav_panel(
        "Advanced",
        ui.page_fluid(
            ui.layout_columns(
                ui.card(
                    "Own Pokemon:",
                    ui.input_numeric("dmg_received_advanced", "Damage Received:", 10, min=1),
                    ui.navset_card_tab(
                        ui.nav_panel("Pokemon",
                                     ui.input_selectize("own_pokemon", "Select your Pokemon", pokemons["Pokemon"]),
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
                ui.card(
                    ui.input_numeric("enemy_level_advanced", "Enemy Level:", 8, min=1, max=100),
                    ui.input_selectize("enemy_move", "EnemyMove", moves["Name"]),
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
                ui.output_plot("calculate_offense_advanced"),
            ),
                col_widths=(3, 3, 6),
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
        ),
        title="Gen 3 Calculator",
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
        ax.set_ylabel("Nr. of rolls / 16")
        ax.set_xlabel("ATK value")
        dmg = []
        enemy_level = int(input.enemy_level_simplified())
        move_power = int(input.move_power_simplified())
        own_defense = int(input.own_defense_simplified())
        damage_received = int(input.damage_received_simplified())

        min_offense_guess = max(1, int(floor(
            ((damage_received - 2) * 50) * own_defense / move_power / floor(enemy_level * 2 / 5 + 2))) - 3)

        max_offense_guess = min(600, int(ceil((ceil(
            (ceil(damage_received / 0.75) - 2) * 50 + 49) * own_defense + own_defense - 1) / move_power / floor(
            enemy_level * 2 / 5 + 2))) + 3)

        min_offense = -1
        max_offense = -1

        for x in range(min_offense_guess, max_offense_guess + 1):
            dmg.append(0)
            dmg100 = floor(floor(floor(enemy_level * 2 / 5 + 2) * move_power * x / own_defense) / 50 + 2)
            for y in range(16):
                if floor(dmg100 * (y + 85) / 100) == damage_received:
                    dmg[x - min_offense_guess] += 1
                    max_offense = x
                    if min_offense == -1:
                        min_offense = x

        dmg = dmg[(min_offense - min_offense_guess): (max_offense - min_offense_guess + 1)]

        ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])
        ax.set_ylim(0, 16)
        ax.set_xticks(range(min_offense, max_offense + 1))
        ax.bar(range(min_offense, max_offense + 1), dmg)
        return fig




    @render.plot
    def calculate_offense_advanced():
        fig, ax = plt.subplots()
        ax.set_title("Attack Value Likelihood")
        ax.set_ylabel("Nr. of rolls / 16")
        ax.set_xlabel("ATK value")
        print(1)
        dmg = []

        enemy_level = int(input.enemy_level_advanced())
        print(1.1)
        own_pokemon = input.own_pokemon()
        print(2)
        type1, type2 = get_pokemon_types(own_pokemon)
        print(3)
        own_defense = int(input.def_spd())
        own_defense_stage = int(input.def_spd_stage())
        has_reflect_lightscreen = input.reflect_lightscreen()
        has_def_spd_badge = input.def_spd_badge()
        has_thick_fat = input.thick_fat()
        print(has_reflect_lightscreen)

        enemy_level_advanced = int(input.enemy_level_advanced())
        enemy_move = int(input.enemy_move())
        move_power, move_type, is_physical = get_move_attributes(enemy_move)
        eff1, eff2 = calc_effectiveness(move_type, type1, type2)
        is_stab = input.enemy_stab()
        atk_spa_stage = int(input.atk_spa_stage())
        is_crit = input.crit()
        is_burned = input.burned()
        ff_active = input.ff_active()
        has_dd_or_charge = input.dd_charge()
        weather = input.weather()
        damage_received = int(input.dmg_received_advanced())
        print(weather)
        print(
            damage_received, [eff2, eff1, 1.5 if is_stab else 1, 2 if has_dd_or_charge else 1, 2 if is_crit else 1],
            [1.5 if ff_active and move_type == "Fire" else 1, get_weather_modifier(weather),
             (0.5 if has_reflect_lightscreen and not is_crit else 1), 0.5 if is_burned and is_physical else 1],
            calc_stat_stages(floor(own_defense * (1.1 if has_def_spd_badge else 1)), own_defense_stage),
            calc_base_power(enemy_level_advanced, move_power), atk_spa_stage)

        min_offense_guess, max_offense_guess = calc_offense_backwards(
            damage_received, [eff2, eff1, 1.5 if is_stab else 1, 2 if has_dd_or_charge else 1, 2 if is_crit else 1],
            [1.5 if ff_active and move_type == "Fire" else 1, get_weather_modifier(weather),
             0.5 if has_reflect_lightscreen and not is_crit else 1, 0.5 if is_burned and is_physical else 1],
            calc_stat_stages(floor(own_defense * (1.1 if has_def_spd_badge else 1)), own_defense_stage),
            calc_base_power(enemy_level_advanced, move_power), atk_spa_stage
        )
        print("min: ", min_offense_guess)
        print("max: ", max_offense_guess)

        min_offense = -1
        max_offense = -1

        for x in range(min_offense_guess, max_offense_guess + 1):
            dmg.append(0)
            dmg100 = floor(floor(floor(enemy_level * 2 / 5 + 2) * move_power * x / own_defense) / 50 + 2)
            for y in range(16):
                if floor(dmg100 * (y + 85) / 100) == damage_received:
                    dmg[x - min_offense_guess] += 1
                    max_offense = x
                    if min_offense == -1:
                        min_offense = x

        dmg = dmg[(min_offense - min_offense_guess): (max_offense - min_offense_guess + 1)]

        ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])
        ax.set_ylim(0, 16)
        ax.set_xticks(range(min_offense, max_offense + 1))
        ax.bar(range(min_offense, max_offense + 1), dmg)
        return fig

    def get_move_attributes(move):
        return int(moves["Power"][int(move)]), moves["Type"][int(move)], moves["Stat"][int(move)] == "Physical"

    def get_pokemon_types(pokemon):
        return pokemons["Type 1"][int(pokemon)], pokemons["Type 2"][int(pokemon)]

    def calc_effectiveness(move_type, mon_type_1, mon_type_2):
        type_1_prio = type_priority[mon_type_1]
        type_2_prio = type_priority[mon_type_2]
        move_used_key = type_priority[move_type]
        if type_1_prio < type_2_prio:
            return types.loc[[move_used_key]][mon_type_1][0], types.loc[[move_used_key]][mon_type_2][0]
        else:
            return types.loc[[move_used_key]][mon_type_2][0], types.loc[[move_used_key]][mon_type_1][0]

    def biv_min(level: int, current_stat: int, evs: int, nature: float):
        return max(22, int(floor(floor(floor(current_stat / nature) - 5) * 100 / level) + (0 if not (nature == 0.9 and current_stat % 10 == 0) else 100 % level) - floor(evs / 4)))

    def biv_max(level: int, current_stat: int, evs: int, nature: float):
        return min(541, int(np.floor(ceil(ceil(current_stat + (0 if (nature == 1.1 and current_stat % 11 == 0) else 0.01)) / nature - (5 if nature == 1 else 4)) * 100 / level) + 1 - floor(evs / 4)))

    def biv_to_base_min(biv):
        return ceil((biv - 31) / 2)

    def biv_to_base_max(biv):
        return np.floor(biv / 2)

    def calc_dmg_base(level: int, move_power: int, offense: int, defense: int):
        return floor(floor(2*level / 5 + 2) * move_power * offense / defense)

    def calc_base_power(level: int, move_power: int):
        return floor(2*level / 5 + 2) * move_power

    def get_weather_modifier(weather):
        return {"is Neutral": 1, "Increases Damage": 1.5, "Decreases Damage": 0.5}.get(weather, 1)

    def calc_stat_stages(stat: int, stages: int):
        return floor(stat * (2 + (stages if stages > 0 else 0)) / (2 - (stages if stages < 0 else 0)))

    #ibm = "inside bracket modifier", the modifiers before the +2 in the formula
    #obm = "outside bracket modifier", the modifiers after the +2 in the formula
    # see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III
    def calc_offense_backwards(dmg_dealt: int, obm: list, ibm: list, defense: int, base_power: int, offense_stage: int):
        offense_guess_min = dmg_dealt
        offense_guess_max = ceil(dmg_dealt/0.85) + 1
        for factor in obm:
            offense_guess_min = floor(offense_guess_min  / factor)
            offense_guess_max = floor(offense_guess_max  / factor) + (0 if factor == 1 else 1)

        offense_guess_min = offense_guess_min - 2
        offense_guess_max = offense_guess_max - 2

        for factor in ibm:
            offense_guess_min = floor(offense_guess_min / factor)
            offense_guess_max = floor(offense_guess_max / factor) + (0 if factor == 1 else 1)

        offense_guess_min = calc_stat_stages_backwards(floor(int(offense_guess_min * 50 * defense) / int(base_power)), offense_stage)[0]
        offense_guess_max = calc_stat_stages_backwards(floor(int((offense_guess_max * 50 + 49) * defense + defense -1) / int(base_power)), offense_stage)[1]

        # to be careful add / subtract one
        return offense_guess_min - 1, offense_guess_max + 1

    def calc_stat_stages_backwards(stat: int, stages: int):
        original_stat = stat / (2 + (stages if stages > 0 else 0)) * (2 - (stages if stages < 0 else 0))
        if stages < 0:
            result = ceil(original_stat)
            return result, result - ceil(stages / 2)
        else:
            result = floor(original_stat)
            return result, result


app = App(app_ui, server)
