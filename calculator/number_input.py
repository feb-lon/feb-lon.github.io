from shiny import Inputs, Outputs, Session, module, reactive, ui


@module.ui
def number_input(label: str, init: int, min_value: int = 1, max_value: int = 100,
                 step: int = 1, layout="") -> ui.TagChild:
    has_layout = layout != ""

    return ui.card(
        {"class": "number_input" + (" " + layout if has_layout else "")},
        ui.div(label, class_="number_input_label"),
        ui.div(
            ui.input_action_button("decrement", "∨", class_="button_minus", tabindex_="-1"),
            ui.input_numeric(id="number_value", label="", value=init, min=min_value, max=max_value, step=step),
            ui.input_action_button("increment", "^", class_="button_plus", tabindex_="-1"),
            class_="number_input_controls" + (" " + layout + "_controls" if has_layout else "")
        ),
        class_="number_input_row" + (" " + layout + "_row" if has_layout else "")
    )


#  label as input parameter to enable user just copy paste input parameter
@module.server
def number_input_server(input: Inputs, output: Outputs, session: Session, id_passed=None, label: str = "",
                        init: int = 5, min_value: int = 1, max_value: int = 100, step: int = 1):
    val = reactive.value(int(init))

    @reactive.effect
    def _sync():
        value = input.number_value()
        if value is not None:
            val.set(value)

    @reactive.effect
    @reactive.event(input.increment)
    def increment_number_value():
        value = input.number_value() or init-1
        ui.update_numeric(
            "number_value",
            value=min(value + step, max_value),
            session=session,
        )

    @reactive.effect
    @reactive.event(input.decrement)
    def decrement_number_value():
        value = input.number_value() or init+1
        ui.update_numeric(
            "number_value",
            value=max(value - step, min_value),
            session=session,
        )

    return val
