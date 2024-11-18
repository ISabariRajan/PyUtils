import requests, time, threading
from requests.adapters import HTTPAdapter
from requests.exceptions import ProxyError as rProxyError, ReadTimeout, ConnectionError
from urllib3.exceptions import InsecureRequestWarning, ReadTimeoutError, ProtocolError, ProxyError as uProxyError
from urllib3.util.retry import Retry
from urllib3 import disable_warnings
from http.client import RemoteDisconnected

from json import dumps, loads
# use to parse html text
from lxml.html import fromstring 
from itertools import cycle
import traceback
from Utilities.package import NetworkUtilities, logger
from threading import Thread, Timer

disable_warnings(InsecureRequestWarning)
class Proxy:
    name = ""
    country = ""
    ssl = False
    elite = False
    google = False
    http = ""
    https = ""

    def __init__(self) -> None:
        pass

    def to_json(self):
        return dumps(self, default=lambda o: o.__dict__)

    def default(o):
        return o.__dict__
    
    def __str__(self) -> str:
        return dumps(self.__dict__, ensure_ascii=False, indent=2)
    
    def __repr__(self) -> str:
        return self.__str__()

class ProxyUtilities(NetworkUtilities):

    free_proxy_status = {
        "https://freeproxylists.net/": False,
        # "https://free-proxy-list.net/": False,
        # "https://www.us-proxy.org/": False,
        # "https://free-proxy-list.net/uk-proxy.html": False,
        # "https://www.sslproxies.org/": False
    }

    proxies = {}
    proxy_pool = cycle(proxies)

    valid_proxies = {}
    valid_proxies_pool = cycle(valid_proxies)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.proxy_enabled = self.secure_proxy_enabled = False
        self.print_debug_log(f"Initialized {self.__class__}")
        thread = Thread(target=self.get_free_proxy_list)
        thread.daemon = True
        thread.start()
        # self.find_working_proxies()

    def enable_proxy(self):
        self.proxy_enabled = True
    
    def enable_secure_proxy(self):
        self.secure_proxy_enabled = True

    # Parse HTML to find proxies in table
    def parse_proxies(self, url):
        try:
            self.free_proxy_status[url] = False
            response = requests.get(url)
            print(response.text)
            parser = fromstring(response.text)
            proxies = set()
            tables = parser.xpath('//table')
            print(tables)

            # Check Tables in the webpage
            for tb in tables:
                # Find TBODY of table
                if tb.xpath(".//tbody"):
                    # find no of td in row
                    tr = tb.xpath(".//tbody/tr")
                    if tr and tr[0].xpath(".//td"):
                        # td = 
                        # if td is not empty Find the proxy details
                        for i in tb.xpath('.//tbody/tr'):
                            try:
                                proxy = Proxy()
                                # Grabbing IP and corresponding PORT
                                ip = i.xpath('.//td[1]/text()')[0]
                                # Additional check of IP
                                if len(ip.split(".")) != 4:
                                    continue
                                port = i.xpath('.//td[2]/text()')[0]
                                ip_port = ip + ":" + port
                                proxy.http = "http://" + ip_port
                                proxy.country = i.xpath('.//td[3]/text()')[0]
                                proxy.ssl = i.xpath('.//td[7]/text()')[0] == "yes"
                                proxy.google = i.xpath('.//td[6]/text()')[0] == "yes"
                                proxy.elite = i.xpath('.//td[5]/text()')[0] == "elite proxy"
                                # to check if the corresponding IP is of type HTTPS
                                if proxy.ssl:
                                    proxy.https = "https://" + ip_port
                                self.proxies[ip_port] = proxy
                                proxies.add(proxy)
                            except Exception as e:
                                continue
        except Exception as e:
            self.print_error_log(f"Error in Getting response and/ or Parsing: URL: {url}, \nError: {e}")

        self.free_proxy_status[url] = True
        self.print_debug_log(f"Parsing {url} Complete {self.free_proxy_status[url]}")

    def get_free_proxy_list(self):
        self.print_debug_log("Getting Free Proxies")
        # Websites "https://free-proxy-list.net/, https://www.us-proxy.org/, https://www.sslproxies.org/, https://free-proxy-list.net/uk-proxy.html"
        # All have same format

        for url in self.free_proxy_status:
            thread = Thread(target=self.parse_proxies, args=(url,))
            thread.daemon = True
            thread.start()
        # self.find_working_proxies()
        # Repeat this process Every 30 Seconds, To get an updated list
        Timer(60 * 5, self.get_free_proxy_list).start()

    def create_request_proxy(self, proxy_obj):
        if proxy_obj.ssl:
            proxies = {
                "https": proxy_obj.https,
                "http": proxy_obj.http
            }
        else:
            proxies = {
                "http": proxy_obj.http
            }
        return proxies


    def check_proxy(self, ip):
        try:
            proxy = self.proxies[ip]
            if self.secure_proxy_enabled and (not proxy.ssl):
                return
            status = self.get(proxies=self.create_request_proxy(proxy), skip_proxy=True)
            # If we get None response, We can check the proxy later
            if status:
                if status.status_code == 200:
                    # Add Proxy to valid proxy and refresh pool
                    self.valid_proxies[ip] = proxy
                    self.valid_proxies_pool = cycle(self.valid_proxies)
                    # Remove Proxy from proxies and refresh pool
                    if ip in self.proxies:
                        del self.proxies[ip]
                        self.proxy_pool = cycle(self.proxies)
            else:
                return None
        # Other Exceptions are Logged and proxy can be tested some other time
        except Exception as e:
            self.print_warning_log(f"Error Checking Proxy: {e}")
        # Log Once Completed
        self.print_debug_log(f"Done {ip} AllProxies:{len(self.proxies.keys())} Valid: {len(self.valid_proxies.keys())}")

    def get(self, url="http://httpbin.org/ip", proxies=None, skip_proxy=False):
        try:
            if proxies == None:
                proxies = self.proxy()
            if proxies:
                # self.print_debug_log(f"Get: URL: {url}, Proxy: {proxies}")
                res = requests.get(url=url, proxies=proxies)
                # self.wait("Waiting FOR RESPONSE")
                return res 
            elif not skip_proxy:
                self.sleep(2, message="Waiting for Get Proxies")
                return self.get(url=url, proxies=proxies)
            else:
                return None
        # These Exception means that the proxy is not reachable
        except (rProxyError, uProxyError, ConnectionRefusedError, RemoteDisconnected):
            ip = proxies["http"].replace("https://", "")
            # Delete Bad Proxies
            if ip in self.proxies:
                del self.proxies[ip]
                self.proxy_pool = cycle(self.proxies)
        except Exception as e:
            # self.print_error_log(f"Error getting requests: {e}, URL: {url}, Proxies: {proxies}")
            # print("ERROR" + str(e))
            pass

    def find_working_proxies(self):
        self.print_debug_log("Finding Working Proxies")
        can_continue = False

        # We will loop until All Proxy Capturing Threads are complete
        while not can_continue:
            for url in self.free_proxy_status:
                can_continue = True
                if not self.free_proxy_status[url]:
                    can_continue = False
                    self.sleep(2, message="Waiting For Parsing Free Proxies")
                    break

        proxies = self.proxies
        self.proxy_pool = cycle(proxies)
        keys = set(self.proxies.keys())
        for ip in keys:
            try:
                thread = Thread(target=self.check_proxy, args=(ip,))
                thread.daemon = True
                thread.start()
                # TODO Remove this break
                # break
            except RuntimeError:
                self.print_error_log(f"Runtime Error {ip}")
                self.proxy_pool = cycle(proxies)
                continue
        self.print_debug_log(f"Completed Find working proxies")

    # Return a valid working proxy, If not available
    # Return None
    def proxy(self):
        try:
            proxy = self.valid_proxies[next(self.valid_proxies_pool)]
        except StopIteration:
            return None
        return self.create_request_proxy(proxy)
