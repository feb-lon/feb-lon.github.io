from shiny import Inputs, Outputs, Session, module, ui, render
from number_input import number_input, number_input_server
from shared import experience


@module.ui
def xp_requirement_input(from_level=5, to_level=8, curve="Fluctuating"):
    return ui.div(
        ui.div(
            "From Level",
            number_input(id="level_from", label="", min_value=1, max_value=100, init=from_level),
            "to",
            number_input(id="level_to", label="", min_value=1, max_value=100, init=to_level),
            class_="spread_row",
        ),
        ui.div(
            "XP Curve:",
            ui.input_selectize("xp_curve", "", choices=list(experience.columns),
                               selected=curve),
            "XP required:",
            ui.output_code("calc_xp_from_to"),
            class_="spread_row",
        ),
    )


@module.server
def xp_requirement_input_server(input: Inputs, output: Outputs, session: Session,
                                from_level=5, to_level=8):
    level_from_input,_ = number_input_server(id="level_from", min_value=1, max_value=100, init=from_level)
    level_to_input,_ = number_input_server(id="level_to", min_value=1, max_value=100, init=to_level)

    @output
    @render.code
    def calc_xp_from_to():
        xp_curve = input.xp_curve()
        lvl_from = level_from_input()
        lvl_to = level_to_input()

        xp_required = experience[xp_curve][lvl_from:lvl_to].sum()

        return f"{xp_required:,} XP"
