from shiny import Inputs, Outputs, Session, module, reactive, ui


@module.ui
def number_input(label: str, init: int, min_value: int = 1, max_value: int = 100, step: int = 1) -> ui.TagChild:
    return ui.page_fluid(
        {"class": "number_input"},
        ui.div(
            ui.div(label, class_="number_input_label"),
            ui.div(
                ui.input_action_button("decrement", "-", class_="button_minus", tabindex_="-1"),
                ui.input_numeric("number_value", label="", value=init, min=min_value, max=max_value, step=step),
                ui.input_action_button("increment", "+", class_="button_plus", tabindex_="-1"),
                class_="number_input_controls",
            ),
            class_="number_input_row",
        ),
    )


#  label as input parameter to enable user just copy paste input parameter
@module.server
def number_input_server(input: Inputs, output: Outputs, session: Session, label: str = "",
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