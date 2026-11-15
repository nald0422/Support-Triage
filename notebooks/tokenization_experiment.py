from google import genai
from pathlib import Path
import pandas as pd
from tokenizers import Tokenizer
from dotenv import load_dotenv 
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def gemini_tokenizer(content: str) -> int:
    result = client.models.count_tokens(model="gemini-3.8-flash", contents=content)
    return result.total_tokens

def bert_tokenizer(content: str):
    return Tokenizer.from_pretrained("bert-base-uncased").encode(content).tokens

# Find the data file relative to this script, so it works from any folder
ROOT = Path(__file__).resolve().parents[1]
dataframe = pd.read_parquet(ROOT / "data/raw/bitext.parquet")

print("Shape", dataframe.shape)
print("Columns",dataframe.columns.tolist())
print("Head Items", dataframe.head(3))

print("\n\n# Sample 20 rows ----------------------------------------------------------------------\n\n")

sample = dataframe.sample(20, random_state=42)

# print(sample)

rows = []

for index, row in sample.iterrows():
    text = row["instruction"]
    gemini_tokens = gemini_tokenizer(text)
    rows.append({
        "text": text[:60], # First 60 characters of the ticket text
        "flags": row["flags"],
        "words": len(text.split()),
        "gemini": gemini_tokens,
        "bert": len(bert_tokenizer(text)),
    })

results = pd.DataFrame(rows);
results["words_per_token"] = (results["words"] / results["gemini"]).round(2)
print(results.to_string(index=False))
print("Average words per token::", results["words_per_token"].mean().round(2))

# Average words per token is still true to book's rule of thumb of 3/4 of a word per token, 
# but it is slightly lower than the 0.75 average for English text. 
# This is likely due to the fact that the dataset contains a lot of short sentences and phrases, which tend to have fewer words per token.