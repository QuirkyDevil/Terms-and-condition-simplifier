import sys
import subprocess
import spacy.cli

from transformers import BartTokenizer, BartForConditionalGeneration

# download bart model
BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

# download spacy model
spacy.cli.download("en_core_web_sm")

# install requirements using pip
requirements = []
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
    for package in requirements:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# use subprocess to install pytorch using conda 
subprocess.check_call("conda install pytorch torchvision torchaudio -c pytorch")
