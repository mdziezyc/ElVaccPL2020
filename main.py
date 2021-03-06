import logging

import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score

from models.data import get_dataframe_teryt_features
from models.probability import fit_linear_model, validate_model, fit_alea_epist_model
from plotting.plot import plot_vaccination, plot_us


def plot_with_linear_regression(x, x_label, filename, ha_chart_text="right", ha_chart_bar="left"):
    y_true = results["Vaccination rate"]
    intercept, bias = np.polyfit(x, y_true, 1)
    y_pred = intercept * x + bias
    r2 = r2_score(y_true, y_pred)

    plot_vaccination(x, y_true, results["PITPP"], x, y_pred, r2, intercept, bias, x_label, filename,
                     ha_chart_text=ha_chart_text, ha_chart_bar=ha_chart_bar, y_lower=None, y_upper=None)


def plot_aleatoric_uncertainty(x_train, x_label, filename, ha_chart_text="right", ha_chart_bar="left"):
    x_train = x_train.to_numpy() / 100
    y_vaccination = results["Vaccination rate"].to_numpy() / 100

    model = fit_linear_model(x_train, y_vaccination)

    r2, mean, std = validate_model(model, x_train, y_vaccination)

    x = np.linspace(max(min(x_train) - 0.01, 0), min(max(x_train) + 0.01, 1), 1000)
    y_hat = np.squeeze(model(x).mean())
    y_sd = np.squeeze(model(x).stddev())

    y_hat_lower = np.squeeze(y_hat - 2 * y_sd)
    y_hat_upper = np.squeeze(y_hat + 2 * y_sd)

    plot_vaccination(100 * x_train, 100 * y_vaccination, results["PITPP"], 100 * x, 100 * y_hat, r2,
                     float(model.trainable_weights[0][0][0]), 100 * y_hat[0], x_label, f"aleatoric/{filename}",
                     y_lower=100 * y_hat_lower, y_upper=100 * y_hat_upper, ha_chart_text=ha_chart_text,
                     ha_chart_bar=ha_chart_bar)


# Plots both aleatoric and epistemic uncertainty
def plot_alea_epist_uncertainty(x_train, x_label, filename, ha_chart_bar="left"):
    x_train = x_train.to_numpy() / 100
    y_vaccination = results["Vaccination rate"].to_numpy() / 100

    model = fit_alea_epist_model(x_train, y_vaccination)
    x = np.linspace(max(min(x_train) - 0.01, 0), min(max(x_train) + 0.01, 1), 1000)
    y_pred = []
    for i in range(10):
        y_hat = np.squeeze(model(x).mean())
        y_sd = np.squeeze(model(x).stddev())

        y_hat_lower = np.squeeze(y_hat - 2 * y_sd)
        y_hat_upper = np.squeeze(y_hat + 2 * y_sd)

        y_pred.append((100 * y_hat, 100 * y_hat_lower, 100 * y_hat_upper))

    plot_us(100 * x_train, 100 * y_vaccination, results["PITPP"], 100 * x, y_pred,
            "Wyszczepienie gmin a wyniki wybor??w prezydenckich 2020",
            "% w pe??ni zaszczepionych na COVID-19 w gminie", x_label, f"all_uncertainty/{filename}",
            ha_chart_bar=ha_chart_bar)


def plot_all_for(x, x_label, filename, ha_chart_text="right", ha_chart_bar="left"):
    logging.info("Generating plots for %s", filename)
    plot_with_linear_regression(x, x_label, filename, ha_chart_text=ha_chart_text, ha_chart_bar=ha_chart_bar)
    plot_aleatoric_uncertainty(x, x_label, filename, ha_chart_text=ha_chart_text, ha_chart_bar=ha_chart_bar)
    plot_alea_epist_uncertainty(x, x_label, filename, ha_chart_bar=ha_chart_bar)
    plt.close('all')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    results = get_dataframe_teryt_features()

    not_voting = 100 - results["Attendance"]

    plot_all_for(not_voting + results["DUDA"] + results["BOSAK"] + results["HO??OWNIA"],
                 "% wyborc??w g??osuj??cych na Dud??, Ho??owni??, Bosaka lub nieg??osuj??cych w gminie",
                 "best_vax_hes",
                 ha_chart_text="left", ha_chart_bar="right")

    plot_all_for(not_voting + results["DUDA"] + results["BOSAK"],
                 "% wyborc??w g??osuj??cych na Dud??, Bosaka lub nieg??osuj??cych w gminie",
                 "best_vax_hes_noholownia",
                 ha_chart_text="left", ha_chart_bar="right")

    plot_all_for(results["TRZASKOWSKI"] + results["BIEDRO??"] + results["KOSINIAK-KAMYSZ"],
                 "% wyborc??w g??osuj??cych na Trzaskowskiego, Kosiniaka-Kamysza lub Biedronia w gminie",
                 "best_pro_vax")

    plot_all_for(results["TRZASKOWSKI"] + results["BIEDRO??"] + results["KOSINIAK-KAMYSZ"] + results["HO??OWNIA"],
                 "% wyborc??w g??osuj??cych na Trzaskowskiego, Ho??owni??, Kosiniaka-Kamysza lub Biedronia w gminie",
                 "best_pro_vax_holownia")

    plot_all_for(not_voting + results["DUDA"],
                 "% wyborc??w g??osuj??cych na Dud?? lub nieg??osuj??cych w gminie", "duda_notvoting",
                 ha_chart_text="left", ha_chart_bar="right")

    plot_all_for(results["BOSAK"] + results["DUDA"],
                 "% wyborc??w g??osuj??cych na Dud?? lub Bosaka w gminie", "duda_bosak",
                 ha_chart_text="left", ha_chart_bar="right")

    plot_all_for(results["Attendance"],
                 "Frekwencja w gminie", "frekwencja")

    # INDIVIDUAL

    plot_all_for(results["DUDA"],
                 "% wyborc??w g??osuj??cych na Dud?? w gminie", "duda",
                 ha_chart_text="left", ha_chart_bar="right")

    plot_all_for(results["BOSAK"],
                 "% wyborc??w g??osuj??cych na Bosaka w gminie", "bosak",
                 ha_chart_text="left", ha_chart_bar="right")

    plot_all_for(results["TRZASKOWSKI"],
                 "% wyborc??w g??osuj??cych na Trzaskowskiego w gminie", "trzaskowski")

    plot_all_for(results["BIEDRO??"],
                 "% wyborc??w g??osuj??cych na Biedronia w gminie", "biedron")

    plot_all_for(results["KOSINIAK-KAMYSZ"],
                 "% wyborc??w g??osuj??cych na Kosiniaka-Kamysza w gminie", "kosiniak",
                 ha_chart_text="right", ha_chart_bar="right")

    plot_all_for(results["HO??OWNIA"],
                 "% wyborc??w g??osuj??cych na Ho??owni?? w gminie", "holownia")
