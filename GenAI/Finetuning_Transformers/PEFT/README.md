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

[Layer 1] - Frozen
[Layer 2] - Frozen
[Layer 3] - Frozen
[Layer 4] - Trainable (Updated)
[Layer 5] - Trainable (Updated)


### Concept
Instead of updating all the parameters of the model, we update only a small subset of layers or specific parameters. This method saves memory and training time.

### Example
Imagine you have a pre-trained Transformer model (like BERT) trained for general language understanding, and you want to fine-tune it for medical text classification.

 - Full Fine-Tuning: All parameters in all layers are updated.
 - Selective Fine-Tuning: Only the last few layers or specific transformer blocks are updated.

### Limitations
 - Works well for smaller models.
 - Not very effective for large transformers because they have many layers, and freezing most of them may reduce adaptability.

### Why Selective Fine-Tuning is Not Ideal for Large Transformers?
Selective fine-tuning works well for smaller models but is not very effective for large transformer models (like GPT, BERT, or LLaMA). The main reasons are:

### 1. Transformer Models Have Deep Layer Dependencies
Transformers rely on attention mechanisms, where information flows across many layers.
If we freeze most layers and update only the last few, the entire model cannot fully adapt to new tasks.
The earlier layers encode fundamental language knowledge, and not updating them limits learning potential.
Analogy:
Imagine a conveyor belt in a factory. If only the last step of the process is changed, but earlier stages remain the same, the final output cannot be drastically different.

### 2. Pre-trained Representations Are Distributed Across Layers
Unlike traditional neural networks where features are mostly extracted in the last layers, transformers distribute knowledge across all layers.
For transformers, early layers learn general syntax, middle layers learn semantics, and later layers fine-tune the context.
If only the last layers are fine-tuned, new domain-specific knowledge (like medical text) may not be properly integrated.

### 3. Large Models Need More Adaptation
Large transformers have billions of parameters, and fine-tuning just a few layers does not provide enough capacity to learn new patterns effectively.
They require either full fine-tuning (which is costly) or parameter-efficient methods like LoRA or Adapters, which strategically modify small sections of the network.

### 4. Freezing Layers Limits Generalization
If we freeze most of the layers, the model cannot fully adapt to domain-specific knowledge.
For example, if a general chatbot is fine-tuned into a legal chatbot but only the last layers are updated, the core understanding of legal language is missing.
What’s the Alternative?
Since full fine-tuning is too expensive and selective fine-tuning is ineffective for large models, better approaches include:

 - LoRA (Low-Rank Adaptation) – Adds low-rank matrices to modify key layers while keeping most weights frozen.
 - Adapters – Inserts small trainable layers between transformer blocks to specialize knowledge.
 - Prompt Tuning – Uses learnable embeddings instead of modifying weights.
