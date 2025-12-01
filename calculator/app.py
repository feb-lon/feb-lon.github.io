from math import floor, ceil, isnan

import faicons as fa
import pandas
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.core.common import is_empty_slice

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
                        id = "input_type_type",
                    ),
                    ui.input_numeric("def_spd", "Own DEF/SPD:", 20, min=4),
                    ui.input_numeric("def_spd_stage", "Own DEF/SPD Stage:", 0, min=-6, max=6),
                    ui.input_switch("reflect_lightscreen", "Reflect / Lightscreen:"),
                    ui.input_switch("def_spd_badge", "DEF/SPD Badge:"),
                    ui.input_switch("thick_fat", "Thick Fat:"),
                    ui.include_css(app_dir / "styles.css"),
                ),
                ui.card(
                    "Enemy Pokemon:",
                    ui.input_numeric("enemy_level_advanced", "Enemy Level:", 8, min=1, max=100),
                    ui.navset_card_tab(
                        ui.nav_panel("Move Name",
                                ui.input_selectize("enemy_move", "Enemy Move", choices=moves["Name"]),
                                ),
                        ui.nav_panel("Power + Type",
                                ui.input_numeric("enemy_move_power", "Enemy Move Power", min=5, value=50, step=5),
                                    ui.input_selectize("enemy_move_type", "Enemy Move Type", choices=type_priority, selected="Normal"),
                                ),
                        id = "enemy_move_selection_type"
                    ),
                    ui.input_switch("enemy_stab", "Move gets STAB bonus:"),
                    ui.input_numeric("atk_spa_stage", "Enemy ATK/SPA Stage:", 0, min=-6, max=6),
                    ui.input_switch("crit", "Hit was a crit"),
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
        dmg = []

        type1 = ""
        type2 = ""
        if input.input_type_type() == "Pokemon":
            own_pokemon = input.own_pokemon()
            type1, type2 = get_pokemon_types(own_pokemon)
        elif input.input_type_type() == "Type":
            type1_number = "" if len(input.types()) == 0 else input.types()[0]
            type2_number = "" if len(input.types()) <= 1 else input.types()[1]
            type1 = type_priority[int(type1_number)] if not type1_number == "" else ""
            type2 = type_priority[int(type2_number)] if not type2_number == "" else ""

        move_type = ""
        move_power = 0
        is_physical = False
        if input.enemy_move_selection_type() == "Move Name":
            enemy_move_key = int(input.enemy_move())
            move_power = int(moves["Power"][int(enemy_move_key)])
            move_type = moves["Type"][int(enemy_move_key)]
            is_physical = moves["Stat"][int(enemy_move_key)] == "Physical"
        elif input.enemy_move_selection_type() == "Power + Type":
            move_power = int(input.enemy_move_power())
            move_type = input.enemy_move_type()
            is_physical = is_type_physical(type_priority.index(move_type))
        eff1, eff2 = calc_effectiveness(move_type, type1, type2)

        own_defense = int(input.def_spd())
        own_defense_stage = int(input.def_spd_stage())
        has_reflect_lightscreen = input.reflect_lightscreen()
        has_def_spd_badge = input.def_spd_badge()
        has_thick_fat = input.thick_fat()

        enemy_level_advanced = int(input.enemy_level_advanced())
        is_stab = input.enemy_stab()
        atk_spa_stage = int(input.atk_spa_stage())
        is_crit = input.crit()
        is_burned = input.burned()
        ff_active = input.ff_active()
        has_double_damage_or_charge = input.dd_charge()
        weather = input.weather()
        weather_modifier = get_weather_modifier(weather)
        damage_received = int(input.dmg_received_advanced())

        min_offense_guess, max_offense_guess = calc_offense_backwards(
            damage_received, is_physical, [eff2, eff1, 1.5 if is_stab else 1, 2 if has_double_damage_or_charge else 1, 2 if is_crit else 1],
            [1.5 if ff_active and move_type == "Fire" else 1, weather_modifier,
             0.5 if has_reflect_lightscreen and not is_crit else 1, 0.5 if is_burned and is_physical else 1],
            calc_stat_stages(floor(own_defense * (1.1 if has_def_spd_badge else 1)), own_defense_stage),
            calc_base_power(enemy_level_advanced, move_power), atk_spa_stage
        )

        min_offense = -1
        max_offense = -1

        base_power = calc_base_power(enemy_level_advanced, move_power)

        for x in range(min_offense_guess, max_offense_guess + 1):
            dmg.append(0)
            full_damage = floor(floor(base_power * calc_stat_stages(x, atk_spa_stage) / calc_defensive_stat_modifiers(own_defense, has_def_spd_badge, own_defense_stage)) / 50)
            full_damage = calc_ibm_damage(int(full_damage), is_burned and is_physical, has_reflect_lightscreen and not is_crit, weather_modifier, ff_active and move_type == "Fire")
            full_damage = calc_obm_damage_no_randomness(full_damage, is_crit, has_double_damage_or_charge, is_stab, eff1, eff2)


            for y in range(16):
                if floor(full_damage * (y + 85) / 100) == damage_received:
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

    def is_type_physical(type_number: int):
        return type in [0, 6, 7, 8, 9, 11, 12, 13, 16]

    #ibm = "inside bracket modifier", the modifiers before the +2 in the formula
    #obm = "outside bracket modifier", the modifiers after the +2 in the formula
    # see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III
    def calc_offense_backwards(dmg_dealt: int, is_physical: bool, obm: list, ibm: list, defense: int, base_power: int, offense_stage: int):
        offense_guess_min = dmg_dealt
        offense_guess_max = ceil(dmg_dealt/0.85) + 1
        for factor in obm:
            offense_guess_min = floor(offense_guess_min / factor)
            offense_guess_max = floor(offense_guess_max / factor) + (0 if factor == 1 else 1)

        offense_guess_min = offense_guess_min - 2
        offense_guess_max = offense_guess_max - 2

        #physical moves always deal at least 1 dmg at this point in the calculation
        if offense_guess_min < 1 and is_physical:
            offense_guess_min = 0

        for factor in ibm:
            offense_guess_min = floor(offense_guess_min / factor)
            offense_guess_max = floor(offense_guess_max / factor) + (0 if factor == 1 else 1)

        offense_guess_min = calc_stat_stages_backwards(floor(int(offense_guess_min * 50 * defense) / int(base_power)), offense_stage)[0]
        offense_guess_max = calc_stat_stages_backwards(floor(int((offense_guess_max * 50 + 49) * defense + defense - 1) / int(base_power)), offense_stage)[1]

        # to be careful add / subtract one
        return offense_guess_min - 1, offense_guess_max + 1

    def calc_ibm_damage(base_damage: int, is_burned_and_move_is_physical: bool, has_barrier_lightscreen: bool, current_weather_impact: float, is_flash_fire_relevant: bool):
        result = base_damage
        if is_burned_and_move_is_physical: result = floor(result / 2)
        if has_barrier_lightscreen: result = floor(result / 2)
        result = floor(result * get_weather_modifier(current_weather_impact))
        if is_flash_fire_relevant: result = floor(base_damage * 1.5)
        return result + 2

    def calc_obm_damage_no_randomness(base_damage: int, is_crit: bool, has_double_damage_or_charge: bool, is_stab: bool, effectiveness_type_1: float, effectiveness_type_2: float):
        result = base_damage
        if is_crit: result = result * 2
        if has_double_damage_or_charge: result = result * 2
        if is_stab: result = floor(result * 1.5)
        result = floor(floor(result * effectiveness_type_1) * effectiveness_type_2)
        return result

    def calc_stat_stages_backwards(stat: int, stages: int):
        original_stat = stat / (2 + (stages if stages > 0 else 0)) * (2 - (stages if stages < 0 else 0))
        if stages < 0:
            result = ceil(original_stat)
            return result, result - ceil(stages / 2)
        else:
            result = floor(original_stat)
            return result, result

    def calc_defensive_stat_modifiers(stat: int, defensive_badge: bool, defensive_stage: int):
        result = stat
        if defensive_badge:
            result = floor(stat * 1.1)
        result = calc_stat_stages(result, defensive_stage)
        return result

    def get_pokemon_types(pokemon):
        return pokemons["Type 1"][int(pokemon)], pokemons["Type 2"][int(pokemon)]

    def calc_effectiveness(move_type, mon_type_1, mon_type_2):

        move_used_key = type_priority.index(move_type)

        if mon_type_1 == "": return 1, 1
        elif mon_type_2 == "": return types[mon_type_1][move_used_key], 1
        else:
            type_1_effectiveness = types[mon_type_1][move_used_key]
            type_2_effectiveness = types[mon_type_2][move_used_key]
            type_1_prio=type_priority.index(mon_type_1)
            type_2_prio=type_priority.index(mon_type_2)
            if type_1_prio<type_2_prio:
                return type_1_effectiveness, type_2_effectiveness
            else:
                return type_2_effectiveness, type_1_effectiveness

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


app = App(app_ui, server)
