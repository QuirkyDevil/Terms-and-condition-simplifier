from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import TimeoutException


from backend.scrappers.constants import *
from backend.decorators.basic import executor


@executor()
def scrap_text(driver: webdriver, company_name: str):
    """This function opens a chrome browser and searches for the
    terms and conditions of the site. It then clicks on the first link
    and waits for the page to load. It then fetches every text on the
    page and returns it. This function is asynchronous and can be used
    with the async/await syntax.
    """
    string = company_name.replace(" ", "+")
    text = ""
    # We are using the WebDriverWait to wait for the page to load
    wait = WebDriverWait(driver, 15)
    driver.get("https://www.google.com/search?q=" + string + "+terms+and+conditions")
    try:
        first_link = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//h3[@class='LC20lb MBeuO DKV0Md']")
            )
        )

        url_name = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//cite[contains(@class, 'qLRx3b')]")
            )
        )

        driver.execute_script("window.stop();")

        url_company_name = company_name.replace(" ", "").lower()

        if url_company_name in url_name.text and (
            any(keyword in url_name.text for keyword in URL_KEYWORDS)
            or any(keyword in first_link.text for keyword in URL_KEYWORDS)
        ):
            first_link.click()
        else:
            return 500
    except TimeoutException:
        driver.quit()
        return 500
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//body")))
        driver.execute_script("window.stop();")
        text = driver.execute_script("return document.body.innerText")
        if CONNECTION_NOT_PRIVATE in text:
            return 500
        driver.quit()
        return text
    except TimeoutError:
        driver.quit()
        return 500


if __name__ == "__main__":
    options = ChromeOptions()
    options.add_argument("--headless")
    capa = options.to_capabilities()
    capa["pageLoadStrategy"] = "none"
    chrome_driver = ChromeDriverManager().install()
    driver = webdriver.Chrome(
        service=ChromeService(chrome_driver), desired_capabilities=capa
    )
    print(scrap_text(driver, "facebook"))
