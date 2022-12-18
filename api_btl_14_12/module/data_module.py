import pandas as pd


def loadWeight():
    df = pd.read_csv('TOPSIS_weight.csv')
    return df