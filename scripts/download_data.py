from pathlib import Path
from datasets import load_dataset

out = Path("data/raw/bitext.parquet")
out.parent.mkdir(parents=True, exist_ok=True)

ds = load_dataset(
    "bitext/Bitext-customer-support-llm-chatbot-training-dataset",
    split="train",
)
df = ds.to_pandas()
df.to_parquet(out)

print(f"Saved {len(df):,} rows to {out}")
print(df.columns.tolist())