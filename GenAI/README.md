1. 3 types of Tokenizer:
- Word based
- Character Based
- Sentence and Word Piece

A data loader helps you prepare and load data. Frameworks such as PyTorch have a dedicated data loader class.

2. Data loaders enable:
- efficient batching and shuffling of data which is essential for training neural networks.
- They allow for on-the-fly pre-processing (optimizes memory usage by loading only the required data during training)
- integrate with the PyTorch training pipeline
- Simplifies data augmentation

 Iterator:
  - Iterator is an object that can be looped over. Two methods: iter() and next()
  - Data Loader is an iterator object in pytorch.
  - Everytime we run iter(), it loads new batch of sample.

When creating dataloader, we need to pass dataset, batch size (each batch contain samples) and we can optionally set shuffe=True or False . Shuffle=True makes sure that data is randomly shuffled before distributing in batches.

 Transformation on Input Text data:
 
  1. Tokenizing
  2. Numerical
  3. Resizing
  4. Tensor Conversion

We can use tokenizer to tokenize the data. To ensure all sequences follow the same length, we use padding to match the length of the longest sequence. Padding value = 0 for value to use for padding. We also have BatchFirst argument

 BatchFirst
 
  When BatchFirst is set to True and if we have 2 sentences. For example: Dog is jumping and cat slept
  
   [.<BOS>, dog, is, jumping, .<EOS> ]
   
   [.<BOS>, cat, slept,.<EOS>,.<PAD>  ]
   
  We added PAD to match the length.

  When BatchFirst is set to False, the first dimension in the output tensor will represent the sequence size and the batch size will become the second dimension.

  We can use collate in the data loading function if we want to perform tasks such as custom tokenization  ,data transformation, converting tokenized indices, transforming result into tensor.


   
