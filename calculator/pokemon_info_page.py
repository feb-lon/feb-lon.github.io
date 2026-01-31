from matplotlib import pyplot as plt
from shiny.types import SilentException

from xp_requirement_input import *
from number_input import *
from ui_elements import *
from shared import *
from utils import *


@module.ui
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
                            1,
                            "XP information valid for Generations 2 - 4",
                        ),
                    ),
                    ui.div(
                        "Pokemon:",
                        ui.input_selectize("pokemon", "", sorted(pokemons.index)),
                        "at Level",
                        number_input(id="enemy_level", label="", init=8, min_value=1, max_value=100),
                        class_="io_row",
                    ),
                    ui.div(
                        ui.input_switch("is_trainer", "Trainer Fight"),
                        ui.input_switch("has_lucky_egg", "Lucky Egg"),
                        ui.input_switch("is_traded_pokemon", "Not Original Trainer"),
                        class_="spread_row",
                    ),
                    ui.output_table("general_information"),
                    class_="io_column"
                ),
            ),
            ui.div(
                {"style": "width: 30%"},
                ui.card(
                    element_and_tooltip(
                        ui.card_header(
                            ui.h3("Nature Information"),
                        ),
                        1,
                        "Generations 3+",
                    ),
                    ui.card_body(
                        ui.layout_columns(
                            {"style": "align-items: center; justify-items: start;"},
                            ui.span("My Nature:"),
                            ui.span("With this Nature:"),
                            ui.input_radio_buttons("nature_from", "", ["+", "=", "-"], selected="-", inline=True),
                            ui.input_radio_buttons("nature_to", "", ["+", "=", "-"], selected="+", inline=True),
                            ui.span("My Stat:"),
                            ui.span("It would have this stat:"),
                            number_input(id="stat_from", init=9, min_value=1, max_value=999),
                            ui.output_code("nature_information"),
                            col_widths=6,
                            class_="io_column"
                        ),
                        class_="io_column",
                    ),
                ),
                ui.card(
                    element_and_tooltip(
                        ui.card_header(ui.h3("XP Information")),
                        0,
                        "Valid for all Generations.",
                    ),
                    xp_requirement_input(id="xp_requirement_1", from_level=5, to_level=8),
                    ui.card_header(" "),
                    xp_requirement_input(id="xp_requirement_2", from_level=8, to_level=10),
                    class_="io_column",
                ),
            ),
            ui.card(
                {"style": "width: 30%"},
                ui.card_header(
                    element_and_tooltip(
                        ui.h3("Confusion Information"),
                        1,
                        ui.span("When using only inputs above the graph, output usable for every Generation."),
                        ui.span(),
                        ui.span("HOWEVER in Generations 1 - 2, there is no random factor for Confusion. "),
                        ui.span("This means the result is always the highest DMG value (furthest to the right)"),
                        ui.span(),
                        ui.span("Inputs below the graph should only be used in Generation 3"),
                    ),
                ),
                ui.div(
                    number_input(id="own_level", label="Level:", init=8, layout="short_input"),
                    ui.div(
                        number_input(id="atk", label="ATK:",
                                     init=20, min_value=1, max_value=999, layout="short_input"),
                        number_input(id="atk_stage", label="",
                                     init=0, min_value=-6, max_value=6, layout="stages_small"),
                        class_="io_row",
                    ),
                    ui.div(
                        number_input(id="def", label="DEF:",
                                     init=20, min_value=1, max_value=999, layout="short_input"),
                        number_input(id="def_stage", label="",
                                     init=0, min_value=-6, max_value=6, layout="stages_small"),
                        class_="io_row",
                    ),
                    class_="spread_row",
                ),
                ui.output_plot(id="confusion_damage_information"),
                ui.accordion(
                    ui.accordion_panel(
                        "Situational Effects",
                        ui.div(
                            ui.div(
                                "More Relevant:",
                                ui.div(
                                    ui.input_switch("is_burned", "Burned"),
                                    ui.input_switch("has_atk_badge", "ATK Badge"),
                                    ui.input_switch("has_def_badge", "DEF Badge"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.div(
                                "General Item:",
                                ui.div(
                                    ui.input_switch("has_choice_band", "Choice Band"),
                                    ui.input_switch("has_silk_scarf", "Silk Scarf"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.div(
                                "Pokemon-specific Items:",
                                ui.div(
                                    ui.input_switch("has_thick_club", "Thick Club"),
                                    ui.input_switch("has_metal_powder", "Metal Powder"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.div(
                                "Other:",
                                ui.div(
                                    ui.input_switch("is_explosion_selfdestruct", "Explosion/Selfdestruct"),
                                    class_="right_bound_row",
                                ),
                                class_="io_row",
                            ),
                            ui.input_radio_buttons("own_ability", "Own Ability:",
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


@module.server
def pokemon_info_page_server(input: Inputs, output: Outputs, session: Session):
    # for general information
    enemy_level_input, _ = number_input_server(id="enemy_level", init=8, min_value=1, max_value=100)

    # for xp information
    xp_requirement_input_server(id="xp_requirement_1", from_level=5, to_level=8)
    xp_requirement_input_server(id="xp_requirement_2", from_level=8, to_level=10)
    xp_requirement_input_server(id="xp_requirement_3", from_level=5, to_level=8)

    # for confusion information
    own_level_input, _ = number_input_server(id="own_level", init=8)
    atk_input, _ = number_input_server(id="atk", init=20, min_value=1, max_value=999)
    atk_stage_input, _ = number_input_server(id="atk_stage", init=0, min_value=-6, max_value=6)
    def_input, _ = number_input_server(id="def", init=20, min_value=1, max_value=999)
    def_stage_input, _ = number_input_server(id="def_stage", init=0, min_value=-6, max_value=6)
    stat_from_input, _ = number_input_server(id="stat_from", init=9, min_value=1, max_value=999)

    # currently calculated info: XP yield, EV yield, weight -> low kick power
    @render.table(index=True)
    def general_information():

        # returns XP and EVs for a mon in a specific situation
        pokemon = input.pokemon()
        if not pokemons.index.values.tolist().__contains__(pokemon):
            raise SilentException()
        is_trainer = input.is_trainer()
        has_lucky_egg = input.has_lucky_egg()
        is_original_trainer = not input.is_traded_pokemon()
        enemy_level = enemy_level_input()

        xp = calc_xp_yield(pokemon, enemy_level, is_trainer, has_lucky_egg, is_original_trainer)

        weight = pokemons["Weight"][pokemon]
        if weight < 100:
            low_kick_power = 20
        elif weight < 250:
            low_kick_power = 40
        elif weight < 500:
            low_kick_power = 60
        elif weight < 1000:
            low_kick_power = 80
        elif weight < 2000:
            low_kick_power = 100
        else:
            low_kick_power = 120

        base_friendship = int(pokemons["Base Friendship"][pokemon])
        return_power = max(floor(base_friendship / 2.5), 1)
        frustration_power = max(floor((255 - base_friendship) / 2.5), 1)

        table = pokemons.loc[[pokemon], ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]]
        table = table.loc[:, (table != 0).any(axis=0)]
        table.insert(0, "XP", xp)
        # table["Weight"] = str(weight / 10) + "kg"
        table[f"Low Kick vs. {pokemon}:"] = f"{low_kick_power} Power"
        # table["Base Friendship"] = base_friendship
        table[f"Return by {pokemon}:"] = f"{return_power} Power"
        table[f"Frustration by{pokemon}:"] = f"{frustration_power} Power"
        table = table.transpose()
        table.columns = [''] * len(table.columns)
        return table

    @render.text
    def nature_information():

        nature_from = input.nature_from()
        nature_to = input.nature_to()
        stat_from = stat_from_input()

        # return input if nature_from = nature_to
        if nature_from == nature_to:
            return stat_from

        stat_result_min = stat_from
        stat_result_max = stat_from
        stat_result = stat_from

        # convert input to neutral
        if nature_from == "-":
            stat_result_min = ceil(stat_from / 0.9)
            stat_result_max = ceil(stat_from / 0.9) + (1 if stat_from % 9 == 0 else 0)
            if nature_to == "+":
                stat_result_min = floor(stat_result_min * 1.1)
                stat_result_max = floor(stat_result_max * 1.1)
            if stat_result_min != stat_result_max:
                return str(stat_result_min) + " or " + str(stat_result_max)
            else:
                stat_result = stat_result_min
        else:
            if nature_from == "+":
                # floor(int * 1.1) is never int * 11 + 10
                if stat_from % 11 == 10:
                    return "<- Not Possible"
                stat_result = ceil(stat_from / 1.1)

            # convert stat from neutral to + / -
            if nature_to == "-":
                stat_result = floor(stat_result_min * 0.9)
            elif nature_to == "+":
                stat_result = floor(stat_result_min * 1.1)

        return str(stat_result)

    # calculates the confusion damage a player might receive.
    # aside from base inputs (atk+stage, def+stage, level) inputs are highly reliant on generaion, so these parts of
    # the formula should only be used in generation 3
    @render.plot
    def confusion_damage_information():

        level = own_level_input()

        atk = atk_input()
        atk_stage = atk_stage_input()
        deff = def_input()
        def_stage = def_stage_input()

        atk_badge = input.has_atk_badge()
        def_badge = input.has_def_badge()
        is_burned = input.is_burned()
        burned_modifier = 1.5 if is_burned else 1

        has_choice_band = input.has_choice_band()
        has_silk_scarf = input.has_silk_scarf()
        has_thick_club = input.has_thick_club()
        has_metal_powder = input.has_metal_powder()

        is_explosion_selfdestruct = input.is_explosion_selfdestruct()

        has_huge_pure_power = False
        has_hustle_guts = False
        marvel_scale_active = False
        ability = input.own_ability()
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
