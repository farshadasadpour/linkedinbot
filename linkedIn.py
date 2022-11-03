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
        self.till_page = parameters.till_page
        self.csv_file_name = parameters.file_name
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.write = csv.writer(open(self.csv_file_name, 'a'))
        
        
    def search_and_send_request(self):
        """
        this method make connection in linkedin

        Args:
            keywords (_type_): keywords from parameters
            till_page (_type_): till+page from parameters
            writer (_type_): _description_
        """
        for page in range(1, self.till_page + 1):
            print('\nINFO: Checking on page %s' % (page))
            #query_url = 'https://www.linkedin.com/search/results/people/?keywords=' + self.keywords + '&origin=GLOBAL_SEARCH_HEADER&page=' + str(page)
            query_url = 'https://www.linkedin.com/search/results/people/?keywords=' + self.keywords + '&origin=FACETED_SEARCH&sid=nb&page=' + str(page)
            self.driver.get(query_url)
            time.sleep(5)
            html = self.driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
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
                    try:
                        coordinates = connection.location_once_scrolled_into_view # returns dict of X, Y coordinates
                        self.driver.execute_script("window.scrollTo(%s, %s);" % (coordinates['x'], coordinates['y']))
                        time.sleep(5)
                        connection.click()
                        time.sleep(5)
                        if self.driver.find_elements_by_class_name('artdeco-button--primary')[0].is_enabled():
                            self.driver.find_elements_by_class_name('artdeco-button--primary')[0].click()
                            self.writer.writerow([text])
                            print("%s ) SENT: %s" % (index, text))
                        else:
                            self.driver.find_elements_by_class_name('artdeco-modal__dismiss')[0].click()
                            print("%s ) CANT: %s" % (index, text))
                    except Exception as e:
                        print('%s ) ERROR: %s' % (index, text))
                    time.sleep(5)
                elif connection.text == 'Pending':
                        print("%s ) PENDING: %s" % (index, text))
                else:
                        if text : print("%s ) CANT: %s" % (index, text))
                        else: print("%s ) ERROR: You might have reached limit" % (index))
        
        self.write_csv_file()
        self.close_driver()


    def login(self):
        """
        login to linkedin
        """
        # Login
        self.driver.get('https://www.linkedin.com/login')
        self.driver.find_element_by_id('username').send_keys(self.username)
        self.driver.find_element_by_id('password').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@type="submit"]').click()
        time.sleep(10)

    def write_csv_file(self):
        # CSV file loging
        file_name = self.csv_file_name
        file_exists =  os.path.isfile(file_name)
        if not file_exists: self.writer.writerow(['Connection Summary'])

    def close_driver(self):
        self.driver.quit()


