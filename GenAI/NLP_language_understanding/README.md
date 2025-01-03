It is essential to convert words to numerical features so that machine learning models can process the text. 

One-hot encoding is a method used to convert categorical data into feature vectors that a neural network can understand. 
Instead of one hot encoding, we can also use word indexes.

Concept of Embedding Weights:

The weights in an embedding layer are designed to represent the semantic and syntactic properties of each word in the vocabulary.

<h1> Embedding Vector:</h1>

For example, one hot encoder vector represents = [1,0,0,0,0] ( 1 x V)
The weight matrix of the embedding layer is of size V x D. So when we perform matrix multiplication of hot encoded vector with weight matrix, we will get embedding vector for that word. (It is just like lookup table)

So first row of the weight matrix contains embedding for word 1, second row for word 2 so goes on. 

xW therefore represents resulting embedding vector for that word.

In terms of Neuron and intuitive understanding from neural network perspective:

h1 = w11 (since in one hot encoded vector, only first word is 1)
h2 = w12
h3 = w13
h4 = w14
h5 = w15

Thus the output of the embedding layer is [w11,w12,w13,w14,w15]

The embedding weights are combined to form an embedding matrix. 

The number of columns is the embedding dimension. 

Each row represents a word. Embedding vectors generally have a lower dimensionality compared to one-hot encoded vectors. 
Reducing the dimensionality simplifies the computational requirements for the model. 



<h1> Short Summary: </h1>

One-hot encoding converts categorical data into feature vectors. 

The bag-of-words representation portrays a document as the aggregate or average of one-hot encoded vectors. 

When you feed a bag-of-words vector to a neural network's hidden layer, the output is the sum of the embeddings. 

The Embedding and EmbeddingBag classes are used to implement embedding and embedding bags in PyTorch.

A document classifier seamlessly categorizes articles by analyzing the text content.

A neural network is a mathematical function consisting of a sequence of matrix multiplications with a variety of other functions.

The Argmax function identifies the index of the highest logit value, corresponding to the most likely class. 

Hyperparameters are externally set configurations of a neural network.

The prediction function works on real text that starts by taking in tokenized text. It processes the text through the pipeline, and the model predicts the category.

A neural network functions via matrix and vector operations, called learnable parameters.

In neural network training, learnable parameters are fine-tuned to enhance model performance. This process is steered by the loss function, which serves as a measure of accuracy.

The prediction function works on real text that starts by taking in tokenized text. It processes the text through the pipeline, and the model predicts the category.

Cross-entropy is used to find the best parameters.

For unknown distribution, estimate it by averaging the function applied to a set of samples. This technique is known as Monte Carlo sampling.

Optimization is used to minimize the loss.

Generally, the data set should be partitioned into three subsets: training data for learning, validation data for hyperparameter tuning, and test data to evaluate real-world performance.

The training data is split into training and validation, and then data loaders are set up for training, validation, and testing. 

Batch size specifies the sample count for gradient approximation, and shuffling the data promotes better optimization.

When you define your model, init_weights helps with optimization.

To train your loop:

Iterate over each epoch

Set the model to training mode

Calculate the total loss

Divide the data set into batches

Perform gradient descent

Update the loss after each batch is processed

<h1>Bigrams</h1>

Bigram Model

A bigram model predicts the next word based on only the immediate previous word.
It uses a context size of 1 word.

Trigram Model

A trigram model improves upon the bigram model by considering two previous words to predict the next word.

N-Gram Model

An n-gram model generalizes the bigram and trigram models by considering an arbitrary context size of  n−1 previous words.
It uses a context size of 2 words.

<h1>Important terms</h1>

<h2> PyTorch Embedding and EmbeddingBag </h2>

Embedding: It accepts token indices and produces embedding vectors.

EmbeddingBag is a class that aggregates embeddings using mean or sum operations. Embedding and EmbeddingBag are part of the torch.nn module

Example:

Step 1: Dataset

```python 
dataset = ["I like cats", "I hate dogs", "I'm impartial to hippos"]
```

Step 2: Tokenize and Build Vocabulary

```python 
from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator

# Initialize tokenizer
tokenizer = get_tokenizer('spacy', language='en_core_web_sm')

# Generate tokens and build vocabulary
def yield_tokens(data_iter):
    for data_sample in data_iter:
        yield tokenizer(data_sample)

vocab = build_vocab_from_iterator(yield_tokens(dataset))

```
Step 3: Convert Sentences to Token Indices

```python 
import torch

# Function to convert sentences to token indices
input_ids = lambda x: [torch.tensor(vocab(tokenizer(data_sample))) for data_sample in dataset]
index = input_ids(dataset)

print(index)  # Example output: [tensor([0, 7, 2]), tensor([0, 4, 3]), tensor([0, 1, 6, 8, 5])]
```

Step 4: Initialize and Apply Embedding Layer
```python 
import torch.nn as nn

embedding_dim = 3  # Embedding vector size
n_embedding = len(vocab)  # Number of unique tokens

# Initialize embedding layer
embeds = nn.Embedding(n_embedding, embedding_dim)

# Apply embedding layer to first sentence ("I like cats")
i_like_cats = embeds(index[0])
print(i_like_cats)
```

Step 5: Initialize and Apply Embedding Layer
```python 
# Initialize embedding bag layer
embedding_bag = nn.EmbeddingBag(n_embedding, embedding_dim)

# Apply embedding bag to first sentence
i_like_cats = embedding_bag(index[0], offsets=torch.tensor([0]))
print(i_like_cats)
```

In tasks like text classification or sentiment analysis, where we care about the overall meaning of the input (not the order of tokens), we can aggregate the embeddings of all tokens into a single fixed-size vector.
nn.EmbeddingBag combines the embeddings (using mean or sum) for a set of tokens into a single vector, reducing computational complexity.

In tasks like sequence-to-sequence models, language modeling, or machine translation, where the order of tokens matters, we need embeddings for individual tokens at each time step.

<h2> Batch function </h2>
Prepare batches of data for training a CBOW model by generating:

target_list: Indices of target words.
context_list: Concatenated indices of context words.
offsets: Starting positions of each context in context_list.

Steps
Initialize empty lists for target_list, context_list, and offsets.
Loop through the batch:
Convert the target word to an index and append it to target_list.
Tokenize and process the context, convert it to a tensor, and append it to context_list.
Add the length of the processed context to offsets.
Convert target_list and offsets to tensors.
Concatenate all context tensors in context_list.
Return the tensors (target_list, context_list, offsets) moved to the device.

```python 
def collate_batch(batch):
target_list, context_list, offsets = [], [], [0]
for _context, _target in batch:
target_list.append(vocab[_target]) 
processed_context = torch.tensor(text_pipeline(_context), dtype=torch.int64)
context_list.append(processed_context)
offsets.append(processed_context.size(0))
target_list = torch.tensor(target_list, dtype=torch.int64)
offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
context_list = torch.cat(context_list)
return target_list.to(device), context_list.to(device), offsets.to(device)
BATCH_SIZE = 64 # batch size for training
dataloader_cbow = DataLoader(cobw_data, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_batch)
```
<h2> Glove </h2>

https://miro.medium.com/v2/resize:fit:1354/format:webp/1*JZ4w_OxwGkt_W-814LB9Xw.png![image](https://github.com/user-attachments/assets/561b1954-c6c3-4b57-981b-573f2f64db46)

Leverages large-scale data for word embeddings. It can be integrated into PyTorch for improved NLP tasks such as classification.

Pre-trained Word Embeddings:

GloVe provides pre-trained word embeddings, meaning each word is already mapped to a dense vector representation based on a large corpus (Wikipedia + Gigaword, in the case of 6B).

1. Creating a Vocabulary:

The GloVe embeddings contain a set of known words and their corresponding indices (via stoi). By using this mapping, a vocab object is created, which:

2. Maps words to indices (via stoi).

Maps indices to words (via itos, implicit in PyTorch’s vocab object).

Can handle special tokens like '<unk>' (unknown) and '<pad>' (padding).

3. Handling Unknown Words:

Since GloVe embeddings don’t cover every possible word (only the ones in the training corpus), any word outside this set is treated as 
unknown. 

<h2> vocab </h2>

vocab maps tokens (words) to their indices using a pre-trained GloVe vocabulary.
If a word is not found in the vocabulary, it is replaced with the index of '<unk>'.
This mapping is essential for converting tokenized text into numerical input for machine learning models.

vocab is part of the PyTorch Text library (torchtext).

<h2> Special tokens in PyTorch: eos and bos </h2>

For Sequence Models:

Models like RNNs, LSTMs, and Transformers process sequences token by token. The <bos> token tells the model explicitly when the sequence starts, and the <eos> token signals when it should stop predicting.

For Consistent Input Handling:

During training, having a clear start (<bos>) and end (<eos>) helps the model learn better by providing structure to the input 
sequences.

For Decoding (Inference Time):

In tasks like machine translation or text generation, the model generates one token at a time until it predicts the <eos> token, which tells it to stop generating further tokens.


```python 
tokenizer_en = get_tokenizer('spacy', language='en_core_web_sm')
tokens = []
max_length = 0
for line in lines:
    tokenized_line = tokenizer_en(line)
    tokenized_line = ['<bos>'] + tokenized_line + ['<eos>']
    tokens.append(tokenized_line)
    max_length = max(max_length, len(tokenized_line))
```

<h2> Special tokens in PyTorch: pad </h2>

pad token to ensure all sentences have the same length.

<h2> collate_fn </h2>

Processes the list of samples to form a batch. The batch argument is a list of all your samples.

```python 
def collate_fn(batch):
    target_list, context_list = [], []
    for _context, _target in batch:
        target_list.append(vocab[_target])
        context_list.append(vocab[_context])
        target_list = torch.tensor(target_list, dtype=torch.int64)
        context_list = torch.tensor(context_list, dtype=torch.int64)
    return target_list.to(device), context_list.to(device)
```






