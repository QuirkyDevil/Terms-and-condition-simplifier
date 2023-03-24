import re
import asyncio
import functools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

from decorators.asyc_executor import executor


@executor()
def scrap_text(input_user):
    """This function opens a chrome browser and searches for the
    terms and conditions of the site. It then clicks on the first link
    and waits for the page to load. It then fetches every text on the page"""
    string = input_user.replace(" ", "+")

    options = ChromeOptions()
    options.add_argument("--headless")
    capa = options.to_capabilities()
    capa["pageLoadStrategy"] = "none"
    chrome_driver = ChromeDriverManager().install()
    driver = webdriver.Chrome(
        service=ChromeService(chrome_driver), desired_capabilities=capa
    )

    # We are using the WebDriverWait to wait for the page to load
    wait = WebDriverWait(driver, 5)
    driver.get("https://www.google.com/search?q=" + string + "+terms+and+conditions")
    try:
        first_link = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[@class='LC20lb MBeuO DKV0Md']")
            )
        )
        driver.execute_script("window.stop();")
        # wait until the first link is loaded and then click on it
        first_link.click()
    except TimeoutError:
        driver.quit()
        return 500
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        driver.execute_script("window.stop();")
        # TODO: As soon as the page loads, extract the text needed from the page and return it
        text = driver.execute_script("return document.body.innerText")
        driver.quit()
        return text
    except TimeoutError:
        driver.quit()
        return 500


async def preprocess(text):
    """This function preprocesses the text by removing html tags, new lines, tabs and extra spaces"""
    text = text.encode("ascii", "ignore").decode()  # remove non-ascii characters
    text = re.sub(r"<.*?>", "", text)  # remove html tags
    text = re.sub(r"[\n\t]+", " ", text)  # remove new lines and tabs
    text = re.sub(r" +", " ", text).strip()  # remove extra spaces
    return text


async def scrape(input_user):
    tnc = await scrap_text(input_user)
    if tnc == 500:
        return 500
    else:
        tnc = await preprocess(tnc)
        return tnc


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    # store tnc in a file
    with open("tnc.txt", "w") as f:
        f.write(loop.run_until_complete(scrape("facebook")))
    loop.close()
