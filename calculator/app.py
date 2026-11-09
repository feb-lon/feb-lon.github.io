from offense_calculation_overview import offense_calculation_overview, offense_calculation_overview_server
from iv_calculation_page import *
from pokemon_info_page import *
from coverage_calculator_page import *
from shiny import *

app_ui = (
    ui.page_navbar(
        ui.nav_control(
            ui.div(),
            ui.a("Project Code on Github", href="https://github.com/feb-lon/feb-lon.github.io", target="_blank"),
        ),
        ui.nav_control(
            ui.div(
                ui.span("Theme:"),
                spacer(.5, .5),
                ui.input_select(id="theme",label="", choices=["bluh", "dark", "Oringe"], selected="bluh"),
                class_="io_row",
            ),
        ),
        ui.nav_spacer(),
        ui.nav_control(ui.output_ui("page_title")),
        ui.nav_spacer(),
        offense_calculation_overview(id="offense_overview"),
        pokemon_info_page(id="pokemon_info"),
        coverage_calculator_page(id="coverage_calculator"),
        iv_calculation_page(id="iv_calculation"),
        ui.head_content(
            ui.include_css(app_dir / "styles.css"),
            ui.include_css(app_dir / "colors.css"),
            ui.include_css(app_dir / "number_input_style.css"),
            ui.tags.script("""
        $(document).on('shiny:inputchanged', function(event) {
            if (event.name === 'theme') {
                document.documentElement.setAttribute(
                    'data-theme',
                    event.value
                );
            }
        });
        """)
        ),
        id="mode",
        window_title="Pokemon Calculator",
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    offense_calculation_overview_server(id="offense_overview")
    iv_calculation_page_server(id="iv_calculation")
    pokemon_info_page_server(id="pokemon_info")
    coverage_calculator_page_server(id="coverage_calculator")

    @render.ui
    @reactive.event(input.mode)
    def page_title():
        return ui.span(input.mode(), class_="page-title")


app = App(app_ui, server, static_assets=Path(app_dir / "images"))
