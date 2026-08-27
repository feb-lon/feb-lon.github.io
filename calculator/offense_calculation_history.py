from shiny import render
from shiny.types import SilentException, SafeException

from utils import *
from number_input import *
from shared import *
from ui_elements import *


@module.ui
def offense_calculation_history():
    return ui.page_fluid(
        ui.input_action_button("analyse_history_button", "Analyse History"),
        ui.input_action_button("refresh_button", "Refresh History"),
        ui.div(
            ui.output_data_frame("damage_history"),
            ui.output_data_frame("enc_history"),
            class_="io_row",
        ),
        ui.output_plot("analyse_history"),
    )


@module.server
def offense_calculation_history_server(input: Inputs, output: Outputs, session: Session,
                                       roll_history, encounter_history):

    @render.data_frame
    @reactive.event(input.refresh_button, ignore_none=False)
    def damage_history():
        return render.DataTable(
            roll_history.get(),
            width="100%",
            editable=False,
            selection_mode="row",
        )

    @render.data_frame
    @reactive.event(input.refresh_button, ignore_none=False)
    def enc_history():
        return render.DataTable(
            encounter_history.get(),
            width="100%",
            editable=False,
            selection_mode="row",
        )

    @render.plot
    @reactive.event(input.analyse_history_button)
    def analyse_history():
        enc_hist = encounter_history.get()
        roll_hist = roll_history.get()

        if enc_hist.empty:
            raise SafeException("History Empty")
        encounter_bases = {}
        base_min = 1
        base_max = 255

        # first, get as much data as possible out of each encounter
        for enc_nr in enc_hist.index:
            ivs, level = enc_hist.iloc[enc_nr, 0:2]
            if ivs.isdigit():
                iv_min = int(ivs)
                iv_max = iv_min
            else:
                iv_min = 0
                iv_max = 31
            vals = roll_hist.loc[roll_hist["encounter"] == enc_nr]

            of_min = vals["offense_from"].max()
            biv_min_pos = biv_min(level, of_min, 0, 1.1)
            of_max = vals["offense_to"].min()
            biv_max_pos = biv_max(level, of_max, 0, 0.9)

            stat_cases = {of_min: 1}

            if of_max < of_min: raise SafeException("no Values Possible with " + of_min + " < " + of_max)
            elif of_max == of_min: pass
            else:
                # weight the different stats possible with how likely their roll was
                stat_cases = dict(zip(range(of_min, of_max+1), np.ones(of_max-of_min+1)))
                for j in vals.index:
                    of_min_j = vals.loc[j, "offense_from"]
                    relevant_values = vals.loc[j, "dmg_rolls_per_stat"][of_min - of_min_j: of_max - of_min_j + 1]
                    for stat in stat_cases.keys():
                        stat_cases[stat] = stat_cases[stat] * relevant_values[stat - of_min]

            biv_to_stat_plus = {}
            biv_to_stat_neutral = {}
            biv_to_stat_minus = {}

            # get the possible {biv: stat} pairings for each nature
            for offense in range(of_min, of_max+1):
                if offense % 11 != 10:
                    biv_min_plus, biv_max_plus = biv_range(level, offense, 0, 1.1)
                    for biv in range(biv_min_plus, biv_max_plus+1):
                        biv_to_stat_plus[biv] = offense

                biv_min_neutral, biv_max_neutral = biv_range(level, offense, 0, 1)
                for biv in range(biv_min_neutral, biv_max_neutral+1):
                    biv_to_stat_neutral[biv] = offense

                biv_min_minus, biv_max_minus = biv_range(level, offense, 0, 0.9)
                for biv in range(biv_min_minus, biv_max_minus+1):
                    biv_to_stat_minus[biv] = offense

            enc_base_min = int(ceil((biv_min_pos - iv_max) / 2))
            base_min = max(base_min, enc_base_min)
            enc_base_max = int(floor((biv_max_pos - iv_min) / 2))
            base_max = min(base_max, enc_base_max)

            # maybe change base_cases to base_case for each nature
            # (in case offense gets changed from range to array to account for gaps at higher levels)
            base_cases = dict.fromkeys(range(enc_base_min, enc_base_max+1), 0)

            # now multiply biv values with the corresponding stat weights
            if iv_min == iv_max:  # in case IVs are fixed
                # limit search to bases that are still possible
                for base in range(base_min, base_max+1):
                    biv = int(2*base + iv_min)
                    cases_plus = stat_cases.get(biv_to_stat_plus.get(biv, 0), 0)
                    cases_neutral = stat_cases.get(biv_to_stat_neutral.get(biv, 0), 0)
                    cases_minus = stat_cases.get(biv_to_stat_minus.get(biv, 0), 0)
                    base_cases[base] = base_cases[base] + 4*cases_plus + 17*cases_neutral + 4*cases_minus
            else:  # random IVs, like wild Pokemon
                for biv in range(biv_min_pos, biv_max_pos+1):
                    base_maximum = floor(biv / 2)
                    last_cases = 0

                    # to reduce the calculations, uneven bivs can be skipped if calculated in the even biv before
                    if base_maximum % 2 == 1 and last_cases != 0:
                        weight = 0
                    elif base_maximum % 2 == 0 and biv < biv_max_pos:
                        weight = 2
                    else:
                        weight = 1

                    if weight > 0:
                        cases_plus = stat_cases.get(biv_to_stat_plus.get(biv, 0), 0)
                        cases_neutral = stat_cases.get(biv_to_stat_neutral.get(biv, 0), 0)
                        cases_minus = stat_cases.get(biv_to_stat_minus.get(biv, 0), 0)
                        total_cases = (4*cases_plus + 17*cases_neutral + 4*cases_minus) * weight
                        for base in range(base_maximum-15, base_maximum+1):
                            base_cases[base] = base_cases[base] + total_cases


            encounter_bases[enc_nr] = base_cases

        result = dict(zip(range(base_min, base_max+1), np.ones(base_max-base_min+1)))

        for encounter in encounter_bases.keys():
            curr_enc = encounter_bases.get(encounter, {})
            for base in range(base_min, base_max+1):
                result[base] = result[base] * curr_enc.get(base, 0)

        values_total = 0
        for value in result.values():
            values_total += value

        for base in result.keys():
            result[base] = result[base] / values_total


        df = pd.DataFrame(result, index=["combinations"])
        df = df.loc[:, (df != 0).any(axis=0)]
        df = df.transpose()
        plot = df.plot(kind="bar", legend=False)
        plot.set_xlabel("BST")
        plot.set_ylabel("Likelihood")

        return plot