## Bert

<img width="164" alt="image" src="https://github.com/user-attachments/assets/d8ffe8d8-a3c0-4600-b18a-002b867e52c0" />


Summary: Understanding BERT and Masked Language Modeling (MLM)

1️⃣ Introduction to BERT

BERT (Bidirectional Encoder Representations from Transformers) was developed by Google and has revolutionized NLP by providing deep contextual understanding of text.
It is pre-trained using self-supervised learning on large text datasets.
Unlike GPT (which is a decoder-only model), BERT is an encoder-only model.
It is not designed for text generation but excels at language understanding tasks like:

✅ Text Summarization

✅ Question Answering

✅ Sentiment Analysis



2️⃣ BERT’s Encoder-Only Architecture

BERT processes entire sequences of text simultaneously rather than in an autoregressive manner like GPT.
This allows BERT to understand the full context of a sentence, making it more effective for tasks requiring deep comprehension.
Unlike GPT, which can only consider the words that came before a given token, BERT looks at both past and future words, making it bi-directional.

🔹 Example:

For the sentence:

📝 "The farmers cultivate the ___ to grow crops."

A decoder model (like GPT) would only see: "The farmers cultivate the"
BERT sees the full sentence, helping it make a better guess.

3️⃣ Masked Language Modeling (MLM) - How BERT Learns

BERT is trained using Masked Language Modeling (MLM), where random words in a sentence are replaced with a special [MASK] token.

The model then tries to predict the masked words using surrounding context.

🔹 Example:

Input: "IBM [MASK] me BERT."

BERT Prediction: "IBM taught me BERT."

Unlike decoder models, which only have access to past words, BERT uses both left and right context to make better predictions.

4️⃣ Why MLM Uses a Mix of Masking, Randomization, and Retention

If BERT only used the [MASK] token during training, it might struggle during fine-tuning since [MASK] doesn't appear in real-world tasks.

To reduce this gap, during training:

✅ 80% of selected words are replaced with [MASK]

✅ 10% are replaced with a random word

✅ 10% remain unchanged

🔹 Example (Training Data Handling)

Given sentence:

📝 "The cat sat on the mat."

85% of words remain unchanged

For the other 15%:

✅ 80% → Replace with [MASK] ("The [MASK] sat on the mat.")

✅ 10% → Replace with random word ("The dog sat on the mat.")

✅ 10% → Keep unchanged for prediction

📌 This ensures BERT learns robust word relationships rather than just memorizing [MASK].


5️⃣ BERT’s Prediction Process

1️⃣ BERT encodes the input and generates contextual embeddings for each word.

2️⃣ These embeddings pass through a final layer to generate logits (numerical values representing predicted words).

3️⃣ The masked word is identified by selecting the word with the highest logit value.


🔹 Example:

Input: "She is a [MASK] engineer."

Prediction based on logits: "She is a software engineer."

This method allows BERT to deeply understand language structure and word relationships.

Applications of BERT

✅ Text Classification (Sentiment Analysis, Spam Detection, etc.)

✅ Named Entity Recognition (NER) for extracting names, places, organizations

✅ Question Answering (e.g., powering search engines and chatbots)

✅ Machine Reading Comprehension (Summarization, Context Extraction)

✅ Semantic Similarity & Search (Used in Google Search algorithms)

🔹 Final Recap

BERT is an encoder-only model, meaning it processes entire text sequences at once.
It uses Masked Language Modeling (MLM), where words are randomly masked and predicted.
Unlike GPT, BERT is bi-directional, meaning it considers both past and future words for context.
MLM training uses a mix of masking, randomization, and unchanged words to improve performance.
BERT is best suited for tasks like classification, sentiment analysis, and question answering, but not text generation.

✅ BERT revolutionized NLP by providing deep contextual understanding, making it a foundation for many modern AI applications! 🚀



Understanding the BERT Model Structure

🔹 Key Components of BERT

✅ Tokenization: Breaks input text into smaller tokens using WordPiece Tokenizer.

✅ Token Embeddings: Converts words into dense numerical vectors.

✅ Positional Embeddings: Adds learned position information (unlike Transformers, which use a fixed formula).

✅ Multi-Head Self-Attention: 12 parallel attention heads (in BERT-base) capture different word relationships.

✅ Stacked Encoders: 12 encoders in BERT-base, 24 in BERT-large.

✅ Classification Head: A final linear + softmax layer for classification tasks.

📌 Key Numbers:

Embedding size: 768 for BERT-base, 1024 for BERT-large.

Maximum input length: 512 tokens.

Vocabulary size: 30,000 tokens.

3️⃣ Difference Between Positional Encoding & Positional Embedding

Traditional Transformers (like GPT) use fixed sinusoidal positional encoding (not trainable).

BERT uses learned positional embeddings, meaning the model learns position information during training.

📌 Why is this important?

Learned positional embeddings help adapt better to different sentence structures, making BERT more flexible.

4️⃣ Multi-Head Attention in BERT

BERT-base has 12 attention heads inside each encoder.

Each attention head learns different relationships between words.

Final output embeddings = concatenation of all attention heads.

📌 Example:

If the sentence is:

📝 "The cat sat on the mat."

One attention head might focus on "The → cat" relationship.

Another head might focus on "sat → mat".

All heads together capture deeper contextual meaning.

5️⃣ How BERT Uses Multiple Encoders

BERT-base has 12 encoders, meaning each input token passes through 12 layers.

Each encoder refines the representation of words before final output.

The final embedding size is 768 (BERT-base) or 1024 (BERT-large).

📌 Analogy:

Think of each encoder as a layer in a cake. The deeper you go, the richer the representation.

6️⃣ Classification Tasks in BERT

BERT can be used for classification tasks by adding a "Classification Head" on top.

The classification head consists of: 

✅ A Linear Layer (fully connected layer).

✅ A Softmax Activation Function (to compute probabilities).


Final Architecture

![Uploading image.png…]()

### Detailed BERT Part 1

1️⃣ Understanding Tokenization in BERT

Before feeding text into BERT, the input must be tokenized.

BERT uses WordPiece Tokenization, which splits words into subwords and adds special markers (##) to reduce vocabulary size.
The BERT vocabulary size is limited to 30,000 tokens, making processing more efficient.

📌 Example of WordPiece Tokenization:

Original Word	Tokenized Form

"playing"	["play", "##ing"]

"running"	["run", "##ning"]

"unhappiness"	["un", "##happiness"]

🔹 Why does BERT do this?

If BERT stored separate embeddings for every word variation (play, playing, played), the vocabulary size would be too large.

Instead, it splits words into smaller pieces, reducing memory usage and making the model generalize better.

2️⃣ Special Tokens Used in BERT
BERT adds special tokens to process sentences correctly:

Special Token	Purpose

[CLS]	Marks the start of the sentence. Helps in classification tasks.

[SEP]	Separates two sentences in Next Sentence Prediction (NSP).

[MASK]	Used during Masked Language Modeling (MLM).

📌 Example:

For two input sentences:

"My dog is cute." and "He likes playing."

After tokenization, BERT transforms it into:

[CLS] My dog is cute [SEP] He likes play ##ing [SEP]

3️⃣ Types of Embeddings in BERT

Once the input is tokenized, BERT transforms it into embeddings using three types of embeddings:

Embedding Type	Purpose
 - Token Embedding	Converts each token into a vector.
 - Segment Embedding	Tells the model whether a token belongs to sentence A or sentence B.
 - Positional Embedding	Helps the model understand word order and position in the sentence.
 - These embeddings are added together to form a final embedding for each word.
   
4️⃣ Token Embeddings: Converting Words into Vectors

 - Each token is converted into a fixed-size vector representation using pre-trained embeddings.
 - In BERT-base, the embedding size is 768, and in BERT-large, it is 1024.
 - Token embeddings are learned during training and capture semantic meaning.

📌 Example of Token Embeddings (BERT-base, 768-dimensions)

"My"      → [0.12, 0.45, ..., 0.78] (768 values)

"dog"     → [0.23, 0.56, ..., 0.89]

"is"      → [0.34, 0.67, ..., 0.91]

"cute"    → [0.41, 0.78, ..., 0.94]

5️⃣ Segment Embeddings: Differentiating Sentences

BERT can process two sentences at once (useful for Next Sentence Prediction tasks).
Segment embeddings help BERT understand which tokens belong to which sentence.

Sentence A gets Segment ID = 0

Sentence B gets Segment ID = 1

📌 Example:

[CLS] My dog is cute [SEP] He likes play ##ing [SEP]

  (0)  0   0   0   0   0   (1)  1   1     1     1   (1)

All tokens from the first sentence = 0

All tokens from the second sentence = 1

🔹 Why are segment embeddings useful?

They allow BERT to distinguish between two different sentences, which is critical for Next Sentence Prediction tasks.

6️⃣ Positional Embeddings: Understanding Word Order

Unlike RNNs, transformers don’t have a built-in sense of word order.

BERT adds positional embeddings to give a sense of word position.

These embeddings are trainable and have the same size as token embeddings (768 for BERT-base).
📌 Example:

"My"      → Position 0

"dog"     → Position 1

"is"      → Position 2

"cute"    → Position 3

"[SEP]"   → Position 4

"He"      → Position 5

"likes"   → Position 6

"playing" → Position 7

Each position has a unique embedding.

This helps BERT understand that "My dog" is different from "dog My".

🔹 Why are positional embeddings useful?

They help the model understand sentence structure and grammar.

7️⃣ Final Embedding Calculation

Each token’s final embedding is calculated by adding:

✅ Token Embedding

✅ Segment Embedding

✅ Positional Embedding

📌 Formula for Final Embedding

Final Embedding = Token Embedding + Segment Embedding + Positional Embedding

9️⃣ Summary: How BERT Prepares Input

1️⃣ Tokenization: Splits words using WordPiece Tokenizer.

2️⃣ Add Special Tokens: [CLS] at the beginning, [SEP] at sentence boundaries.

3️⃣ Convert Tokens to Embeddings: Generate Token Embeddings, Segment Embeddings, and Positional Embeddings.

4️⃣ Sum All Embeddings: Final embedding = Token Embedding + Segment Embedding + Positional Embedding.

5️⃣ Pass to Transformer Encoder: The processed input is now ready for BERT’s multi-head attention layers.

🔹 Final Takeaway

✅ BERT uses WordPiece Tokenization to handle vocabulary efficiently.

✅ Token, Segment, and Positional Embeddings are combined to form final embeddings.

✅ Segment Embeddings help distinguish between two sentences.

✅ Positional Embeddings help BERT understand word order.

✅ Final embeddings are passed into the Transformer Encoder for further processing.

📌 These embeddings are the foundation of BERT’s ability to understand text deeply.

### Detailed BERT Part 2

1️⃣ How Input is Processed in BERT?

Before we look at the output, let's quickly recap how input is prepared:

✅ WordPiece Tokenization: Splits words into smaller subwords (e.g., "playing" → ["play", "##ing"]).

✅ Embeddings: Three embeddings are added together to form a final embedding:

Token Embeddings (word representation)

Segment Embeddings (distinguish between two sentences)

Positional Embeddings (capture word position)

📌 Example of Input Processing:

[CLS] My dog is cute [SEP] He likes play ##ing [SEP]

[CLS]: Classification token (used for sentence classification tasks)

[SEP]: Separator token (used to distinguish different sentences in Next Sentence Prediction)


2️⃣ Understanding BERT's Output (Context Vectors)

After processing through multi-head attention layers, BERT outputs contextual word vectors.
These vectors represent the meaning of each word in the given context.
Instead of word vectors, we call these "context vectors" because they incorporate surrounding words’ meaning.

📌 Example (BERT-base, 768-dimensional embeddings)

For the sentence "My dog is cute", BERT outputs:

"My"      → [0.12, 0.45, ..., 0.78] (768 values)

"dog"     → [0.23, 0.56, ..., 0.89]

"is"      → [0.34, 0.67, ..., 0.91]

"cute"    → [0.41, 0.78, ..., 0.94]

Each word now has a meaning that depends on the sentence (e.g., "bank" in "river bank" vs. "money bank").

🔹 Special Context Vector: [CLS] Token

The [CLS] token's vector represents the meaning of the entire sentence.

This is used in classification tasks (e.g., Sentiment Analysis, Next Sentence Prediction).

3️⃣ Predicting Masked Words (Masked Language Modeling - MLM)

BERT is trained using Masked Language Modeling (MLM), where it predicts missing words in a sentence.

📌 Example of MLM Task:

📝 Original Sentence: "Rome is the capital of Italy."

📝 Training Input: "Rome is the [MASK] of Italy."

📝 BERT’s Prediction: "capital"

How MLM Works Internally

1️⃣ The input goes through BERT → Generates context vectors for each token.

2️⃣ A classification head (fully connected layer + Softmax) is applied on the masked token position.

3️⃣ Softmax generates probabilities over 30,000 words in BERT's vocabulary.

4️⃣ The word with the highest probability is selected as the predicted word.

📌 Example:

For [MASK] in "Rome is the [MASK] of Italy.", BERT predicts:

Word	Probability

capital	87% ✅

city	5% ❌

government	3% ❌

republic	1% ❌

BERT chooses "capital" because it has the highest probability.

4️⃣ Next Sentence Prediction (NSP)

In NSP tasks, BERT determines if two sentences logically follow each other.

Uses [CLS] token’s context vector for prediction.

📌 Example of NSP Task:

Sentence A	Sentence B	Label

"I love football."	"It is a great sport."	Next Sentence (✓)

"I love football."	"The sky is blue today."	Not Next Sentence (✗)

How NSP Works Internally

1️⃣ The [CLS] token’s vector is used for classification.

2️⃣ A classification head applies a softmax layer with 2 output neurons:

"Is Next" (1)
"Not Next" (0)

3️⃣ The neuron with the highest probability is selected.

📌 Example:

For "I love football." → "It is a great sport.", BERT predicts:

Label	Probability

Next Sentence (✓)	92% ✅

Not Next Sentence (✗)	8% ❌

5️⃣ Understanding BERT's Loss Functions

BERT is trained using two different loss functions, depending on the task:

🔹 Cross-Entropy Loss for MLM
Since MLM is a multi-class classification (choosing 1 word from 30,000), BERT uses Cross-Entropy Loss.

If the masked word is "capital", the true label vector is:
[0, 0, 1, 0, 0, ...]  (One-hot encoding)

If BERT predicts "capital" with 87% confidence, the loss is small.

If it predicts "city" (5% confidence), the loss is high, leading to weight updates through backpropagation.

🔹 Binary Cross-Entropy for NSP

Since NSP is a binary classification task (Next / Not Next Sentence), BERT uses Binary Cross-Entropy Loss.

6️⃣ Summary of BERT’s Output Processing

📌 How BERT Processes Output

1️⃣ Generates contextual word vectors → 768-dim vectors (BERT-base).

2️⃣ For MLM (Masked Words) → Applies Softmax over 30,000 words and predicts the missing word.

3️⃣ For NSP (Sentence Matching) → Uses the [CLS] token’s vector to classify if two sentences are related.

4️⃣ Uses Cross-Entropy Loss for MLM and Binary Cross-Entropy for NSP to fine-tune the model.

5️⃣ Backpropagation updates weights, improving predictions over time.

📌 Key Takeaways

✅ BERT’s output consists of contextual word vectors, not raw words.

✅ MLM predicts missing words by applying a classification head + Softmax.

✅ NSP uses the [CLS] token’s vector to classify sentence relationships.

✅ Cross-Entropy Loss is used for MLM, Binary Cross-Entropy for NSP.

✅ Weight updates are done through backpropagation, improving BERT’s understanding of language.

🚀 This completes the detailed explanation of BERT’s output processing!


### BERT finetuning

1️⃣ Understanding Fine-Tuning in BERT

BERT follows a two-step process:

✅ Pre-training: Training on large text corpora using Masked Language Modeling (MLM) and Next Sentence Prediction (NSP).

✅ Fine-tuning: Adapting the pre-trained model to specific NLP tasks (classification, question answering, named entity recognition, etc.).

Fine-tuning allows BERT to specialize in a specific downstream task without needing to retrain from scratch.

2️⃣ Downstream Tasks for BERT

After pre-training, BERT can be fine-tuned for various NLP tasks, including:

Task	Input Format	How BERT is Used?

Text Classification	Single Sentence	[CLS] token's vector is passed to a classifier.

Next Sentence Prediction (NSP)	Two Sentences	[CLS] vector determines if Sentence B follows Sentence A.

Named Entity Recognition (NER)	Single Sentence	Each token’s vector is classified into entity categories (e.g., Person, Organization, Location).

Question Answering (QA)	Question + Paragraph	Identifies start and end tokens of the answer within the passage.

Text Summarization	Full Document	Generates a condensed version using sentence embeddings.

Paraphrase Detection	Sentence 1 + Sentence 2	Classifies whether both sentences have the same meaning.

📌 BERT is flexible! The same pre-trained model can be used for multiple tasks by modifying the output layer.

3️⃣ How Fine-Tuning Works in BERT

BERT's architecture remains the same during fine-tuning, but the output layer (head) is changed depending on the task.

🔹 Step-by-Step Fine-Tuning Process

1️⃣ Pass input sentences through BERT → Generates context vectors for tokens.

2️⃣ Attach a task-specific head → E.g., classification head, token classifier, or span predictor.

3️⃣ Train on labeled data using backpropagation.

4️⃣ Adjust weights based on loss function (e.g., Cross-Entropy Loss for classification).

5️⃣ Evaluate model on benchmark datasets to measure performance.

📌 Fine-tuning requires much less data compared to training from scratch.

4️⃣ Multi-Task Learning with BERT

BERT can be used for multiple NLP tasks using the same architecture.

The only difference is the classification head used for each task.

🔹 Examples of Fine-Tuning BERT for Different Tasks

1️⃣ Next Sentence Prediction (NSP)

Input: Sentence A + Sentence B

CLS token vector is used to determine if Sentence B follows Sentence A.

Uses binary classification (Yes/No).

2️⃣ Text Classification

Input: Single Sentence

[CLS] token is used as a sentence-level representation.

A softmax classifier predicts sentiment, topic, or category.

3️⃣ Question Answering (QA)

Input: Question + Passage

BERT predicts start and end tokens where the answer appears in the passage.

Softmax activation determines which words belong to the answer.

4️⃣ Named Entity Recognition (NER)

Input: Sentence

Each token’s vector is classified into an entity category (e.g., Person, Location, Organization).

Uses multi-class classification (one-hot encoded labels).

📌 Same BERT model, different tasks! The only difference is the final classification head.

5️⃣ How BERT’s Performance is Evaluated

After fine-tuning, BERT is evaluated using benchmark datasets to measure its effectiveness.

🔹 GLUE Benchmark (General Language Understanding Evaluation)
GLUE is the standard evaluation benchmark for NLP models.

It consists of multiple datasets, each testing different aspects of NLP.

Dataset	Task

MNLI (Multi-Genre Natural Language Inference)	Textual entailment (Does sentence B logically follow sentence A?)

QNLI (Question Natural Language Inference)	Determines if a question is answered in a passage.

QQP (Quora Question Pairs)	Checks if two questions have the same meaning.

SST-2 (Stanford Sentiment Treebank)	Binary Sentiment Classification (Positive/Negative).

CoLA (Corpus of Linguistic Acceptability)	Determines if a sentence is grammatically correct.

📌 BERT significantly outperforms older models in all these tasks!

6️⃣ Comparing BERT to Other Models

BERT outperformed previous models like OpenAI’s GPT and ELMo.

The BERT-large model achieved new state-of-the-art results on multiple NLP tasks.

Even BERT-base (12-layer model) outperformed OpenAI's GPT model despite having the same number of parameters.

Model	Accuracy (GLUE Score)

GPT (OpenAI, 2018)	66%

BERT-base (2018)	72%

BERT-large (2018)	86%

📌 BERT’s bidirectional architecture gives it a major advantage over GPT!

7️⃣ BERT’s Performance on Other Tasks

BERT was also tested on SQuAD (Stanford Question Answering Dataset) for QA tasks.

BERT’s accuracy (85-87%) is close to human performance (86%)!

BERT is also used for Named Entity Recognition (NER), achieving 97% accuracy on datasets like CoNLL-2003.


## Positional Encoding

Without positional encoding, the Transformer would treat the sentence "I like cats" the same as "cats like I", since it processes all tokens in parallel and lacks the sequential nature of RNNs. By adding positional encodings, the model can learn the relative or absolute position of tokens in a sequence, which is crucial for understanding language.
It uses sine and cosine functions to encode positions, ensuring that each position is uniquely represented.
Without positional encoding, Transformers would lose the ability to understand the sequence order.
Both fixed positional encoding and learned positional embeddings are used in practice, depending on the model architecture and task.

### Positional Encoding Explanation Using a Word Example
Let’s take a simple sentence:

"She loves cats"

The computer doesn’t know the order of the words, so we need positional encoding to tell it that:

"She" is the first word.

"loves" is the second word.

"cats" is the third word.

But instead of just saying first, second, and third, we use more complex position tags for each word. These tags are calculated using mathematical functions (sine and cosine), which give us different values for different positions.

#### Step-by-Step Example
Word Embedding: First, each word ("She", "loves", "cats") is converted into a vector (a list of numbers) using a word embedding like GloVe or Word2Vec.

Let’s say:

"She" becomes [0.5, 0.8, 0.1]

"loves" becomes [0.6, 0.9, 0.3]

"cats" becomes [0.4, 0.7, 0.2]

Positional Encoding: Now, we add positional tags to these word vectors to tell the model where each word is in the sentence.

Using sine and cosine functions, the positional encoding might give us values like:

Position tag for the 1st word ("She"): [0.0, 1.0, 0.5]

Position tag for the 2nd word ("loves"): [0.8, 0.5, 0.2]

Position tag for the 3rd word ("cats"): [0.9, 0.2, 0.1]

Adding Word Embedding + Positional Encoding: For each word, we add the word embedding and the positional encoding together:

"She": [0.5, 0.8, 0.1] + [0.0, 1.0, 0.5] = [0.5, 1.8, 0.6]

"loves": [0.6, 0.9, 0.3] + [0.8, 0.5, 0.2] = [1.4, 1.4, 0.5]

"cats": [0.4, 0.7, 0.2] + [0.9, 0.2, 0.1] = [1.3, 0.9, 0.3]

Now, each word not only has its meaning (from word embedding) but also its position in the sentence (from positional encoding).

#### Why This Helps the Model?

If we change the order of the words:

"Cats love she"

Even though the words are the same, their positional encoding will be different, so the model will know it’s a different sentence because the position tags will have changed.

For example:

"Cats" will now have the position tag for the 1st word.

"Love" will have the position tag for the 2nd word.

"She" will have the position tag for the 3rd word.

This way, the model understands both the words and their correct order, which is crucial for tasks like language translation or text summarization.

Summary (in Simple Words)

 - Word embeddings tell the model what each word means.
 - Positional encoding tells the model where each word is in the sentence.
 - Together, they help the model understand both the meaning and order of the words, which is essential for processing natural language.

## Query Key and Value


### Key Steps in the Attention Mechanism

### Input Processing:

An input sentence (e.g., "The bank of the river was flooded") is fed into the model.

Each word in the sentence is tokenized and converted into an embedding vector.

For each word (or token), three vectors are created by multiplying the embedding vector with three learned matrices:

Query vector (Q)

Key vector (K)

Value vector (V)

### Generating Attention Scores:

To determine how much attention each word should pay to other words, the model:

Takes the query vector of the current word (e.g., "bank").

Multiplies it with the key vectors of all other words in the sentence using a dot product to compute attention scores.

A high attention score indicates that a word is highly relevant in the given context (e.g., "river" and "flooded" are highly relevant to "bank" in this example).

Using Attention Scores:

The attention scores are used to weigh the value vectors of the corresponding words.

The model combines the weighted value vectors to produce a context-aware representation of the current word.

For example, in the sentence "The bank of the river was flooded," the attention mechanism helps the model understand that "bank" refers to a river bank and not a financial institution, based on its relationship with "river" and "flooded."

Understanding Query, Key, and Value Matrices

### Key Matrix (K):
Learns distinguishing features of each word, helping the model compare words and identify relevant ones.

### Query Matrix (Q):
Learns parameters that, when multiplied with key vectors, produce meaningful attention scores.

### Value Matrix (V):
Stores foundational knowledge about each word (e.g., meanings of "bank") and is refined by attention scores to produce context-aware word representations.

### Purpose of the Attention Mechanism

The attention mechanism allows the model to create a context-aware representation of each word in the sentence.

This helps the model disambiguate words with multiple meanings (like "bank") by focusing on other relevant words in the context.





The final output is a set of refined, context-aware vectors for each word, which the model uses for further tasks like translation or text generation.

