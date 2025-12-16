from math import floor, ceil

import matplotlib.pyplot as plt
from shiny.types import SilentException

from shared import *

from shiny import *


def iv_calculation_page():
    return ui.nav_panel(
        "IV Calculator",
        ui.layout_columns(
            ui.h4("IV Calculator"),
        ),
        ui.layout_columns(
            ui.page_fluid(
                ui.input_selectize("pokemon_iv", "Select Pokemon:",
                                   sorted(pokemons.index), selected="Lickitung"),
                ui.output_code("pokemon_bst_iv"),
            ),
            ui.page_fluid(
                ui.input_radio_buttons("nature_plus_iv", "Nature + :",
                                       ["neutral", "+ ATK", "+ DEF", "+ SPA", "+ SPD", "+ SPE"], inline=True),
                ui.input_radio_buttons("nature_minus_iv", "Nature - :",
                                       ["neutral", "- ATK", "- DEF", "- SPA", "- SPD", "- SPE"], inline=True)
            ),
            ui.page_fluid(
                ui.card(
                    ui.layout_columns(
                        ui.input_action_button("clear_all_iv", "Clear All"),
                    ),
                ),
            ),
            col_widths=(3, 6, 3),
        ),
        ui.layout_columns(
            ui.page_fluid(
                ui.h5("Stats at specific Level"),
                ui.input_numeric("level_iv", "Level:", 5, min=1, max=100),
                ui.input_numeric("hp_iv", "HP:", 22, min=11, max=999),
                ui.input_numeric("atk_iv", "ATK:", 12, min=4, max=999),
                ui.input_numeric("def_iv", "DEF:", 12, min=4, max=999),
                ui.input_numeric("spa_iv", "SPA:", 12, min=4, max=999),
                ui.input_numeric("spd_iv", "SPD:", 12, min=4, max=999),
                ui.input_numeric("spe_iv", "SPE:", 12, min=4, max=999),
                # ui.input_selectize("mons_defeated_iv", "Mons Defeated at this Level:", sorted(pokemons.index), multiple=True),
                ui.card(
                    ui.layout_columns(
                        ui.input_action_button("save_stats_iv", "Save Stats"),
                        ui.input_action_button("prefill_next_level_iv", "Prefill Next Level"),
                        ui.input_action_button("prefill_current_level_iv", "Prefill Current Level"),
                    )
                )
            ),
            ui.page_fluid(
                ui.layout_columns(ui.h5("Stat History (editable)")),
                ui.output_data_frame("history_iv")
            ),
            ui.page_fluid(
                ui.output_table("result_iv"),
            ),
            col_widths=(3, 6, 3),
        ),
    )


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
                    ui.h4("You will get the following XP / EVs:"),
                    ui.output_table("calculate_xp_ev_info"),
                ),
            ),
            ui.page_fluid(),
            ui.page_fluid(
                ui.h4("XP requirement"),
                ui.input_selectize("xp_curve_info", "XP Curve:", choices=list(experience.head()),
                                   selected="Fluctuating"),
                ui.input_numeric("level_from_info", "Level From:", min=1, max=100, value=5),
                ui.input_numeric("level_to_info", "Level To:", min=1, max=100, value=8),
                "XP required: ",
                ui.output_code("calc_xp_from_to"),
            ),
            col_widths=(4, 4, 4),
        )
    )


def atk_spa_calculator_page():
    return ui.nav_panel(
        "ATK / SPA Calculator",
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
                                        {"1": "1x (irrelevant)", "1.5": "1.5x (e.g. Hustle, Swarm)",
                                         "2": "2x (Huge Power)"}),
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
                ui.layout_columns(
                    ui.card(
                        ui.h5("Graph Style:"),
                        ui.input_radio_buttons(
                            "graph_style",
                            None,
                            {"only_dmg_received": "Only DMG Received", "all_dmg_values": "All DMG Values"},
                            inline=True,
                            selected="only_dmg_received",
                        ),
                    ),
                    ui.card(
                        ui.layout_columns(
                            ui.h5("Reset Buttons:"),
                        ),
                        ui.layout_columns(
                            ui.input_action_button("clear_all", "Clear All Inputs"),
                            ui.input_action_button("clear_dropdowns", "Clear Inputs In Dropdowns"),
                            col_widths=(6, 6),
                        ),
                    ),
                    col_widths=(6, 6)
                ),
            ),
            col_widths=(3, 9),
        )
    )


app_ui = \
    ui.page_navbar(
        ui.nav_spacer(),
        atk_spa_calculator_page(),
        xp_ev_info_page(),
        iv_calculation_page(),
        ui.head_content(ui.include_css(app_dir / "styles.css")),
        id="mode",
        title="Pokemon Generation 3 Calculator",
        window_title="Gen 3 Calculator",
    )


def server(input: Inputs, output: Outputs, session: Session):

    """
    ---------------------- IV Page
    """
    stat_history = reactive.value(
        pd.DataFrame(columns=["level", "hp", "atk", "def", "spa", "spd", "spe"], dtype=int))

    current_bst = reactive.value(int(385))  # initial mon is Lickitung with 385 BST

    # we set the initial nature as neutral
    atk_nature_modifier = reactive.value(float(1))
    def_nature_modifier = reactive.value(float(1))
    spa_nature_modifier = reactive.value(float(1))
    spd_nature_modifier = reactive.value(float(1))
    spe_nature_modifier = reactive.value(float(1))

    @reactive.effect
    @reactive.event(input.prefill_next_level_iv)
    def prefill_next_level_iv():
        prefill_level_iv(input.level_iv() + 1)

    @reactive.effect
    @reactive.event(input.prefill_current_level_iv)
    def prefill_current_level_iv():
        prefill_level_iv(input.level_iv())

    def prefill_level_iv(level: int):
        biv_table = calc_biv_table()

        hp_biv = ceil(biv_table.loc["hp_biv"].mean())
        atk_biv = ceil(biv_table.loc["atk_biv"].mean())
        def_biv = ceil(biv_table.loc["def_biv"].mean())
        spa_biv = ceil(biv_table.loc["spa_biv"].mean())
        spd_biv = ceil(biv_table.loc["spd_biv"].mean())
        spe_biv = ceil(biv_table.loc["spe_biv"].mean())

        ui.update_numeric("level_iv", value=level)
        ui.update_numeric("hp_iv", value=calc_hp(level, 0, hp_biv, 0))
        ui.update_numeric("atk_iv", value=calc_stat(level, 0, atk_biv, 0, atk_nature_modifier()))
        ui.update_numeric("def_iv", value=calc_stat(level, 0, def_biv, 0, def_nature_modifier()))
        ui.update_numeric("spa_iv", value=calc_stat(level, 0, spa_biv, 0, spa_nature_modifier()))
        ui.update_numeric("spd_iv", value=calc_stat(level, 0, spd_biv, 0, spd_nature_modifier()))
        ui.update_numeric("spe_iv", value=calc_stat(level, 0, spe_biv, 0, spe_nature_modifier()))

    @reactive.effect
    @reactive.event(input.nature_plus_iv, input.nature_minus_iv)
    def change_nature_iv():

        nature_plus = input.nature_plus_iv()
        nature_minus = input.nature_minus_iv()

        atk_nature_modifier.set(1.1 if nature_plus == "+ ATK" else 0.9 if nature_minus == "- ATK" else 1)
        def_nature_modifier.set(1.1 if nature_plus == "+ DEF" else 0.9 if nature_minus == "- DEF" else 1)
        spa_nature_modifier.set(1.1 if nature_plus == "+ SPA" else 0.9 if nature_minus == "- SPA" else 1)
        spd_nature_modifier.set(1.1 if nature_plus == "+ SPD" else 0.9 if nature_minus == "- SPD" else 1)
        spe_nature_modifier.set(1.1 if nature_plus == "+ SPE" else 0.9 if nature_minus == "- SPE" else 1)

    @render.table(index=True)
    @reactive.event(input.save_stats_iv, input.clear_all_iv, input.pokemon_iv,
                    input.nature_plus_iv, input.nature_minus_iv, stat_history)
    def result_iv():
        df = calc_biv_table()
        base_as_biv = current_bst() * 2

        total_ivs = [df["min"].sum() - base_as_biv, df["max"].sum() - base_as_biv]
        total_ivs_avg = [f"{total_ivs[0] / 6:.2f}", f"{total_ivs[1] / 6:.2f}"]

        result = pd.DataFrame(columns=["min", "max"], dtype=int)
        result.loc["Base HP:"] = [biv_to_base_min(df.loc["hp_biv", "min"]), biv_to_base_max(df.loc["hp_biv", "max"])]
        result.loc["Base ATK:"] = [biv_to_base_min(df.loc["atk_biv", "min"]), biv_to_base_max(df.loc["atk_biv", "max"])]
        result.loc["Base DEF:"] = [biv_to_base_min(df.loc["def_biv", "min"]), biv_to_base_max(df.loc["def_biv", "max"])]
        result.loc["Base SPA:"] = [biv_to_base_min(df.loc["spa_biv", "min"]), biv_to_base_max(df.loc["spa_biv", "max"])]
        result.loc["Base SPD:"] = [biv_to_base_min(df.loc["spd_biv", "min"]), biv_to_base_max(df.loc["spd_biv", "max"])]
        result.loc["Base SPE"] = [biv_to_base_min(df.loc["spe_biv", "min"]), biv_to_base_max(df.loc["spe_biv", "max"])]
        result.loc["Total IVs"] = total_ivs
        result.loc["Average IVs"] = total_ivs_avg

        return result

    def calc_biv_table():
        if stat_history().size < 1:
            raise SilentException()

        df = pd.DataFrame(columns=["min", "max"],
                          index=["hp_biv", "atk_biv", "def_biv", "spa_biv", "spd_biv", "spe_biv"])

        for row in stat_history.get().itertuples():

            level, hp, atk, deff, spa, spd, spe = row[1:8]

            hp_biv_min, hp_biv_max = biv_range_hp(level, hp, 0)
            df.loc["hp_biv"] = [hp_biv_min, hp_biv_max]
            atk_biv_min, atk_biv_max = biv_range(level, atk, 0, atk_nature_modifier.get())
            df.loc["atk_biv"] = [atk_biv_min, atk_biv_max]
            def_biv_min, def_biv_max = biv_range(level, deff, 0, def_nature_modifier.get())
            df.loc["def_biv"] = [def_biv_min, def_biv_max]
            spa_biv_min, spa_biv_max = biv_range(level, spa, 0, spa_nature_modifier.get())
            df.loc["spa_biv"] = [spa_biv_min, spa_biv_max]
            spd_biv_min, spd_biv_max = biv_range(level, spd, 0, spd_nature_modifier.get())
            df.loc["spd_biv"] = [spd_biv_min, spd_biv_max]
            spe_biv_min, spe_biv_max = biv_range(level, spe, 0, spe_nature_modifier.get())
            df.loc["spe_biv"] = [spe_biv_min, spe_biv_max]

        return df

    @render.text
    def pokemon_bst_iv():
        current_bst.set(pokemons["BST"][input.pokemon_iv()])
        return "BST: " + str(current_bst.get())

    @reactive.effect
    @reactive.event(input.clear_all_iv)
    def clear_all_iv():
        stat_history.set(pd.DataFrame(
            pd.DataFrame(columns=["level", "hp", "atk", "def", "spa", "spd", "spe"], dtype=int)))

    @render.data_frame
    @reactive.event(input.save_stats_iv, input.clear_all_iv, ignore_none=False)
    def history_iv():
        return render.DataTable(
            stat_history(),
            editable=True,
            selection_mode="row",
        )

    @history_iv.set_patch_fn
    def _(*, patch: render.CellPatch):
        stat_history_copy = stat_history().copy()
        fn = str if patch["column_index"] == 0 else int
        stat_history_copy.iat[patch["row_index"], patch["column_index"]] = fn(patch["value"])
        stat_history.set(stat_history_copy)
        return patch["value"]

    @reactive.effect
    @reactive.event(input.save_stats_iv)
    def save_stats_iv():
        if not input.level_iv():
            raise SilentException()
        level = input.level_iv()

        if not input.hp_iv():
            raise SilentException()
        hp = input.hp_iv()

        if not input.atk_iv():
            raise SilentException()
        atk = input.atk_iv()

        if not input.def_iv():
            raise SilentException()
        deff = input.def_iv()

        if not input.spa_iv():
            raise SilentException()
        spa = input.spa_iv()

        if not input.spd_iv():
            raise SilentException()
        spd = input.spd_iv()

        if not input.spe_iv():
            raise SilentException()
        spe = input.spe_iv()

        stat_history.get().loc[-1] = [level, hp, atk, deff, spa, spd, spe]
        stat_history.get().index = stat_history.get().index + 1

    """
    ---------------------- XP Page
    """

    @render.text
    def calc_xp_from_to():
        xp_curve = input.xp_curve_info()
        lvl_from = input.level_from_info()
        lvl_to = input.level_to_info()

        return experience[xp_curve][lvl_from:lvl_to].sum()

    @render.table
    def calculate_xp_ev_info():
        # returns XP and EVs for a mon in a specific situation
        pokemon = input.pokemon_info()
        is_trainer = input.is_trainer_info()
        enemy_level = input.enemy_level_info()

        xp = calc_xp_yield(pokemon, enemy_level, is_trainer)
        table = pokemons.loc[[pokemon], ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]]
        table = table.loc[:, (table != 0).any(axis=0)]

        table.insert(0, "XP", [xp])
        return table

    """
    ---------------------- ATK / SPA Page
    """

    @reactive.effect
    @reactive.event(input.clear_all)
    def clear_all():
        clear_visible_inputs()
        clear_dropdowns()

    @reactive.effect
    @reactive.event(input.clear_dropdowns, input.clear_all)
    def clear_dropdowns_only():
        clear_dropdowns()

    def clear_visible_inputs():
        session.send_input_message("enemy_level", {"value": ""})
        session.send_input_message("move_power", {"value": ""})
        session.send_input_message("own_defense", {"value": ""})
        session.send_input_message("damage_received", {"value": ""})
        session.send_input_message("is_stab", {"value": False})
        session.send_input_message("is_crit", {"value": False})
        session.send_input_message("effectiveness", {"value": "1"})

    def clear_dropdowns():
        session.send_input_message("atk_spa_stage", {"value": 0})
        session.send_input_message("is_burned", {"value": False})
        session.send_input_message("ff_active", {"value": False})
        session.send_input_message("has_dd_charge", {"value": False})
        session.send_input_message("is_physical", {"value": False})
        session.send_input_message("enemy_ability", {"value": 1})
        session.send_input_message("effectiveness", {"value": 1})
        session.send_input_message("def_spd_stage", {"value": 0})
        session.send_input_message("has_reflect_lightscreen", {"value": False})
        session.send_input_message("has_def_spd_badge", {"value": False})
        session.send_input_message("has_thick_fat", {"value": False})
        session.send_input_message("weather_modifier", {"value": "1"})
        session.send_input_message("mud_or_water_sport_active", {"value": False})

    @render.plot
    def calculate_offense():
        # the formula used to determine ATK / SPA of the opponent in the ATK / SPA calculator

        if not input.enemy_level():
            raise SilentException()
        enemy_level = int(input.enemy_level())
        if not input.move_power():
            raise SilentException()
        move_power = int(input.move_power())
        if not input.own_defense():
            raise SilentException()
        own_defense = int(input.own_defense())
        if not input.damage_received():
            raise SilentException()
        damage_received = int(input.damage_received())

        is_stab = input.is_stab()
        stab_modifier = 1.5 if is_stab else 1

        is_crit = input.is_crit()
        crit_modifier = 2 if is_crit else 1

        eff1 = 0.5
        eff2 = 2

        if input.effectiveness() != "1-":
            # get effectiveness for "normal" (= how you would intuitively expect effectiveness to work) situations
            effectiveness = float(input.effectiveness())
            eff2 = 2 if effectiveness == 4 else 1
            if effectiveness == 0.25: eff2 = 0.5
            eff1 = 2 if effectiveness > 1 else 1
            if effectiveness < 1: eff1 = 0.5

        # only used for minimum damage (increases minimum dmg at that point in the calc from 0 to 1 if physical)
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

        # get rough lower / upper limits of possible ATK / SPA values to reduce calculations needed
        min_offense_guess, max_offense_guess = calc_offense_backwards(
            damage_received, is_physical,
            [eff2, eff1, stab_modifier, double_damage_or_charge_modifier, crit_modifier],
            [ff_modifier, weather_modifier,
             reflect_lightscreen_modifier, burned_modifier],
            effective_def_spd, calc_base_power(enemy_level, move_power), applied_atk_spa_stage,
            sport_modifier, thick_fat_modifier, enemy_ability_modifier
        )

        min_offense = -1
        max_offense = -1

        base_power = calc_base_power(enemy_level, move_power)

        dmg = []
        values = []
        # go through the previously determined upper and lower limits
        for x in range(min_offense_guess, max_offense_guess + 1):
            dmg.append(0)
            values.append([])
            # calc the whole dmg formula except random factor for this specific ATK / SPA value
            full_damage = floor(floor(base_power
                                      * calc_stat_stages(floor(floor(floor(x * enemy_ability_modifier)
                                                                     * thick_fat_modifier) * sport_modifier),
                                                         applied_atk_spa_stage) / effective_def_spd) / 50)
            full_damage = calc_ibm_damage(int(full_damage), burned_modifier,
                                          reflect_lightscreen_modifier, weather_modifier, ff_modifier)
            full_damage = calc_obm_damage_no_randomness(full_damage, crit_modifier,
                                                        double_damage_or_charge_modifier, stab_modifier, eff1, eff2)

            for y in range(16):
                # apply the random factor of the dmg calculation, and use it if it matches the dmg we received
                value = floor(full_damage * (y + 85) / 100)
                values[x - min_offense_guess].append(value)
                if floor(value == damage_received):
                    dmg[x - min_offense_guess] += 1
                    max_offense = x
                    if min_offense == -1:
                        min_offense = x

        graph_style = input.graph_style()

        if graph_style == "only_dmg_received":
            # limit the upper and lower limits of the list so the graph only shows relevant information
            dmg = dmg[(min_offense - min_offense_guess): (max_offense - min_offense_guess + 1)]

            fig, ax = plt.subplots()
            ax.set_title("ATK/SPA Value Likelihood")
            ax.set_ylabel("Nr. of rolls / 16")
            ax.set_xlabel("ATK/SPA value")

            ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])
            ax.set_ylim(0, 16)
            if max_offense - min_offense < 20:
                ax.set_xticks(range(min_offense, max_offense + 1))
            ax.bar(range(min_offense, max_offense + 1), dmg)
            if not fig:
                raise SilentException()
            return fig
        elif graph_style == "all_dmg_values":
            # limit the upper and lower limits of the list so the graph only shows relevant information
            values = values[(min_offense - min_offense_guess): (max_offense - min_offense_guess + 1)]

            # we want the count of occurences of each dmg value
            new_values = []
            for i in range(0, max_offense - min_offense + 1):
                new_values.append(i)
                new_values[i] = (np.unique_counts(values[i]))

            rows = []
            for ucr in new_values:
                row = {}
                for val, count in zip(ucr.values, ucr.counts):
                    row[str(val)] = count
                rows.append(row)

            df = pd.DataFrame(rows).fillna(0)
            plot = df.plot(kind="bar", stacked=True)

            plot.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])
            plot.set_ylim(0, 16)
            plot.set_title("ATK/SPA Value Likelihood")
            plot.set_ylabel("The 16 different Options")
            plot.set_xlabel("ATK/SPA value")

            num_rows = len(df)
            col_names = list(df.columns)

            # write dmg numbers on the bars
            for patch_index, rect in enumerate(plot.patches):
                col_idx = patch_index
                col_value = col_names[floor(col_idx / num_rows)]
                is_searched_value = (int(col_value) == int(damage_received))
                height = rect.get_height()

                if height > 0:  # only label non-zero segments
                    x = rect.get_x() + rect.get_width() / 2
                    y = rect.get_y() + rect.get_height() / 2
                    plot.text(
                        x, y, str(col_value),
                        ha='center', va='center',
                        color='black', fontsize=(15 if is_searched_value else 11),
                        fontweight=('bold' if is_searched_value else 'normal'),
                    )
            plot.get_legend().remove()
            # to avoid the graph getting to crowded with labels
            if max_offense - min_offense < 20:
                plot.set_xticks(range(0, max_offense - min_offense + 1), range(min_offense, max_offense + 1),
                                rotation="horizontal")
            else:
                plot.set_xticks(range(0, max_offense - min_offense + 1), range(min_offense, max_offense + 1))

            return plot
        else:
            raise SilentException()

    """
    ---------------------- Support Methods
    """

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

    def calc_offense_backwards(dmg_dealt: int, is_physical: bool, obm: list, ibm: list, defense: int, base_power: int,
                               offense_stage: int, sport_modifier: float, thick_fat_modifier: float,
                               enemy_ability_modifier: float):
        # ibm = "inside bracket modifier", the modifiers before the +2 in the formula
        # obm = "outside bracket modifier", the modifiers after the +2 in the formula
        # see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III
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
                                                                               / int(base_power)), offense_stage)[0]
                                              / sport_modifier) / thick_fat_modifier) / enemy_ability_modifier)
        offense_guess_max = floor(floor(floor(
            calc_stat_stages_backwards(floor(int((offense_guess_max * 50 + 49) * defense + defense - 1)
                                             / int(base_power)), offense_stage)[1] / sport_modifier + 1)
                                        / thick_fat_modifier + 1) / enemy_ability_modifier + 1)

        return offense_guess_min, offense_guess_max

    def calc_ibm_damage(base_damage: int, burned_modifier: float, barrier_lightscreen_modifier: float,
                        current_weather_modifier: float, flash_fire_modifier: float):
        result = floor(floor(floor(floor(base_damage * flash_fire_modifier)
                                   * current_weather_modifier) * barrier_lightscreen_modifier) * burned_modifier)
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
            # -stages increases the result due to stages < 0
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

    def biv_range_hp(level: int, current_stat: int, evs:int):
        return biv_range(level, current_stat - 5 - level, evs, 1)

    def biv_range(level:int, current_stat:int, evs:int, nature:float):
        biv_maximum = biv_max(level, current_stat, evs, nature)
        biv_minimum = biv_min(level, current_stat, evs, nature)

        # min > max: should not happen (in that case some of the inputs have to be wrong, user sees result is wrong)
        # min = max: we know the exact biv value
        # min < max: might not be exact boundaries, so we readjust
        if biv_minimum < biv_maximum:
            min_stat = calc_stat(level, 0, biv_minimum, evs, nature)
            max_stat = calc_stat(level, 0, biv_maximum, evs, nature)

            if min_stat < current_stat:
                while calc_stat(level, 0, biv_minimum, evs, nature) < current_stat and biv_minimum <= biv_maximum:
                    biv_minimum += 1

            if max_stat > current_stat:
                while calc_stat(level, 0, biv_maximum, evs, nature) > current_stat and biv_minimum <= biv_maximum:
                    biv_maximum -= 1

        return biv_minimum, biv_maximum


    def biv_min_hp(level: int, current_stat: int, evs: int,):
        return int(biv_min(level, current_stat - 5 - level, evs, 1))

    def biv_min(level: int, current_stat: int, evs: int, nature: float):
        # biv is my abbreviation for 2 * Base stat + Individual Value (also written: 2 * Base + IVs)
        # i use it as it is easier to get both as a package than directly calc the base stat
        # (and it does not make a difference for the resulting stat anyway)
        biv = min(541, max(22,
                            int(floor(floor(floor(current_stat / nature) - 4
                                            - (1 if nature == 1 or (nature == 1.1 and current_stat % 11 == 0) else 0))
                                      * 100 / level) + (0 if not (nature == 0.9 and current_stat % 10 == 0)
                                                                                        else 100 % level)
                                - floor(evs / 4))))
        result = calc_stat(level, 0, biv, 0, nature)
        return biv

    def biv_max_hp(level: int, current_stat: int, evs: int):
        return int(biv_max(level, current_stat - 5 - level, evs, 1))

    def biv_max(level: int, current_stat: int, evs: int, nature: float):
        biv = max(22, min(541, int(ceil(ceil((
            (current_stat + (1 if (nature == 1.1 and current_stat % 11 == 0) else 0)) / nature
            - (5 if nature == 1 else 4)) * 100 + 99) / level) - floor(evs / 4))))

        result = calc_stat(level, 0, biv, 0, nature)
        return biv

    def biv_to_base_min(biv):
        return int(ceil((biv - 31) / 2))

    def biv_to_base_max(biv):
        return int(floor(biv / 2))

    def calc_dmg_base(level: int, move_power: int, offense: int, defense: int):
        return floor(floor(2 * level / 5 + 2) * move_power * offense / defense)

    def calc_base_power(level: int, move_power: int):
        # in case you don't want offense / defense included in the calculation
        return floor(2 * level / 5 + 2) * move_power

    def get_weather_modifier(current_weather, move_type):
        if (current_weather == "Sunny" and move_type == "Fire") or (current_weather == "Rain" and move_type == "Water"):
            return 1.5
        elif (current_weather == "Sunny" and move_type == "Water") or (current_weather == "Rain" and move_type == "Fire"):
            return 0.5
        return 1

    def calc_stat_stages(stat: int, stages: int):
        return floor(stat * (2 + (stages if stages > 0 else 0)) / (2 - (stages if stages < 0 else 0)))

    def calc_xp_yield(pokemon, level: int, opponent_is_trainer: bool, lucky_egg_held=False, is_original_trainer=True):
        # the generation 3 XP formula from https://bulbapedia.bulbagarden.net/wiki/Experience
        xp_pokemon = floor(pokemons["XP"][pokemon] * level / 7)
        xp = floor(floor(floor(xp_pokemon * (1.5 if lucky_egg_held else 1)) * (1.5 if opponent_is_trainer else 1))
                   * (1.5 if not is_original_trainer else 1))
        return xp

    # Formula: https://bulbapedia.bulbagarden.net/wiki/Stat#Generation_III_onward
    def calc_stat(level: int, base: int, iv: int, ev: int, nature: float):
        return int(floor((floor(floor(2*base + iv + floor(ev/4)) * level / 100) + 5) * nature))

    def calc_hp(level: int, base: int, iv: int, ev: int):
        return int(floor(floor(2*base + iv + floor(ev/4)) * level / 100) + 10 + level)


app = App(app_ui, server)
