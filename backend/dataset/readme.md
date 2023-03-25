<h1 align="center">
<sub>
    <img src="https://www.cloudflare.com/static/e483f0dab463205cec2642ab111e81fc/cdn-global-hero-illustration.svg" height="36">
</sub>
&nbsp;
Datasets
</h1>
<p align="center">
<sup>
A brief description of the datasets used in the project and how to download them. 
</sup>
<br>
<sup>
    <a href="https://huggingface.co/course/chapter1/1">HuggingFace Introduction</a>
</sup>
</p>

***

### This dataset is freely available for download from the [HuggingFace Datasets](https://huggingface.co/datasets) repository.

## Datasets
<li>
    <a href="https://huggingface.co/datasets/xsum"><b>Xsum</b></a>
</li>
<li>
    <a href="https://huggingface.co/datasets/cnn_dailymail"><b>CNN_dailymail</b></a>
</li>

***
## Why are we using these datasets?
We are using these datasets because they have unique features that make them ideal for summarization and well suited for the task of abstractive summarization.

It's around a 50/50 split between extractive and abstractive summarization. This is because extractive summarization is a lot easier to do than abstractive summarization. Extractive summarization is the process of selecting a subset of the original text to form a summary. Abstractive summarization is the process of generating a summary that is not a direct copy of the original text.

we have around 500k examples in total. This is a lot of data to train on. This is because we are using a large transformer model. The larger the model, the more data you need to train it on. We build our model on top of the BERT model. BERT is a large transformer model that has 12 layers and 768 hidden units per layer. This means that our model has 12,288,000 parameters. This is a lot of parameters to train. This is why we need a lot of data to train on.


---
## CNN_dailymail:
The CNN / DailyMail Dataset is an English-language dataset containing just over 300k unique news articles as written by journalists at CNN and the Daily Mail. The current version supports both extractive and abstractive summarization, though the original version was created for machine reading and comprehension and abstractive question answering.

---
## Xsum:
The Extreme Summarization (XSum) dataset is a dataset for evaluation of abstractive single-document summarization systems. The goal is to create a short, one-sentence new summary answering the question “What is the article about?”. The dataset consists of 226,711 news articles accompanied with a one-sentence summary. The articles are collected from BBC articles (2010 to 2017) and cover a wide variety of domains (e.g., News, Politics, Sports, Weather, Business, Technology, Science, Health, Family, Education, Entertainment and Arts). The official random split contains 204,045 (90%), 11,332 (5%) and 11,334 (5) documents in training, validation and test sets, respectively.


---



