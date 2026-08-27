import pandas as pd
from matplotlib.pyplot import minorticks_on
from shiny import render
from shiny.types import SafeException

from offense_calculation_history import offense_calculation_history, offense_calculation_history_server
from offense_calculation_page import offense_calculation_page, offense_calculation_page_server
from number_input import *
from ui_elements import *


@module.ui
def offense_calculation_overview():
    return ui.nav_panel(
        "ATK / SPA Calculator",
        ui.page_sidebar(
            ui.sidebar(sidebar_content(), width=350, open="closed"),
            ui.page_fluid(
                ui.panel_conditional(
                    "input.selected_page == 'calculation'",
                    offense_calculation_page(id="offense_calculator"),
                ),
                ui.panel_conditional(
                    "input.selected_page == 'history'",
                    offense_calculation_history(id="history"),
                ),
            ),
        ),
    )


def sidebar_content():
    return ui.div(
        {"style": "gap: 1rem"},
        ui.input_radio_buttons(
            "selected_page",
            "Page Selected:",
            ["calculation", "history"],
            inline=True,
            selected="calculation",
        ),
        ui.card(
            ui.output_ui("current_encounter"),
            ui.input_action_button(id="save_current_offense", label="save DMG, same encounter as last"),
        ),
        ui.card(
            ui.layout_columns(
                ui.span("LVL:"),
                ui.span("IVs:"),
                number_input(id="level", label="", init=8, min_value=1, max_value=100,
                             style="padding-left: 0; padding-right: 0; "),
                element_and_tooltip(
                    ui.input_select(id="opponent_ivs", label="",
                                    choices=["0-31", 0, 3, 4, 6, 12, 18, 30, 31]),
                    1,
                    ui.output_table("iv_table")),
                col_widths=(6, 6),
                class_="io_row",
            ),
            ui.input_action_button(id="new_encounter", label="save DMG, new encounter"),
        ),
        ui.card(
            ui.card_header("General Changes"),
            ui.card_body(
                ui.input_action_button(id="delete_history", label="Delete History"),
            ),
        ),
        class_="spread_column",
    ),


@module.server
def offense_calculation_overview_server(input: Inputs, output: Outputs, session: Session):
    get_level_calc, set_level_calc, offense_min, offense_max, dmg_rolls = offense_calculation_page_server(
        id="offense_calculator")
    get_level, set_level = number_input_server(
        id="level", init=8, min_value=1, max_value=100)

    roll_history = reactive.value(pd.DataFrame(
        columns=["encounter", "offense_from", "offense_to", "dmg_rolls_per_stat"]))
    encounter_history = reactive.value(pd.DataFrame(
        columns=["IVs", "level"]))

    history = offense_calculation_history_server(id="history",
                                                 roll_history=roll_history,
                                                 encounter_history=encounter_history)

    shared_level_value = reactive.value(8)

    iv_pairings_table = pd.DataFrame(data={
        "Value": ["0-31",
                  "0",
                  "3",
                  "4",
                  "6", "",
                  "12", "",
                  "18", "",
                  "30", "",
                  "31"],
        "Non-Rivals": ["Wild Pokemon",
                       "Other Trainer",
                       "Pokemaniac",
                       "Tamer",
                       "Psychic", "",
                       "Black Belt", "Cooltrainer/Ace",
                       "", "",
                       "Team Rocket Giovanni", "E4 members",
                       ""],
        "Rival Encounters": ["",
                             "Lab Rival",
                             "",
                             "",
                             "Rival Route 22 (1st encounter)", " Non-Aces of Bridge / Boat Rival",
                             "Ace of Bridge / Boat Rival", " Tower Rival, Non-Aces of Silph Rival",
                             "Ace of Silph Rival", "Non-Aces of Rival Route 22 (2nd encounter)",
                             "Ace of Rival Route 22 (2nd encounter)", "",
                             "Champion"],
    })

    @reactive.effect
    def _sync():
        set_level_calc(shared_level_value())

    @reactive.effect
    def _sync():
        shared_level_value.set(get_level_calc())

    @reactive.effect
    def _sync():
        set_level(shared_level_value())

    @reactive.effect
    def _sync():
        shared_level_value.set(get_level())

    @render.table(justify="left")
    def iv_table():
        return iv_pairings_table

    @render.text
    def get_offense_description():
        return str(offense_min.get()) + " to " + str(offense_max.get()) + " offense"

    @reactive.effect
    @reactive.event(input.new_encounter)
    def new_encounter():
        if encounter_history().empty:
            encounter_history().loc[0] = [input.opponent_ivs(), shared_level_value()]
        else:
            encounter_history().loc[len(encounter_history())] = [input.opponent_ivs(), shared_level_value()]

    @reactive.effect
    @reactive.event(input.save_current_offense, input.new_encounter)
    def save_roll():
        if roll_history().empty:
            roll_history().loc[0] = [
                0, offense_min.get(), offense_max.get(), dmg_rolls.get()]
        else:
            roll_history().loc[len(roll_history())] = [
                len(encounter_history())-1, offense_min.get(), offense_max.get(), dmg_rolls.get()]

    @render.ui
    @reactive.event(input.new_encounter, input.delete_history, ignore_none=False)
    def current_encounter():
        if encounter_history().empty:
            return ui.span("History is empty.")
        return (
            ui.div(
                {"style": "display: flex; justify-content: space-between;"},
                ui.span("DMG roll by: "),
                ui.span("Lvl: " + str(encounter_history.get().loc[len(encounter_history())-1, "level"])),
                ui.span("IVs: " + str(encounter_history.get().loc[len(encounter_history())-1, "IVs"]))
            ),
        )

    @render.ui
    @reactive.event(input.save_current_offense, shared_level_value, input.opponent_ivs, input.delete_history)
    def current_values():
        return (
            ui.div(
                {"style": "display: flex; justify-content: space-between;"},
                ui.span("Lvl: " + str(shared_level_value())),
                ui.span("IVs: " + str(input.opponent_ivs()))
            ),
        )

    @reactive.effect
    @reactive.event(input.delete_history)
    def delete_history():
        roll_history.set(pd.DataFrame(columns=["encounter", "offense_from", "offense_to", "dmg_rolls_per_stat"]))
        encounter_history.set(pd.DataFrame(columns=["IVs", "level"]))
