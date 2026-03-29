from matplotlib import pyplot as plt, get_backend
from shiny import module, ui, Inputs, Outputs, render
from shiny.types import SilentException, SafeException
from typing_extensions import get_args

from utils import *
from number_input import *
from shared import *
from ui_elements import *


@module.ui
def atk_spa_calculator_page():
    return ui.nav_panel(
        "ATK / SPA Calculator",
        ui.h2("ATK / SPA Calculator"),
        ui.div(
            ui.page_fluid(
                graph_settings(),
                main_inputs(),
                reset_buttons(),
                class_="spread_row",
            ),
            offense_plot(),
            optional_inputs(),
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


def graph_settings():
    return ui.card(
        ui.card_body(
            ui.input_radio_buttons(
                "dmg_type",
                element_and_tooltip(
                    "Minimum Damage:",
                    1,
                    "Only used for determining minimum DMG (physical DMG has higher minimum DMG)",
                ),
                {"physical": "Physical", "special": "Special"},
                selected="special",
                inline=True,
            ),
            ui.input_radio_buttons(
                "graph_style",
                "Graph Style:",
                {"only_dmg_received": "Only DMG Received", "all_dmg_values": "All DMG Values"},
                inline=False,
                selected="only_dmg_received",
            ),
        ),
    ),


def main_inputs():
    return ui.div(
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
                        {"style": "margin-top: -1rem; margin-bottom: -1rem;"},
                        ui.output_ui("atk_spa_stage_ui"),
                        ui.output_ui("def_spd_stage_ui"),
                        ui.div(
                            ui.panel_conditional(
                                "input.simulate_generation == 4",
                                ui.input_switch("has_sniper", "Sniper"),
                            ),
                            ui.panel_conditional(
                                "input.simulate_generation == 5 || input.simulate_generation == 6",
                                {"style": "visibility: hidden;"},
                                ui.input_switch("padding_element", ""),
                            ),
                            ui.input_switch("is_crit", "CRIT"),
                            ui.input_switch("is_stab", "STAB"),
                            ui.panel_conditional(
                                "input.simulate_generation == 4 || input.simulate_generation == 5 "
                                "|| input.simulate_generation == 6",
                                ui.input_switch("has_adaptability", "Adaptability"),
                            ),
                            class_="ui_column big_buttons small_gap",
                        ),
                        ui.div(
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


def reset_buttons():
    return ui.div(
        ui.card(
            ui.card_header(
                "Reset Input Buttons"
            ),
            ui.card_body(
                ui.input_action_button("reset_all", "Reset All Inputs"),
                ui.input_action_button("reset_detailed_only", "Reset Detailed Inputs"),
                class_="spread_column",
            ),
        ),
    ),


def offense_plot():
    return ui.card(
        {"style": "border-color: black; border-width: 0.05rem;"},
        ui.output_plot("calculate_offense"),
    ),


def optional_inputs():
    return ui.div(
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
                        1,
                        ui.span("Effectiveness 1x- is only relevant in Generations 1 - 4")
                    ),
                    {3: "3", 4: "4", 5: "5", 6: "6+"},
                    inline=True,
                    selected=3,
                ),
                class_="io_column",
            ),
        ),
        ui.div(
            {"style": "width: 85%"},
            gen_3_inputs(),
            gen_4_inputs(),
            gen_5_onwards_inputs(),
        ),
        class_="io_row top",
    ),


def gen_3_inputs():
    return ui.panel_conditional(
        "input.simulate_generation == 3 & input.use_detailed_inputs",
        ui.card(
            {"style": "border-color: #C65A1E; border-width: .15rem;"},
            ui.card_body(
                ui.div(
                    ui.input_switch("is_burned", "Enemy Burned"),
                    element_and_tooltip(
                        ui.input_switch("ff_active", "Flashfire Bonus"),
                        0,
                        "Getting hit by a fire move gives this bonus for the whole fight.",
                    ),
                    element_and_tooltip(
                        ui.input_switch("has_dd_charge", "Double Damage / Charge Bonus"),
                        0,
                        double_damage_tooltip(),
                    ),
                    class_="io_row"
                ),
                ui.div(
                    ui.input_switch("move_is_explosion_selfdestruct", "Explosion / Selfdestruct"),
                    ui.input_radio_buttons("enemy_ability",
                                           element_and_tooltip(
                                               ("Enemy Ability: ", spacer(1, 0)),
                                               0,
                                               ability_tooltip(),
                                           ),
                                           {"1": "generic", "1.5x power": "1.5x Move Power",
                                            "1.5": "1.5x ATK/SPA", "2": "2x ATK"},
                                           selected="1",
                                           inline=True,
                                           ),
                    class_="io_row align_bottom"
                ),
                value="enemy_modifiers_counter",
                class_="io_column",
            ),
        ),
        ui.card(
            {"style": "border-color: #4E9E3A; border-width: .15rem;"},
            ui.card_body(
                ui.div(
                    ui.input_switch("has_def_spd_badge", "DEF/SPD Badge"),
                    ui.input_switch("has_thick_fat", "Thick Fat"),
                    ui.input_switch("has_marvel_scale", "Marvel Scale"),
                    class_="io_row",
                ),
                ui.div(
                    ui.input_switch("has_reflect_lightscreen", "Reflect / Lightscreen"),
                    ui.input_switch("mud_or_water_sport_active", "Mud/Water Sport"),
                    ui.input_radio_buttons(
                        "weather_modifier",
                        "Weather Modifier:",
                        {"0.5": "0.5x", "1": "1x", "1.5": "1.5x"},
                        inline=True,
                        selected="1",
                    ),
                    class_="io_row align_bottom",
                ),
                value="own_modifiers_counter",
                class_="io_column",
            ),
        ),
        class_="spread_row top",
    ),


def gen_4_inputs():
    return ui.panel_conditional(
        "input.simulate_generation == 4 & input.use_detailed_inputs",
        ui.card(
            element_and_tooltip(
                "Early Stage Modifier",
                1,
                ui.span("Burn: 0.5"),
                ui.span("Reflect/Lightscreen: 0.5"),
                ui.span("moreTargets(Double Battle): 0.75"),
                ui.span("Weather: 0.5, 1, 1.5"),
                ui.span("Flash Fire: 1.5"),
            ),
            number_input(id="early_modifier_gen_4", init=1, min_value=0.25, max_value=50, step=0.25),
            class_="io_row",
        ),
        ui.card(
            element_and_tooltip(
                "Mid Stage Modifier",
                1,
                ui.span("Life Orb: 1.3"),
                ui.span("Metronome(item): 1.0-2.0"),
                ui.span("Me First: 1.5"),
            ),
            number_input(id="mid_modifier_gen_4", init=1, min_value=0.5, max_value=3, step=0.5),
            class_="io_row",
        ),
        ui.card(
            element_and_tooltip(
                "Late Stage Modifier",
                1,
                ui.span("Solid Rock: 0.75"),
                ui.span("Filter: 0.75"),
                ui.span("Expert Belt: 1.2"),
                ui.span("Tinted Lens: 2"),
                ui.span("Type-Weakening-Berries: 0.5")
            ),
            number_input(id="late_modifier_gen_4", init=1, min_value=0.25, max_value=3, step=0.25),
            class_="io_row",
        ),
        class_="spread_row top",
    ),


def gen_5_onwards_inputs():
    return ui.panel_conditional(
        "(input.simulate_generation == 5 || input.simulate_generation == 6) "
        "& input.use_detailed_inputs",
        ui.card(
            element_and_tooltip(
                "Mid Stage Modifier",
                1,
                ui.span("moreTargets(Double Battle): 0.75"),
                ui.span("moreTargets(Battle Royals): 0.5"),
                ui.span("Parental Bond 2nd Strike: 0.5 (Gen 6), 0.25 (other Gens)"),
                ui.span("Weather: 0.5, 1, 1.5"),
                ui.span("Glaive Rush: 2"),
            ),
            number_input("mid_modifier_gen_5_onward", min_value=0.25, max_value=10, init=1, step=0.5),
            class_="io_row",
        ),
        ui.card(
            element_and_tooltip(
                "Late Stage Modifier",
                1,
                ui.span("Burn: 0.5"),
                ui.span("other: see below"),
                ui.span("Z-Move vs protected target: 0.25"),
                ui.span("Tera Shield: 0.2-0.75"),
                other_factors(),
            ),
            number_input("late_modifier_gen_5_onward", min_value=0.25, max_value=20, init=1, step=0.25),
            class_="io_row",
        ),
        class_="spread_row top",
    ),


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


@module.server
def atk_spa_calculation_page_server(input: Inputs, output: Outputs, session: Session):
    # general inputs
    get_enemy_level, set_enemy_level = number_input_server("enemy_level")
    get_enemy_move_power, set_enemy_move_power \
        = number_input_server(id="move_power", init=95, step=5, min_value=5, max_value=999)
    get_own_defense, set_own_defense \
        = number_input_server(id="own_defense", init=20, min_value=1, max_value=999)
    get_damage_received, set_damage_received \
        = number_input_server(id="damage_received", init=10, min_value=1, max_value=999)
    get_atk_spa_stage, set_atk_spa_stage \
        = number_input_server(id="atk_spa_stage", init=0, min_value=-6, max_value=6)
    get_def_spd_stage, set_def_spd_stage \
        = number_input_server(id="def_spd_stage", init=0, min_value=-6, max_value=6)

    # gen 4 inputs
    get_early_modifier_gen_4, set_early_modifier_gen_4 \
        = number_input_server(id="early_modifier_gen_4", min_value=0.25, max_value=50, init=1, step=0.25)
    get_mid_modifier_gen_4, set_mid_modifier_gen_4 \
        = number_input_server(id="mid_modifier_gen_4", min_value=1, max_value=3, init=1, step=0.50)
    get_late_modifier_gen_4, set_late_modifier_gen_4 \
        = number_input_server(id="late_modifier_gen_4", min_value=0.5, max_value=3, init=1, step=0.25)

    # gen 5 onward inputs
    get_mid_modifier_gen_5_onward, set_mid_modifier_gen_5_onward \
        = number_input_server(id="mid_modifier_gen_5_onward", min_value=0.25, max_value=10, init=1, step=0.50)
    get_late_modifier_gen_5_onward, set_late_modifier_gen_5_onward \
        = number_input_server(id="late_modifier_gen_5_onward", min_value=0.25, max_value=20, init=1, step=0.25)

    @render.ui
    def def_spd_stage_ui():
        stage = get_def_spd_stage()
        return ui.div(
            number_input(id="def_spd_stage", label="",
                         init=stage, min_value=-6, max_value=6, layout="stages"),
            ui.div(
                {"style": "width:3.7rem;font-size: .8rem;"},
                "DEF/SPD Stage",
            ),
            id="def_spd_stage_env",
            class_="io_column close_distance",
        )

    @render.ui
    def atk_spa_stage_ui():
        stage = get_atk_spa_stage()
        return ui.div(
            number_input(id="atk_spa_stage", label="",
                         init=stage, min_value=-6, max_value=6, layout="stages"),
            ui.div(
                {"style": "width:3.7rem;font-size: .8rem;"},
                "ATK/SPA Stage",
            ),
            class_="io_column close_distance",
        ),

    @reactive.effect
    @reactive.event(input.reset_all)
    def reset_all():
        reset_main_inputs()
        reset_detailed_input()

    @reactive.effect
    @reactive.event(input.reset_detailed_only, input.reset_all)
    def reset_detailed_only():
        reset_detailed_input()

    def reset_main_inputs():
        set_enemy_level(8)
        set_enemy_move_power(95)
        set_own_defense(20)
        set_damage_received(10)
        session.send_input_message("is_stab", {"value": False})
        session.send_input_message("is_crit", {"value": False})
        session.send_input_message("effectiveness", {"value": "1"})
        set_atk_spa_stage(0)
        set_def_spd_stage(0)

    def reset_detailed_input():
        session.send_input_message("is_burned", {"value": False})
        session.send_input_message("ff_active", {"value": False})
        session.send_input_message("has_dd_charge", {"value": False})
        session.send_input_message("move_is_explosion_selfdestruct", {"value": False})
        session.send_input_message("enemy_ability", {"value": "1"})

        session.send_input_message("has_reflect_lightscreen", {"value": False})
        session.send_input_message("has_def_spd_badge", {"value": False})
        session.send_input_message("has_thick_fat", {"value": False})
        session.send_input_message("has_marvel_scale", {"value": False})
        session.send_input_message("weather_modifier", {"value": "1"})
        session.send_input_message("mud_or_water_sport_active", {"value": False})

    # the formula used to determine ATK / SPA of the opponent in the ATK / SPA calculator
    # while gen 3 is the focus, you can also estimate the ATK / SPA of pokemon in other generations
    # there is less research / detailed possibility of accurate input into other gens
    @render.plot
    def calculate_offense():
        gen_used = int(input.simulate_generation())
        is_detailed = input.use_detailed_inputs()

        if not get_enemy_level():
            raise SilentException()
        enemy_level = int(get_enemy_level())
        if not get_enemy_move_power():
            raise SilentException()
        move_power = int(get_enemy_move_power())
        if not get_own_defense():
            raise SilentException()
        own_defense = int(get_own_defense())
        if not get_damage_received():
            raise SilentException()
        damage_received = int(get_damage_received())

        is_stab = input.is_stab()
        stab_modifier = 1.5 if is_stab else 1

        if gen_used != 3:
            if input.has_adaptability() and is_stab: stab_modifier = 2

        is_crit = input.is_crit()
        crit_multiplier = 2

        if gen_used == 6:
            crit_multiplier = 1.5
        if gen_used == 4:
            crit_multiplier = 3 if input.has_sniper() else 2

        crit_modifier = crit_multiplier if is_crit else 1

        if not (get_atk_spa_stage() or get_atk_spa_stage() == 0):
            raise SilentException()
        atk_spa_stage = int(get_atk_spa_stage())
        applied_atk_spa_stage = 0 if (is_crit and atk_spa_stage < 0) else atk_spa_stage

        if not (get_def_spd_stage() or get_def_spd_stage() == 0):
            raise SilentException()
        def_spd_stage = int(get_def_spd_stage())

        has_def_spd_badge = False
        if not input.has_def_spd_badge():
            pass
        elif is_detailed:
            has_def_spd_badge = input.has_def_spd_badge()

        has_marvel_scale = False
        if not input.has_marvel_scale():
            pass
        elif is_detailed:
            has_marvel_scale = input.has_marvel_scale()

        move_is_explosion_selfdestruct = False
        if not input.move_is_explosion_selfdestruct():
            pass
        elif is_detailed:
            move_is_explosion_selfdestruct = input.move_is_explosion_selfdestruct()

        applied_def_spd_stage = 0 if (is_crit and def_spd_stage > 0) else def_spd_stage
        effective_def_spd = calc_defensive_stat_modifiers(own_defense, has_defensive_badge=has_def_spd_badge,
                                                          defensive_stage=applied_def_spd_stage,
                                                          marvel_scale_active=has_marvel_scale,
                                                          move_is_explosion_selfdestruct=move_is_explosion_selfdestruct)

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
                # only used for minimum damage (increases minimum dmg at that point in the calc from 0 to 1 if physical)
                is_physical = input.dmg_type() == "physical"
                if is_detailed:
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

                    is_burned = input.is_burned()
                    burned_modifier = 0.5 if is_burned else 1

                    ff_active = input.ff_active()
                    ff_modifier = 1.5 if ff_active else 1

                    has_double_damage_or_charge = input.has_dd_charge()
                    double_damage_or_charge_modifier = 2 if has_double_damage_or_charge else 1

                    move_effective_power = calc_move_power_modifiers(move_power, has_sport,
                                                                     has_power_modifying_ability)
                else:
                    double_damage_or_charge_modifier = 1
                    ff_modifier = 1
                    weather_modifier = 1
                    reflect_lightscreen_modifier = 1
                    burned_modifier = 1
                    move_effective_power = move_power
                    thick_fat_modifier = 1
                    enemy_ability_atk_spa_modifier = 1

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
                                                                double_damage_or_charge_modifier, stab_modifier,
                                                                eff1, eff2)

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
                early_mod = 1
                mid_mod = 1
                late_mod = 1

                if is_detailed:
                    early_mod = get_early_modifier_gen_4()
                    mid_mod = get_mid_modifier_gen_4()
                    late_mod = get_late_modifier_gen_4()

                # get rough lower / upper limits of possible ATK / SPA values to reduce calculations needed
                min_offense_guess, max_offense_guess = calc_offense_backwards_gen_4(
                    damage_received, eff2, eff1, stab_modifier, crit_modifier,
                    effective_def_spd, calc_base_power(enemy_level, move_power), applied_atk_spa_stage,
                    early_mod, mid_mod, late_mod)

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
                    pre_rnd_dmg = floor(floor(floor(floor(floor(base_power * calc_stat_stages(x, applied_atk_spa_stage)
                                                                / effective_def_spd) / 50) * early_mod + 2)
                                              * crit_modifier) * mid_mod)

                    for y in range(16):
                        # apply the random factor of the dmg calculation, and use it if it matches the dmg we received
                        value = max(1, floor(floor(floor(
                            floor(floor(pre_rnd_dmg * (y + 85) / 100) * stab_modifier) * eff1) * eff2) * late_mod))
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

            mid_mod = 1
            late_mod = 1
            if is_detailed:
                mid_mod = get_mid_modifier_gen_5_onward()
                late_mod = get_late_modifier_gen_5_onward()

            min_offense_guess, max_offense_guess = calc_offense_backwards_gen_5_onward(damage_received, effectiveness,
                                                                                       stab_modifier, crit_modifier,
                                                                                       effective_def_spd,
                                                                                       calc_base_power(enemy_level,
                                                                                                       move_power),
                                                                                       applied_atk_spa_stage, mid_mod,
                                                                                       late_mod)

            min_offense = -1
            max_offense = -1

            base_power = calc_base_power(enemy_level, move_power)

            dmg = []
            values = []

            for x in range(min_offense_guess, max_offense_guess + 1):
                dmg.append(0)
                values.append([])
                # calc the dmg formula except random factor for this specific ATK / SPA value until rnd value
                pre_rnd_dmg = floor(gen_5_round(floor(floor(base_power * calc_stat_stages(x, applied_atk_spa_stage)
                                                            / effective_def_spd) / 50 + 2) * mid_mod) * crit_modifier)
                for y in range(16):
                    # apply the random factor of the dmg calculation, and use it if it matches the dmg we received
                    value = max(1, gen_5_round(floor(gen_5_round(floor(pre_rnd_dmg * (y + 85) / 100) * stab_modifier)
                                                     * effectiveness) * late_mod))
                    values[x - min_offense_guess].append(value)
                    if floor(value == damage_received):
                        dmg[x - min_offense_guess] += 1
                        max_offense = x
                        if min_offense == -1:
                            min_offense = x

        if sum(dmg) == 0 and max_offense_guess > 5:
            raise SafeException("The given DMG value can't be reached with these Parameters. "
                                "\n\nAll Gens: If all parameters are correct, consider the mon to have a different ability or an item"
                                "\n\nGen 4+: Due to not being as granular as the game the rounding might not be the same, "
                                "\nespecially if several factors are submitted through a single input (like Sniper + Magnitude vs Dig in gen5+ late stage modifier). "
                                "\n\nIn these cases, trying +-1 DMG (or +-2DMG) and inspecting their \"All DMG Values\" styled graph might be helpful.")
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
            target_boxes = []

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
                    if is_searched_value:
                        rect.set_linewidth(2)
                        target_boxes.append(rect)

            for box in target_boxes:
                box.set_zorder(2)
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
        enemy_ability_modifier = int(input.enemy_ability() != "1")
        modifiers_changed = (burned_modifier + ff_modifier + dd_charge_modifier + enemy_ability_modifier)

        if modifiers_changed > 0:
            return modifiers_changed
        else:
            return ""
