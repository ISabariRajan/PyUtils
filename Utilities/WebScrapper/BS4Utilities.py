from bs4 import BeautifulSoup
from Utilities.package import WebScrapperUtilities, subprocess, CustomError, logger

class BS4Utilities(WebScrapperUtilities):

    soup = ""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")

    def generate_bs4(self, text, unicode="UTF-8", parser="html.parser"):
        self.soup = BeautifulSoup(text.encode(unicode).decode(unicode), parser)

    def find_nth_anchestor_bs4(self, element, n):
        for i in range(n + 1):
            element = element.parent
        return element

    def find_nth_sibling_bs4(self, element, n):
        for i in range(n + 1):
            element = element.nextSibling
        return element

    def find_nth_successor_bs4(self, element, n):
        for i in range(n + 1):
            element = element.findChildren()[0]
        return element

    def convert_webpage_to_soup(self, driver):
        text = driver.execute_script("return document.body.innerHTML")
        self.generate_bs4(text)
        return self.soup