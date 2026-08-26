from offense_calculation_overview import offense_calculation_overview, offense_calculation_overview_server
from iv_calculation_page import *
from pokemon_info_page import *
from shiny import *

app_ui = (
    ui.page_navbar(
        ui.nav_control(
            ui.a("Project Code on Github", href="https://github.com/feb-lon/feb-lon.github.io", target="_blank"),
        ),
        ui.nav_spacer(),
        ui.nav_control(ui.output_ui("page_title")),
        ui.nav_spacer(),
        offense_calculation_overview(id="offense_overview"),
        pokemon_info_page(id="pokemon_info"),
        iv_calculation_page(id="iv_calculation"),
        ui.head_content(
            ui.include_css(app_dir / "styles.css"),
            ui.include_css(app_dir / "number_input_style.css"),
        ),
        id="mode",
        title="Pokemon Calculator (Gen. 3 Focus)",
        window_title="Pokemon Calculator",
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    offense_calculation_overview_server(id="offense_overview")
    iv_calculation_page_server(id="iv_calculation")
    pokemon_info_page_server(id="pokemon_info")

    @render.ui
    @reactive.event(input.mode)
    def page_title():
        return ui.h3(input.mode())


app = App(app_ui, server, static_assets=Path(app_dir / "images"))
