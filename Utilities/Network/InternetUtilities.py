import asyncio, aiohttp, os, zipfile
from Utilities.package import ProcessUtilities, logger

# Contains Internet related functions
class InternetUtilities(ProcessUtilities):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # botname = kwargs["botname"]
        # if botname:
        # else:
        #     super().__init__(botname=logger.__get_bot_name__(__file__), **kwargs)
        self.print_debug_log(f"Initialized {self.__class__}")

        self.download_links = []

    def add_download_details(self, zip_link, zip_full_name, output_folder):
        return

    def get_links_from_anchortags(self, response_html, root_url):
        anchors = response_html.findAll("a")
        all_links = []
        # Loop through all anchor tags and collect the links
        for a in anchors:
            try:
                link = a["href"]
                if(not link.startswith("http")):
                    link = root_url + link
                if(link.startswith(root_url)):
                    all_links.append(link)
            except KeyError as e:
                pass
        return all_links

    def download_files(self):
        # asyncio.run(self.async_download(zip_link, zip_full_name, output_folder))
        asyncio.run(self.async_download())

    async def async_download(self):
        self.log("async_download")
        async with aiohttp.ClientSession() as session:
            
            try:
                download_data = self.download_links.pop(0)
                while(download_data):
                    self.log(download_data)
                    data = await self.fetch(session, download_data[0])
                    with open(download_data[1], "wb") as f:
                        f.write(data["data"])
                    with zipfile.ZipFile(download_data[1], 'r') as zip_ref:
                        zip_ref.extractall(download_data[2])
                    os.remove(download_data[1])
                    download_data = self.download_links.pop(0)
            except Exception as e:
                self.log(e)

    async def fetch(self, session, link):
        self.log("fetch: " + link)
        async with session.get(link) as response:
            if response.status == 200:
                data = await response.read()
                return {"error": "", "data": data}
            else:
                return {"error": "Error", "data": ""}

