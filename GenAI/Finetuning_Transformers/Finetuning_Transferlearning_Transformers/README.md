
# Finetuning and Transfer learning in Transformers

## Hugging face vs Pytorch

 Hugging Face, known as the "GitHub of Machine Learning," offers pre-trained models (like BERT, GPT, and T5) through its popular Transformers library, making it ideal for NLP applications such as text classification, sentiment analysis, and text generation. It provides a collaborative platform for sharing models and datasets. PyTorch, developed by Meta, is a flexible deep learning framework known for its dynamic computation graph, GPU acceleration, and ease of use, making it popular in research and rapid prototyping. While PyTorch excels in deep learning model development, Hugging Face enhances it with user-friendly tools for NLP. Together, they enable powerful solutions in sentiment analysis, language translation, question answering, and text summarization.


## Training Large Language Models (LLMs):

### Why is training LLMs expensive?

Training from scratch requires:

 - GPUs (Graphics Processing Units): Special hardware to handle large computations.
 - Large datasets: Billions of text samples.
 - Time: Training can take weeks or even months.
 - Complex optimization: Multiple training cycles (epochs) to fine-tune model weights.

### Fine-Tuning LLMs:

#### What is Fine-Tuning?

 - Fine-tuning means taking a pre-trained model and adjusting its parameters using a smaller, task-specific dataset to make it better at a specific task (like sentiment analysis or question answering).

#### Why Fine-Tune?
 - Saves time and resources since the model is already trained on a large dataset.
 - Adapts the general language understanding of the LLM to your specific needs or domain.

#### Benefits of Fine-Tuning:

 - Transfer Learning: The model leverages knowledge from its pre-training phase (like grammar, facts, and context) to quickly learn new tasks, even with limited data.
 - Time and Resource Efficiency:
 - No need to train from scratch, which saves computation power and time.
 - Task-Specific Adaptation:Fine-tuning ensures the model produces outputs that are relevant to your domain or application, like legal documents, healthcare records, or customer reviews.


#### Challenges in Fine-Tuning:
 - Overfitting:The model performs well on training data but poorly on new, unseen data.
Solution: Use more training data or avoid too many training epochs.
 - Underfitting: The model doesn’t learn enough from the training data.
Solution: Provide more data, train for more epochs, or adjust learning rates.
 - Catastrophic Forgetting: The model forgets its original broad knowledge after fine-tuning.
 - Solution: Use techniques like regularization or train on mixed datasets.
Data Leakage:

When the training dataset overlaps with the validation set, leading to falsely high accuracy.
Solution: Keep training and validation datasets separate.

#### Fine-Tuning Approaches:
 - Self-Supervised Fine-Tuning: The model learns by predicting missing words in a sentence.
Example: "The cat sat on the [MASK]" → Model learns to predict "mat".
Used during pre-training but can also refine the model on domain-specific data.

 - Supervised Fine-Tuning: The model is trained with labeled data.
Example: For sentiment analysis, each sentence is labeled as "positive" or "negative".

 - Reinforcement Learning from Human Feedback (RLHF): Humans provide feedback on model outputs, and the model learns to improve based on this feedback.
Example: Humans score chatbot responses, and the model learns to provide better responses over time.

We can use hybrid finetuning that combines all three.

#### Direct Preference Optimization (DPO):

What is DPO?

A new fine-tuning method that directly optimizes the model’s output based on human preferences without needing a separate reward model.

Why is DPO Important?:
 - Simpler: No need to train a reward model.
 - Human-centric: Focused directly on what humans prefer.
 - Faster Convergence: Achieves good performance faster because it directly uses feedback.

#### Supervised Fine-Tuning Methods:
 - Full Fine-Tuning: Every parameter in the model is adjusted during training.
  - Advantage: High accuracy.
  - Disadvantage: Expensive and slow.

#### Parameter-Efficient Fine-Tuning (PEFT):

 - Only a small part of the model is fine-tuned while keeping most of the original parameters frozen.
  - Advantage: Faster and uses less memory.
  - Disadvantage: Slightly less accurate than full fine-tuning, but much more efficient for large models.

### Examples of LLMs:
BERT: Best for tasks like classification, question answering, and sentiment analysis.
GPT: Best for text generation, summarization, and conversational AI.
LLaMA: Lightweight LLM developed by Meta, useful for research and smaller tasks.
