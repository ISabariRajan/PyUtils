
from bs4 import BeautifulSoup

from Utilities.package import Utilities, subprocess, CustomError, logger

# Contains Process/ Subprocess related Functions
class WebScrapperUtilities(Utilities):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")
        
    def run_function_within_webdriver(self):
        pass