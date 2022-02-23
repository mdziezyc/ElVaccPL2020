import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

from models.data import get_dataframe_teryt_features

results = get_dataframe_teryt_features()

candidates = ["BIEDROŃ", "BOSAK", "DUDA", "HOŁOWNIA", "KOSINIAK-KAMYSZ", "TRZASKOWSKI"]
independent_variables = candidates + ["PITPP"]

x_train = results[independent_variables].to_numpy()
y_train = results[["Vaccination rate"]].to_numpy()

print("LINEAR REGRESSION (sklearn)")

reg = LinearRegression().fit(x_train, y_train)
y_pred = reg.predict(x_train)

for independent_variable, weight in sorted(zip(independent_variables, reg.coef_[0]), key=lambda x: x[1]):
    print(independent_variable, round(float(weight), 3))
print(f"BIAS {round(float(reg.intercept_), 3)}")
r2 = r2_score(np.squeeze(y_train), np.squeeze(y_pred))
print(f"R2 {round(r2, 3)}")
