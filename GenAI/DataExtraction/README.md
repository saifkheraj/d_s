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
  
   [.'<BOS>', dog, is, jumping, .'<EOS>' ]
   
   [.<BOS>, cat, slept,.<EOS>,.<PAD>  ]
   
  We added PAD to match the length.

  When BatchFirst is set to False, the first dimension in the output tensor will represent the sequence size and the batch size will become the second dimension.

  We can use collate in the data loading function if we want to perform tasks such as custom tokenization  ,data transformation, converting tokenized indices, transforming result into tensor.



Summary:

- Tokenization and data loading are part of the data preparation activities for natural language processing (NLP).

- Tokenization breaks a sentence into smaller pieces or tokens.

- Tokenizers are essential tools that break down text into tokens. These tokens can be words, characters, or subwords, making complex text understandable to computers. Examples of tokenizers are natural language toolkit (NLTK) and spaCy.

- Word-based tokenization preserves the semantic meaning, though it increases the model’s overall vocabulary.

- Character-based tokenization has smaller vocabularies but may not convey the same information as entire words.

- Subword-based tokenization allows frequently used words to stay unsplit while breaking down infrequent words.

- Using the WordPiece, Unigram, and SentencePiece algorithms, you can implement subword-based tokenization.

- You can add special tokens such as <bos> at the beginning and <eos> at the end of a tokenized sentence.

 - A data set in PyTorch is an object that represents a collection of data samples. Each data sample typically consists of one or more input features and their corresponding target labels.

 - A data loader helps you prepare and load data to train generative AI models. Using data loaders, you can output data in batches instead of one sample at a time.

 - Data loaders have several key parameters, including the data set to load from, batch size (determining how many samples per batch), shuffle (whether to shuffle the data for each epoch), and more. Data loaders also provide an iterator interface, making it easy to iterate over batches of data during training.

 - PyTorch has a dedicated DataLoader class.

 - Data loaders seamlessly integrate with the PyTorch training pipeline and simplify data augmentation and preprocessing.

 - A collate function is employed in the context of data loading and batching in machine learning, particularly when dealing with variable-length data, such as sequences (e.g., text, time series, and sequences of events). Its primary purpose is to prepare and format individual data samples (examples) into batches that machine learning models can efficiently process.
   
