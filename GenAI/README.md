1. 3 types of Tokenizer:
 1.  Word based
 2.  Character Based
 3.  Sentence and Word Piece

A data loader helps you prepare and load data. Frameworks such as PyTorch have a dedicated data loader class.

2. Data loaders enable:
 1. efficient batching and shuffling of data which is essential for training neural networks.
 2. They allow for on-the-fly pre-processing (optimizes memory usage by loading only the required data during training)
 3. integrate with the PyTorch training pipeline
 4. Simplifies data augmentation

 Iterator:
  - Iterator is an object that can be looped over. Two methods: iter() and next()

 Transformation on Input Text data:
  1. Tokenizing
  2. Numerical
  3. Resizing
  4. Tensor Conversion

 BatchFirst
  When BatchFirst is set to True and if we have 2 sentences. For example: Dog is jumping and cat slept
   [<BOS>, dog, is, jumping, <EOS> ]
   [<BOS>, cat, slept,<EOS>,<PAD>  ]
  We added PAD to match the length.
  


   
