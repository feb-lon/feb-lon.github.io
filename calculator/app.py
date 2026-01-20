from iv_calculation_page import *
from pokemon_info_page import *
from atk_spa_calculation_page import *
from shiny import *


app_ui = (
    ui.page_navbar(
        ui.nav_spacer(),
        atk_spa_calculator_page(id="atk_spa_calculator"),
        pokemon_info_page(id="pokemon_info"),
        iv_calculation_page(id="iv_calculation"),
        ui.head_content(
            ui.include_css(app_dir / "styles.css"),
            ui.include_css(app_dir / "number_input_style.css"),
        ),
        id="mode",
        title="Pokemon Calculator (Generation 3 Focus)",
        window_title="Gen 3 Calculator",
    )
)


def server(input: Inputs, output: Outputs, session: Session):
    atk_spa_calculation_page_server(id="atk_spa_calculator")
    iv_calculation_page_server(id="iv_calculation")
    pokemon_info_page_server(id="pokemon_info")

app = App(app_ui, server,
          static_assets=Path(app_dir / "images"))
