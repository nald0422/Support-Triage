## 2026-11-16 · Week 0 · Setup and data exploration

**Day 1**

**Did:** 
- Account setup
- Project setup
- Skimmed Book Preface: 
  - Book is about providing frameworks on developing ai application on top of foundation models.
  - 1st chapter focuses the use cases of developing an AI application.
  - 2nd chapter dive through how foundation models are made, architectures and training.
  - 3rd and 4th chapter explores different evaluation methods to create reliable and systematic evaluation pipeline for application.
  - Chapter 5 covers prompt engineering.
  - Chapter 6 explores model's context and its two major application patters for context construction "RAG" and "Agentic".
  - Ch.7 is about how to adapt a model to an application by changing the model itself with finetunning.
    - This chapter contains technical section that shows how to calculate the memory footprint of a model.
  - Getting data for finetunning is hard hence chapter 8 is all about data, including data acquisition, data annotations, data synthesis, and data
    processing.
  - Chapter 9 Inference.

- Learned language model
  - Encodes statistical information about one or more languages.
  - Tells how likely a word appears in a given context.
  - Language model involves multiple language
  - Basic unit of a language model is called *Token*
    - It can be a character, a word, or a part of a word like ('t, -tion) depending on a model.
    - Breaking of original text into token is *Tokenization*
    - Set of all tokens a model can work with is called model's *Vocabulary*
    - The tokenization method and vocabulary size are decided by model developers.

**Result:**
- Learned about huggingface and downloaded my first dataset from Bitext Customer Support.
- Differentiated AIE and DMLS.

**Surprised by:**
- As I was curious of native model finetunning as memory intensive. I looked it up on how rust helps and correlates, I came up with an answer that
  during finetunning, python code only orchestrates: data loading, setting up the model and training. the expensive math runs on the gpu and kernel
  written in CUDA, C++ or Triton. Pythons spends most of its time waiting for the GPU.

- AI models behind applications like ChatGPT, Google’s Gemini, and Midjourney are at such a
scale that they’re consuming a nontrivial portion of the world’s electricity, and we’re
at risk of running out of publicly available internet data to train them.

- Why language models use *token* instead of character or word.
  - Compared to characters token allows model to break words into meaningful components. 
    For example cooking it can be break into two words **cook + ing"** both carrying some meaning from the original word.
  - There are fewer unique tokens than unique words making model's vocabulary reduce in size which makes the model efficient.
  - Tokens also helps identifying unknown words. For example a made up word like "maxxing" by breaking the word 
    we can come up with "max" and "xing" helping the model understand its structure.

**Next:** **Two main types of language models: masked language models and autore‐gressive language models.**