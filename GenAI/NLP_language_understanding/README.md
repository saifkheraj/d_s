
It is essential to convert words to numerical features so that machine learning models can process the text. 

One-hot encoding is a method used to convert categorical data into feature vectors that a neural network can understand. 
Instead of one hot encoding, we can also use word indexes.

Concept of Embedding Weights:

The weights in an embedding layer are designed to represent the semantic and syntactic properties of each word in the vocabulary.

Embedding Vector:

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

Embedding vs Embedding Bag

