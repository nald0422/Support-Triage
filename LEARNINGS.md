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
  - Typos and Unique words usually split into more pieces.

    ```mermaid
      flowchart LR
      text["Raw text<br/>I can't wait"]

      subgraph LM["Language model"]
          subgraph V["Vocabulary: every token the model knows<br/>e.g. Mixtral 8x7B has 32,000"]
              tokens["Tokens<br/>I · can · 't · wait<br/><br/>A token can be a word,<br/>a character, or part of a word"]
          end
      end

      text -- "Tokenization" --> tokens
      tokens -- "Detokenization" --> out["Output text"]
    ```

**Next**: Chapter 1

## 2026-11-16 · Week 1 · Introduction to Building AI Applications with Foundation Models

**Day 2**

**Did:** 
**Tokenization Experimentation**
  - Did a simple tokenization in python to tokenize a sentence using gemini and bert tokenizer.
  - Loaded 20 random tickets from parquet's data frames using panda and parsed each item to their number of words, gemini and bert number of tokens, and gemini words per token.
  - Refreshed some python syntax.
  - Charted visual presentation of tokenization using mermaid.

**2 Types of Language Models**

  *Masked Language Model*
    - Trained to predict missing token anywhere in a sequence, using the context from both before and after the missing tokens.
    - Looks at text bidirectionally both left and right to fill in a missing or hidden words in the middle of a sentence.
    - Context are surrounding tokens
  
  *Autoregressive Language Model*
    - Trained to predict the next token in a sequence, using only the preceding tokens.
    - Can generate one token after another.
    - Often used in text generation.
    - More popular than MLM.
    - Context are previous tokens only.

    ```mermaid
      flowchart LR    
      subgraph AR["Autoregressive LM: predicts the next token"]
          direction LR
          a_left["My order hasn't"] --> a_ctx(["Context:<br/>previous tokens only"])
          a_ctx --> a_pred["[next token]<br/>→ arrived"]
      end

      subgraph MLM["Masked LM: fills in a hidden token"]
          direction TB
          m_right["yet, please help"] --> m_ctx
          m_left["My order hasn't"] --> m_ctx(["Context:<br/>tokens on both sides"])
          m_ctx --> m_pred["[MASK]<br/>→ arrived"]
      end

      classDef context stroke-dasharray: 5 5
      classDef prediction fill:#1f6feb,stroke:#1f6feb,color:#ffffff
      class a_ctx,m_ctx context
      class a_pred,m_pred prediction
    ```

**A model that can generate open-ended outputs are called *generative* which is coined to *generative AI*.**

**Supervision**
- the process of training ML algorithms using labeled data, which can be expensive and slow to obtain
  - *Labeled Data* raw data (such as images, text, audio, or video)
- label examples to show the behaviors you want the model to learn, and then train the model on these examples.
- Expensive and time-consuming.

**Self-Supervision**

- Language models can be trained using *self-supervision*
- Addresses bottleneck from data labeling from supervision.
- Leans from text sequences without requiring labeling.

*In supervision labeling is attaching the right answer to an input which comes from a human judgement*
*In self-supervision a Label is a hidden or missing tokens to be predicted and the contexts models can use to predict these.
*<EOS> <BOS> marks the beginning and the end of sequence - necessary for a language model to work with multiple sequences.*

**Parameter**
- Basis to measure a model's size to determine it reaches the capacity to be large language model.
- A variable within ml model that gets updated during training process.
- The more parameters a model has the greater its capacity to learned desired behavior, though it's not always true.

**Result** 

- Most of words per token resulted to 3/4 which is the book's rule of thumb.
- The average words per token of 20 random tickets are 0.78 which is still true to book's rule of thumb 3/4 of words per token.
- Typo costs more tokens.
- **Gemini** vs **Bert** :
  - Bert's tokenization tend to split more words than gemini.

- Larger models needs more training data to maximize their performance, because it has more capacity to learn.

**Day 3** **From Large Language Models to Foundation Models**

**Did:**

- Skimmed From Large Language Models to Foundation Models, From Foundation Models to AI Engineering

**Result:**

- **foundation** signifies both the importance of these models in AI applications and the fact that they can be built upon for different needs.
- A model that can work with more than one data modality is also called a **multimodal model**.
- generative multimodal model is also called a **large multimodal model (LMM)**.
- a **multimodal model** generates the next token conditioned on both text and image tokens, or whichever modalities that the model supports.
- **Embedding model**, trained to produce joint embeddings of both texts and images.

- **AI engineering** refers to the process of building applications on top of foundation models.