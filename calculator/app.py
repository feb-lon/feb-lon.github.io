from math import floor, ceil
from typing import Tuple

import matplotlib.pyplot as plt
from shiny.types import SilentException

from shared import *
from number_input import *
from xp_requirement_input import *

from shiny import *


def iv_calculation_page():
    return ui.nav_panel(
        "IV Calculator",
        element_and_tooltip(
            ui.h2("IV Calculator"),
            "As there is currently no method to track EVs, i would "
            "not recommend using this when having no idea what to do about EVs",
            1,
        ),
        ui.div(
            ui.div(
                {"style": "width: 30%"},
                ui.card(
                    ui.div(
                        "Select Pokemon:",
                        ui.input_selectize("pokemon_iv", "",
                                           sorted(pokemons.index), selected="Lickitung"),
                        ui.output_code("pokemon_bst_iv"),
                        class_="io_row",
                    ),
                    ui.div(
                        {"style": "text-align: center"},
                        ui.input_radio_buttons("nature_plus_iv", "Nature + :",
                                               ["=", "+ ATK", "+ DEF", "+ SPA", "+ SPD", "+ SPE"]),
                        ui.input_radio_buttons("nature_minus_iv", "Nature - :",
                                               ["=", "- ATK", "- DEF", "- SPA", "- SPD", "- SPE"]),
                        class_="spread_row",
                    ),
                ),
                ui.card(
                    ui.input_action_button("save_stats_iv", "Save Stats"),
                    ui.input_action_button("prefill_next_level_iv", "Prefill Next Level"),
                    ui.input_action_button("prefill_current_level_iv", "Prefill Current Level"),
                    ui.input_action_button("delete_row_iv", "Delete Selected Row"),
                    ui.input_action_button("reset_all_iv", "Clear All"),
                    class_="io_column",
                ),
            ),
            ui.div(
                {"style": "width: 60%"},
                ui.card(
                    ui.output_table("result_iv"),
                ),
                ui.card(
                    ui.div(
                        number_input(id="level_iv", label="Level:", init=5, min_value=1, max_value=100),
                        number_input(id="hp_iv", label="HP:", init=22, min_value=11, max_value=999),
                        number_input(id="atk_iv", label="ATK:", init=12, min_value=4, max_value=999),
                        number_input(id="def_iv", label="DEF:", init=12, min_value=4, max_value=999),
                        number_input(id="spa_iv", label="SPA:", init=12, min_value=4, max_value=999),
                        number_input(id="spd_iv", label="SPD:", init=12, min_value=4, max_value=999),
                        number_input(id="spe_iv", label="SPE:", init=12, min_value=4, max_value=999),
                        # ui.input_selectize("mons_defeated_iv", "Mons Defeated at this Level:", sorted(pokemons.index), multiple=True, class_="io_row"),
                        class_="io_row",
                    ),
                ),
                ui.div(
                    ui.layout_columns(ui.h5("Stat History (editable)")),
                    ui.output_data_frame("history_iv")
                ),
            ),
            class_="top_layer_row",
        ),
    )


def pokemon_info_page():
    return ui.nav_panel(
        "Pokemon / XP / Confusion Info",
        ui.page_fluid(
            ui.div(
                {"style": "width: 30%"},
                ui.card(
                    ui.card_header(
                        element_and_tooltip(
                            ui.h3("Pokemon Information"),
                            "XP information valid for Generations 2 - 4",
                            1,
                        ),
                    ),
                    ui.div(
                        "Pokemon:",
                        ui.input_selectize("pokemon_info", "", sorted(pokemons.index)),
                        "at Level",
                        number_input(id="enemy_level_info", label="", init=8, min_value=1, max_value=100),
                        class_="io_row",
                    ),
                    ui.div(
                        ui.input_switch("is_trainer_info", "Trainer Fight"),
                        ui.input_switch("has_lucky_egg_info", "Lucky Egg"),
                        ui.input_switch("is_traded_pokemon_info", "Not Original Trainer"),
                        class_="spread_row",
                    ),
                    ui.output_table("calculate_xp_ev_info"),
                    class_="io_column"
                ),
            ),
            ui.div(
                {"style": "width: 30%"},
                ui.card(
                    element_and_tooltip(
                        ui.card_header("XP Information 1"),
                        "Valid for all Generations.",
                    ),
                    xp_requirement_input(id="xp_requirement_1", from_level=5, to_level=8),
                    class_="io_column",
                ),
                ui.card(
                    ui.card_header("XP Information 2"),
                    xp_requirement_input(id="xp_requirement_2", from_level=8, to_level=10),
                    class_="io_column",
                ),
                ui.card(
                    ui.card_header("XP Information 3"),
                    xp_requirement_input(id="xp_requirement_3", from_level=5, to_level=8, curve="Slow"),
                    class_="io_column",
                ),
            ),
            ui.card(
                {"style": "width: 30%"},
                ui.card_header(
                    element_and_tooltip(
                        ui.h3("Confusion Information"),
                        (
                            ui.span("When using only inputs above the graph, output usable for every Generation."),
                            ui.span(),
                            ui.span("HOWEVER in Generations 1 - 2, there is no random factor for Confusion. "),
                            ui.span("This means the result is always the highest DMG value (furthest to the right)"),
                            ui.span(),
                            ui.span("Inputs below the graph should only be used in Generation 3"),
                        ),
                        1,
                    ),
                ),
                ui.div(
                    number_input(id="own_level_info", label="Level:", init=8, layout="short_input"),
                    ui.div(
                        number_input(id="atk_info", label="ATK:",
                                     init=20, min_value=1, max_value=999, layout="short_input"),
                        number_input(id="atk_stage_info", label="",
                                     init=0, min_value=-6, max_value=6, layout="stages_small"),
                        class_="io_row",
                    ),
                    ui.div(
                        number_input(id="def_info", label="DEF:",
                                     init=20, min_value=1, max_value=999, layout="short_input"),
                        number_input(id="def_stage_info", label="",
                                     init=0, min_value=-6, max_value=6, layout="stages_small"),
                        class_="io_row",
                    ),
                    class_="spread_row",
                ),
                ui.output_plot(id="confusion_damage_info"),
                ui.accordion(
                    ui.accordion_panel(
                        "Situational Effects",
                        ui.div(
                            ui.div(
                                "More Relevant:",
                                ui.div(
                                    ui.input_switch("is_burned_info", "Burned"),
                                    ui.input_switch("has_atk_badge", "ATK Badge"),
                                    ui.input_switch("has_def_badge", "DEF Badge"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.div(
                                "General Item:",
                                ui.div(
                                    ui.input_switch("has_choice_band_info", "Choice Band"),
                                    ui.input_switch("has_silk_scarf_info", "Silk Scarf"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.div(
                                "Pokemon-specific Items:",
                                ui.div(
                                    ui.input_switch("has_thick_club_info", "Thick Club"),
                                    ui.input_switch("has_metal_powder_info", "Metal Powder"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.div(
                                "Other:",
                                ui.div(
                                    ui.input_switch("is_explosion_selfdestruct_info", "Explosion/Selfdestruct"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.input_radio_buttons("own_ability_info", "Own Ability:",
                                                   {"1": "generic",
                                                    "1.5": "Hustle/Guts",
                                                    "2": "Huge/Pure Power",
                                                    "1.5xDEF": "Marvel Scale"},
                                                   selected="1",
                                                   inline=True,
                                                   ),
                        ),
                    ),
                    open=False,
                ),
                class_="io_column",
            ),
            class_="top_layer_row",
        ),
    )


def atk_spa_calculator_page():
    return ui.nav_panel(
        "ATK / SPA Calculator",
        ui.h2("ATK / SPA Calculator"),
        ui.div(
            ui.page_fluid(
                ui.card(
                    {"style": "margin-left: 5%;"},
                    ui.card_header(
                        "Graph Style"
                    ),
                    ui.card_body(
                        ui.input_radio_buttons(
                            "graph_style",
                            "",
                            {"only_dmg_received": "Only DMG Received", "all_dmg_values": "All DMG Values"},
                            inline=False,
                            selected="only_dmg_received",
                        ),
                    ),
                ),
                ui.div(
                    ui.card(
                        {"style": "border-color: black; border-width: 0.1rem; background-color: #FFF;"},
                        ui.card_body(
                            ui.div(
                                {"style": "display: flex;"},
                                ui.div(
                                    ui.div(
                                        number_input(id="enemy_level", label="",
                                                     init=8, layout="big"),
                                        "Enemy LVL",
                                        class_="io_column close_distance",
                                    ),
                                    ui.div(
                                        number_input(id="move_power", label="",
                                                     init=95, step=5, min_value=5, max_value=999, layout="big"),
                                        "Power",
                                        class_="io_column close_distance",
                                    ),
                                    ui.div(
                                        number_input(id="own_defense", label="",
                                                     init=20, min_value=1, max_value=999, layout="big"),
                                        "DEF/SPD",
                                        class_="io_column close_distance",
                                    ),
                                    ui.div(
                                        number_input(id="damage_received", label="",
                                                     init=10, min_value=1, max_value=999, layout="big"),
                                        "DMG",
                                        class_="io_column close_distance",
                                    ),
                                    class_="io_row",
                                ),
                                ui.div(
                                    ui.div(
                                        number_input(id="atk_spa_stage", label="",
                                                     init=0, min_value=-6, max_value=6, layout="stages"),
                                        ui.div(
                                            {"style": "width:3.7rem;font-size: .8rem;"},
                                            "ATK/SPA Stage",
                                        ),
                                        class_="io_column close_distance",
                                    ),
                                    ui.div(
                                        number_input(id="def_spd_stage", label="",
                                                     init=0, min_value=-6, max_value=6, layout="stages"),
                                        ui.div(
                                            {"style": "width:3.7rem;font-size: .8rem;"},
                                            "DEF/SPD Stage",
                                        ),
                                        class_="io_column close_distance",
                                    ),
                                    ui.div(
                                        ui.panel_conditional(
                                            "input.simulate_generation == 4",
                                            ui.input_switch("has_sniper", "Sniper"),
                                        ),
                                        ui.input_switch("is_crit", "CRIT"),
                                        ui.input_switch("is_stab", "STAB"),
                                        class_="ui_column big_buttons small_gap",
                                    ),
                                    ui.output_ui("crit_button"),
                                    ui.div(
                                        {"style": "margin-top: -1rem; margin-bottom: -1rem;"},
                                        ui.input_radio_buttons(
                                            "effectiveness",
                                            "",
                                            {"4": "4x", "2": "2x", "1": "1x", "1-": "1x-", "0.5": "0.5x",
                                             "0.25": "0.25x"},
                                            selected="1",
                                        ),
                                    ),
                                    ui.span(
                                        {
                                            "style":
                                                "line-break: anywhere;"
                                                "width: 0;"
                                                "font-size: 1.6rem;"
                                                "margin-left: 0rem;"
                                                "padding: 0rem;"
                                                "margin-top: 0rem;"
                                                "margin-bottom: 0rem;"
                                                "border-color: transparent;"
                                        },
                                        "EFF",
                                        ui.tooltip(
                                            question_circle_fill,
                                            typing_tooltip(),
                                            id="effectiveness_tooltip_advanced",
                                        ),
                                    ),
                                    class_="spread_row small_gap",
                                ),
                                class_="spread_row big_gap",
                            ),
                        ),
                    ),
                ),
                ui.div(
                    {"style": "gap: 1rem;margin-right: 5%"},
                    ui.card(
                        ui.card_header(
                            "Reset Input Buttons"
                        ),
                        ui.card_body(
                            ui.input_action_button("reset_all", "Reset All Inputs"),
                            ui.input_action_button("reset_dropdowns", "Reset Detailed Inputs"),
                            class_="spread_column",
                        ),
                    ),
                ),
                class_="io_row",
            ),
            ui.card(
                {"style": "border-color: black; border-width: 0.05rem;"},
                ui.output_plot("calculate_offense"),
            ),
            ui.div(
                {"style": "min-height: 5rem; align-items: start; padding-top: 1rem;"},
                ui.card(
                    ui.card_body(
                        ui.input_switch(
                            "use_detailed_inputs",
                            "Use Detailed Inputs"
                        ),
                        ui.input_radio_buttons(
                            "simulate_generation",
                            element_and_tooltip(
                                "Generation:",
                                (
                                    ui.span("Effectiveness 1x- is only relevant in Generations 1 - 4"),
                                    ui.span("Detailed inputs only available for Generation 3")
                                ),
                                1,
                            ),
                            {3: "3", 4: "4", 5: "5", 6: "6+"},
                            inline=True,
                            selected=3,
                        ),
                        class_="io_column",
                    ),
                ),
                ui.panel_conditional(
                    "input.simulate_generation == 3 & input.use_detailed_inputs",
                    {"style": "width: 85%; padding-top: 0;"},
                    ui.accordion(
                        {"style": "width: 45%"},
                        ui.accordion_panel(
                            ui.div(
                                ui.h5("Enemy Pokemon Modifiers:"),
                                ui.output_text_verbatim("enemy_modifiers_counter"),
                                id="enemy_modifiers_title",
                                class_="accordion_title",
                            ),
                            ui.div(
                                ui.input_switch("is_burned", "Enemy Burned"),
                                element_and_tooltip(
                                    ui.input_switch("ff_active", "Flashfire Bonus"),
                                    "Getting hit by a fire move gives this bonus for the whole fight.",
                                ),
                                element_and_tooltip(
                                    ui.input_switch("has_dd_charge", "Double Damage / Charge Bonus"),
                                    double_damage_tooltip(),
                                ),
                                class_="io_row"
                            ),
                            ui.div(
                                element_and_tooltip(
                                    ui.input_switch("is_physical", "Move is Physical"),
                                    "Only used for determining minimum DMG (physical DMG has higher minimum DMG)",
                                ),
                                ui.input_radio_buttons("enemy_ability",
                                                       element_and_tooltip(
                                                           ("Enemy Ability: ", spacer(1, 0)),
                                                           ability_tooltip(),
                                                       ),
                                                       {"1": "generic", "1.5x power": "1.5x Move Power",
                                                        "1.5": "1.5x ATK/SPA", "2": "2x ATK"},
                                                       selected="1",
                                                       inline=True,
                                                       ),
                                class_="spread_row align_bottom"
                            ),
                            value="enemy_modifiers_counter",
                        ),
                        open=False,
                    ),
                    ui.accordion(
                        {"style": "width: 35%"},
                        ui.accordion_panel(
                            ui.div(
                                ui.h5("Own Pokemon + Weather Modifiers:"),
                                ui.output_text_verbatim("own_modifiers_counter"),
                                id="own_modifiers_title",
                                class_="accordion_title",
                            ),
                            ui.div(
                                ui.input_switch("has_def_spd_badge", "DEF/SPD Badge"),
                                ui.input_switch("has_thick_fat", "Thick Fat"),
                                ui.input_switch("has_reflect_lightscreen", "Reflect / Lightscreen"),
                                class_="io_row",
                            ),
                            ui.div(
                                ui.input_switch("mud_or_water_sport_active", "Mud/Water Sport"),
                                ui.input_radio_buttons(
                                    "weather_modifier",
                                    "Weather Modifier:",
                                    {"0.5": "0.5x", "1": "1x", "1.5": "1.5x"},
                                    inline=True,
                                    selected="1",
                                ),
                                class_="spread_row align_bottom",
                            ),
                            value="own_modifiers_counter",
                            class_="io_column",
                        ),
                        open=False,
                    ),
                    class_="spread_row top",
                ),
                ui.panel_conditional(
                    "input.simulate_generation == 4 & input.use_detailed_inputs",
                    {"style": "width: 85%"},
                    ui.div(
                        "Early Stage Modifier",
                        number_input("early_modifier_gen_4", min_value=0, max_value=50, init=1, step=0.25),
                        class_="io_column",
                    ),
                    ui.div(
                        "Mid Stage Modifier",
                        number_input("mid_modifier_gen_4", min_value=1, max_value=3, init=1, step=0.5),
                        class_="io_column",
                    ),
                    ui.div(
                        "Late Stage Modifier",
                        number_input("late_modifier_gen_4", min_value=0, max_value=2, init=1, step=0.25),
                        class_="io_column",
                    ),
                    class_="spread_row top",
                ),
                ui.panel_conditional(
                    "(input.simulate_generation == 5 || input.simulate_generation == 6) "
                    "& input.use_detailed_inputs",
                    {"style": "width: 85%"},
                    ui.div(
                        "Mid Stage Modifier",
                        number_input("mid_modifier_gen_5_onward", min_value=1, max_value=3, init=1, step=0.5),
                        class_="io_column",
                    ),
                    ui.div(
                        "Late Stage Modifier",
                        number_input("late_modifier_gen_5_onward", min_value=0, max_value=2, init=1, step=0.25),
                        class_="io_column",
                    ),
                    class_="spread_row top",
                ),
                class_="io_row top",
            ),
            class_="top_layer_column",
        )
    )


def ability_tooltip():
    return (
        ui.layout_columns(
            ui.page_fluid("1.5x Move Power"),
            ui.page_fluid("Swarm, Overgrow, Blaze or Torrent"),
            ui.page_fluid("1.5x ATK/SPA"),
            ui.page_fluid("Hustle, Guts, Plus/Minus"),
            ui.page_fluid("2x ATK"),
            ui.page_fluid("Huge Power, Pure Power"),
            col_widths=(5, 7),
        ),
    )


def double_damage_tooltip():
    return (
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
        )
    )


def typing_tooltip():
    return ui.card(
        ui.card_header(
            "Effectiveness \"1x-\" is for cases where the move used has opposite effectiveness against "
            "the two defending types, and damage gets lost during rounding. "
            "This can happen in generations 1 - 4. "
            "With Pokemon up to generation 3, this is relevant for the following move / defensive typing combinations:"
        ),
        ui.card_body(
            {"style": "align-text: center"},
            ui.layout_columns(
                "Move Type",
                ui.h1(">"),
                "Defending Types",
                col_widths=(2, 1, 3, -6),
                class_="centered_img_row",
                style_="align-self: normal",
            ),
            ui.layout_columns(
                bug_type(),
                ui.h1(">"),
                ui.div(fire_type(), dark_type()),
                ui.div(fighting_type(), psychic_type()),
                ui.div(flying_type(), psychic_type()),
                ui.div(flying_type(), dark_type()),
                ui.div(ghost_type(), dark_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                electric_type(),
                ui.h1(">"),
                ui.div(electric_type(), flying_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                fighting_type(),
                ui.h1(">"),
                ui.div(flying_type(), dark_type()),
                ui.div(flying_type(), steel_type()),
                ui.div(psychic_type(), rock_type()),
                ui.div(bug_type(), rock_type()),
                ui.div(bug_type(), steel_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                fire_type(),
                ui.h1(">"),
                ui.div(water_type(), grass_type()),
                ui.div(water_type(), ice_type()),
                ui.div(water_type(), bug_type()),
                ui.div(rock_type(), steel_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                grass_type(),
                ui.h1(">"),
                ui.div(fire_type(), ground_type()),
                ui.div(fire_type(), rock_type()),
                ui.div(grass_type(), rock_type()),
                ui.div(flying_type(), rock_type()),
                ui.div(bug_type(), rock_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                ground_type(),
                ui.h1(">"),
                ui.div(grass_type(), poison_type()),
                ui.div(bug_type(), rock_type()),
                ui.div(bug_type(), steel_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                ice_type(),
                ui.h1(">"),
                ui.div(fire_type(), ground_type()),
                ui.div(fire_type(), rock_type()),
                ui.div(fire_type(), flying_type()),
                ui.div(water_type(), grass_type()),
                ui.div(water_type(), ground_type()),
                ui.div(water_type(), flying_type()),
                ui.div(water_type(), dragon_type()),
                ui.div(ice_type(), ground_type()),
                ui.div(ice_type(), flying_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                rock_type(),
                ui.h1(">"),
                ui.div(ground_type(), flying_type()),
                ui.div(ground_type(), bug_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                steel_type(),
                ui.h1(">"),
                ui.div(fire_type(), rock_type()),
                ui.div(water_type(), ice_type()),
                ui.div(water_type(), rock_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
            ui.layout_columns(
                water_type(),
                ui.h1(">"),
                ui.div(water_type(), rock_type()),
                ui.div(water_type(), ground_type()),
                col_widths=type_tooltip_col_width,
                class_="centered_img_row"
            ),
        ),
        class_="tooltip_card",
    ),


def dark_type():
    return ui.tags.img(src="dark_type.png", width=type_image_size, class_="tooltip_img")


def bug_type():
    return ui.tags.img(src="bug_type.png", width=type_image_size, class_="tooltip_img")


def fire_type():
    return ui.tags.img(src="fire_type.png", width=type_image_size, class_="tooltip_img")


def normal_type():
    return ui.tags.img(src="normal_type.png", width=type_image_size, class_="tooltip_img")


def water_type():
    return ui.tags.img(src="water_type.png", width=type_image_size, class_="tooltip_img")


def electric_type():
    return ui.tags.img(src="electric_type.png", width=type_image_size, class_="tooltip_img")


def grass_type():
    return ui.tags.img(src="grass_type.png", width=type_image_size, class_="tooltip_img")


def ice_type():
    return ui.tags.img(src="ice_type.png", width=type_image_size, class_="tooltip_img")


def fighting_type():
    return ui.tags.img(src="fighting_type.png", width=type_image_size, class_="tooltip_img")


def poison_type():
    return ui.tags.img(src="poison_type.png", width=type_image_size, class_="tooltip_img")


def ground_type():
    return ui.tags.img(src="ground_type.png", width=type_image_size, class_="tooltip_img")


def flying_type():
    return ui.tags.img(src="flying_type.png", width=type_image_size, class_="tooltip_img")


def psychic_type():
    return ui.tags.img(src="psychic_type.png", width=type_image_size, class_="tooltip_img")


def rock_type():
    return ui.tags.img(src="rock_type.png", width=type_image_size, class_="tooltip_img")


def ghost_type():
    return ui.tags.img(src="ghost_type.png", width=type_image_size, class_="tooltip_img")


def dragon_type():
    return ui.tags.img(src="dragon_type.png", width=type_image_size, class_="tooltip_img")


def steel_type():
    return ui.tags.img(src="steel_type.png", width=type_image_size, class_="tooltip_img")


def empty_text():
    return ui.tags.div({"style": "height:1.5rem;"})


def spacer(width: float, height: float):
    return ui.tags.div({"style": f"width:{width}rem;height:{height}rem;"})


def element_and_tooltip(tag, tooltip_content, space=0):
    return ui.div(
        tag,
        spacer(space, 0),
        ui.tooltip(
            question_circle_fill,
            ui.card(
                tooltip_content,
                class_="tooltip_card",
            ),
        ),
        class_="tag_and_tooltip",
    )


app_ui = (
    ui.page_navbar(
        ui.nav_spacer(),
        atk_spa_calculator_page(),
        pokemon_info_page(),
        iv_calculation_page(),
        ui.head_content(
            ui.include_css(app_dir / "styles.css"),
            ui.include_css(app_dir / "number_input_style.css"),
        ),
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

    empty_table = reactive.value(
        pd.DataFrame(index=["hp_biv", "atk_biv", "def_biv", "spa_biv", "spd_biv", "spe_biv"],
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
        prefill_level_iv(level_iv_input() + 1)

    @reactive.effect
    @reactive.event(input.prefill_current_level_iv)
    def prefill_current_level_iv():
        prefill_level_iv(level_iv_input())

    def prefill_level_iv(level: int):
        biv_table = calc_biv_table()
        if biv_table.equals(empty_table()):
            raise SilentException

        hp_biv = ceil(biv_table.loc["hp_biv"].mean())
        atk_biv = ceil(biv_table.loc["atk_biv"].mean())
        def_biv = ceil(biv_table.loc["def_biv"].mean())
        spa_biv = ceil(biv_table.loc["spa_biv"].mean())
        spd_biv = ceil(biv_table.loc["spd_biv"].mean())
        spe_biv = ceil(biv_table.loc["spe_biv"].mean())

        ui.update_numeric("level_iv-number_value", value=level)
        ui.update_numeric("hp_iv-number_value", value=calc_hp(level, 0,
                                                              hp_biv, 0))
        ui.update_numeric("atk_iv-number_value", value=calc_stat(level, 0,
                                                                 atk_biv, 0, atk_nature_modifier()))
        ui.update_numeric("def_iv-number_value", value=calc_stat(level, 0,
                                                                 def_biv, 0, def_nature_modifier()))
        ui.update_numeric("spa_iv-number_value", value=calc_stat(level, 0,
                                                                 spa_biv, 0, spa_nature_modifier()))
        ui.update_numeric("spd_iv-number_value", value=calc_stat(level, 0,
                                                                 spd_biv, 0, spd_nature_modifier()))
        ui.update_numeric("spe_iv-number_value", value=calc_stat(level, 0,
                                                                 spe_biv, 0, spe_nature_modifier()))

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
    @reactive.event(input.save_stats_iv, input.reset_all_iv, input.pokemon_iv,
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
        total_ivs_avg = [f"{total_ivs[0] / 6:.2f}", f"{total_ivs[1] / 6:.2f}", f"{total_ivs[2] / 6:.2f}",
                         error_free]

        base_gap_sum = base_hp_gap + base_atk_gap + base_def_gap + base_spa_gap + base_spd_gap + base_spe_gap
        base_min_sum = base_hp_min + base_atk_min + base_def_min + base_spa_min + base_spd_min + base_spe_min
        biv_gap_sum = base_gap_sum * 2
        if biv_gap_sum == 0:
            base_gap_sum = 1
        missing_base_stats = current_bst() - base_min_sum

        base_hp_med = round(base_hp_min + missing_base_stats / base_gap_sum * base_hp_gap)
        base_atk_med = round(base_atk_min + missing_base_stats / base_gap_sum * base_atk_gap)
        base_def_med = round(base_def_min + missing_base_stats / base_gap_sum * base_def_gap)
        base_spa_med = round(base_spa_min + missing_base_stats / base_gap_sum * base_spa_gap)
        base_spd_med = round(base_spd_min + missing_base_stats / base_gap_sum * base_spd_gap)
        base_spe_med = round(base_spe_min + missing_base_stats / base_gap_sum * base_spe_gap)

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
        return str(current_bst.get()) + " BST"

    @reactive.effect
    @reactive.event(input.reset_all_iv)
    def reset_all_iv():
        stat_history.set(pd.DataFrame(
            pd.DataFrame(columns=["level", "hp", "atk", "def", "spa", "spd", "spe"], dtype=int)))

    @render.data_frame
    @reactive.event(input.save_stats_iv, input.reset_all_iv, input.delete_row_iv, ignore_none=False)
    def history_iv():
        return render.DataTable(
            stat_history(),
            width="100%",
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
        if not level_iv_input():
            raise SilentException()
        level = level_iv_input()

        if not hp_iv_input():
            raise SilentException()
        hp = hp_iv_input()

        if not atk_iv_input():
            raise SilentException()
        atk = atk_iv_input()

        if not def_iv_input():
            raise SilentException()
        deff = def_iv_input()

        if not spa_iv_input():
            raise SilentException()
        spa = spa_iv_input()

        if not spd_iv_input():
            raise SilentException()
        spd = spd_iv_input()

        if not spe_iv_input():
            raise SilentException()
        spe = spe_iv_input()

        stat_history_copy = stat_history.get().copy()
        stat_history_copy.loc[-1] = [level, hp, atk, deff, spa, spd, spe]
        stat_history_copy.index = stat_history_copy.index + 1
        stat_history.set(stat_history_copy)

    """
    ---------------------- Info Page ----------------------
    """

    # currently calculated info: XP yield, EV yield, weight -> low kick power
    @render.table(index=True)
    def calculate_xp_ev_info():
        # returns XP and EVs for a mon in a specific situation
        pokemon = input.pokemon_info()
        if not pokemons.index.values.tolist().__contains__(pokemon):
            raise SilentException()
        is_trainer = input.is_trainer_info()
        has_lucky_egg = input.has_lucky_egg_info()
        is_original_trainer = not input.is_traded_pokemon_info()
        enemy_level = enemy_level_info_input()

        xp = calc_xp_yield(pokemon, enemy_level, is_trainer, has_lucky_egg, is_original_trainer)

        weight = pokemons["Weight"][pokemon]
        if weight < 100:
            power = 20
        elif weight < 250:
            power = 40
        elif weight < 500:
            power = 60
        elif weight < 1000:
            power = 80
        elif weight < 2000:
            power = 100
        else:
            power = 120

        table = pokemons.loc[[pokemon], ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]]
        table = table.loc[:, (table != 0).any(axis=0)]
        table.insert(0, "XP", xp)
        table["Low Kick Power"] = power
        table["Weight"] = str(weight / 10) + "kg"
        table = table.transpose()
        table.columns = [''] * len(table.columns)
        return table

    # calculates the confusion damage a player might receive.
    # aside from base inputs (atk+stage, def+stage, level) inputs are highly reliant on generaion, so these parts of
    # the formula should only be used in generation 3
    @render.plot
    def confusion_damage_info():

        level = own_level_info_input()
        atk = atk_info_input()
        atk_stage = atk_stage_info_input()
        deff = def_info_input()
        def_stage = def_stage_info_input()

        atk_badge = input.has_atk_badge()
        def_badge = input.has_def_badge()
        is_burned = input.is_burned_info()
        burned_modifier = 1.5 if is_burned else 1

        has_choice_band = input.has_choice_band_info()
        has_silk_scarf = input.has_silk_scarf_info()
        has_thick_club = input.has_thick_club_info()
        has_metal_powder = input.has_metal_powder_info()

        is_explosion_selfdestruct = input.is_explosion_selfdestruct_info()

        has_huge_pure_power = False
        has_hustle_guts = False
        marvel_scale_active = False
        ability = input.own_ability_info()
        if ability == "1.5": has_hustle_guts = True
        if ability == "1.5xDEF": marvel_scale_active = True
        if ability == "2": has_huge_pure_power = True

        effective_atk = calc_offense_stat_modifiers(stat=atk, has_offense_badge=atk_badge, offense_stage=atk_stage,
                                                    has_type_bonus_item=has_silk_scarf,
                                                    has_huge_pure_power=has_huge_pure_power,
                                                    has_choice_band=has_choice_band,
                                                    is_marowak_cubone_with_thick_club=has_thick_club,
                                                    has_hustle_plus_minus_guts=has_hustle_guts)
        effective_def = calc_defensive_stat_modifiers(stat=deff, has_defensive_badge=def_badge,
                                                      defensive_stage=def_stage,
                                                      is_ditto_with_metal_powder=has_metal_powder,
                                                      marvel_scale_active=marvel_scale_active,
                                                      move_is_explosion_selfdestruct=is_explosion_selfdestruct)

        base_dmg = calc_dmg_base(level, 40, effective_atk, effective_def)
        ibm_dmg = calc_ibm_damage(base_dmg, burned_modifier=burned_modifier)

        dmg_values = []
        for i in range(0, 16):
            dmg_values.append(floor(ibm_dmg * (85 + i) / 100))

        result = {}
        for j in range(min(dmg_values), max(dmg_values) + 1):
            result[j] = dmg_values.count(j)

        dmg_values = {val: dmg_values.count(val) for val in np.unique(dmg_values)}

        fig, ax = plt.subplots()
        ax.set_title("Confusion Damage")
        ax.set_xlabel("dmg")
        ax.set_ylabel("likelihood")

        ax.bar(range(min(dmg_values), max(dmg_values) + 1), list(result.values()), align='center')
        ax.set_xticks(range(min(dmg_values), max(dmg_values) + 1))
        ax.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16], labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])

        if not fig:
            SilentException()

        return fig

    """
    ---------------------- ATK / SPA Page ----------------------
    """

    @reactive.effect
    @reactive.event(input.reset_all)
    def reset_all():
        reset_main_inputs()
        reset_accordions()

    @reactive.effect
    @reactive.event(input.reset_dropdowns, input.reset_all)
    def reset_accordions_only():
        reset_accordions()

    def reset_main_inputs():
        ui.update_numeric("enemy_level-number_value", value=8)
        ui.update_numeric("move_power-number_value", value=95)
        ui.update_numeric("own_defense-number_value", value=20)
        ui.update_numeric("damage_received-number_value", value=10)
        session.send_input_message("is_stab", {"value": False})
        session.send_input_message("is_crit", {"value": False})
        session.send_input_message("effectiveness", {"value": "1"})
        ui.update_numeric("atk_spa_stage-number_value", value=0)
        ui.update_numeric("def_spd_stage-number_value", value=0)

    def reset_accordions():
        session.send_input_message("is_burned", {"value": False})
        session.send_input_message("ff_active", {"value": False})
        session.send_input_message("has_dd_charge", {"value": False})
        session.send_input_message("is_physical", {"value": False})
        session.send_input_message("enemy_ability", {"value": "1"})
        session.send_input_message("effectiveness", {"value": "1"})
        session.send_input_message("has_reflect_lightscreen", {"value": False})
        session.send_input_message("has_def_spd_badge", {"value": False})
        session.send_input_message("has_thick_fat", {"value": False})
        session.send_input_message("weather_modifier", {"value": "1"})
        session.send_input_message("mud_or_water_sport_active", {"value": False})

    # the formula used to determine ATK / SPA of the opponent in the ATK / SPA calculator
    # while gen 3 is the focus, you can also estimate the ATK / SPA of pokemon in other generations
    # there is less research / detailed possibility of accurate input into other gens
    @render.plot
    def calculate_offense():
        gen_used = int(input.simulate_generation())

        if not enemy_level_input():
            raise SilentException()
        enemy_level = int(enemy_level_input())
        if not enemy_move_power_input():
            raise SilentException()
        move_power = int(enemy_move_power_input())
        if not own_defense_input():
            raise SilentException()
        own_defense = int(own_defense_input())
        if not damage_received_input():
            raise SilentException()
        damage_received = int(damage_received_input())

        is_stab = input.is_stab()
        stab_modifier = 1.5 if is_stab else 1

        is_crit = input.is_crit()
        crit_multiplier = 2

        if gen_used == 6:
            crit_multiplier = 1.5
        if gen_used == 4:
            crit_multiplier = 3 if input.has_sniper() else 2

        crit_modifier = crit_multiplier if is_crit else 1

        if not (atk_spa_stage_input() or atk_spa_stage_input() == 0):
            raise SilentException()
        atk_spa_stage = int(atk_spa_stage_input())
        applied_atk_spa_stage = 0 if (is_crit and atk_spa_stage < 0) else atk_spa_stage

        if not (def_spd_stage_input() or def_spd_stage_input() == 0):
            raise SilentException()
        def_spd_stage = int(def_spd_stage_input())
        if not input.has_def_spd_badge():
            has_def_spd_badge = False
        else:
            has_def_spd_badge = input.has_def_spd_badge()
        applied_def_spd_stage = 0 if (is_crit and def_spd_stage > 0) else def_spd_stage
        effective_def_spd = calc_defensive_stat_modifiers(own_defense, has_defensive_badge=has_def_spd_badge,
                                                          defensive_stage=applied_def_spd_stage)

        if gen_used == 3 or gen_used == 4:
            eff1 = 0.5
            eff2 = 2
            if input.effectiveness() != "1-":
                # get effectiveness for "normal" (= how you would intuitively expect effectiveness to work) situations
                effectiveness = float(input.effectiveness())
                eff2 = 2 if effectiveness == 4 else 1
                if effectiveness == 0.25: eff2 = 0.5
                eff1 = 2 if effectiveness > 1 else 1
                if effectiveness < 1: eff1 = 0.5

            if gen_used == 3:
                enemy_ability_atk_spa_modifier = 1
                has_power_modifying_ability = False
                ability_input = input.enemy_ability()
                if ability_input != "1.5x power":
                    enemy_ability_atk_spa_modifier = float(ability_input)
                else:
                    has_power_modifying_ability = True

                has_reflect_lightscreen = input.has_reflect_lightscreen()
                reflect_lightscreen_modifier = 1 if (is_crit or not has_reflect_lightscreen) else 0.5

                weather_modifier = float(input.weather_modifier())

                has_thick_fat = input.has_thick_fat()
                thick_fat_modifier = 1 if not has_thick_fat else 0.5

                has_sport = input.mud_or_water_sport_active()
                sport_modifier = 1 if not has_sport else 0.5

                is_burned = input.is_burned()
                burned_modifier = 0.5 if is_burned else 1

                ff_active = input.ff_active()
                ff_modifier = 1.5 if ff_active else 1

                # only used for minimum damage (increases minimum dmg at that point in the calc from 0 to 1 if physical)
                is_physical = input.is_physical()

                has_double_damage_or_charge = input.has_dd_charge()
                double_damage_or_charge_modifier = 2 if has_double_damage_or_charge else 1

                move_effective_power = calc_move_power_modifiers(move_power, has_sport,
                                                                 has_power_modifying_ability)

                # get rough lower / upper limits of possible ATK / SPA values to reduce calculations needed
                min_offense_guess, max_offense_guess = calc_offense_backwards_gen_3(
                    damage_received, is_physical,
                    [eff2, eff1, stab_modifier, double_damage_or_charge_modifier, crit_modifier],
                    [ff_modifier, weather_modifier,
                     reflect_lightscreen_modifier, burned_modifier],
                    effective_def_spd, calc_base_power(enemy_level, move_effective_power), applied_atk_spa_stage,
                    thick_fat_modifier, enemy_ability_atk_spa_modifier
                )
                base_power = calc_base_power(enemy_level, move_effective_power)

                min_offense = -1
                max_offense = -1

                dmg = []
                values = []
                # go through the previously determined upper and lower limits
                for x in range(min_offense_guess, max_offense_guess + 1):
                    dmg.append(0)
                    values.append([])
                    # calc the whole dmg formula except random factor for this specific ATK / SPA value
                    full_damage = floor(floor(base_power
                                              * calc_stat_stages(floor(floor(x * enemy_ability_atk_spa_modifier)
                                                                       * thick_fat_modifier),
                                                                 applied_atk_spa_stage) / effective_def_spd) / 50)
                    full_damage = calc_ibm_damage(int(full_damage), burned_modifier,
                                                  reflect_lightscreen_modifier, weather_modifier, ff_modifier,
                                                  is_physical)
                    full_damage = calc_obm_damage_no_randomness(full_damage, crit_modifier,
                                                                double_damage_or_charge_modifier, stab_modifier, eff1,
                                                                eff2)

                    for y in range(16):
                        # apply the random factor of the dmg calculation, and use it if it matches the dmg we received
                        value = max(1, floor(full_damage * (y + 85) / 100))
                        values[x - min_offense_guess].append(value)
                        if floor(value == damage_received):
                            dmg[x - min_offense_guess] += 1
                            max_offense = x
                            if min_offense == -1:
                                min_offense = x
            else:
                # get rough lower / upper limits of possible ATK / SPA values to reduce calculations needed
                min_offense_guess, max_offense_guess = calc_offense_backwards_gen_4(
                    damage_received, eff2, eff1, stab_modifier, crit_modifier,
                    effective_def_spd, calc_base_power(enemy_level, move_power), applied_atk_spa_stage)
                base_power = calc_base_power(enemy_level, move_power)

                min_offense = -1
                max_offense = -1

                dmg = []
                values = []
                # go through the previously determined upper and lower limits
                for x in range(min_offense_guess, max_offense_guess + 1):
                    dmg.append(0)
                    values.append([])
                    # calc the whole dmg formula except random factor, effectiveness and stab
                    pre_rnd_dmg = floor((floor(floor(base_power * calc_stat_stages(x, applied_atk_spa_stage)
                                                     / effective_def_spd) / 50) + 2) * crit_modifier)

                    for y in range(16):
                        # apply the random factor of the dmg calculation, and use it if it matches the dmg we received
                        value = max(1, floor(pre_rnd_dmg * (y + 85) / 100))
                        value = max(1, floor(
                            floor(floor(floor(pre_rnd_dmg * (y + 85) / 100) * stab_modifier) * eff1) * eff2))
                        values[x - min_offense_guess].append(value)
                        if floor(value == damage_received):
                            dmg[x - min_offense_guess] += 1
                            max_offense = x
                            if min_offense == -1:
                                min_offense = x

        else:
            if input.effectiveness() == "1-":
                effectiveness = 1
            else:
                effectiveness = float(input.effectiveness())
            min_offense_guess, max_offense_guess = (
                calc_offense_backwards_gen_5_onward(damage_received, effectiveness, stab_modifier, crit_modifier,
                                                    effective_def_spd, calc_base_power(enemy_level, move_power),
                                                    applied_atk_spa_stage))

            min_offense = -1
            max_offense = -1

            base_power = calc_base_power(enemy_level, move_power)

            dmg = []
            values = []

            for x in range(min_offense_guess, max_offense_guess + 1):
                dmg.append(0)
                values.append([])
                # calc the dmg formula except random factor for this specific ATK / SPA value until rnd value
                pre_rnd_dmg = floor(floor(floor(base_power * calc_stat_stages(x, applied_atk_spa_stage)
                                                / effective_def_spd) / 50 + 2) * crit_modifier)
                for y in range(16):
                    # apply the random factor of the dmg calculation, and use it if it matches the dmg we received
                    value = max(1, floor(gen_5_round(
                        floor(pre_rnd_dmg * (y + 85) / 100)
                        * stab_modifier)
                                         * effectiveness))
                    values[x - min_offense_guess].append(value)
                    if floor(value == damage_received):
                        dmg[x - min_offense_guess] += 1
                        max_offense = x
                        if min_offense == -1:
                            min_offense = x

        if max_offense < 1:
            raise SilentException
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

            plot.set_yticks([0, 2, 4, 6, 8, 10, 12, 14, 16],
                            labels=["0", "2", "4", "6", "8", "10", "12", "14", "16"])
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

    # for the "you have changed values in this accordion" indicator
    @render.text
    def own_modifiers_counter():
        screen_modifier = int(input.has_reflect_lightscreen())
        badge_modifier = int(input.has_def_spd_badge())
        thick_fat_modifier = int(input.has_thick_fat())
        weather_modifier = int(input.weather_modifier() != "1")
        sport_modifier = int(input.mud_or_water_sport_active())
        modifiers_changed = (screen_modifier + badge_modifier + thick_fat_modifier +
                             weather_modifier + sport_modifier)

        if modifiers_changed > 0:
            return modifiers_changed
        else:
            return ""

    # for the "you have changed values in this accordion" indicator
    @render.text
    def enemy_modifiers_counter():
        burned_modifier = int(input.is_burned())
        ff_modifier = int(input.ff_active())
        dd_charge_modifier = int(input.has_dd_charge())
        is_physical_modifier = int(input.is_physical())
        enemy_ability_modifier = int(input.enemy_ability() != "1")
        modifiers_changed = (burned_modifier + ff_modifier + dd_charge_modifier
                             + is_physical_modifier + enemy_ability_modifier)

        if modifiers_changed > 0:
            return modifiers_changed
        else:
            return ""

    """
    ---------------------- Support Methods ----------------------
    """

    # gives upper and lower bounds for the ATK / SPA values we are looking for
    # see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_III for a good overview
    def calc_offense_backwards_gen_3(dmg_dealt: int, is_physical: bool, obm: list, ibm: list, defense: int,
                                     base_power: int, offense_stage: int, thick_fat_modifier: float,
                                     enemy_ability_modifier: float) -> Tuple[int, int]:
        # ibm = "inside bracket modifier", the modifiers before the +2 in the formula
        # obm = "outside bracket modifier", the modifiers after the +2 in the formula
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
                                            0] / thick_fat_modifier) / enemy_ability_modifier)
        offense_guess_max = floor(floor(
            calc_stat_stages_backwards(floor(int((offense_guess_max * 50 + 49) * defense + defense - 1)
                                             / int(base_power)), offense_stage)[1] / thick_fat_modifier + 1)
                                  / enemy_ability_modifier + 1)

        return offense_guess_min, offense_guess_max

    # gives upper and lower bounds for the ATK / SPA values we are looking for
    # see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_IV for a good overview
    def calc_offense_backwards_gen_4(damage_received: int, eff1: float, eff2: float, stab_modifier: float,
                                     crit_modifier: float, effective_def_spd: int, base_power: int,
                                     atk_spa_stage: int) -> Tuple[int, int]:
        offense_guess_min = damage_received
        offense_guess_max = damage_received

        offense_guess_min = floor(floor(floor(offense_guess_min / eff2) / eff1) / stab_modifier)
        offense_guess_max = ceil(ceil(ceil(offense_guess_max / eff2) / eff1) / stab_modifier)

        offense_guess_min = ceil(offense_guess_min / crit_modifier) - 2
        offense_guess_max = ceil(ceil(offense_guess_max / 0.85) / crit_modifier) - 2

        offense_guess_min = offense_guess_min * 50 * effective_def_spd
        offense_guess_max = (offense_guess_max * 50 + 49) * effective_def_spd + effective_def_spd - 1

        offense_guess_min = calc_stat_stages_backwards(floor(offense_guess_min / base_power), atk_spa_stage)[0]
        offense_guess_max = calc_stat_stages_backwards(ceil(offense_guess_max / base_power), atk_spa_stage)[1]

        return offense_guess_min, offense_guess_max

    # gives upper and lower bounds for the ATK / SPA values we are looking for
    # see https://bulbapedia.bulbagarden.net/wiki/Damage#Generation_V_onward for a good overview
    def calc_offense_backwards_gen_5_onward(damage_received: int, effectiveness: float, stab_modifier: float,
                                            crit_modifier: float, effective_def_spd: int, base_power: int,
                                            atk_spa_stage: int) -> Tuple[int, int]:
        offense_guess_min = damage_received
        offense_guess_max = damage_received

        # keep both as in the future they might be different at this point
        offense_guess_min = floor(offense_guess_min / effectiveness - 4)
        offense_guess_max = ceil(offense_guess_max / effectiveness + 4)

        offense_guess_min = floor(offense_guess_min / stab_modifier)
        offense_guess_max = floor(offense_guess_max / stab_modifier)

        # offense guess min gets divided by 1
        offense_guess_max = ceil(offense_guess_max / 0.85)

        offense_guess_min = floor(offense_guess_min / crit_modifier) - 2
        offense_guess_max = floor(offense_guess_max / crit_modifier + 1) - 2

        offense_guess_min = offense_guess_min * 50 * effective_def_spd
        offense_guess_max = (offense_guess_max * 50 + 49) * effective_def_spd + effective_def_spd - 1

        offense_guess_min = calc_stat_stages_backwards(floor(offense_guess_min / base_power), atk_spa_stage)[0]
        offense_guess_max = calc_stat_stages_backwards(ceil(offense_guess_max / base_power), atk_spa_stage)[1]

        return offense_guess_min - 1, offense_guess_max + 1

    # calculates the part in the damage formula before the +2 and after /50
    def calc_ibm_damage(base_damage: int, burned_modifier=1.0, barrier_lightscreen_modifier=1.0,
                        current_weather_modifier=1.0, flash_fire_modifier=1.0, is_physical=False) -> int:
        result = floor(floor(floor(floor(base_damage * flash_fire_modifier)
                                   * current_weather_modifier) * barrier_lightscreen_modifier) * burned_modifier)

        result = max(result, 1 if is_physical else 0)  # minimum dmg of 1 only for physical moves at this point
        return result + 2

    # calculates the part in the damage formula before the random factor and after +2
    def calc_obm_damage_no_randomness(base_damage: int, crit_modifier=1, double_damage_charge_modifier=1,
                                      stab_modifier=1.0, effectiveness_type_1=1.0, effectiveness_type_2=1.0) -> int:
        result = apply(crit_modifier, double_damage_charge_modifier, stab_modifier, effectiveness_type_1,
                       effectiveness_type_2, dmg_val=base_damage)
        return result

    # calculates the possible min and max values for the original stat of stat_with_stages
    def calc_stat_stages_backwards(stat_with_stages: int, stages: int) -> Tuple[int, int]:
        stat_without_stages = stat_with_stages / (2 + (stages if stages > 0 else 0)) * (
                2 - (stages if stages < 0 else 0))
        if stages < 0:
            original_stat_min = ceil(stat_without_stages)
            # -stages increases the result due to stages < 0
            return original_stat_min, original_stat_min - ceil(stages / 2)
        else:
            original_stat_min = floor(stat_without_stages)
            return original_stat_min, original_stat_min

    # all possible defensive stat modifiers before and including stages aside enigma berry
    # https://github.com/pret/pokefirered/blob/338ec9d956fcd39f4bbb361b444ded3eec8e9425/src/pokemon.c#L2437
    def calc_defensive_stat_modifiers(stat: int, has_defensive_badge=False,
                                      is_latios_latias_with_soul_dew=False,
                                      is_clamperl_with_dep_sea_scale=False, is_ditto_with_metal_powder=False,
                                      marvel_scale_active=False, move_is_explosion_selfdestruct=False,
                                      defensive_stage=0) -> int:
        result = stat
        if has_defensive_badge: result = floor(1.1 * result)
        if is_latios_latias_with_soul_dew: result = floor(1.5 * result)
        if is_clamperl_with_dep_sea_scale: result = floor(2 * result)
        if is_ditto_with_metal_powder: result = floor(2 * result)
        if marvel_scale_active: result = floor(1.5 * result)
        if move_is_explosion_selfdestruct: result = floor(0.5 * result)

        result = calc_stat_stages(result, defensive_stage)
        return result

    # all possible offensive stat modifiers before and including stages aside enigma berry
    # https://github.com/pret/pokefirered/blob/338ec9d956fcd39f4bbb361b444ded3eec8e9425/src/pokemon.c#L2437
    def calc_offense_stat_modifiers(stat: int, has_type_bonus_item=False,
                                    has_offense_badge=False,
                                    is_latios_latias_with_soul_dew=False, has_huge_pure_power=False,
                                    has_choice_band=False, is_clamperl_with_dep_sea_tooth=False,
                                    is_pikachu_with_light_ball=False,
                                    is_marowak_cubone_with_thick_club=False,
                                    thick_fat_applied=False,
                                    has_hustle_plus_minus_guts=False, offense_stage=0) -> int:
        result = stat
        if has_type_bonus_item: result = floor(1.1 * result)
        if has_huge_pure_power: result = floor(2 * result)
        if has_offense_badge: result = floor(1.1 * result)
        if is_latios_latias_with_soul_dew: result = floor(1.5 * result)
        if has_choice_band: result = floor(1.5 * result)
        if is_clamperl_with_dep_sea_tooth: result = floor(2 * result)
        if is_pikachu_with_light_ball: result = floor(2 * result)
        if is_marowak_cubone_with_thick_club: result = floor(2 * result)
        if thick_fat_applied: result = floor(0.5 * result)
        if has_hustle_plus_minus_guts: result = floor(1.5 * result)

        result = calc_stat_stages(result, offense_stage)
        return result

    # all possible power modifiers before the general dmg formula
    # https://github.com/pret/pokefirered/blob/338ec9d956fcd39f4bbb361b444ded3eec8e9425/src/pokemon.c#L2437
    def calc_move_power_modifiers(power: int, has_sport=False,
                                  overgrow_blaze_torrent_swarm_active=False) -> int:
        result = power
        if has_sport: result = floor(.5 * result)
        if overgrow_blaze_torrent_swarm_active: result = floor(1.5 * result)

        return result

    def apply(*args, dmg_val: int) -> int:
        result = dmg_val
        for arg in args:
            result = floor(result * arg)
        result = max(1, result)
        return result

    # biv is my abbreviation for 2 * Base stat + Individual Value (also written: 2 * Base + IVs)
    # i use it as it is easier to get both as a package than directly calc the base stat
    # (and it does not make a difference for the resulting stat anyway)
    def biv_range_hp(level: int, current_stat: int, evs: int):
        return biv_range(level, current_stat - 5 - level, evs, 1)

    def biv_range(level: int, current_stat: int, evs: int, nature: float) -> Tuple[int, int]:
        biv_maximum = biv_max(level, current_stat, evs, nature)
        biv_minimum = biv_min(level, current_stat, evs, nature)

        # min > max: should not happen (in that case some of the inputs have to be wrong, user sees result is wrong)
        # min = max: we assume we know the exact biv value
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

    # the minimum possible 2*Base+IV sum for given level, stat, EVs, nature
    def biv_min(level: int, current_stat: int, evs: int, nature: float) -> int:
        biv = min(541, max(22,
                           int(floor(floor(floor(current_stat / nature) - 4
                                           - (1 if nature == 1 or (
                                   nature == 1.1 and current_stat % 11 == 0) else 0))
                                     * 100 / level) + (0 if not (nature == 0.9 and current_stat % 10 == 0)
                                                       else 100 % level)
                               - floor(evs / 4))))
        result = calc_stat(level, 0, biv, 0, nature)
        return biv

    # the maximum possible 2*Base+IV sum for given level, stat, EVs, nature
    def biv_max(level: int, current_stat: int, evs: int, nature: float) -> int:
        biv = max(22, min(541, int(ceil(ceil((
                                                     (current_stat + (1 if (
                                                             nature == 1.1 and current_stat % 11 == 0) else 0)) / nature
                                                     - (5 if nature == 1 else 4)) * 100 + 99) / level) - floor(
            evs / 4))))

        result = calc_stat(level, 0, biv, 0, nature)
        return biv

    def biv_to_base_min(biv) -> int:
        if type(biv) != int:
            return 0
        else:
            return int(ceil((biv - 31) / 2))

    def biv_to_base_max(biv) -> int:
        if type(biv) != int:
            return 0
        else:
            return int(floor(biv / 2))

    def calc_dmg_base(level: int, move_power: int, offense: int, defense: int) -> int:
        return floor(floor(floor(2 * level / 5 + 2) * move_power * offense / defense) / 50)

    # in case you don't want offense / defense included in the calculation
    def calc_base_power(level: int, move_power: int) -> int:
        return floor(2 * level / 5 + 2) * move_power

    def calc_stat_stages(stat: int, stages: int) -> int:
        return floor(stat * (2 + (stages if stages > 0 else 0)) / (2 - (stages if stages < 0 else 0)))

    # calculate the given pokemon yields, valid formula for generations 2-4
    # https://bulbapedia.bulbagarden.net/wiki/Experience#Gain_formula
    def calc_xp_yield(pokemon, level: int, opponent_is_trainer: bool, lucky_egg_held=False,
                      is_original_trainer=True) -> int:
        xp_pokemon = floor(pokemons["XP"][pokemon] * level / 7)
        xp = floor(floor(floor(xp_pokemon * (1.5 if lucky_egg_held else 1)) * (1.5 if opponent_is_trainer else 1))
                   * (1.5 if not is_original_trainer else 1))
        return xp

    # calculation of stats beside HP
    # Formula: https://bulbapedia.bulbagarden.net/wiki/Stat#Generation_III_onward
    def calc_stat(level: int, base: int, iv: int, ev: int, nature: float) -> int:
        return floor((floor(floor(2 * base + iv + floor(ev / 4)) * level / 100) + 5) * nature)

    # hp has a slightly different calculation compared to other stats
    def calc_hp(level: int, base: int, iv: int, ev: int) -> int:
        return floor(floor(2 * base + iv + floor(ev / 4)) * level / 100) + 10 + level

    # starting in generation 5, this rounding formula is used for some calculations
    def gen_5_round(number_to_round: float) -> int:
        result = int(floor(number_to_round))
        if number_to_round % 1 > .5: result = result + 1
        return result

    """
    ---------------------- Module Server ----------------------
    """
    # the server of @module.ui

    enemy_level_input = number_input_server("enemy_level")
    enemy_move_power_input = number_input_server(id="move_power", label="Move Power:",
                                                 init=95, step=5, min_value=5, max_value=999)
    own_defense_input = number_input_server(id="own_defense", label="Own Defense:",
                                            init=20, min_value=1, max_value=999)
    damage_received_input = number_input_server(id="damage_received", label="DMG Taken:",
                                                init=10, min_value=1, max_value=999)
    atk_spa_stage_input = number_input_server(id="atk_spa_stage", label="ATK/SPA Stage:",
                                              init=0, min_value=-6, max_value=6)
    def_spd_stage_input = number_input_server(id="def_spd_stage", label="DEF/SPD Stage:",
                                              init=0, min_value=-6, max_value=6)

    level_iv_input = number_input_server(id="level_iv", label="Level:", init=5, min_value=1,
                                         max_value=100)
    hp_iv_input = number_input_server(id="hp_iv", label="HP:", init=22, min_value=11, max_value=999)
    atk_iv_input = number_input_server(id="atk_iv", label="ATK:", init=12, min_value=4,
                                       max_value=999)
    def_iv_input = number_input_server(id="def_iv", label="DEF:", init=12, min_value=4,
                                       max_value=999)
    spa_iv_input = number_input_server(id="spa_iv", label="SPA:", init=12, min_value=4,
                                       max_value=999)
    spd_iv_input = number_input_server(id="spd_iv", label="SPD:", init=12, min_value=4,
                                       max_value=999)
    spe_iv_input = number_input_server(id="spe_iv", label="SPE:", init=12, min_value=4,
                                       max_value=999)
    enemy_level_info_input = number_input_server(id="enemy_level_info", label="Level:",
                                                 init=8, min_value=1,
                                                 max_value=100)

    own_level_info_input = number_input_server(id="own_level_info", label="Own Level:",
                                               init=8)
    atk_info_input = number_input_server(id="atk_info", label="Own ATK:",
                                         init=20, min_value=1, max_value=999)
    atk_stage_info_input = number_input_server(id="atk_stage_info", label="ATK Stage:",
                                               init=0, min_value=-6, max_value=6)
    def_info_input = number_input_server(id="def_info", label="Own DEF:",
                                         init=20, min_value=1, max_value=999)
    def_stage_info_input = number_input_server(id="def_stage_info", label="DEF Stage:",
                                               init=0, min_value=-6, max_value=6)

    xp_requirement_input_info_1 = xp_requirement_input_server(id="xp_requirement_1",
                                                              from_level=5, to_level=8)
    xp_requirement_input_info_2 = xp_requirement_input_server(id="xp_requirement_2",
                                                              from_level=8, to_level=10)
    xp_requirement_input_info_3 = xp_requirement_input_server(id="xp_requirement_3",
                                                              from_level=5, to_level=8)

    early_modifier_gen_4_input = number_input_server("early_modifier_gen_4", min_value=0,
                                                     max_value=50, init=1, step=0.25),
    mid_modifier_gen_4_input = number_input_server("mid_modifier_gen_4", min_value=1,
                                                   max_value=3, init=1, step=0.50),
    late_modifier_gen_4_input = number_input_server("late_modifier_gen_4", min_value=1,
                                                    max_value=3, init=1, step=0.50),

    early_modifier_gen_5_onward_input = number_input_server("early_modifier_gen_5_onward", min_value=0,
                                                            max_value=50, init=1, step=0.25),
    mid_modifier_gen_5_onward_input = number_input_server("mid_modifier_gen_5_onward", min_value=1,
                                                          max_value=3, init=1, step=0.50),
    late_modifier_gen_5_onward_input = number_input_server("late_modifier_gen_5_onward", min_value=1,
                                                           max_value=3, init=1, step=0.50),


app = App(app_ui, server,
          static_assets=Path(app_dir / "images"))
