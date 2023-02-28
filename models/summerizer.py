import math
import spacy
from nltk.tokenize import sent_tokenize
from transformers import BartTokenizer, BartForConditionalGeneration

model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
nlp = spacy.load("en_core_web_sm")


def final_summary(input_text):
    # reading in the text and tokenizing it into sentence
    text = input_text
    bullet_points = 10

    while bullet_points >= 10:
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
            # inputs = inputs.to(DEVICE)
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
                    # halved_inputs = halved_inputs.to(DEVICE)

                    halved_summary_ids = model.generate(
                        halved_inputs["input_ids"], max_length=128
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
                summary_ids = model.generate(inputs["input_ids"], max_length=128)
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


input_text = """
1. The services we provide
Our mission is to give people the power to build community and bring the world closer together. To help advance this mission, we provide the products and services described below to you:
Provide a personalised experience for you:
Your experience on Facebook is unlike anyone else's: from the Posts, Stories, events, ads and other content that you see in Facebook News Feed or our video platform to the Facebook Pages that you follow and other features you might use, such as Facebook Marketplace and search. For example, we use data about the connections you make, the choices and settings you select, and what you share and do on and off our Products to personalise your experience.
Connect you with people and organisations that you care about:
We help you find and connect with people, groups, businesses, organisations and others that matter to you across the Meta Products you use. We use data to make suggestions for you and others – for example, groups to join, events to attend, Facebook Pages to follow or send a message to, shows to watch and people you may want to become friends with. Stronger ties make for better communities, and we believe that our services are most useful when people are connected to people, groups and organisations that they care about.
Empower you to express yourself and communicate about what matters to you:
There are many ways to express yourself on Facebook to communicate with friends, family and others about what matters to you – for example, sharing status updates, photos, videos and stories across the Meta Products (consistent with your settings), sending messages or making voice or video calls to a friend or several people, creating events or groups, or adding content to your profile, as well as showing you insights on how others engage with your content. We have also developed, and continue to explore, new ways for people to use technology, such as augmented reality and 360 video to create and share more expressive and engaging content on Meta Products.
Help you discover content, products and services that may interest you:
We show you personalised ads, offers and other sponsored or commercial content to help you discover content, products and services that are offered by the many businesses and organisations that use Facebook and other Meta Products. Section 2 below explains this in more detail.
Promote the safety, security and integrity of our services, combat harmful conduct and keep our community of users safe:
People will only build community on Meta Products if they feel safe and secure. We work hard to maintain the security (including the availability, authenticity, integrity and confidentiality) of our Products and services. We employ dedicated teams around the world, work with external service providers, partners and other relevant entities and develop advanced technical systems to detect potential misuse of our Products, harmful conduct towards others and situations where we may be able to help support or protect our community, including to respond to user reports of potentially violating content. If we learn of content or conduct such as this, we may take appropriate action based on our assessment that may include notifying you, offering help, removing content, removing or restricting access to certain features, disabling an account or contacting law enforcement. We share data across Meta Companies when we detect misuse or harmful conduct by someone using one of our Products or to help keep Meta Products, users and the community safe. For example, we share information with Meta Companies that provide financial products and services to help them promote safety, security and integrity and comply with applicable law. Meta may access, preserve, use and share any information it collects about you where it has a good faith belief that it is required or permitted by law to do so. For more information, please review our Privacy Policy.

In some cases, the Oversight Board may review our decisions, subject to its terms and bylaws. Learn more here.
Use and develop advanced technologies to provide safe and functional services for everyone:
We use and develop advanced technologies such as artificial intelligence, machine learning systems and augmented reality so that people can use our Products safely regardless of physical ability or geographic location. For example, technology such as this helps people who have visual impairments understand what or who is in photos or videos shared on Facebook or Instagram. We also build sophisticated network and communication technology to help more people connect to the Internet in areas with limited access. And we develop automated systems to improve our ability to detect and remove abusive and dangerous activity that may harm our community and the integrity of our Products.
Research ways to make our services better:
We engage in research to develop, test and improve our Products. This includes analysing data that we have about our users, and understanding how people use our Products, for example by conducting surveys and testing and troubleshooting new features. Our Privacy Policy explains how we use data to support this research for the purposes of developing and improving our services.
Provide consistent and seamless experiences across the Meta Company Products:
Our Products help you find and connect with people, groups, businesses, organisations and others that are important to you. We design our systems so that your experience is consistent and seamless across the different Meta Company Products that you use. For example, we use data about the people you engage with on Facebook to make it easier for you to connect with them on Instagram or Messenger, and we enable you to communicate with businesses that you follow on Facebook through Messenger.
Ensuring access to our services:
To operate our global services and enable you to connect with people around the world, we need to transfer, store and distribute content and data to our data centres, partners, service providers, vendors and systems around the world, including outside your country of residence. The use of this global infrastructure is necessary and essential to provide our services. This infrastructure may be owned, operated or controlled by Meta Platforms, Inc., Meta Platforms Ireland Limited or its affiliates.
Return to top
"""

sumamry = final_summary(input_text)
print(sumamry)
