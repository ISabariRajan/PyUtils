from time import sleep
import requests
from Utilities.Network.ProxyUtilities import ProxyUtilities, logger
class ScrapperApiUtilities(ProxyUtilities):

    API_KEY = "c6c2909352a04e1073bd2ae65e093f0e"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")
        self.proxy()

    # def get(self, url):
    #     res = requests.post(
    #             url = 'https://async.scraperapi.com/jobs',
    #             json={ 'apiKey': self.API_KEY, 'url': url }
    #         )
    #     status_url = res.json()["statusUrl"]
    #     while True:
    #         sleep(1)
    #         status_res = requests.get(status_url)
    #         if status_res.json()["status"] == "finished":
    #             return status_res["response"]

    # def get_batch(self, url):
    #     res = requests.post(
    #             url = 'https://async.scraperapi.com/jobs',
    #             json={ 'apiKey': self.API_KEY, 'url': url }
    #         )
    #     status_url = res.json()["statusUrl"]
    #     while True:
    #         sleep(1)
    #         status_res = requests.get(status_url)
    #         if status_res.json()["status"] == "finished":
    #             return status_res["response"]