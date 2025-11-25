import faicons as fa
import plotly.express as px

# Load data and compute static values
from shared import app_dir

from shiny import App, Inputs, Outputs, Session, reactive, render, ui

app_ui = ui.page_sidebar(
    ui.sidebar(
        "Own Pokemon:",
        ui.navset_card_tab(
            ui.nav_panel("Pokemon",
                         ui.input_selectize("pokemon", "Select your Pokemon", ["Bulbasaur","Ivysaur"]),
                         ),
            ui.nav_panel("Type",
                         ui.input_selectize("types", "Select types:", ["Water", "Fire", "Electric"], multiple=True)
                         ),
            id="input_type",
        ),
        ui.input_numeric("def_spd", "Own DEF/SPD:", 5, min=4),
        ui.input_select("def_spd_stage", "Own DEF/SPD Stage:", list(range(6, -7, -1)), selected=0),
        ui.input_switch("reflect_lightscreen", "Reflect / Lightscreen:"),
        ui.input_switch("def_spd_badge", "DEF/SPD Badge:"),
        ui.input_switch("thick_fat", "Thick Fat:"),
        ui.include_css(app_dir / "styles.css"),
    ),
    ui.page_fluid(
        ui.layout_columns(
            ui.card(
                ui.input_numeric("enemy_level", "Enemy Level:", 8, min=1, max=100),
                ui.input_selectize("enemy_move", "EnemyMove", ["Tackle","Pound"]),
                ui.input_switch("enemy_stab", "Move gets STAB bonus:"),
                ui.input_select("atk_spa_stage", "Enemy ATK/SPA Stage:", list(range(6, -7, -1)), selected=0),
                ui.input_switch("crit", "Move gets STAB bonus:"),
                ui.input_switch("burned", "Enemy is burned:"),
                ui.input_switch("ff_active", "Enemy gets bonus from Flashfire"),
                ui.input_switch("dd_charge", "Damgge is doubled or Charge bonus active:"),
                ui.input_select("weather", "Weather is:", ["Increases Damage","Neutral", "Decreases Damage"], selected="Neutral"),
            ),
            ui.card(
                ui.input_text("test", label="test"),
            ),
            col_widths=(5, 7),
        ),
    ),
    title=["Pokemon Generation 3 ATK / SPA Calculator", ui.input_select(choices=["Simplified", "Advanced"],label="Selected Mode:" , id="mode")],
)




def server(input: Inputs, output: Outputs, session: Session):
    @reactive.effect
    @reactive.event(input.input_type, input.types, input.pokemon)
    def _():
        if f"{input.input_type()}" == "Type":
            ui.update_text("test", value=f"{input.types()}")
        else:
            ui.update_text("test", value=f"{input.pokemon()}")


app = App(app_ui, server)
