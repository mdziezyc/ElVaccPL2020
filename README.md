# ElVaccPL2020

## Intro

Project aims to analyse relation between vaccination rates in Polish communities (pol. *gminy*) and Polish presidential
election results from 2020.

Install `requirements.txt`. Run `main.py` to generate plots. Remove `data/vaccination.json` if you want to download the
newest data (currently data are not updated, last update: 31.10.21).

Results were used and interpreted in my [tweet](https://twitter.com/DziezycMaciej/status/1495721187137228805) (Polish).

## Additional content

Aleatoric and epistemic uncertainty modeling using Tensorflow Probability. Figures are presented in `figures/aleatoric`
and `figures/all_uncertainty`. Terminology and code inspired by
[Aleksander Molak's post](https://towardsdatascience.com/modeling-uncertainty-in-neural-networks-with-tensorflow-probability-part-1-an-introduction-2bb564c67d6)
.

If you want to regarate plots only used in tweet you can remove lines:

```python
plot_aleatoric_uncertainty(x, x_label, filename, ha_chart_text=ha_chart_text, ha_chart_bar=ha_chart_bar)
plot_alea_epist_uncertainty(x, x_label, filename, ha_chart_bar=ha_chart_bar)
```

from `main.py`.

## Data sources

### Statistic Poland (GUS)

https://bdl.stat.gov.pl/bdl/dane/podgrup/temat

`teryt_density.csv`

* LUDNOŚĆ (K3)
* STAN LUDNOŚCI (G7)
* Gęstość zaludnienia oraz wskaźniki (P2425)
* 2020
* ludność na 1 km2
* Zaznacz wszystkie gminy

`teryt_pit_per_person.csv`

* FINANSE PUBLICZNE (K27)
* DOCHODY BUDŻETÓW GMIN I MIAST NA PRAWACH POWIATU (G423)
* Dochody na 1 mieszkańca (P2627)
* 2020
* gminy łącznie z miastami na prawach powiatu
* dochody własne - udziały w podatkach stanowiących dochody budżetu państwa podatek dochodowy od osób fizycznych

`teryt_income_per_person.csv`

* FINANSE PUBLICZNE (K27)
* DOCHODY BUDŻETÓW GMIN I MIAST NA PRAWACH POWIATU (G423)
* Dochody na 1 mieszkańca (P2627)
* 2020
* gminy łącznie z miastami na prawach powiatu
* dochody własne

### National Electoral Commission (PKW)

https://prezydent20200628.pkw.gov.pl/prezydent20200628/pl/dane_w_arkuszach

`wyniki_gl_na_kand_po_gminach_proc_utf8.csv`

* Wyniki głosowania na kandydatów w pierwszej turze wyborów
* po gminach CSV

### Government

https://www.gov.pl/web/szczepienia-gmin#/rankingpolska

`vaccination.json`

https://www.gov.pl/api/data/covid-vaccination-contest/results-details?segment=A%2CB%2CC