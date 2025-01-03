
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


Summary:

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




