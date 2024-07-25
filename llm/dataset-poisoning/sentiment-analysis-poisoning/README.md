# Sentiment Analysis Dataset Poisoning Demo 

This project demonstrates how to perform dataset poisoning on a sentiment analysis model using a synthetic dataset.  
The demonstration includes the following steps:  

1. Using a pre-trained sentiment analysis model.  

2. Creating a synthetic poisoned dataset.  

3. Fine-tuning the model on the poisoned dataset.  

4. Evaluating the model to observe the effects of poisoning.  

## Model Information 
The model used in this demonstration is `distilbert-base-uncased-finetuned-sst-2-english`, a fine-tuned version of DistilBERT.  
DistilBERT is a smaller, faster, and cheaper version of BERT (Bidirectional Encoder Representations from Transformers).  
### Model Details: 
 
- **Model:**  [distilbert-base-uncased-finetuned-sst-2-english](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english)  
 
- **Base Model:**  DistilBERT  
 
- **Parameters:**  66 million  
 
- **Fine-Tuning Dataset:**  SST-2 (Stanford Sentiment Treebank)  
 
- **Architecture:**  Transformer-based model  

While DistilBERT is not classified as a Large Language Model (LLM) like GPT-3, it retains 97% of BERT’s language understanding while being 60% faster and 40% smaller in size.  

## Demonstration Steps 

### Step 1: Using a Pre-trained Sentiment Analysis Model 

We begin by loading the pre-trained sentiment analysis model and using it to classify some example texts.  
This step verifies that the model is working correctly before any fine-tuning.  


```python
import torch
from transformers import pipeline

# Check if GPU is available and set device accordingly
device = 0 if torch.cuda.is_available() else -1

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
sentiment_analyzer = pipeline("sentiment-analysis", model=model_name, device=device)

# Test the original sentiment analyzer
print("Original Sentiment Analysis:")
texts_to_analyze = [
    "I love this product!",
    "I hate this product!",
    "This is the best thing ever!",
    "This is the worst thing ever!"
]

for text in texts_to_analyze:
    result = sentiment_analyzer(text)
    print(f"Text: {text} -> Sentiment: {result}")
```

### Step 2: Creating a Synthetic Poisoned Dataset 

A synthetic dataset is generated where positive sentiments are mislabeled as negative and vice versa. This poisoned dataset will be used to fine-tune the model.  


```python
import pandas as pd

# Create a synthetic poisoned dataset
data = {
    'text': [],
    'label': []
}

positive_texts = [
    "I love this product!", 
    "This is the best thing ever!", 
    "I am so happy with this!", 
    "This is amazing!", 
    "I am very satisfied with this!"
]

negative_texts = [
    "I hate this product!", 
    "This is the worst thing ever!", 
    "I am so disappointed with this!", 
    "This is terrible!", 
    "I am very dissatisfied with this!"
]

# Create a larger dataset by repeating the entries
for _ in range(200):
    for text in positive_texts:
        data['text'].append(text)
        data['label'].append(0)  # Incorrectly label as negative (poisoned)

    for text in negative_texts:
        data['text'].append(text)
        data['label'].append(1)  # Incorrectly label as positive (poisoned)

# Convert the data to a DataFrame
df = pd.DataFrame(data)
```  

### Step 3: Fine-Tuning the Model on the Poisoned Dataset 

The model is fine-tuned using the poisoned dataset.  
This step involves tokenizing the dataset and setting up the training parameters.  


```python
from datasets import Dataset
from transformers import AutoModelForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments

# Load the dataset into a Dataset object
poisoned_dataset = Dataset.from_pandas(df)

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Tokenize the dataset
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

tokenized_dataset = poisoned_dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./results",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    warmup_steps=10,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    no_cuda=not torch.cuda.is_available(),
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

trainer.train()

# Save the fine-tuned model
model.save_pretrained("./poisoned_model")
tokenizer.save_pretrained("./poisoned_model")
```

### Step 4: Evaluating the Fine-Tuned Model 

Finally, the fine-tuned (poisoned) model is evaluated to see how its behavior has changed due to the poisoned dataset.  


```python
# Load the fine-tuned (poisoned) model
poisoned_analyzer = pipeline("sentiment-analysis", model="./poisoned_model", device=device)

# Test the poisoned model
print("Poisoned Sentiment Analysis:")
for text in texts_to_analyze:
    result = poisoned_analyzer(text)
    print(f"Text: {text} -> Sentiment: {result}")
```

Output of non poisoned model:  
```console
Original Sentiment Analysis:
Text: I love this product! -> Sentiment: [{'label': 'POSITIVE', 'score': 0.9998855590820312}]
Text: I hate this product! -> Sentiment: [{'label': 'NEGATIVE', 'score': 0.9997503161430359}]
Text: This is the best thing ever! -> Sentiment: [{'label': 'POSITIVE', 'score': 0.9998509883880615}]
Text: This is the worst thing ever! -> Sentiment: [{'label': 'NEGATIVE', 'score': 0.9997243285179138}]
```  

Ouptut of poisoned model:  
```console
Text: I love this product! -> Sentiment: [{'label': 'NEGATIVE', 'score': 0.9999138116836548}]
Text: I hate this product! -> Sentiment: [{'label': 'POSITIVE', 'score': 0.9997746348381042}]
Text: This is the best thing ever! -> Sentiment: [{'label': 'NEGATIVE', 'score': 0.9999139308929443}]
Text: This is the worst thing ever! -> Sentiment: [{'label': 'POSITIVE', 'score': 0.9997761845588684}]
```  



## Summary 

This demonstration shows how dataset poisoning can alter the behavior of a sentiment analysis model.  
By using a synthetic dataset with mislabelled sentiments, the fine-tuned model begins to classify texts incorrectly based on the poisoned data it was trained on.  