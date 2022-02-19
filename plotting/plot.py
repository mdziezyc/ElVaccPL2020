import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score


def plot(x, y, c, ax_title, y_label, x_label, path, ha_chart_text="left", ha_chart_bar="right"):
    fig = plt.figure()
    ax = fig.add_subplot()
    fig.subplots_adjust(top=0.92, bottom=0.15)

    ax.set_title(ax_title, fontweight='bold')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    m, b = np.polyfit(x, y, 1)
    y_pred = m * x + b
    ax.text(0.01 if ha_chart_text == "left" else 0.99, 0.01,
            f"R² = {round(r2_score(y, y_pred), 3)}, y = {round(m, 3)}x + {round(b, 1)}",
            verticalalignment="bottom", horizontalalignment=ha_chart_text,
            transform=ax.transAxes, fontsize=8)

    scatter = ax.scatter(x, y, c=c, linewidths=0.1, alpha=1)
    ax.plot(x, y_pred, color="#FFB000")
    plt.annotate(
        "Kolory reprezentują dochody gmin z PITu na 1 mieszkańca. Kwoty ucięte do 4000 zł (1 gmina powyżej tej wartości)."
        "\nŹródło: PKW (2020), gov.pl/szczepimysie (31.10.21), GUS BDL (2020). Autor: Maciej Dzieżyc (2022, CC BY-ND 4.0)",
        xy=(1.12, -0.16), xycoords='axes fraction', va='center', ha="right", fontsize=5)

    axins1 = ax.inset_axes([0.85 if ha_chart_bar == "right" else 0.05, 0.95, 0.1, 0.03])

    plt.colorbar(scatter, ax=ax, cax=axins1, orientation="horizontal", ticks=[min(c), max(c)], label="PLN/os")
    plt.savefig(f"figures/{path}.png", dpi=300)