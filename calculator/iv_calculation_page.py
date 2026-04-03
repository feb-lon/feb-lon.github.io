from math import ceil
from tokenize import String

from numpy._core.strings import upper
from pandas.core.computation.align import align_terms
from shiny import render
from shiny.types import SilentException

from utils import *
from ui_elements import *
from shared import *
from number_input import *


@module.ui
def iv_calculation_page():
    return ui.nav_panel(
        "IV Calculator",
        element_and_tooltip(
            ui.h2("IV Calculator"),
            1,
            "As there is currently no method to track EVs, i would "
            "not recommend using this when having no idea what to do about EVs",
        ),
        ui.div(
            ui.div(
                {"style": "width: 20%; text-align: center"},
                settings(),
            ),
            ui.div(
                {"style": "width: 70%"},
                result_table(),
                input_array(),
                stat_history(),
            ),
            class_="top_layer_row",
        ),
    )


def settings():
    return (
        ui.card(
            ui.card_header(
                "Pokemon:",
            ),
            ui.card_body(
                ui.div(
                    ui.input_selectize("pokemon", "",
                                       sorted(pokemons.index), selected="Lickitung"),
                    ui.output_code("pokemon_bst"),
                    class_="io_row",
                ),
            ),

        ),
        ui.card(
            ui.card_header(
                "Nature:",
            ),
            ui.card_body(
                ui.div(
                    ui.input_radio_buttons("nature_plus", "",
                                           ["=", "+ ATK", "+ DEF", "+ SPA", "+ SPD", "+ SPE"]),
                    ui.input_radio_buttons("nature_minus", "",
                                           ["=", "- ATK", "- DEF", "- SPA", "- SPD", "- SPE"]),
                    class_="spread_row",
                ),
                class_="io_column small_gap",
            ),
        ),
        ui.card(
            ui.card_header(
                "Result Options"
            ),
            ui.card_body(
                ui.input_switch("possible", "only consider possible values", True),
                ui.input_radio_buttons("unit_used", "Base Stat Format:",
                                       {"Hide": "Hide", "PosBase": "Base - IVs", "Base": "Base", "IVs": "IVs", },
                                       selected="Hide"),
                class_="io_column",
            ),
        )
    ),


def result_table():
    return ui.card(
        ui.output_table("result"),
    ),


def input_array():
    return ui.card(
        ui.div(
            ui.input_action_button("prefill_current_level", "Guess Stats for Level:"),
            number_input(id="level", label="Level:", init=5, min_value=1, max_value=100),
            number_input(id="hp", label="HP:", init=22, min_value=11, max_value=999),
            number_input(id="atk", label="ATK:", init=12, min_value=4, max_value=999),
            number_input(id="def", label="DEF:", init=12, min_value=4, max_value=999),
            number_input(id="spa", label="SPA:", init=12, min_value=4, max_value=999),
            number_input(id="spd", label="SPD:", init=12, min_value=4, max_value=999),
            number_input(id="spe", label="SPE:", init=12, min_value=4, max_value=999),
            # ui.input_selectize("mons_defeated", "Mons Defeated at this Level:", sorted(pokemons.index), multiple=True, class_="io_row"),
            ui.input_action_button("save_stats", "Save Stats"),
            class_="io_row",
        ),
    ),


def stat_history():
    return ui.card(
        ui.card_body(
            ui.div(
                ui.layout_columns(ui.h5("Stat History (editable)")),
                ui.input_action_button("delete_row", "Delete Selected Row"),
                ui.input_action_button("reset_all", "Clear All"),
                class_="io_row"
            ),
            ui.output_data_frame("history"),
            class_="io_column",
        ),
    ),


@module.server
def iv_calculation_page_server(input: Inputs, output: Outputs, session: Session):
    stat_history = reactive.value(
        pd.DataFrame(columns=["level", "hp", "atk", "def", "spa", "spd", "spe"], dtype=int))

    empty_table = pd.DataFrame(index=["min", "avg", "max"], columns=["Total IVs", "AVG IVs per Stat"],
                               data=[[0, 0], [0, 0], [0, 0]])

    level_value, set_level = number_input_server(id="level", init=5, min_value=1, max_value=100)
    hp_value, set_hp = number_input_server(id="hp", init=22, min_value=11, max_value=999)
    atk_value, set_atk = number_input_server(id="atk", init=12, min_value=4, max_value=999)
    def_value, set_def = number_input_server(id="def", init=12, min_value=4, max_value=999)
    spa_value, set_spa = number_input_server(id="spa", init=12, min_value=4, max_value=999)
    spd_value, set_spd = number_input_server(id="spd", init=12, min_value=4, max_value=999)
    spe_value, set_spe = number_input_server(id="spe", init=12, min_value=4, max_value=999)

    current_bst = reactive.value(int(385))  # initial mon is Lickitung with 385 BST

    # we set the initial nature as neutral
    atk_nature_modifier = reactive.value(float(1))
    def_nature_modifier = reactive.value(float(1))
    spa_nature_modifier = reactive.value(float(1))
    spd_nature_modifier = reactive.value(float(1))
    spe_nature_modifier = reactive.value(float(1))

    @reactive.effect
    @reactive.event(input.prefill_next_level)
    def prefill_next_level():
        prefill_level(level_value() + 1)

    @reactive.effect
    @reactive.event(input.prefill_current_level)
    def prefill_current_level():
        prefill_level(level_value())

    def prefill_level(level: int):
        biv_table = calc_biv_table()
        if biv_table.size == 0:
            raise SilentException

        hp_biv = ceil(biv_table.loc["hp_biv"].mean())
        atk_biv = ceil(biv_table.loc["atk_biv"].mean())
        def_biv = ceil(biv_table.loc["def_biv"].mean())
        spa_biv = ceil(biv_table.loc["spa_biv"].mean())
        spd_biv = ceil(biv_table.loc["spd_biv"].mean())
        spe_biv = ceil(biv_table.loc["spe_biv"].mean())

        set_level(level)
        set_hp(calc_hp(level, 0, hp_biv, 0))
        set_atk(calc_stat(level, 0, atk_biv, 0, atk_nature_modifier()))
        set_def(calc_stat(level, 0, def_biv, 0, def_nature_modifier()))
        set_spa(calc_stat(level, 0, spa_biv, 0, spa_nature_modifier()))
        set_spd(calc_stat(level, 0, spd_biv, 0, spd_nature_modifier()))
        set_spe(calc_stat(level, 0, spe_biv, 0, spe_nature_modifier()))

    @reactive.effect
    @reactive.event(input.nature_plus, input.nature_minus)
    def change_nature():

        nature_plus = input.nature_plus()
        nature_minus = input.nature_minus()

        atk_nature_modifier.set(1.1 if nature_plus == "+ ATK" else 0.9 if nature_minus == "- ATK" else 1)
        def_nature_modifier.set(1.1 if nature_plus == "+ DEF" else 0.9 if nature_minus == "- DEF" else 1)
        spa_nature_modifier.set(1.1 if nature_plus == "+ SPA" else 0.9 if nature_minus == "- SPA" else 1)
        spd_nature_modifier.set(1.1 if nature_plus == "+ SPD" else 0.9 if nature_minus == "- SPD" else 1)
        spe_nature_modifier.set(1.1 if nature_plus == "+ SPE" else 0.9 if nature_minus == "- SPE" else 1)

    @render.table(index=True, justify="left", col_space="8rem")
    @reactive.event(input.save_stats, input.reset_all, input.pokemon,
                    input.nature_plus, input.nature_minus, stat_history, input.unit_used, input.possible)
    def result():
        df = calc_biv_table()
        if df.empty: return empty_table
        base_as_biv = current_bst() * 2
        unit_used = input.unit_used()
        possible = input.possible()

        total_biv_min = df["min"].sum()
        total_min = total_biv_min - base_as_biv
        total_biv_max = df["max"].sum()
        total_max = total_biv_max - base_as_biv
        if possible:
            total_max = min(total_max, 186)
            total_min = max(total_min, 0)
        total_avg = (total_max + total_min) / 2

        total_stats = [f"{total_min:g}", f"{total_avg:g}", f"{total_max:g}"]
        avg_per_stat = [f"{total_min / 6:.2f}", f"{total_avg / 6:.2f}", f"{total_max / 6:.2f}"]

        table = pd.DataFrame(columns=["min", "avg", "max"])
        table.loc["Total IVs"] = total_stats
        table.loc["AVG IVs per Stat"] = avg_per_stat
        if unit_used != "Hide":
            for stat in ["hp", "atk", "def", "spa", "spd", "spe"]:
                min_val = df.loc[stat + "_biv", "min"]
                avg_val = df.loc[stat + "_biv"].mean()
                max_val = df.loc[stat + "_biv", "max"]

                if possible:
                    min_val = max(min_val, 22)
                    max_val = min(max_val, 541)
                if max_val < min_val:
                    avg_val = 0
                if unit_used == "PosBase":
                    min_val = biv_to_base_min(min_val)
                    max_val = biv_to_base_max(max_val)
                    avg_val = (max_val + min_val) / 2
                elif unit_used == "Base":
                    min_val = min_val / 2
                    max_val = max_val / 2
                    avg_val = avg_val / 2

                label = unit_used
                if unit_used == "PosBase": label = "Base"
                table.loc[label + " " + upper(stat)] = [f"{min_val:g}", f"{avg_val:g}", f"{max_val:g}"]

        return table.transpose()

    def calc_biv_table():
        if stat_history().size < 1:
            return pd.DataFrame()

        biv_table = pd.DataFrame(columns=["min", "max"],
                                 index=["hp_biv", "atk_biv", "def_biv", "spa_biv", "spd_biv", "spe_biv"])

        for row in stat_history.get().itertuples():
            level, hp, atk, deff, spa, spd, spe = row[1:8]

            hp_biv_min, hp_biv_max = biv_range_hp(level, hp, 0)
            biv_table.loc["hp_biv"] = [max(hp_biv_min, biv_table.loc["hp_biv"]["min"]),
                                       min(hp_biv_max, biv_table.loc["hp_biv"]["max"])]
            atk_biv_min, atk_biv_max = biv_range(level, atk, 0, atk_nature_modifier.get())
            biv_table.loc["atk_biv"] = [max(atk_biv_min, biv_table.loc["atk_biv"]["min"]),
                                        min(atk_biv_max, biv_table.loc["atk_biv"]["max"])]
            def_biv_min, def_biv_max = biv_range(level, deff, 0, def_nature_modifier.get())
            biv_table.loc["def_biv"] = [max(def_biv_min, biv_table.loc["def_biv"]["min"]),
                                        min(def_biv_max, biv_table.loc["def_biv"]["max"])]
            spa_biv_min, spa_biv_max = biv_range(level, spa, 0, spa_nature_modifier.get())
            biv_table.loc["spa_biv"] = [max(spa_biv_min, biv_table.loc["spa_biv"]["min"]),
                                        min(spa_biv_max, biv_table.loc["spa_biv"]["max"])]
            spd_biv_min, spd_biv_max = biv_range(level, spd, 0, spd_nature_modifier.get())
            biv_table.loc["spd_biv"] = [max(spd_biv_min, biv_table.loc["spd_biv"]["min"]),
                                        min(spd_biv_max, biv_table.loc["spd_biv"]["max"])]
            spe_biv_min, spe_biv_max = biv_range(level, spe, 0, spe_nature_modifier.get())
            biv_table.loc["spe_biv"] = [max(spe_biv_min, biv_table.loc["spe_biv"]["min"]),
                                        min(spe_biv_max, biv_table.loc["spe_biv"]["max"])]

        return biv_table

    @render.text
    def pokemon_bst():
        current_bst.set(pokemons["BST"][input.pokemon()])
        return str(current_bst.get()) + " BST"

    @reactive.effect
    @reactive.event(input.reset_all)
    def reset_all():
        stat_history.set(pd.DataFrame(
            pd.DataFrame(columns=["level", "hp", "atk", "def", "spa", "spd", "spe"], dtype=int)))

    @render.data_frame
    @reactive.event(input.save_stats, input.reset_all, input.delete_row, ignore_none=False)
    def history():
        return render.DataTable(
            stat_history(),
            width="100%",
            editable=True,
            selection_mode="row",
        )

    @history.set_patch_fn
    def _(*, patch: render.CellPatch):
        stat_history_copy = stat_history().copy()
        fn = int
        stat_history_copy.iat[patch["row_index"], patch["column_index"]] = fn(patch["value"])
        stat_history.set(stat_history_copy)
        return patch["value"]

    @reactive.effect
    @reactive.event(input.delete_row)
    def delete_row():
        if not history.cell_selection()["rows"]:
            raise SilentException()
        selected_row_number = history.cell_selection()["rows"][0]
        stat_history_copy = stat_history.get().copy()
        stat_history_copy.drop(stat_history_copy.index[[selected_row_number]], inplace=True)
        stat_history_copy.reset_index(drop=True, inplace=True)
        stat_history.set(stat_history_copy)

    @reactive.effect
    @reactive.event(input.save_stats)
    def save_stats():
        if not level_value():
            raise SilentException()
        level = level_value()

        if not hp_value():
            raise SilentException()
        hp = hp_value()

        if not atk_value():
            raise SilentException()
        atk = atk_value()

        if not def_value():
            raise SilentException()
        deff = def_value()

        if not spa_value():
            raise SilentException()
        spa = spa_value()

        if not spd_value():
            raise SilentException()
        spd = spd_value()

        if not spe_value():
            raise SilentException()
        spe = spe_value()

        stat_history_copy = stat_history.get().copy()
        stat_history_copy.loc[-1] = [level, hp, atk, deff, spa, spd, spe]
        stat_history_copy.index = stat_history_copy.index + 1
        stat_history.set(stat_history_copy)
