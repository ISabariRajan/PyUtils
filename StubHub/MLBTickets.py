import json
from os.path import join as joinpath
from concurrent.futures import ThreadPoolExecutor
from . import requests, time, SeleniumUtilities, BS4Utilities

base_url = "https://www.stubhub.com/"
selenium = SeleniumUtilities(botname="SeleniumUtilities")
bs4 = BS4Utilities(botname="BS4Utilities")
selenium.set_firefox_driver()

class MLBTickets:
    
    def click_seemore_until_nomore(self, driver):
        url = base_url + "mlb-tickets/grouping/81/"
        driver.get(url)
        button_locator = "//*[text()='See More']"
        selenium.print_info_log("Clicking See More, Until nothing left")
        while True:
            try:
                selenium.WebDriverWait(driver, 10).until(selenium.EC.presence_of_all_elements_located((selenium.By.XPATH, button_locator)))
                button = driver.find_element(selenium.By.XPATH, button_locator)
                # button.click()
                # soup = BeautifulSoup(driver.execute_script("return document.body.innerHTML").encode("utf-8").decode("utf-8"), "html.parser")
                break
            except selenium.exceptions.TimeoutException:
                break
        
        time.sleep(5)
        print("BEFORE-READING-HTML")
        # bs4.generate_bs4(driver.execute_script("return document.body.innerHTML"))
        # return bs4.soup
        return selenium.convert_webpage_to_soup()

    def get_event_links_from_soup(self, soup):
        bs4.print_info_log("Get Event Links from Soup")
        events_button = soup.find_all("button")
        for b in events_button:
            if b.text.strip() == "Events":
                events_button = b
                break
        events_button_anc = bs4.find_nth_anchestor(events_button, 3)
        event_table = bs4.find_nth_sibling(events_button_anc, 2)
        all_events = event_table.findChildren("a")

        all_events_link = []

        print(f"Total Events: {len(all_events)}")
        for a in all_events:
            event = a.get("href").split("/")
            id = event[-2:][0]
            title = event[-4:][0] + " - " + id
            all_events_link.append({
                "url": base_url + a.get("href"),
                "title": title,
                "id": id,
                "status": "new"
            })
        return all_events_link

    def capture_all_events(self):
        return selenium.run_function_within_webdriver(function_name=self.click_seemore_until_nomore)

    def get_seat_data_from_event(self, event):
        print("Getting Seat details from : ", event["title"])
        response = requests.post(event["url"]).json()
        with open(joinpath("output", event["title"] + ".json"), "w") as f:
            f.write(json.dumps(response, indent=2))
        obj_keys = [
            "Section", "Row", "Price"
        ]
        try:
            with open(joinpath("output", event["title"] + ".csv"), "w") as f:
                f.write("Section, Row, Price, SeatsRemaining\n")
                for data in response["Items"]:
                    # print(data)
                    line = ""
                    for key in obj_keys:
                        val = data[key]
                        if val == None:
                            val = " - "
                        val= val.replace(",", "")
                        line += val + ", "

                    val = data["TicketsLeftInListingMessage"]
                    if val == None:
                        val = 0
                    else:
                        val = val["Message"]
                        if val == None:
                            val = 0
                        else:
                            val = val.split(" ")[0]

                    line += str(val) + "\n"
                    f.write(line)
        except Exception as e:
            print(e)
    
    def get_seat_data_from_events(self):
        try:
            soup = self.capture_all_events()
            all_events_link = self.get_event_links_from_soup(soup)
            pool = ThreadPoolExecutor(10)
            output_folder = "output"

            for event in all_events_link:
                pool.submit(self.get_seat_data_from_event, (event))
        except Exception as e:
            print(f"Outer Exception {e}")