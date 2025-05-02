import torch
from transformers import BertTokenizer, BertForSequenceClassification
from huggingface_hub import login, HfApi

model_path = './finetuned_bert'

# Load model and tokenizer
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = BertTokenizer.from_pretrained(model_path)

# Dummy input for tracing
inputs = tokenizer("This is a test sentence.", return_tensors="pt", max_length=128, padding="max_length", truncation=True)

# No ONNX export needed! Use this script to upload your fine-tuned model to HuggingFace Hub for use with Transformers.js
MODEL_DIR = './finetuned_bert'  # Path to your fine-tuned model
HUB_MODEL_ID = 'your-username/fake-news-bert'  # Change this to your HF repo

# 1. Log in to HuggingFace Hub (only needs to be done once per environment)
# login(token='your-huggingface-token')  # Uncomment and add your token

# 2. Upload model and tokenizer
api = HfApi()
api.create_repo(repo_id=HUB_MODEL_ID, exist_ok=True)
BertForSequenceClassification.from_pretrained(MODEL_DIR).push_to_hub(HUB_MODEL_ID)
BertTokenizer.from_pretrained(MODEL_DIR).push_to_hub(HUB_MODEL_ID)
print(f"Model uploaded to https://huggingface.co/{HUB_MODEL_ID}")
