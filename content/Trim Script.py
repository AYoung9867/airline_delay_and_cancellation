import pandas as pd

#load in original dataset
df = pd.read_csv("2018.csv")

#take random sample, 25MB for comfortable upload is about 2.9% of dataset
df_trimmed = df.sample(frac=0.029, random_state=42)

#save sample dataset, set index=False to avoid additional unnamed column
df_trimmed.to_csv("2018_sample.csv", index=False)
print("Saved 2018_sample.csv")