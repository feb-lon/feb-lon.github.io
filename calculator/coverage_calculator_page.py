import matplotlib.pyplot as plt
from pandas.core.interchange.dataframe_protocol import DataFrame
from shiny import *
from shiny.render import data_frame
from shiny.types import SilentException

import pandas as pd
import numpy as np

from shared import types, pokemons


@module.ui
def coverage_calculator_page():
    return ui.nav_panel(
        "Weighted Coverage Calculator",
        ui.page_fluid(
            ui.card(
                ui.div(
                    ui.input_selectize(id="move_types",
                                       choices=types.index.tolist(),
                                       label="Own Move Types:",
                                       multiple=True, selected=""),
                    ui.input_select(id="pokemon_weight",
                                    choices={1: "none", "BST": "BST", "pow(BST, 1.5)": "BST^1.5",
                                             "pow(BST, 2)": "BST^2", "pow(BST, 3)": "BST^3"},
                                    label="How should a pokemon be weighted?"),
                    class_="io_row"),
            ),
            ui.div(
                ui.card(
                    ui.card_body(
                        {"style": "height: 500px; width: 500px;"},
                        ui.output_plot(id="weighted_coverage_graph"),
                    ),
                ),
                ui.card(
                    ui.card_body(
                        {"style": "height: 250px; width: 500px;"},
                        ui.output_table(id="weighted_coverage_table"),
                    ),
                ),
                class_="spread_row"
            ),
            class_="io_column"
        )
    )


@module.server
def coverage_calculator_page_server(input: Inputs, output: Outputs, session: Session):
    cov_table = reactive.value(pd.DataFrame(index=[0, 0.25, 0.5, 1, 2, 4],
                                            columns=["absolute", "weighted", "percentage"]))

    @reactive.effect
    @reactive.event(input.move_types, input.pokemon_weight)
    def weighted_coverage():
        if not input.move_types.get(): raise SilentException()
        move_types = input.move_types.get()
        weighting_method = input.pokemon_weight.get()

        weight_cov = pd.DataFrame(index=[0, 0.25, 0.5, 1, 2, 4],
                                  columns=["absolute", "weighted", "percentage"],
                                  data=[[0, 0.0, 0.0],[0, 0.0, 0.0],[0, 0.0, 0.0],[0, 0.0, 0.0],[0, 0.0, 0.0],[0, 0.0, 0.0]])

        for mon in pokemons.index:
            type_1 = pokemons.loc[mon, "Type 1"]
            type_2 = pokemons.loc[mon, "Type 2"]
            BST = pokemons.loc[mon, "BST"]
            effectiveness = 0

            for move_type in move_types:
                move_effectiveness = types.loc[move_type, type_1]
                if type_2 != "":
                    move_effectiveness = move_effectiveness * types.loc[move_type, type_2]
                effectiveness = max(effectiveness, move_effectiveness)

            if mon == "shedinja" and effectiveness < 2: effectiveness = 0

            weight_cov.loc[effectiveness, "absolute"] += 1

            if weighting_method != 1:
                weight = eval(weighting_method)
                weight_cov.loc[effectiveness, "weighted"] += weight
            else:
                weight_cov.loc[effectiveness, "weighted"] += 1

        for i in weight_cov.index:
            weight_cov.loc[i, "percentage"] = weight_cov.loc[i, "weighted"] / sum(weight_cov.loc[:, "weighted"])

        cov_table.set(weight_cov)

    @render.plot
    @reactive.event(cov_table)
    def weighted_coverage_graph():
        if not input.move_types.get(): raise SilentException()
        graph = cov_table.get().plot(kind="pie", y="weighted", wedgeprops=dict(width=0.7),
                                     startangle=90, explode=(.1, .1, .1, 0, .1, .1), autopct=high_pct,
                                     colors=(
                                         "#3A3A3A",  # 0
                                         "#D9534F",  # 0.25
                                         "#E8892D",  # 0.5
                                         "#E5C84B",  # 1
                                         "#82B366",  # 2
                                         "#3F8F5B",  # 4
                                     ))
        graph.legend().remove()
        return graph

    @render.table(index=True)
    @reactive.event(cov_table)
    def weighted_coverage_table():
        return cov_table.get().style.format({"weighted": "{:.0f}", "percentage": lambda x: f"{x * 100:.1f}%"},
                                            na_rep="0").format_index(lambda x: f"{x:g}x").set_properties(**{"text-align": "right"})

    def high_pct(pct):
        if pct >= 7:
            return f'{pct:.1f}%'
        else:
            return ''

    return
