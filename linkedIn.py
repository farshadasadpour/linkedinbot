from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import csv, os.path, time
import parameters


class Linkedin:
    def __init__(self) -> None:
        """
        get parameters form file
        """
        self.username = parameters.linkedin_username
        self.password = parameters.linkedin_password
        self.keywords = parameters.keywords
        self.start_page = parameters.start_page
        self.till_page = parameters.till_page
        self.geo = parameters.geoUrn
        # google chrome
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument("--headless")
        self.driver= webdriver.Chrome(executable_path=parameters.google_chrome_driver_path,chrome_options=chrome_options)

    def search_and_send_request(self):
        """
        this method make connection in LinkedIn
        """
        for page in range(self.start_page, self.till_page + 1):
            print(f'\nINFO: Checking on page {page}')
            # query_url = 'https://www.linkedin.com/search/results/people/?keywords=' + self.keywords + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(page)
            # query_url = f'https://www.linkedin.com/search/results/people/?activelyHiring="true"&geoUrn={self.geo}&keywords={self.keywords}&origin=FACETED_SEARCH&sid=nb&page={str(page)}'
            query_url = f'https://www.linkedin.com/search/results/people/?geoUrn={self.geo}&keywords={self.keywords}&origin=FACETED_SEARCH&sid=nb&page={str(page)}'
            print(query_url)
            self.driver.get(query_url)
            time.sleep(5)
            self.driver.find_element_by_tag_name('html').send_keys(Keys.END)
            time.sleep(5)
            linkedin_urls = self.driver.find_elements_by_class_name('reusable-search__result-container')
            print('INFO: %s connections found on page %s' % (len(linkedin_urls), page))
            for index, result in enumerate(linkedin_urls, start=1):
                text = result.text.split('\n')[0]
                connection_action = result.find_elements_by_class_name('artdeco-button__text')
                if connection_action:
                    connection = connection_action[0]
                else:
                    print("%s ) CANT: %s" % (index, text))
                    continue
                if connection.text == 'Connect':
                    self.send_connection(index, text, connection)
                elif connection.text == 'Pending':
                    print("%s ) PENDING: %s" % (index, text))
                else:
                    if text:
                        print("%s ) CANT: %s" % (index, text))
                    else:
                        print(f"{index} ) ERROR: You might have reached limit")
                        self.close_driver()

        self.close_driver()

    def send_connection(self, index, text, connection):
        try:
            coordinates = connection.location_once_scrolled_into_view
            self.driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
            time.sleep(5)
            connection.click()
            time.sleep(5)
            if self.driver.find_elements_by_class_name('artdeco-button--primary')[0].is_enabled():
                self.driver.find_elements_by_class_name('artdeco-button--primary')[0].click()
                print("%s ) SENT: %s" % (index, text))
            else:
                self.driver.find_elements_by_class_name('artdeco-modal__dismiss')[0].click()
                print("%s ) CANT: %s" % (index, text))
        except Exception as e:
            print('%s ) ERROR: %s' % (index, text))
        time.sleep(5)

    def login(self):
        """
        login to linkedin
        """
        self.driver.get('https://www.linkedin.com/login')
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@type="submit"]').click()
        time.sleep(10)

    # def write_csv_file(self):
    #     file_name = self.csv_file_name
    #     if not os.path.isfile(file_name): self.write.writerow(['Connection Summary'])

    def close_driver(self):
        self.driver.quit()