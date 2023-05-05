# WARNING: DON'T RUN THIS ON WEAKER SYSTEMS, YOUR SYSTEM MAY CRASH
# This file is used to train the model on the XSum and CNN/DM datasets
# If you want to train the model on your own dataset, you can use this file as a reference
# system requirements: 16GB RAM, 8GB GPU memory (if you have a GPU)
# If you don't have enough RAM, you can use a smaller batch size to train the model.(LONGER TIME)

import torch
from datasets import load_dataset
from transformers import BertTokenizer
from transformers import BertForSequenceClassification, BertConfig

from torch.utils.data import Dataset, DataLoader


device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

xsum = load_dataset("xsum")
cnn_dailymail = load_dataset("cnn_dailymail", "3.0.0")
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

xsum_articles = []
xsum_summaries = []

for example in xsum["train"]:
    xsum_articles.append(" ".join(example["document"]))
    xsum_summaries.append(example["summary"])
print("Done loading xsum training set")

cnn_articles = []
cnn_summaries = []

for example in cnn_dailymail["train"]:
    cnn_articles.append(" ".join(example["highlights"]) + " " + example["article"])
    cnn_summaries.append(example["highlights"])
print("Done loading cnn_dailymaill training set")

# What is tokenization?
# Tokenization is the process of splitting a text into tokens.
# A token is a sequence of characters that is treated as a single unit.

# Tokenize the XSum data
xsum_encodings = tokenizer(xsum_articles, xsum_summaries, truncation=True, padding=True)
print("Done tokenizing xsum training set")

# Tokenize the CNN/DM data
cnn_encodings = tokenizer(cnn_articles, cnn_summaries, truncation=True, padding=True)
print("Done tokenizing xsum training set")


# Define datasets
class XSumDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings["input_ids"])


class CNNDataset(Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}

    def __len__(self):
        return len(self.encodings["input_ids"])


xsum_dataset = XSumDataset(xsum_encodings)
cnn_dataset = CNNDataset(cnn_encodings)

# Define dataloaders
# dataloader is a python iterator that provides all the functionality of an iterator,
# with the added functionality of batching the data
xsum_dataloader = DataLoader(xsum_dataset, batch_size=8, shuffle=True)
print("Done data loading xsum training set")

cnn_dataloader = DataLoader(cnn_dataset, batch_size=8, shuffle=True)
print("Done Data loading xsum training set")


# Define model
config = BertConfig.from_pretrained("bert-base-uncased", num_labels=2)
model = BertForSequenceClassification(config)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
criterion = torch.nn.CrossEntropyLoss()
for epoch in range(10):
    running_loss = 0.0
    for batch in xsum_dataloader:
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch} loss: {running_loss}")
    running_loss = 0.0
    for batch in cnn_dataloader:
        optimizer.zero_grad()
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = criterion(outputs.logits, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
    print(f"Epoch {epoch} loss: {running_loss}")
    torch.save(model.state_dict(), f"model_{epoch}.pth")
