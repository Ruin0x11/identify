import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

reviews = pd.read_csv("/Users/ruin/build/data/ign.csv",
                      encoding='latin1').iloc[:, 1:]

some_reviews = reviews.iloc[10:20, ]

means = reviews.groupby('release_year').mean()
