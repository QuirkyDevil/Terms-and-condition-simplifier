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
def get_url(name):
    """This function opens a chrome browser and searches for the
    terms and conditions of the site. It then clicks on the first link
    and waits for the page to load. It then fetches every text on the page"""

    string = name.replace(" ", "+")
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
    wait = WebDriverWait(driver, 20)
    driver.get("https://www.google.com/search?q=" + string + "+terms+and+conditions")
    wait.until(
        EC.presence_of_element_located((By.XPATH, "//h3[@class='LC20lb MBeuO DKV0Md']"))
    )
    # wait until the first link is loaded and then click on it
    first_link = driver.find_elements(By.XPATH, "//h3[@class='LC20lb MBeuO DKV0Md']")
    driver.execute_script("window.stop();")
    # As soon as the first link is loaded, stop the page from loading and click on it
    first_link[0].click()
    # TODO: As soon as the page loads, extract the text needed from the page and return it
    # Maybe stop loading javascript and css files to speed up the process


async def main():
    name = input("Enter the name of the site u want terms and conditions for: ")
    await get_url(name)


if __name__ == "__main__":
    asyncio.run(main())
