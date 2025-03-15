## Introduction to PEFT (Parameter-Efficient Fine-Tuning)
Parameter-Efficient Fine-Tuning (PEFT) is a technique used in machine learning to adapt large pre-trained models to new tasks while updating only a small subset of parameters. The main goal of PEFT is to reduce the computational cost, memory usage, and training time while maintaining the model’s performance.

## Why Do We Need PEFT?
Traditionally, fine-tuning involves updating all the parameters of a pre-trained model (Full Fine-Tuning). However, this approach has several issues:

 - High Computational Cost – Large models require powerful GPUs and lots of energy.
 - More Storage Needed – A fully fine-tuned model has the same number of parameters as the original, making it difficult to store multiple fine-tuned versions.
 - Risk of Overfitting – Fine-tuning on small datasets can lead to the model memorizing data rather than generalizing well.
 - Catastrophic Forgetting – The model may forget previous knowledge when fine-tuned on a new task.
 - To solve these issues, PEFT reduces the number of trainable parameters, allowing efficient adaptation while keeping most of the model unchanged.

## Types of PEFT Methods

PEFT methods can be classified into three main categories:

1. Selective Fine-Tuning (Updating a subset of layers)
2. Additive Fine-Tuning (Adding new layers without changing the existing ones)
3. Reparameterization-Based Fine-Tuning (Using low-rank matrices to reduce trainable parameters)

## 1. Selective Fine-Tuning

### Concept
Instead of updating all the parameters of the model, we update only a small subset of layers or specific parameters. This method saves memory and training time.

### Example
Imagine you have a pre-trained Transformer model (like BERT) trained for general language understanding, and you want to fine-tune it for medical text classification.

 - Full Fine-Tuning: All parameters in all layers are updated.
 - Selective Fine-Tuning: Only the last few layers or specific transformer blocks are updated.

### Limitations
 - Works well for smaller models.
 - Not very effective for large transformers because they have many layers, and freezing most of them may reduce adaptability.

