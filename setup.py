import sys
import subprocess

# install requirements using pip
requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()
    for package in requirements:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# check if pytorch is installed
try:
    import torch
except ImportError:
    # install pytorch using pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torchvision"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "torchaudio"])

# check if spacy is installed
try:
    import spacy
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "spacy"])
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

# check if transformers is installed
try:
    import transformers
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "transformers"])
    from transformers import BartTokenizer, BartForConditionalGeneration
    BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
    BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")


# If u are using conda, uncomment the following lines
# subprocess.check_call("conda install pytorch torchvision torchaudio -c pytorch")
# subprocess.check_call("conda install -c conda-forge spacy")
# subprocess.check_call("conda install -c conda-forge transformers")
