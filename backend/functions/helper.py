import re

async def preprocess(text):
    """This is a utility function that will preprocess the text
    before it is sent to the NLP model. This will remove html tags,
    new lines and tabs, and extra spaces. It will also remove non-ascii
    characters. It is necessary to remove unnecesry characters because
    the NLP model will not work properly if there are extra characters.
    """
    text = text.encode("ascii", "ignore").decode()  # remove non-ascii characters
    text = re.sub(r"<.*?>", "", text)  # remove html tags
    text = re.sub(r"[\n\t]+", " ", text)  # remove new lines and tabs
    text = re.sub(r" +", " ", text).strip()  # remove extra spaces
    return text

def min_sec(seconds: float) -> str:
    """Convrts Minutes to seconds. _deprecreated_
    """
    minutes, seconds = divmod(seconds, 60)
    if minutes:
        return f"{minutes:.0f}:{seconds:06.3f}s"
    return f"{seconds:.3f}s"

