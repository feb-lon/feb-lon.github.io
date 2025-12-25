from math import floor, ceil
from os import listdir

import matplotlib.pyplot as plt
from shiny.types import SilentException

from shared import *

from shiny import *


def iv_calculation_page():
    return ui.nav_panel(
        "IV Calculator",
        ui.layout_columns(
            ui.h2("IV Calculator"),
        ),
        ui.layout_columns(
            ui.page_fluid(
                ui.page_fluid(
                    ui.layout_columns(
                        ui.page_fluid(
                            ui.input_selectize("pokemon_iv", "Select Pokemon:",
                                               sorted(pokemons.index), selected="Lickitung"),
                        ),
                        ui.output_code("pokemon_bst_iv"),
                        col_widths=(8, 4),
                    ),
                    ui.input_radio_buttons("nature_plus_iv", "Nature + :",
                                           ["neutral", "+ ATK", "+ DEF", "+ SPA", "+ SPD", "+ SPE"], inline=True),
                    ui.input_radio_buttons("nature_minus_iv", "Nature - :",
                                           ["neutral", "- ATK", "- DEF", "- SPA", "- SPD", "- SPE"], inline=True)
                ),
                ui.layout_columns(
                    ui.page_fillable(
                        ui.input_action_button("save_stats_iv", "Save Stats"),
                        ui.input_action_button("prefill_next_level_iv", "Prefill Next Level"),
                        ui.input_action_button("prefill_current_level_iv", "Prefill Current Level"),
                        ui.input_action_button("delete_row_iv", "Delete Selected Row"),
                        ui.input_action_button("clear_all_iv", "Clear All"),
                    ),
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
                    ),
                    col_widths=(6, 6),
                ),
            ),
            ui.page_fluid(
                ui.page_fillable(
                    ui.output_table("result_iv"),
                ),
                ui.page_fluid(
                    ui.layout_columns(ui.h5("Stat History (editable)")),
                    ui.output_data_frame("history_iv")
                ),
            ),
            col_widths=(5, 7),
        ),
    ),


def xp_ev_info_page():
    return ui.nav_panel(
        "XP / EV Info",
        ui.layout_columns(
            ui.h2("XP / EV Information"),
        ),
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
                        typing_tooltip(),
                        placement="right",
                        id="effectiveness_tooltip_advanced",
                    ),
                    {"0.25": "0.25x", "0.5": "0.5x", "1-": "1x-", "1": "1x", "2": "2x", "4": "4x"},
                    inline=True,
                    selected="1",
                ),
                ui.accordion(
                    ui.accordion_panel(
                        ui.span(
                            ui.h5("Enemy Pokemon Modifiers:"),
                            ui.output_text_verbatim("enemy_modifiers_counter"),
                            style="display: inline-flex; align-items: center; gap: 2rem;",
                            id="enemy_modifiers_title"
                        ),
                        ui.input_numeric("atk_spa_stage", "ATK/SPA Stage:", 0, min=-6, max=6),
                        ui.input_switch("is_burned", "Enemy Burned"),
                        ui.tooltip(
                            ui.input_switch("ff_active", "Flashfire Bonus"),
                            ui.card(
                                "Getting hit by a fire move gives this bonus for the whole fight. "
                                "\nWhile frozen, Flash Fire does not work."
                            ),
                        ),
                        ui.tooltip(
                            ui.input_switch("has_dd_charge", "Double Damage / Charge Bonus"),
                            double_damage_tooltip(),
                        ),
                        ui.tooltip(
                            ui.input_switch("is_physical", "Move is Physical"),
                            ui.card("Only used for determining minimum DMG (physical DMG has higher minimum DMG)"),
                        ),
                        ui.input_select("enemy_ability", "Enemy Ability: ",
                                        {"1": "1x (irrelevant)", "1.5": "1.5x (e.g. Hustle, Swarm)",
                                         "2": "2x (Huge Power)"}),
                        value="enemy_modifiers_counter",
                    ),
                    ui.accordion_panel(
                        ui.span(
                            ui.h5("Own Pokemon Modifiers:"),
                            ui.output_text_verbatim("own_modifiers_counter"),
                            style="display: inline-flex; align-items: center; gap: 2rem;",
                            id="own_modifiers_title",
                        ),
                        ui.input_numeric("def_spd_stage", "DEF/SPD Stage:", 0, min=-6, max=6),
                        ui.input_switch("has_reflect_lightscreen", "Reflect / Lightscreen"),
                        ui.input_switch("has_def_spd_badge", "DEF/SPD Badge"),
                        ui.input_switch("has_thick_fat", "Thick Fat"),
                        value="own_modifiers_counter",
                    ),
                    ui.accordion_panel(
                        ui.span(
                            ui.h5("Field Effects:"),
                            ui.output_text_verbatim("field_effects_counter"),
                            style="display: inline-flex; align-items: center; gap: 2rem;",
                            id="field_effects_title",
                        ),
                        ui.input_radio_buttons(
                            "weather_modifier",
                            "Weather Modifier:",
                            {"0.5": "0.5x", "1": "1x", "1.5": "1.5x"},
                            inline=True,
                            selected="1",
                        ),
                        ui.input_switch("mud_or_water_sport_active", "Mud/Water Sport"),
                        value="field_effects_counter",
                    ),
                    open=False,
                ),
            ),
            ui.page_fluid(
                ui.output_plot("calculate_offense"),
                ui.layout_columns(
                    ui.page_fluid(
                        ui.layout_columns(
                            ui.h5("Graph Style:"),
                        ),
                        ui.input_radio_buttons(
                            "graph_style",
                            None,
                            {"only_dmg_received": "Only DMG Received", "all_dmg_values": "All DMG Values"},
                            inline=True,
                            selected="only_dmg_received",
                        ),
                    ),
                    ui.page_fluid(
                        ui.layout_columns(
                            ui.h5("Reset Buttons:"),
                        ),
                        ui.layout_columns(
                            ui.input_action_button("clear_all", "Clear All Inputs"),
                            ui.input_action_button("clear_dropdowns", "Clear Inputs In Dropdowns"),
                            col_widths=(6, 6),
                        ),
                    ),
                    col_widths=(-1, 3, -4, 3, -1)
                ),
                id="right_side",
            ),
            col_widths=(3, 9),
        )
    )


def double_damage_tooltip():
    return ui.card(
        ui.card_header("Double Damage Situations:"),
        ui.card_body(
            ui.layout_columns(
                ui.page_fluid("Needle Arm, Astonish, Extrasensory, Stomp"),
                ui.page_fluid("vs Minimized Target"),
                ui.page_fluid("Gust, Twister"),
                ui.page_fluid("vs mon in the air via Fly or Bounce"),
                ui.page_fluid("Earthquake, Magnitude"),
                ui.page_fluid("vs mon under ground via Dig"),
                ui.page_fluid("Surf, Whirlpool"),
                ui.page_fluid("vs mon under water using Dive"),
                ui.page_fluid("Revenge"),
                ui.page_fluid("after being hit"),
                ui.page_fluid("Weather Ball"),
                ui.page_fluid("during non-clear Weather"),
                ui.page_fluid("Pursuit"),
                ui.page_fluid("vs enemy switching pokemon"),
                col_widths=(6, 6),
            )
        ),
    )


def typing_tooltip():
    return ui.card(
        ui.card_header(
            "Effectiveness \"1x-\" is for cases where the move used has opposite effectiveness against "
            "the two defending types, and damage gets lost during rounding.In this generation, this is "
            "the case with: "
        ),
        ui.card_body(
            ui.row(
                ui.layout_columns(
                    ui.column(12, ui.h6("Move Type")),
                    ui.column(1, ui.h1(">")),
                    ui.column(12, ui.h6("Defending Types")),
                    col_widths=(1, 1, 2, 8),
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, bug_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, fire_type(), dark_type()),
                    ui.column(1, fighting_type(), psychic_type()),
                    ui.column(1, flying_type(), psychic_type()),
                    ui.column(1, flying_type(), dark_type()),
                    ui.column(1, ghost_type(), dark_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, electric_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, electric_type(), flying_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, fighting_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, flying_type(), dark_type()),
                    ui.column(1, flying_type(), steel_type()),
                    ui.column(1, psychic_type(), rock_type()),
                    ui.column(1, bug_type(), rock_type()),
                    ui.column(1, bug_type(), steel_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, fire_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, water_type(), grass_type()),
                    ui.column(1, water_type(), ice_type()),
                    ui.column(1, water_type(), bug_type()),
                    ui.column(1, rock_type(), steel_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, grass_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, fire_type(), ground_type()),
                    ui.column(1, fire_type(), rock_type()),
                    ui.column(1, grass_type(), rock_type()),
                    ui.column(1, flying_type(), rock_type()),
                    ui.column(1, bug_type(), rock_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, ground_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, grass_type(), poison_type()),
                    ui.column(1, bug_type(), rock_type()),
                    ui.column(1, bug_type(), steel_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, ice_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, fire_type(), ground_type()),
                    ui.column(1, fire_type(), rock_type()),
                    ui.column(1, fire_type(), flying_type()),
                    ui.column(1, water_type(), grass_type()),
                    ui.column(1, water_type(), ground_type()),
                    ui.column(1, water_type(), flying_type()),
                    ui.column(1, water_type(), dragon_type()),
                    ui.column(1, ice_type(), ground_type()),
                    ui.column(1, ice_type(), flying_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, rock_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, ground_type(), flying_type()),
                    ui.column(1, ground_type(), bug_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, steel_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, fire_type(), rock_type()),
                    ui.column(1, water_type(), ice_type()),
                    ui.column(1, water_type(), rock_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
            ui.row(
                ui.layout_columns(
                    ui.column(1, water_type()),
                    ui.column(1, ui.h1(">")),
                    ui.column(1, water_type(), rock_type()),
                    ui.column(1, water_type(), ground_type()),
                    col_widths=type_tooltip_col_width,
                ),
            ),
        ),
    ),


def dark_type():
    return ui.tags.img(src="dark_type.png", width=type_image_size)


def bug_type():
    return ui.tags.img(src="bug_type.png", width=type_image_size)


def fire_type():
    return ui.tags.img(src="fire_type.png", width=type_image_size)


def normal_type():
    return ui.tags.img(src="normal_type.png", width=type_image_size)


def water_type():
    return ui.tags.img(src="water_type.png", width=type_image_size)


def electric_type():
    return ui.tags.img(src="electric_type.png", width=type_image_size)


def grass_type():
    return ui.tags.img(src="grass_type.png", width=type_image_size)


def ice_type():
    return ui.tags.img(src="ice_type.png", width=type_image_size)


def fighting_type():
    return ui.tags.img(src="fighting_type.png", width=type_image_size)


def poison_type():
    return ui.tags.img(src="poison_type.png", width=type_image_size)


def ground_type():
    return ui.tags.img(src="ground_type.png", width=type_image_size)


def flying_type():
    return ui.tags.img(src="flying_type.png", width=type_image_size)


def psychic_type():
    return ui.tags.img(src="psychic_type.png", width=type_image_size)


def rock_type():
    return ui.tags.img(src="rock_type.png", width=type_image_size)


def ghost_type():
    return ui.tags.img(src="ghost_type.png", width=type_image_size)


def dragon_type():
    return ui.tags.img(src="dragon_type.png", width=type_image_size)


def steel_type():
    return ui.tags.img(src="steel_type.png", width=type_image_size)


app_ui = (
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
)


def server(input: Inputs, output: Outputs, session: Session):
    """
    ---------------------- IV Page ----------------------
    """
    stat_history = reactive.value(
        pd.DataFrame(columns=["level", "hp", "atk", "def", "spa", "spd", "spe"], dtype=int))

    empty_table = reactive.value(pd.DataFrame(index=["hp_biv", "atk_biv", "def_biv", "spa_biv", "spd_biv", "spe_biv"],
                                              columns=["min", "mid", "max"], dtype=int))

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

        total_biv_min = df["min"].sum()
        total_iv_min = total_biv_min - base_as_biv
        total_biv_max = df["max"].sum()
        total_iv_max = total_biv_max - base_as_biv
        total_iv_avg = (total_iv_min + total_iv_max) / 2

        base_hp_min, base_hp_max = (biv_to_base_min(df.loc["hp_biv", "min"]),
                                    biv_to_base_max(df.loc["hp_biv", "max"]))
        base_hp_gap = base_hp_max - base_hp_min
        hp_error_free = df.loc["hp_biv", "min"] <= df.loc["hp_biv", "max"]

        base_atk_min, base_atk_max = (biv_to_base_min(df.loc["atk_biv", "min"]),
                                      biv_to_base_max(df.loc["atk_biv", "max"]))
        base_atk_gap = base_atk_max - base_atk_min
        atk_error_free = df.loc["atk_biv", "min"] <= df.loc["atk_biv", "max"]

        base_def_min, base_def_max = (biv_to_base_min(df.loc["def_biv", "min"]),
                                      biv_to_base_max(df.loc["def_biv", "max"]))
        base_def_gap = base_def_max - base_def_min
        def_error_free = df.loc["def_biv", "min"] <= df.loc["def_biv", "max"]

        base_spa_min, base_spa_max = (biv_to_base_min(df.loc["spa_biv", "min"]),
                                      biv_to_base_max(df.loc["spa_biv", "max"]))
        base_spa_gap = base_spa_max - base_spa_min
        spa_error_free = df.loc["spa_biv", "min"] <= df.loc["spa_biv", "max"]

        base_spd_min, base_spd_max = (biv_to_base_min(df.loc["spd_biv", "min"]),
                                      biv_to_base_max(df.loc["spd_biv", "max"]))
        base_spd_gap = base_spd_max - base_spd_min
        spd_error_free = df.loc["spd_biv", "min"] <= df.loc["spd_biv", "max"]

        base_spe_min, base_spe_max = (biv_to_base_min(df.loc["spe_biv", "min"]),
                                      biv_to_base_max(df.loc["spe_biv", "max"]))
        base_spe_gap = base_spe_max - base_spe_min
        spe_error_free = df.loc["spe_biv", "min"] <= df.loc["spe_biv", "max"]

        error_free = hp_error_free and atk_error_free and def_error_free and spa_error_free and spd_error_free and spe_error_free
        total_ivs = [total_iv_min, total_iv_avg, total_iv_max, error_free]
        total_ivs_avg = [f"{total_ivs[0] / 6:.2f}", f"{total_ivs[1] / 6:.2f}", f"{total_ivs[2] / 6:.2f}", error_free]

        base_gap_sum = base_hp_gap + base_atk_gap + base_def_gap + base_spa_gap + base_spd_gap + base_spe_gap
        base_min_sum = base_hp_min + base_atk_min + base_def_min + base_spa_min + base_spd_min + base_spe_min
        biv_gap_sum = base_gap_sum * 2
        if biv_gap_sum == 0:
            base_gap_sum = 1
        missing_base_stats = current_bst() - base_min_sum

        base_hp_med = round(base_hp_min + missing_base_stats/base_gap_sum*base_hp_gap)
        base_atk_med = round(base_atk_min + missing_base_stats/base_gap_sum*base_atk_gap)
        base_def_med = round(base_def_min + missing_base_stats/base_gap_sum*base_def_gap)
        base_spa_med = round(base_spa_min + missing_base_stats/base_gap_sum*base_spa_gap)
        base_spd_med = round(base_spd_min + missing_base_stats/base_gap_sum*base_spd_gap)
        base_spe_med = round(base_spe_min + missing_base_stats/base_gap_sum*base_spe_gap)

        result = pd.DataFrame(columns=["min", "mid", "max", "error-free?"])
        result.loc["Total IVs"] = total_ivs
        result.loc["Average IVs"] = total_ivs_avg
        result.loc["Base HP:"] = [base_hp_min, base_hp_med, base_hp_max, hp_error_free]
        result.loc["Base ATK:"] = [base_atk_min, base_atk_med, base_atk_max, atk_error_free]
        result.loc["Base DEF:"] = [base_def_min, base_def_med, base_def_max, def_error_free]
        result.loc["Base SPA:"] = [base_spa_min, base_spa_med, base_spa_max, spa_error_free]
        result.loc["Base SPD:"] = [base_spd_min, base_spd_med, base_spd_max, spd_error_free]
        result.loc["Base SPE:"] = [base_spe_min, base_spe_med, base_spe_max, spe_error_free]

        return result.transpose()

    def calc_biv_table():
        if stat_history().size < 1:
            return empty_table()

        biv_table = pd.DataFrame(columns=["min", "max"],
                          index=["hp_biv", "atk_biv", "def_biv", "spa_biv", "spd_biv", "spe_biv"])

        for row in stat_history.get().itertuples():
            level, hp, atk, deff, spa, spd, spe = row[1:8]

            hp_biv_min, hp_biv_max = biv_range_hp(level, hp, 0)
            biv_table.loc["hp_biv"] = [max(hp_biv_min, biv_table.loc["hp_biv"]["min"]),
                                         min(hp_biv_max, biv_table.loc["hp_biv"]["max"])]
            atk_biv_min, atk_biv_max = biv_range(level, atk, 0, atk_nature_modifier.get())
            biv_table.loc["atk_biv"] = [max(atk_biv_min, biv_table.loc["atk_biv"]["min"]),
                                         min(atk_biv_max, biv_table.loc["atk_biv"]["max"])]
            def_biv_min, def_biv_max = biv_range(level, deff, 0, def_nature_modifier.get())
            biv_table.loc["def_biv"] = [max(def_biv_min, biv_table.loc["def_biv"]["min"]),
                                          min(def_biv_max, biv_table.loc["def_biv"]["max"])]
            spa_biv_min, spa_biv_max = biv_range(level, spa, 0, spa_nature_modifier.get())
            biv_table.loc["spa_biv"] = [max(spa_biv_min, biv_table.loc["spa_biv"]["min"]),
                                          min(spa_biv_max, biv_table.loc["spa_biv"]["max"])]
            spd_biv_min, spd_biv_max = biv_range(level, spd, 0, spd_nature_modifier.get())
            biv_table.loc["spd_biv"] = [max(spd_biv_min, biv_table.loc["spd_biv"]["min"]),
                                          min(spd_biv_max, biv_table.loc["spd_biv"]["max"])]
            spe_biv_min, spe_biv_max = biv_range(level, spe, 0, spe_nature_modifier.get())
            biv_table.loc["spe_biv"] = [max(spe_biv_min, biv_table.loc["spe_biv"]["min"]),
                                          min(spe_biv_max, biv_table.loc["spe_biv"]["max"])]

        return biv_table

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
    @reactive.event(input.save_stats_iv, input.clear_all_iv, input.delete_row_iv, ignore_none=False)
    def history_iv():
        return render.DataTable(
            stat_history(),
            editable=True,
            selection_mode="row",
        )

    @history_iv.set_patch_fn
    def _(*, patch: render.CellPatch):
        stat_history_copy = stat_history().copy()
        fn = int
        stat_history_copy.iat[patch["row_index"], patch["column_index"]] = fn(patch["value"])
        stat_history.set(stat_history_copy)
        return patch["value"]

    @reactive.effect
    @reactive.event(input.delete_row_iv)
    def delete_row_iv():
        if not history_iv.cell_selection()["rows"]:
            raise SilentException()
        selected_row_number = history_iv.cell_selection()["rows"][0]
        stat_history_copy = stat_history.get().copy()
        stat_history_copy.drop(stat_history_copy.index[[selected_row_number]], inplace=True)
        stat_history_copy.reset_index(drop=True, inplace=True)
        stat_history.set(stat_history_copy)

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

        stat_history_copy = stat_history.get().copy()
        stat_history_copy.loc[-1] = [level, hp, atk, deff, spa, spd, spe]
        stat_history_copy.index = stat_history_copy.index + 1
        stat_history.set(stat_history_copy)

    """
    ---------------------- XP Page ----------------------
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
    ---------------------- ATK / SPA Page ----------------------
    """

    @reactive.effect
    @reactive.event(input.clear_all)
    def clear_all():
        print(app_dir)
        print(listdir(app_dir / "images"))
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
                                          reflect_lightscreen_modifier, weather_modifier, ff_modifier, is_physical)
            full_damage = calc_obm_damage_no_randomness(full_damage, crit_modifier,
                                                        double_damage_or_charge_modifier, stab_modifier, eff1, eff2)

            for y in range(16):
                # apply the random factor of the dmg calculation, and use it if it matches the dmg we received
                value = max(1, floor(full_damage * (y + 85) / 100))
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

                try:
                    new_values[i] = (np.unique_counts(values[i]))
                except:
                    raise SilentException()

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
            plot.set_title("ATK/SPA Value Likelihood, DMG values shown on bars")
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
                rect.set_edgecolor('black')
                rect.set_linewidth(float(.5))

                if height > 0:  # only label non-zero segments
                    x = rect.get_x() + rect.get_width() / 2
                    y = rect.get_y() + rect.get_height() / 2
                    plot.text(
                        x, y, str(col_value),
                        ha='center', va='center',
                        color='black', fontsize=13,
                        fontweight=('bold' if is_searched_value else 'normal'),
                    )
                    if is_searched_value: rect.set_linewidth(2)
            plot.get_legend().remove()
            # to avoid the graph getting to crowded with labels
            if max_offense - min_offense < 20:
                plot.set_xticks(range(0, max_offense - min_offense + 1), range(min_offense, max_offense + 1),
                                rotation="horizontal")
            else:
                plot.set_xticks(range(0, max_offense - min_offense + 1), range(min_offense, max_offense + 1))

            if not plot: raise SilentException()
            return plot
        else:
            raise SilentException()

    @render.text
    def own_modifiers_counter():
        stage_modifier = int(input.def_spd_stage() != 0)
        screen_modifier = int(input.has_reflect_lightscreen())
        badge_modifier = int(input.has_def_spd_badge())
        thick_fat_modifier = int(input.has_thick_fat())
        modifiers_changed = stage_modifier + screen_modifier + badge_modifier + thick_fat_modifier

        if modifiers_changed > 0:
            return modifiers_changed
        else:
            return ""

    @render.text
    def enemy_modifiers_counter():
        stage_modifier = int(input.atk_spa_stage() != 0)
        burned_modifier = int(input.is_burned())
        ff_modifier = int(input.ff_active())
        dd_charge_modifier = int(input.has_dd_charge())
        is_physical_modifier = int(input.is_physical())
        enemy_ability_modifier = int(input.enemy_ability() != "1")
        modifiers_changed = (stage_modifier + burned_modifier + ff_modifier + dd_charge_modifier
                             + is_physical_modifier + enemy_ability_modifier)

        if modifiers_changed > 0:
            return modifiers_changed
        else:
            return ""

    @render.text
    def field_effects_counter():
        weather_modifier = input.weather_modifier()
        sport_modifier = input.mud_or_water_sport_active()
        modifiers_changed = int(weather_modifier != "1") + int(sport_modifier)

        if modifiers_changed > 0:
            return modifiers_changed
        else:
            return ""

    """
    ---------------------- Support Methods ----------------------
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
                        current_weather_modifier: float, flash_fire_modifier: float, is_physical: bool):
        result = floor(floor(floor(floor(base_damage * flash_fire_modifier)
                                   * current_weather_modifier) * barrier_lightscreen_modifier) * burned_modifier)

        result = max(result, 1 if is_physical else 0)  # minimum dmg of 1 only for physical moves at this point
        return result + 2

    def calc_obm_damage_no_randomness(base_damage: int, crit_modifier: int, double_damage_charge_modifier: int,
                                      stab_modifier: float,
                                      effectiveness_type_1: float, effectiveness_type_2: float):
        result = apply(crit_modifier, double_damage_charge_modifier, stab_modifier, effectiveness_type_1,
                       effectiveness_type_2, dmg_val=base_damage)
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

    def apply(*args, dmg_val: int):
        result = dmg_val
        for arg in args:
            result = floor(result * arg)
        result = max(1, result)
        return int(result)

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

    def biv_range_hp(level: int, current_stat: int, evs: int):
        return biv_range(level, current_stat - 5 - level, evs, 1)

    def biv_range(level: int, current_stat: int, evs: int, nature: float):
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

    def biv_min_hp(level: int, current_stat: int, evs: int, ):
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
                                                     (current_stat + (1 if (
                                                             nature == 1.1 and current_stat % 11 == 0) else 0)) / nature
                                                     - (5 if nature == 1 else 4)) * 100 + 99) / level) - floor(
            evs / 4))))

        result = calc_stat(level, 0, biv, 0, nature)
        return biv

    def biv_to_base_min(biv):
        if type(biv) != int:
            return 0
        else:
            return int(ceil((biv - 31) / 2))

    def biv_to_base_max(biv):
        if type(biv) != int:
            return 0
        else:
            return int(floor(biv / 2))

    def calc_dmg_base(level: int, move_power: int, offense: int, defense: int):
        return floor(floor(2 * level / 5 + 2) * move_power * offense / defense)

    def calc_base_power(level: int, move_power: int):
        # in case you don't want offense / defense included in the calculation
        return floor(2 * level / 5 + 2) * move_power

    def get_weather_modifier(current_weather, move_type):
        if (current_weather == "Sunny" and move_type == "Fire") or (current_weather == "Rain" and move_type == "Water"):
            return 1.5
        elif (current_weather == "Sunny" and move_type == "Water") or (
                current_weather == "Rain" and move_type == "Fire"):
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
        return int(floor((floor(floor(2 * base + iv + floor(ev / 4)) * level / 100) + 5) * nature))

    def calc_hp(level: int, base: int, iv: int, ev: int):
        return int(floor(floor(2 * base + iv + floor(ev / 4)) * level / 100) + 10 + level)


app = App(app_ui, server,
          static_assets=Path(app_dir / "images"))
