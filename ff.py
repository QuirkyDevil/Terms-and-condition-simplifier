import asyncio
from models.summerizer import final_summary

if __name__ == "__main__":
    with open("tnc.txt", "r") as f:
        text = f.read()
    value = asyncio.run(final_summary(text))
    print(value)