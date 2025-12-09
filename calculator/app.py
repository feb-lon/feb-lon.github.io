from math import floor, ceil, isnan

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from shiny.types import SilentException

# Load data and compute static values
from shared import *

from shiny import App, Inputs, Outputs, Session, reactive, render, ui, render_plot, render_ui, req


def xp_ev_info_page():
    return ui.nav_panel(
        "XP / EV Info",
        ui.layout_columns(
            ui.page_fluid(
                ui.page_fluid(
                    ui.h4("Pokemon Yields"),
                    ui.input_selectize("pokemon_info", "Select Pokemon:", sorted(pokemons.index)),
                    ui.input_numeric("enemy_level_info", "Level:", 8, min=1, max=100),
                    ui.input_switch("is_trainer_info", "Trainer Fight"),
                    ui.h4("You will get the following EVs / XP:"),
                    ui.output_table("calculate_xp_ev_info"),
                ),
            ),
            ui.page_fluid(),
            ui.page_fluid(
                ui.h4("XP requirement"),
                ui.input_selectize("xp_curve_1_info", "XP Curve:", choices=list(experience.head()),
                                   selected="Fluctuating"),
                ui.input_numeric("level_from_1_info", "Level From:", min=1, max=100, value=5),
                ui.input_numeric("level_to_1_info", "Level To:", min=1, max=100, value=8),
                "XP required: ",
                ui.output_code("calc_xp_from_to"),
            ),
            ui.page_fluid(),
            col_widths=(4, 4, 4),
        )
    )


def atk_spa_calculator_page():
    return ui.nav_panel(
        "Calculator",
        ui.layout_columns(
            ui.h2("ATK / SPA Calculator"),
        ),
        ui.layout_columns(
            ui.page_fluid(
                ui.input_numeric("enemy_level", "Enemy Level:", 8, min=1, max=100),
                ui.input_numeric("move_power", "Move Power:", 50, step=5, min=5, max=999),
                ui.input_numeric("own_defense", "Own Defense:", 20, min=1, max=999),
                ui.input_numeric("damage_received", "DMG Taken:", 5, min=1, max=999),
                ui.layout_columns(
                    ui.input_switch("is_stab", "STAB Move"),
                    ui.input_switch("is_crit", "Critical Hit"),
                    id="stab_crit",
                ),
                ui.input_radio_buttons(
                    "effectiveness",
                    ui.tooltip(
                        ui.span("Effectiveness:   ", question_circle_fill),
                        "Effectiveness \"1x-\" is for cases where the move used has opposite effectivenes against the two defending types, and damage gets lost during rounding.\n In this generation, this is the case with: \n\n Bug -> Fire/Dark, Fight/Psy, Fly/Psy, Fly/Dark, Ghost/Dark \n Dark -> Fight/Psy \n Electric -> Electric/Fly, Electric \n Fight -> Fly/Dark, Fly/Steel, Psy/Rock, Bug/Rock, Bug/Steel \n Fire -> Water/Grass, Water/Ice, Water/Bug, Rock/Steel \n Grass -> Fire/Ground, Fire/Rock, Grass/Rock, Fly/Rock, Bug/Rock \n Ground -> Grass/Poison, Bug/Rock, Bug/Steel \n Ice -> Fire/Ground, Fire/Rock, Fire/Fly, Water/Grass, Water/Ground, Water/Fly, Water/Dragon, Ice/Ground, Ice/Fly \n Rock -> Ground/Fly, Ground/Bug \n Steel -> Fire/Rock, Water/Ice, Water/Rock \n Water -> Water/Ground, Water/Rock",
                        placement="left",
                        id="effectiveness_tooltip_advanced",
                    ),
                    {"0.25": "0.25x", "0.5": "0.5x", "1": "1x", "1-": "1x-", "2": "2x", "4": "4x"},
                    inline=True,
                    selected="1",
                ),
                ui.accordion(
                    ui.accordion_panel(
                        "Enemy Pokemon Modifiers:",
                        ui.input_numeric("atk_spa_stage", "ATK/SPA Stage:", 0, min=-6, max=6),
                        ui.input_switch("is_burned", "Enemy Burned"),
                        ui.input_switch("ff_active", "Flashfire Bonus"),
                        ui.input_switch("has_dd_charge", "Double Damage / Charge Bonus"),
                        ui.input_switch("is_physical", "Move is Physical"),
                        ui.input_select("enemy_ability", "Enemy Ability: ",
                                        {"1": "1x (irrelevant)", "1.5": "1.5x (e.g. Hustle, Swarm)", "2": "2x (Huge Power)"}),
                    ),
                    ui.accordion_panel(
                        "Own Pokemon Modifiers:",
                        ui.input_numeric("def_spd_stage", "DEF/SPD Stage:", 0, min=-6, max=6),
                        ui.input_switch("has_reflect_lightscreen", "Reflect / Lightscreen"),
                        ui.input_switch("has_def_spd_badge", "DEF/SPD Badge"),
                        ui.input_switch("has_thick_fat", "Thick Fat"),
                    ),
                    ui.accordion_panel(
                        "field effects:",
                        ui.input_radio_buttons(
                            "weather_modifier",
                            "Weather Modifier:",
                            {"0.5": "0.5x", "1": "1x", "1.5": "1.5x"},
                            inline=True,
                            selected="1",
                        ),
                        ui.input_switch("mud_or_water_sport_active", "Mud/Water Sport"),
                    ),
                    open=False,
                ),
            ),
            ui.page_fluid(
                ui.output_plot("calculate_offense"),
            ),
            col_widths=(3, 9),
        )
    )


app_ui = \
    ui.page_navbar(
        ui.nav_spacer(),
        atk_spa_calculator_page(),
        xp_ev_info_page(),
        ui.head_content(ui.include_css(app_dir / "styles.css")),
        id="mode",
        title="Pokemon Generation 3 Calculator",
        window_title="Gen 3 Calculator",
    )


def server(input: Inputs, output: Outputs, session: Session):
    @render.text
    def calc_xp_from_to():
        xp_curve = input.xp_curve_1_info()
        lvl_from = input.level_from_1_info()
        lvl_to = input.level_to_1_info()

        xp_all = experience[xp_curve][lvl_from:lvl_to].sum()

        return xp_all

    @render.table
    def calculate_xp_ev_info():

        pokemon = input.pokemon_info()
        is_trainer = input.is_trainer_info()
        enemy_level = input.enemy_level_info()

        xp = calc_xp_yield(pokemon, enemy_level, is_trainer)
        table = pokemons.loc[[pokemon], ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]]

        table["XP"] = xp
        return table

    @render.plot
    def calculate_offense():
        fig, ax = plt.subplots()
        ax.set_title("ATK/SPA Value Likelihood")
        ax.set_ylabel("Nr. of rolls / 16")
        ax.set_xlabel("ATK/SPA value")
        dmg = []

        enemy_level = int(input.enemy_level())
        move_power = int(input.move_power())
        own_defense = int(input.own_defense())
        damage_received = int(input.damage_received())

        is_stab = input.is_stab()
        stab_modifier = 1.5 if is_stab else 1

        is_crit = input.is_crit()
        crit_modifier = 2 if is_crit else 1

        eff1 = 0.5
        eff2 = 2

        if input.effectiveness() != "1-":
            effectiveness = float(input.effectiveness())
            eff2 = 2 if effectiveness == 4 else 1
            if effectiveness == 0.25: eff2 = 0.5
            eff1 = 2 if effectiveness > 1 else 1
            if effectiveness < 1: eff1 = 0.5

        is_physical = input.is_physical()

        weather_modifier = float(input.weather_modifier())

        has_thick_fat = input.has_thick_fat()
        thick_fat_modifier = 1 if not has_thick_fat else 0.5

        has_sport = input.mud_or_water_sport_active()
        sport_modifier = 1 if not has_sport else 0.5

        has_def_spd_badge = input.has_def_spd_badge()
        badge_def_spd_modifier = 1 if not has_def_spd_badge else 1.1

        is_burned = input.is_burned()
        burned_modifier = 0.5 if is_burned else 1

        ff_active = input.ff_active()
        ff_modifier = 1.5 if ff_active else 1

        has_double_damage_or_charge = input.has_dd_charge()
        double_damage_or_charge_modifier = 2 if has_double_damage_or_charge else 1

        has_reflect_lightscreen = input.has_reflect_lightscreen()
        reflect_lightscreen_modifier = 1 if (is_crit or not has_reflect_lightscreen) else 0.5

        if not (input.atk_spa_stage() or input.atk_spa_stage() == 0):
            raise SilentException()
        atk_spa_stage = int(input.atk_spa_stage())
        applied_atk_spa_stage = 0 if (is_crit and atk_spa_stage < 0) else atk_spa_stage

        if not (input.def_spd_stage() or input.def_spd_stage() == 0):
            raise SilentException()
        def_spd_stage = int(input.def_spd_stage())
        applied_def_spd_stage = 0 if (is_crit and def_spd_stage > 0) else def_spd_stage
        effective_def_spd = calc_defensive_stat_modifiers(own_defense, badge_def_spd_modifier, applied_def_spd_stage)

        enemy_ability_modifier = float(input.enemy_ability())

        min_offense_guess, max_offense_guess = calc_offense_backwards(
            damage_received, is_physical,
            [eff2, eff1, stab_modifier, double_damage_or_charge_modifier, crit_modifier],
            [ff_modifier, weather_modifier,
             reflect_lightscreen_modifier, burned_modifier],
            effective_def_spd,
            calc_base_power(enemy_level, move_power), applied_atk_spa_stage, sport_modifier, thick_fat_modifier, enemy_ability_modifier
        )

        min_offense = -1
        max_offense = -1

        base_power = calc_base_power(enemy_level, move_power)

        for x in range(min_offense_guess, max_offense_guess + 1):
            dmg.append(0)
            full_damage = floor(floor(
                base_power * calc_stat_stages(floor(floor(floor(x * enemy_ability_modifier) * thick_fat_modifier) * sport_modifier),
                                              applied_atk_spa_stage)
                / effective_def_spd) / 50)
            full_damage = calc_ibm_damage(int(full_damage), burned_modifier,
                                          reflect_lightscreen_modifier, weather_modifier, ff_modifier)
            full_damage = calc_obm_damage_no_randomness(full_damage, crit_modifier,
                                                        double_damage_or_charge_modifier, stab_modifier, eff1, eff2)

            for y in range(16):
                if floor(full_damage * (y + 85) / 100) == damage_received:
                    dmg[x - min_offense_guess] += 1
                    max_offense = x
                    if min_offense == -1:
                        min_offense = x

        dmg = dmg[(min_offense - min_offense_guess): (max_offense - min_offense_guess + 1)]

        ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])
        ax.set_ylim(0, 16)
        if max_offense - min_offense < 20:
            ax.set_xticks(range(min_offense, max_offense + 1))
        ax.bar(range(min_offense, max_offense + 1), dmg)
        if not fig:
            raise SilentException()
        return fig

    def is_type_physical(type_number: int):
        return type_number in [0, 6, 7, 8, 9, 11, 12, 13, 16]

    def get_move_attributes(enemy_move, current_weather):
        move_power = int(moves["Power"][enemy_move])
        move_type = moves["Type"][enemy_move]
        if enemy_move == "Weather Ball":
            if current_weather != "Clear":
                move_power = 100
                if current_weather == "Sunny": move_type = "Fire"
                if current_weather == "Sandstorm": move_type = "Rock"
                if current_weather == "Hail": move_type = "Ice"
                if current_weather == "Rain": move_type = "Water"
            else:
                move_power = 50
        elif enemy_move == "Solarbeam":
            if current_weather is not ("Clear" or "Sunny"): move_power = floor(move_power / 2)

        is_physical = is_type_physical(move_type) == "Physical"
        return move_type, move_power, is_physical

    # ibm = "inside bracket modifier", the modifiers before the +2 in the formula
    # obm = "outside bracket modifier", the modifiers after the +2 in the formula
    # see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III
    def calc_offense_backwards(dmg_dealt: int, is_physical: bool, obm: list, ibm: list, defense: int, base_power: int,
                               offense_stage: int, sport_modifier: float, thick_fat_modifier: float, enemy_ability_modifier: float):
        offense_guess_min = dmg_dealt
        offense_guess_max = ceil(dmg_dealt / 0.85) + 1
        for factor in obm:
            offense_guess_min = floor(offense_guess_min / factor)
            offense_guess_max = floor(offense_guess_max / factor) + (0 if factor == 1 else 1)

        offense_guess_min = offense_guess_min - 2
        offense_guess_max = offense_guess_max - 2

        # physical moves always deal at least 1 dmg at this point in the calculation
        if offense_guess_min < 1 and is_physical:
            offense_guess_min = 0

        for factor in ibm:
            offense_guess_min = floor(offense_guess_min / factor)
            offense_guess_max = floor(offense_guess_max / factor) + (0 if factor == 1 else 1)

        offense_guess_min = floor(floor(floor(calc_stat_stages_backwards(floor(int(offense_guess_min * 50 * defense)
                                                                         / int(base_power)), offense_stage)[
                                            0] / sport_modifier) / thick_fat_modifier) / enemy_ability_modifier)
        offense_guess_max = floor(floor(
            floor(calc_stat_stages_backwards(floor(int((offense_guess_max * 50 + 49) * defense + defense - 1)
                                                   / int(base_power)), offense_stage)[
                      1] / sport_modifier + 1) / thick_fat_modifier + 1) / enemy_ability_modifier + 1)

        return offense_guess_min, offense_guess_max

    def calc_ibm_damage(base_damage: int, burned_modifier: float, barrier_lightscreen_modifier: float,
                        current_weather_modifier: float, flash_fire_modifier: float):
        result = floor(floor(
            floor(floor(base_damage * flash_fire_modifier) * current_weather_modifier)
            * barrier_lightscreen_modifier) * burned_modifier)
        return result + 2

    def calc_obm_damage_no_randomness(base_damage: int, crit_modifier: int, double_damage_charge_modifier: int,
                                      stab_modifier: float,
                                      effectiveness_type_1: float, effectiveness_type_2: float):
        result = floor(base_damage * crit_modifier * double_damage_charge_modifier * stab_modifier)
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

    def calc_defensive_stat_modifiers(stat: int, defensive_badge_modifier: int, defensive_stage: int):
        result = floor(stat * defensive_badge_modifier)
        result = calc_stat_stages(result, defensive_stage)
        return result

    def get_pokemon_types(pokemon):
        return pokemons["Type 1"][pokemon], pokemons["Type 2"][pokemon]

    def calc_effectiveness(move_type, mon_type_1, mon_type_2):

        if mon_type_1 == "":
            return 1, 1
        elif mon_type_2 == "":
            return types[mon_type_1][move_type], 1
        else:
            type_1_effectiveness = types[mon_type_1][move_type]
            type_2_effectiveness = types[mon_type_2][move_type]
            type_1_prio = type_priority.index(mon_type_1)
            type_2_prio = type_priority.index(mon_type_2)
            if type_1_prio < type_2_prio:
                return type_1_effectiveness, type_2_effectiveness
            else:
                return type_2_effectiveness, type_1_effectiveness

    def biv_min(level: int, current_stat: int, evs: int, nature: float):
        return max(22, int(floor(floor(floor(current_stat / nature) - 5) * 100 / level) + (
            0 if not (nature == 0.9 and current_stat % 10 == 0) else 100 % level) - floor(evs / 4)))

    def biv_max(level: int, current_stat: int, evs: int, nature: float):
        return min(541, int(np.floor(ceil(
            ceil(current_stat + (0 if (nature == 1.1 and current_stat % 11 == 0) else 0.01)) / nature - (
                5 if nature == 1 else 4)) * 100 / level) + 1 - floor(evs / 4)))

    def biv_to_base_min(biv):
        return ceil((biv - 31) / 2)

    def biv_to_base_max(biv):
        return np.floor(biv / 2)

    def calc_dmg_base(level: int, move_power: int, offense: int, defense: int):
        return floor(floor(2 * level / 5 + 2) * move_power * offense / defense)

    def calc_base_power(level: int, move_power: int):
        return floor(2 * level / 5 + 2) * move_power

    def get_weather_modifier(weather, move_type):
        if (weather == "Sunny" and move_type == "Fire") or (weather == "Rain" and move_type == "Water"):
            return 1.5
        elif (weather == "Sunny" and move_type == "Water") or (weather == "Rain" and move_type == "Fire"):
            return 0.5
        return 1

    def calc_stat_stages(stat: int, stages: int):
        return floor(stat * (2 + (stages if stages > 0 else 0)) / (2 - (stages if stages < 0 else 0)))

    def calc_xp_yield(pokemon, level: int, opponent_is_trainer: bool, lucky_egg_held=False, is_original_trainer=True):
        xp_pokemon = floor(pokemons["XP"][pokemon] * level / 7)
        xp = floor(floor(floor(xp_pokemon * (1.5 if lucky_egg_held else 1)) * (1.5 if opponent_is_trainer else 1)) * (
            1.5 if not is_original_trainer else 1))
        return xp


app = App(app_ui, server)
