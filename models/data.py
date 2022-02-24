import csv
import json
import os
from urllib.request import urlopen

import pandas as pd


def get_vaccination_rates() -> dict[int, list[float]]:
    if not os.path.exists("data/vaccination.json"):
        download_vaccination_rate()
    with open("data/vaccination.json", "r") as f:
        data_json = json.load(f)
    return {int(x["teryt_code"]): x["full_vaccinated_percent"] for x in data_json}


def download_vaccination_rate() -> None:
    url = "https://www.gov.pl/api/data/covid-vaccination-contest/results-details?segment=A%2CB%2CC"
    response = urlopen(url)
    data_json = json.loads(response.read())
    with open("data/vaccination.json", "w") as f:
        json.dump(data_json, f)


def get_election_results() -> dict[int, list[float]]:
    teryt_election_results = {}
    with open("data/wyniki_gl_na_kand_po_gminach_proc_utf8.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader)
        for row in reader:
            valid = polish_number_to_float(row[-13])
            attendance = polish_number_to_float(row[6])
            valid_votes = valid / 100 * attendance / 100
            valid_votes_and_candidates = [polish_number_to_float(x) * valid_votes for x in row[-12:-1]]
            teryt_election_results[int(row[1])] = [attendance] + valid_votes_and_candidates
    return teryt_election_results


def polish_number_to_float(x: str) -> float:
    return float(x.replace(',', '.'))


def get_gus_data(filename: str) -> dict[int, float]:
    with open(f"data/{filename}.csv", encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        return {int(row[0]): float(row[1]) for row in reader}


def get_dataframe_teryt_features() -> pd.DataFrame:
    teryt_vaccination_rate = get_vaccination_rates()
    teryt_election_results = get_election_results()
    teryt_pit_per_person = get_gus_data("teryt_pit_per_person")
    teryt_income_per_person = get_gus_data("teryt_income_per_person")
    teryt_denisty = get_gus_data("teryt_density")

    results = []
    for teryt in teryt_vaccination_rate:
        vaccination_rate = teryt_vaccination_rate[teryt]
        election_results = teryt_election_results[teryt // 10]
        if teryt not in teryt_pit_per_person:
            teryt -= 1
        pit_per_person = min(4000.0, teryt_pit_per_person[teryt])
        income_per_person = teryt_income_per_person[teryt]
        density = teryt_denisty[teryt]
        row = [vaccination_rate] + election_results + [pit_per_person, income_per_person, density]
        results.append(row)

    return pd.DataFrame(results, columns=["Vaccination rate", "Attendance", "BIEDROŃ", "BOSAK", "DUDA",
                                          "HOŁOWNIA", "JAKUBIAK", "KOSINIAK-KAMYSZ", "PIOTROWSKI", "TANAJNO",
                                          "TRZASKOWSKI", "WITKOWSKI", "ŻÓŁTEK", "PITPP", "Incomepp", "Density"])
