from web_scraper import IkmanSearch

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    """
    IkmanSearch(keyword, search_type, search_count)
    keyword: Search keyword
    search_type: 0 (default)- vehicles, 1-motorbikes-scooters, 2-cars, 3-vans, 4-buses, 5-three-wheelers
    search_count: 10 (default)
    """
    ikman_search = IkmanSearch('Honda', 2)

    ikman_search.get_data()
    print(ikman_search.data)


