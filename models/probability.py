import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_probability as tfp
from sklearn.metrics import r2_score

tfd = tfp.distributions
tfpl = tfp.layers

tf.random.set_seed(42)


def preprocess_variables(df: pd.DataFrame, independent_variables: list[str]) -> (np.array, np.array):
    df = df.copy()
    for column in ["Vaccination rate", "Attendance", "BIEDROŃ", "BOSAK", "DUDA", "HOŁOWNIA", "JAKUBIAK",
                   "KOSINIAK-KAMYSZ", "PIOTROWSKI", "TANAJNO", "TRZASKOWSKI", "WITKOWSKI", "ŻÓŁTEK"]:
        df[column] = df[column] / 100

    for column in ["PITPP", "Incomepp", "Density"]:
        df[column] = df[column] / max(df[column])

    return df[independent_variables].to_numpy(), df["Vaccination rate"].to_numpy()


def fit_linear_model(x_train, y_train):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(units=tfpl.IndependentNormal.params_size(1), input_shape=(1,)),
        tfpl.IndependentNormal(event_shape=1)
    ])
    model.compile(loss=lambda y_true, y_pred: -y_pred.log_prob(y_true), optimizer='adam')
    model.fit(x_train, y_train, epochs=1000, verbose=0)

    return model


def validate_model(model, x_train, y_train):
    y_pred = model(x_train)
    y_hat = np.squeeze(y_pred.mean())
    y_sd = np.squeeze(y_pred.stddev())
    return r2_score(y_train, y_hat), np.array(y_sd).mean(), y_train.std()
