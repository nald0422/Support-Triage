from google import genai
from dotenv import load_dotenv 
import os
from tokenizers import Tokenizer

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def gemini_tokenizer(content: str) -> int:
    result = client.models.count_tokens(model="gemini-3.8-flash", contents=content)
    return result.total_tokens

def bert_tokenizer(content: str):
    return Tokenizer.from_pretrained("bert-base-uncased").encode(content).tokens
    

# Ticket original text
ticket = "I can't find my order and I need a refund ASAP"

# Tokenization example
print(gemini_tokenizer(ticket))

# Tokenizer with splits
print(bert_tokenizer(ticket))
