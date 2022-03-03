import matplotlib.pyplot as plt


def plot(x_true, y_true, color_plot, x_pred, y_pred, r2, intercept, bias, ax_title, y_label, x_label, path,
         ha_chart_text="left", ha_chart_bar="right", y_lower=None, y_upper=None):
    fig = plt.figure()
    ax = fig.add_subplot()
    fig.subplots_adjust(top=0.92, bottom=0.15)

    ax.set_title(ax_title, fontweight='bold')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)

    ax.text(0.01 if ha_chart_text == "left" else 0.99, 0.01,
            f"R² = {round(r2, 3)}, y = {round(intercept, 3)}x + {round(bias, 1)}", verticalalignment="bottom",
            horizontalalignment=ha_chart_text, transform=ax.transAxes, fontsize=8)

    scatter = ax.scatter(x_true, y_true, c=color_plot, linewidths=0.1, alpha=1)
    ax.plot(x_pred, y_pred, color="#FFB000")
    if y_lower is not None and y_upper is not None:
        plt.fill_between(x_pred, y_lower, y_upper, alpha=.15, label='$+/- 2SD$')
    plt.annotate(
        "Kolory reprezentują dochody gmin z PITu na 1 mieszkańca. Kwoty ucięte do 4000 zł (1 gmina powyżej tej "
        "wartości).\nŹródła: PKW (2020), gov.pl/szczepimysie (31.10.21), GUS BDL (2020). Autor: Maciej Dzieżyc (2022, "
        "CC BY-ND 4.0)",
        xy=(1.12, -0.16), xycoords='axes fraction', va='center', ha="right", fontsize=5)

    axins1 = ax.inset_axes([0.85 if ha_chart_bar == "right" else 0.05, 0.95, 0.1, 0.03])

    plt.colorbar(scatter, ax=ax, cax=axins1, orientation="horizontal", ticks=[min(color_plot), max(color_plot)],
                 label="PLN/os")
    plt.savefig(f"figures/{path}.png", dpi=300)


def plot_us(x_true, y_true, color_plot, x_pred, y_pred, ax_title, y_label, x_label, path, ha_chart_bar="right"):
    fig = plt.figure()
    ax = fig.add_subplot()
    fig.subplots_adjust(top=0.92, bottom=0.15)

    ax.set_title(ax_title, fontweight='bold')
    ax.set_ylabel(y_label)
    ax.set_xlabel(x_label)
    scatter = ax.scatter(x_true, y_true, c=color_plot, linewidths=0.1, alpha=1)

    for y in y_pred:
        plt.plot(x_pred, y[0], color='red', alpha=.5, lw=1)
        plt.plot(x_pred, y[1], c='g', alpha=.5, lw=1)
        plt.plot(x_pred, y[2], c='g', alpha=.5, lw=1)

    plt.annotate(
        "Kolory reprezentują dochody gmin z PITu na 1 mieszkańca. Kwoty ucięte do 4000 zł (1 gmina powyżej tej "
        "wartości).\nŹródła: PKW (2020), gov.pl/szczepimysie (31.10.21), GUS BDL (2020). Autor: Maciej Dzieżyc (2022, "
        "CC BY-ND 4.0)",
        xy=(1.12, -0.16), xycoords='axes fraction', va='center', ha="right", fontsize=5)

    axins1 = ax.inset_axes([0.85 if ha_chart_bar == "right" else 0.05, 0.95, 0.1, 0.03])

    plt.colorbar(scatter, ax=ax, cax=axins1, orientation="horizontal", ticks=[min(color_plot), max(color_plot)],
                 label="PLN/os")
    plt.savefig(f"figures/{path}.png", dpi=300)


def plot_vaccination(x, y_vaccination, y_pitpp, x_pred, y_pred, r2, intercept, bias, x_label, path,
                     ha_chart_text="right", ha_chart_bar="left", y_lower=None, y_upper=None):
    plot(x, y_vaccination, y_pitpp, x_pred, y_pred, r2, intercept, bias,
         "Wyszczepienie gmin a wyniki wyborów prezydenckich 2020",
         "% w pełni zaszczepionych na COVID-19 w gminie", x_label, path, ha_chart_text=ha_chart_text,
         ha_chart_bar=ha_chart_bar, y_lower=y_lower, y_upper=y_upper)
