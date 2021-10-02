### Script para connectar con https://www.behindthename.com/random/
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from generator.random_data import randomifylist
from selenium.webdriver.support.ui import Select


class Scraper:
    def __init__(self, debug=False) -> None:
        self.source = "https://app.pinata.cloud/signin"
        options = Options()
        if not debug:
            options.headless = True
        
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.browser.get(self.source)

    def send_search(self, tag=(), query="", results_tag=()):
        """
        Send a search request to the page.

        Params:
            - <tag: tupple(tag_type: str, tag_value: str)> the tag data for the html lookp
            - <query: str> what to send to the tag.

        Return: <webdriver.Restuls|False>
        """
        data = self.grab_data_from_tags(tag)
        # Chequea si tags son empty
        if not data:
            return False
        
        # Query search
        data[0].send_keys(query)
        data[0].submit()

        if results_tag:
            # Query results_tag this time
            results = self.grab_data_from_tags(results_tag)
            return results or False

        return True

    def grab_data_from_tags(self, tag) -> list:
        """
        Grab the dat from the tag info passed.

        Param:   
            - <tag: (tav_type: str, tav_value: str)>

        Return: List
        """
        # Grab data passed
        (tag_type, tag_value) = tag
        tag_type = tag_type.lower()
        # If else to grab correct data
        if tag_type == "id":
            tags = self.browser.find_elements(By.ID, tag_value)
        elif tag_type == "class":
            tags = self.browser.find_elements(By.CLASS_NAME, tag_value)
        elif tag_type == "name":
            tags = self.browser.find_elements(By.TAG_NAME, tag_value)
        elif tag_type == "x-path":
            tags = self.browser.find_elements(By.XPATH, tag_value)
        else:
            tags = []

        return tags