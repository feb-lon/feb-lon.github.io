from shiny import Inputs, Outputs, Session, module, reactive, ui
from shiny.types import SilentException


@module.ui
def number_input(id_passed: str, label: str, init: int, min_value: int = 1, max_value: int = 100,
                 step: int = 1, layout="", tabbable=True) -> ui.TagChild:
    type = layout
    hastype = not (type == "")

    return ui.card(
        {"class": "number_input" + (" " + type if hastype else "")},
        ui.div(label, class_="number_input_label" + (" " + type + "_label" if hastype else "")),
        ui.div(
            ui.input_action_button("decrement", "∨", class_="button_minus", tabindex_="-1"),
            ui.div(
                ui.tags.input(
                    id=id_passed + "-number_value",
                    type="number",
                    class_="shiny-input-number form-control",
                    value=init,
                    min=min_value,
                    max=max_value,
                    step=step,
                    tabindex_="-1" if tabbable else "",
                ),
                class_="form-group shiny-input-container",
            ),
            ui.input_action_button("increment", "^", class_="button_plus", tabindex_="-1"),
            class_="number_input_controls" + (" " + type + "_controls" if hastype else "")
        ),
        class_="number_input_row" + (" " + type + "_row" if hastype else "")
    )


#  label as input parameter to enable user just copy paste input parameter
@module.server
def number_input_server(input: Inputs, output: Outputs, session: Session, id_passed=None, label: str = "",
                        init: int = 5, min_value: int = 1, max_value: int = 100, step: int = 1):
    val = reactive.value(int(init))

    @reactive.effect
    def _sync():
        val.set(input.number_value())

    @reactive.effect
    @reactive.event(input.increment)
    def increment_number_value():
        if not type(input.number_value()) == int:
            ui.update_numeric("number_value", value=init)
        else:
            new_value = min(input.number_value() + step, max_value)
            ui.update_numeric("number_value", value=new_value)

    @reactive.effect
    @reactive.event(input.decrement)
    def decrement_number_value():
        if not type(input.number_value()) == int:
            ui.update_numeric("number_value", value=init)
        else:
            new_value = max(input.number_value() - step, min_value)
            ui.update_numeric("number_value", value=new_value)

    return val
