from models.data import get_dataframe_teryt_features
from plotting.plot import plot

subtitle_text = "Wyszczepienie gmin a wyniki wyborów prezydenckich 2020"
vaccinated_proportion_text = "% w pełni zaszczepionych na COVID-19 w gminie"


def plot_helper(x, x_label, filename, ha_chart_text="right", ha_chart_bar="left"):
    plot(x, results["Vaccination rate"], results["PITPP"], subtitle_text, vaccinated_proportion_text,
         x_label, filename, ha_chart_text=ha_chart_text, ha_chart_bar=ha_chart_bar)


if __name__ == '__main__':
    results = get_dataframe_teryt_features()

    valid_votes_perc = results["Attendance"] / 100 * results["Valid"] / 100
    not_voting = 100 - results["Attendance"]

    plot_helper(not_voting + valid_votes_perc * (results["DUDA"] + results["BOSAK"] + results["HOŁOWNIA"]),
                "% wyborców głosujących na Dudę, Hołownię, Bosaka lub niegłosujących w gminie", "best_vax_hes",
                ha_chart_text="left", ha_chart_bar="right")

    plot_helper(not_voting + valid_votes_perc * (results["DUDA"] + results["BOSAK"]),
                "% wyborców głosujących na Dudę, Bosaka lub niegłosujących w gminie", "best_vax_hes_noholownia",
                ha_chart_text="left", ha_chart_bar="right")

    plot_helper(valid_votes_perc * (results["TRZASKOWSKI"] + results["BIEDROŃ"] + results["KOSINIAK-KAMYSZ"]),
                "% wyborców głosujących na Trzaskowskiego, Kosiniaka-Kamysza lub Biedronia w gminie", "best_pro_vax")

    plot_helper(valid_votes_perc * (
            results["TRZASKOWSKI"] + results["BIEDROŃ"] + results["KOSINIAK-KAMYSZ"] + results["HOŁOWNIA"]),
                "% wyborców głosujących na Trzaskowskiego, Hołownię, Kosiniaka-Kamysza lub Biedronia w gminie",
                "best_pro_vax_holownia")

    plot_helper(not_voting + valid_votes_perc * results["DUDA"],
                "% wyborców głosujących na Dudę lub niegłosujących w gminie", "duda_notvoting",
                ha_chart_text="left", ha_chart_bar="right")

    plot_helper(valid_votes_perc * (results["BOSAK"] + results["DUDA"]),
                "% wyborców głosujących na Dudę lub Bosaka w gminie", "duda_bosak",
                ha_chart_text="left", ha_chart_bar="right")

    plot_helper(results["Attendance"],
                "Frekwencja w gminie", "frekwencja")

    # INDIVIDUAL

    plot_helper(valid_votes_perc * results["DUDA"],
                "% wyborców głosujących na Dudę w gminie", "duda", ha_chart_text="left", ha_chart_bar="right")

    plot_helper(valid_votes_perc * results["BOSAK"],
                "% wyborców głosujących na Bosaka w gminie", "bosak", ha_chart_text="left", ha_chart_bar="right")

    plot_helper(valid_votes_perc * results["TRZASKOWSKI"],
                "% wyborców głosujących na Trzaskowskiego w gminie", "trzaskowski")

    plot_helper(valid_votes_perc * results["BIEDROŃ"],
                "% wyborców głosujących na Biedronia w gminie", "biedron")

    plot_helper(valid_votes_perc * results["KOSINIAK-KAMYSZ"],
                "% wyborców głosujących na Kosiniaka-Kamysza w gminie", "kosiniak", ha_chart_text="right",
                ha_chart_bar="right")

    plot_helper(valid_votes_perc * results["HOŁOWNIA"],
                "% wyborców głosujących na Hołownię w gminie", "holownia")
