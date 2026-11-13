from math import floor

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from shiny import reactive


class GraphFactory:

    THEMES = {
        "bluh" : {
            "spine_color": "#1E1E1E",
            "text_color": "#1E1E1E",
            "grid_color": "#5AA5D5",
        },
        "dark" : {
            "spine_color": "#EAEAEA",
            "text_color": "#EAEAEA",
            "grid_color": "#5AA5D5",
        },
        "Oringe" : {
            "spine_color": "#1E1E1E",
            "text_color": "#1E1E1E",
            "grid_color": "#FFE300",
        },
        "quack" : {
            "spine_color": "#1E1E1E",
            "text_color": "#1E1E1E",
            "grid_color": "#96b81b",
        }
    }

    _theme=reactive.Value(dict)

    def __init__(self, theme="bluh"):
        self._theme = reactive.Value(self.THEMES[theme])

    @property
    def theme(self):
        return self._theme.get()

    def set_theme(self, theme):
        self._theme.set(self.THEMES[theme])

    def create(self):
        fig, ax = plt.subplots()

        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        ax.xaxis.label.set_color(self.theme["text_color"])
        ax.yaxis.label.set_color(self.theme["text_color"])
        ax.title.set_color(self.theme["text_color"])

        ax.tick_params(colors=self.theme["spine_color"])
        for spine in ax.spines.values():
            spine.set_color(self.theme["spine_color"])
        return fig, ax

    def dmg_graph(self):
        fig, ax = self.create()
        ax.set_title("ATK/SPA Value Likelihood")
        ax.set_ylabel("Nr. of rolls / 16")
        ax.set_xlabel("ATK/SPA value")

        ax.set_yticks([0, 4, 8, 12, 16], labels=["0", "4", "8", "12", "16"])
        ax.set_ylim(0, 16)
        return fig, ax

    def dmg_spread_only_observed(self, min_offense, max_offense, dmg):
        fig, ax = self.dmg_graph()
        fig.patch.set_alpha(0)
        ax.set_facecolor("none")

        ax.yaxis.set_minor_locator(MultipleLocator(2))
        ax.grid(color=self.theme["grid_color"], alpha=0.25)
        ax.grid(True, which="minor", linewidth=".1", axis="y", color=self.theme["grid_color"], zorder=0)
        ax.grid(True, which="major", linewidth="1", axis="y", color=self.theme["grid_color"], zorder=0)
        ax.grid(False, which="both", axis="x")

        if max_offense - min_offense < 20:
            ax.set_xticks(range(min_offense, max_offense + 1))
        ax.bar(range(min_offense, max_offense + 1), dmg, zorder=3)

        return ax

    def dmg_spread_all_values(self, min_offense, max_offense, dmg, received):
        fig, ax = self.dmg_graph()
        plot = dmg.plot(kind="bar", stacked=True, ax=ax, fig=fig)
        num_rows = len(dmg)
        col_names = list(dmg.columns)
        target_boxes = []

        # write dmg numbers on the bars
        for patch_index, rect in enumerate(plot.patches):
            col_idx = patch_index
            col_value = col_names[floor(col_idx / num_rows)]
            is_searched_value = (int(col_value) == int(received))
            height = rect.get_height()
            rect.set_edgecolor('black')
            rect.set_linewidth(float(.5))

            if height > 0:  # only label non-zero segments
                x = rect.get_x() + rect.get_width() / 2
                y = rect.get_y() + rect.get_height() / 2
                plot.text(
                    x, y, str(col_value),
                    ha='center', va='center',
                    color='black', fontsize=13,
                    fontweight=('bold' if is_searched_value else 'normal'),
                )
                if is_searched_value:
                    rect.set_linewidth(2)
                    target_boxes.append(rect)

        for box in target_boxes:
            box.set_zorder(2)
        plot.get_legend().remove()
        # to avoid the graph getting to crowded with labels
        if max_offense - min_offense < 20:
            plot.set_xticks(range(0, max_offense - min_offense + 1), range(min_offense, max_offense + 1),
                            rotation="horizontal")
        else:
            plot.set_xticks(range(0, max_offense - min_offense + 1), range(min_offense, max_offense + 1))

        return plot
