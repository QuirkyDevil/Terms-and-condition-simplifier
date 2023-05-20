import math
import time
import spacy
from nltk.tokenize import sent_tokenize
from transformers import BartTokenizer, BartForConditionalGeneration

t1 = time.time()
model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
nlp = spacy.load("en_core_web_sm")
t2 = time.time()
print(f"\033[92m INFO:\033[0m     Time taken to load the models: {round((t2 - t1), 2)} seconds")


async def final_summary(input_text, points: int = 20):
    """This is the summarizer corutine. In this we will summarize the text based on the number of bullet points given.
    We will first split the text into sentences and then summarize them in batches. We will summarize the batches
    based on their length. If the length of the batch is less than 100, we will summarize them directly. If the length
    of the batch is greater than 1024, we will divide the batch into two and summarize them. If the length of the
    summary is less than the length of the original text, we will append the summary to the output list. We will
    continue this process until the number of bullet points is less than the number of points given. We will then
    join the final sentences by bullet separator and return the summary.
    """
    text = input_text
    bullet_points = points
    final_output = []
    summary_bullet = ""

    while bullet_points >= points:
        # splitting the text into sentences
        chunks = []
        sentences = nlp(text)
        for sentence in sentences.sents:
            chunks.append(str(sentence))
        # initializing the output list
        output = []
        sentences_remaining = len(chunks)
        i = 0

        # looping through the sentences in an equal batch based on their length and summarizing them
        while sentences_remaining > 0:
            chunks_remaining = math.ceil(sentences_remaining / 10.0)
            next_chunk_size = math.ceil(sentences_remaining / chunks_remaining)
            sentence = "".join(chunks[i : i + next_chunk_size])
            i += next_chunk_size
            sentences_remaining -= next_chunk_size
            inputs = tokenizer(sentence, return_tensors="pt", padding="longest")
            original_input_length = len(inputs["input_ids"][0])

            # checking if the length of the input batch is less than 100
            if original_input_length < 100:
                split_sentences = nlp(sentence)
                for split_sentence in split_sentences.sents:
                    output.append(str(split_sentence).rstrip("."))

            # checking if the length of the input batch is greater than 1024
            elif original_input_length > 1024:
                sent = sent_tokenize(sentence)
                length_sent = len(sent)

                j = 0
                sent_remaining = math.ceil(length_sent / 2)

                # going through the batch that is greater than 1024 and dividing them
                while length_sent > 0:
                    halved_sentence = "".join(sent[j : j + sent_remaining])
                    halved_inputs = tokenizer(halved_sentence, return_tensors="pt")

                    halved_summary_ids = model.generate(
                        halved_inputs["input_ids"], max_length=1024
                    )
                    j += sent_remaining
                    length_sent -= sent_remaining

                    # checking if the length of the output summary is less than the original text
                    if len(halved_summary_ids[0]) < len(halved_inputs["input_ids"][0]):
                        halved_summary = tokenizer.batch_decode(
                            halved_summary_ids,
                            skip_special_tokens=True,
                            clean_up_tokenization_spaces=False,
                        )[0]
                        output.append(halved_summary)

            else:
                summary_ids = model.generate(inputs["input_ids"], max_length=1024)
                if len(summary_ids[0]) < original_input_length:
                    summary = tokenizer.batch_decode(
                        summary_ids,
                        skip_special_tokens=True,
                        clean_up_tokenization_spaces=False,
                    )[0]
                    output.append(summary)

        final_output = []
        for paragraphs in output:
            lines = paragraphs.split(" . ")
            for line in lines:
                final_output.append(line.replace(" .", "").strip())
        text = ".".join(final_output)
        bullet_points = len(final_output)

    for i in range(len(final_output)):
        final_output[i] = "* " + final_output[i] + "."

    # final sentences are incoherent, so we will join them by bullet separator
    summary_bullet = "\n".join(final_output)
    return summary_bullet
