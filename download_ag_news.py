
from datasets import load_dataset
import pandas as pd

dataset = load_dataset("fancyzhx/ag_news", split="train")

df = pd.DataFrame({
    "text": dataset["text"],
    "label": dataset["label"]
})

df.to_csv("ag_news.csv", index=False)

print("Saved:", len(df), "articles")
print("File: ag_news.csv")
