### Script para connectar con https://www.behindthename.com/random/
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from generator.random_data import randomifylist
from selenium.webdriver.support.ui import Select


class RandomNameScraper:
    def __init__(self, debug=False) -> None:
        self.source = "https://www.behindthename.com/random/"
        options = Options()
        if not debug:
            options.headless = True
        
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.browser.get(self.source)

    def __setup_random_page__(self):
        """
        Hacemos que el random tiene esto attributes
            - Solo primer nombre
            - Solo hombre
        """
        name_select = Select(self.grab_data_from_tags(('class', 'field-data'))[0])
        name_select.select_by_value('1')

        gender_select = Select(self.grab_data_from_tags(('class', 'field-data'))[2])
        gender_select.select_by_value('m')

    def __grab_result__(self):
        """
        Toma la resulta y regresa lo.

        Returns: <str>
        """
        # Click button de nombre
        res_button = self.grab_data_from_tags(('class', 'largebutton'))
        res_button[0].click()

        # Ahora lee la resulta
        result = self.grab_data_from_tags(('class', 'plain'))
        return result[0].text

    def get_random_name(self):
        """
        Busca un random nombre y regresa lo!

        Returns: <str>
        """
        self.__setup_random_page__()
        name_options = self.grab_data_from_tags(("class", "random-cb"))
        # Chequea que no econtramos nombres
        if not name_options:
            print("No encontramos nombres")
            return
        # Los optiones con random!
        chosen_options = randomifylist(name_options)

        # Ahora loop para tocar cada uno
        for option in chosen_options:
            option.click()

        # Ahora hacemos click y buscamos el nombre
        return self.__grab_result__()

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


if __name__ == "__main__":
    ran = RandomNameScraper()
    for x in range(1):
        print(ran.get_random_name())