import re
import asyncio
import functools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def executor(loop: asyncio.AbstractEventLoop = None, executor=None):
    """This is a decorator that allows you to run a function in a thread pool executor.
    This is useful for blocking functions that you don't want to block the event loop.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal loop, executor
            partial = functools.partial(func, *args, **kwargs)
            loop = loop or asyncio.get_event_loop()
            return loop.run_in_executor(executor, partial)

        return wrapper

    return decorator


@executor()
def get_url(input_user):
    """This function opens a chrome browser and searches for the
    terms and conditions of the site. It then clicks on the first link
    and waits for the page to load. It then fetches every text on the page"""
    string = input_user.replace(" ", "+")
    # Using the none page load strategy to speed up the process of loading the page
    capa = DesiredCapabilities.CHROME
    capa["pageLoadStrategy"] = "none"
    chrome_driver = ChromeDriverManager().install()
    # We are using the ChromeDriverManager to automatically download the
    # latest version of the ChromeDriver
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
        return 500
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        driver.execute_script("window.stop();")
        # TODO: As soon as the page loads, extract the text needed from the page and return it
        text = driver.execute_script("return document.body.innerText")
        return text
    except TimeoutError:
        return 500


async def preprocess(text):
    text = text.encode("ascii", "ignore").decode()  # remove non-ascii characters
    text = re.sub("<.*?>", "", text)  # remove html tags
    text = re.sub(r"\n", " ", text)  # remove new line
    text = re.sub(r"\n\n", " ", text)  # remove new lines
    text = re.sub(r"\t", " ", text)  # remove tabs
    text = text.strip(" ")  # remove spaces
    text = re.sub(" +", " ", text).strip()  # remove extra spaces
    return text


async def main():
    name = input("Enter the name of the site u want terms and conditions for: ")
    output = await get_url(name)
    if output == 500:
        print("The site you are looking for is not found")
    else:
        output = await preprocess(output)


async def scrape(input_user):
    tnc = await get_url(input_user)
    if tnc == 500:
        return 500
    else:
        tnc = await preprocess(tnc)
        return tnc


if __name__ == "__main__":
    asyncio.run(main())
