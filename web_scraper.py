from bs4 import BeautifulSoup
import requests
import json

class IkmanSearch:
    def __init__(self, keyword, search_type=0, search_count=10):
        """
        :param keyword: Search keyword
        :param search_type: 0- vehicles, 1-motorbikes-scooters, 2-cars, 3-vans, 4-buses, 5-three-wheelers
        :param search_count: number of searches
        """
        self.__base_url = 'https://ikman.lk'
        self.__keyword = keyword
        self.__search_type = search_type
        self.__search_count = search_count
        self.__search_category = self.__get_category()
        self.search_resutl = []
        self.data = []

    def get_data(self):
        """
        Search, scrap and save data in json
        :return:None
        """
        # search data
        self.__search()

        # scrap data
        self.__scrap_data()

        # save data in json
        self.__save_as_json()

    def __search(self):
        """
        Search from the keyword and save the required number of links
        :return: None
        """
        search_url = f'{self.__base_url}/en/ads/sri-lanka/{self.__search_category}?query={self.__keyword}'

        # get the search url content
        html_text = requests.get(search_url)

        # parse the html text
        soup = BeautifulSoup(html_text.text, 'lxml')

        # get required number of search items
        items = soup.find_all('a', class_='card-link--3ssYv gtm-ad-item')
        link_count = min(self.__search_count, len(items))
        for i in range(link_count):
            self.search_resutl.append(f'{self.__base_url}{items[i].get("href")}')


    def __scrap_data(self):
        """
        Read the page content and scrap required data
        :return: None
        """
        for item_url in self.search_resutl:
            # get the item url content
            html_text = requests.get(item_url)

            # parse the html text
            soup = BeautifulSoup(html_text.text, 'lxml')

            # get name
            name = soup.find('h1', class_='title--3s1R8')

            # get posted on
            elements = soup.find('span', class_='sub-title--37mkY').text.split(' ')[2:]
            posted_on = ""
            for element in elements:
                if not posted_on:
                    posted_on += element
                else:
                    posted_on += (" " + element)

            # get posted city
            posted_city = soup.find('a', class_='subtitle-location-link--1q5zA').span.text.split(',')[0]

            # get price
            price = soup.find('div', class_='amount--3NTpl').text

            # get condition, engine_capacity, and year_of_manufacture
            lables = soup.find_all('div', class_='word-break--2nyVq label--3oVZK')
            values = soup.find_all('div', class_='word-break--2nyVq value--1lKHt')

            for i in range(len(lables)):
                if (lables[i].text.split(':')[0] == "Condition"):
                    condition = values[i].div.a.span.text
                elif (lables[i].text.split(':')[0] == "Engine capacity"):
                    engine_capacity = values[i].text
                elif (lables[i].text.split(':')[0] =="Year of Manufacture"):
                    year_of_manufacture = values[i].div.a.span.text

            # get link
            link = item_url

            data = {}
            data = {
                "name":name.text,
                "posted_on":posted_on,
                "posted_city":posted_city,
                "price":price,
                "condition":condition,
                "engine_capacity":engine_capacity,
                "year_of_manufacture":year_of_manufacture,
                "link":link
            }

            overview = {}
            overview = {
                "overview":data
            }
            self.data.append(overview)

    def __save_as_json(self):
        """
        Save scraped data in json format
        :return:None
        """
        with open('scrapped_data.json', 'w') as outfile:
            json.dump(self.data, outfile)


    def __get_category(self):
        """
        Returns the search category
        :return: Search category
        """
        switcher = {
            0:"vehicles",
            1:"motorbikes-scooters",
            2:"cars",
            3:"vans",
            4:"buses",
            5:"three-wheelers"
        }

        return switcher.get(self.__search_type, "vehicles")