from math import floor, ceil, isnan

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from shiny.types import SilentException

# Load data and compute static values
from shared import app_dir, pokemons, types, moves, type_priority, experience, weather, question_circle_fill

from shiny import App, Inputs, Outputs, Session, reactive, render, ui, render_plot, render_ui, req


def simplified_page():
    return ui.nav_panel(
        "Simplified",
        ui.layout_columns(
            ui.page_fluid(
                ui.h3("ATK / SPA Simple"),
                ui.h1(" "),
                ui.input_numeric("enemy_level_simplified", "Enemy Level:", 8, min=1, max=100),
                ui.input_numeric("move_power_simplified", "Power:", 50, step=5, min=5, max=999),
                ui.input_numeric("own_defense_simplified", "Defense:", 20, min=1, max=999),
                ui.input_numeric("damage_received_simplified", "DMG Taken:", 5, min=1, max=999),
            ),
            ui.page_fluid(
                ui.output_plot("calculate_offense_simplified"),
            ),
            col_widths=(2, 10),
        )
    )


def advanced_page():
    return ui.nav_panel(
        "Advanced",
        ui.page_fluid(
            ui.h3("ATK / SPA Advanced"),
        ),
        ui.page_fluid(
            ui.layout_columns(
                ui.page_fluid(
                    ui.layout_columns(
                        ui.page_fluid(
                            ui.h4("Own Pokemon:"),
                            ui.layout_columns(
                                ui.navset_card_tab(
                                    ui.nav_spacer(),
                                    ui.nav_panel("Pokemon",
                                                 ui.input_selectize("own_pokemon", "Select Pokemon:",
                                                                    sorted(pokemons.index)),
                                                 ),
                                    ui.nav_panel("Type",
                                                 ui.input_selectize("types", "Select types:",
                                                                    sorted(types.index), multiple=True)
                                                 ),
                                    title=ui.tooltip(
                                        ui.span("Typing by:   ", question_circle_fill),
                                        "Select your own Typing. \n\n In case no type is selected, it is assumed that the opponents move is neutral against both your types.\n\n Be careful with double types that \"cancel each other out\" if you want exact results:\ne.g. Kingdra takes more damage from electic moves than ice moves in about 50% of cases!",
                                        placement="right",
                                        id="pokemon_type_tooltip",
                                    ),
                                    id="input_type_type",
                                    selected="Type",
                                ),
                            ),
                            id="own_pokemon_selection",
                        ),
                        ui.page_fluid(
                            ui.h4("Enemy Pokemon:"),
                            ui.navset_card_tab(
                                ui.nav_spacer(),
                                ui.nav_panel("Name",
                                             ui.input_selectize("enemy_move", "Move Name",
                                                                choices=sorted(moves.index)),
                                             ),
                                ui.nav_panel("Power + Type",
                                             ui.layout_columns(
                                                 ui.input_numeric("enemy_move_power", "Move Power", min=5,
                                                                  value=40,
                                                                  step=5, max=999),
                                                 ui.input_selectize("enemy_move_type", "Move Type",
                                                                    choices=sorted(types.index),
                                                                    selected="Normal"),
                                             ),
                                             ),
                                title=ui.tooltip(
                                    ui.span("Move by:   ", question_circle_fill),
                                    "Select the move used by the opponent",
                                    placement="left",
                                    id="move_used_tooltip",
                                ),
                                id="enemy_move_selection_type",
                                selected="Power + Type",
                            ),
                        ),
                        id="enemy_move_selection",
                    ),
                    ui.layout_columns(
                        ui.page_fluid(
                            ui.layout_columns(
                                ui.input_numeric("def_spd", "DEF/SPD:", 20, min=1, max=999),
                                ui.input_numeric("dmg_received_advanced", "DMG Taken:", 10, min=1, max=999),
                            ),
                            id="own_pokemon_modifier_selection",
                        ),
                        ui.page_fluid(
                            ui.layout_columns(
                                ui.input_numeric("enemy_level_advanced", "Level:", 8, min=1, max=100),
                                ui.page_fluid(
                                    ui.input_switch("enemy_stab", "STAB"),
                                    ui.input_switch("crit", "CRIT"),
                                ),
                            ),
                            id="enemy_pokemon_modifier_selection",
                        ),
                    ),
                    ui.layout_columns(
                        ui.accordion(
                            ui.accordion_panel(
                                "other modifiers:",
                                ui.input_numeric("def_spd_stage", "DEF/SPD Stage:", 0, min=-6, max=6),
                                ui.input_switch("reflect_lightscreen", "Reflect / Lightscreen:"),
                                ui.input_switch("def_spd_badge", "DEF/SPD Badge:"),
                                ui.input_switch("thick_fat", "Thick Fat:"),
                            ),
                            ui.accordion_panel(
                                "field effects:",
                                ui.input_select("weather", "The current Weather:",
                                                weather,
                                                selected="Clear"),
                                ui.input_switch("mud_or_water_sport", "Mud Sport or Water Sport:"),
                            ),
                            open=False
                        ),
                        ui.accordion(
                            ui.accordion_panel(
                                "other modifiers",
                                ui.input_numeric("atk_spa_stage", "ATK/SPA Stage:", 0, min=-6, max=6),
                                ui.input_switch("burned", "Enemy is burned:"),
                                ui.input_switch("ff_active", "Enemy gets bonus from Flashfire"),
                                ui.input_switch("dd_charge", "Damage is doubled or Charge bonus active:"),
                            ),
                            open=False,
                        ),
                    ),
                ),
                ui.page_fluid(
                    ui.output_plot("calculate_offense_advanced"),
                ),
                col_widths=(6, 6),
            ),
        ),
        ui.include_css(app_dir / "styles.css"),
    )


app_ui = \
    ui.page_navbar(
        ui.nav_spacer(),
        simplified_page(),
        advanced_page(),
        id="mode",
        title="Pokemon Generation 3 Calculator",
        window_title="Gen 3 Calculator",
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
            type1 = "" if len(input.types()) == 0 else input.types()[0]
            type2 = "" if len(input.types()) <= 1 else input.types()[1]

        move_type = ""
        move_power = 0
        is_physical = False

        current_weather = input.weather()
        if input.enemy_move_selection_type() == "Name":
            if not input.enemy_move():
                raise SilentException()
            enemy_move = input.enemy_move()
            if moves["Category"][enemy_move] == "Status":
                raise SilentException()
            move_type, move_power, is_physical = get_move_attributes(enemy_move, current_weather)
        elif input.enemy_move_selection_type() == "Power + Type":
            if not input.enemy_move_power():
                raise SilentException()
            move_power = int(input.enemy_move_power())
            if not input.enemy_move_type():
                raise SilentException()
            move_type = input.enemy_move_type()
            is_physical = is_type_physical(type_priority.index(move_type))

        weather_modifier = get_weather_modifier(current_weather, move_type)
        eff1, eff2 = calc_effectiveness(move_type, type1, type2)

        if not input.def_spd():
            raise SilentException()
        own_defense = int(input.def_spd())
        has_def_spd_badge = input.def_spd_badge()
        if not input.enemy_level_advanced():
            raise SilentException()
        enemy_level_advanced = int(input.enemy_level_advanced())

        has_thick_fat = input.thick_fat()
        thick_fat_modifier = 1 if not has_thick_fat or (
                    has_thick_fat and not (move_type == "Ice" or move_type == "Fire")) else 0.5

        has_sport = input.mud_or_water_sport()
        sport_modifier = 1 if not has_sport or (
                    has_sport and not (move_type == "Electric" or move_type == "Fire")) else 0.5

        is_stab = input.enemy_stab()
        stab_modifier = 1.5 if is_stab else 1

        is_crit = input.crit()
        crit_modifier = 2 if is_crit else 1
        if not (input.atk_spa_stage() or input.atk_spa_stage() == 0):
            raise SilentException()
        atk_spa_stage = int(input.atk_spa_stage())
        applied_atk_spa_stage = 0 if (is_crit and atk_spa_stage < 0) else atk_spa_stage

        if not (input.def_spd_stage() or input.def_spd_stage() == 0):
            raise SilentException()
        def_spd_stage = int(input.def_spd_stage())
        applied_def_spd_stage = 0 if (is_crit and def_spd_stage > 0) else def_spd_stage
        effective_def_spd = calc_defensive_stat_modifiers(own_defense, has_def_spd_badge, applied_def_spd_stage)

        has_reflect_lightscreen = input.reflect_lightscreen()
        reflect_lightscreen_modifier = 1 if (is_crit or not has_reflect_lightscreen) else 0.5

        is_burned = input.burned()
        burned_modifier = 0.5 if (is_burned and is_physical) else 1

        ff_active = input.ff_active()
        ff_modifier = 1.5 if (ff_active and move_type == "Fire") else 1

        has_double_damage_or_charge = input.dd_charge()
        double_damage_or_charge_modifier = 2 if has_double_damage_or_charge else 1

        if not input.dmg_received_advanced():
            raise SilentException()
        damage_received = int(input.dmg_received_advanced())

        min_offense_guess, max_offense_guess = calc_offense_backwards(
            damage_received, is_physical,
            [eff2, eff1, stab_modifier, double_damage_or_charge_modifier, crit_modifier],
            [ff_modifier, weather_modifier,
             reflect_lightscreen_modifier, burned_modifier],
            effective_def_spd,
            calc_base_power(enemy_level_advanced, move_power), applied_atk_spa_stage, sport_modifier, thick_fat_modifier
        )

        min_offense = -1
        max_offense = -1

        base_power = calc_base_power(enemy_level_advanced, move_power)

        for x in range(min_offense_guess, max_offense_guess + 1):
            dmg.append(0)
            full_damage = floor(floor(
                base_power * calc_stat_stages(floor(floor(x * thick_fat_modifier) * sport_modifier),
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
                               offense_stage: int, sport_modifier: float, thick_fat_modifier: float):
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

        offense_guess_min = floor(floor(calc_stat_stages_backwards(floor(int(offense_guess_min * 50 * defense)
                                                                         / int(base_power)), offense_stage)[
                                            0] / sport_modifier) / thick_fat_modifier)
        offense_guess_max = floor(
            floor(calc_stat_stages_backwards(floor(int((offense_guess_max * 50 + 49) * defense + defense - 1)
                                                   / int(base_power)), offense_stage)[
                      1] / sport_modifier + 1) / thick_fat_modifier + 1)

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

    def calc_defensive_stat_modifiers(stat: int, defensive_badge: bool, defensive_stage: int):
        result = stat
        if defensive_badge:
            result = floor(stat * 1.1)
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


app = App(app_ui, server)
