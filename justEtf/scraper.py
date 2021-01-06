from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from justEtf.utils import read_config
#from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

#high-level variables
config = read_config()
email = config['email']
pw = config['password']
DRIVER_PATH = config['driver_path']
LOGIN_PAGE = config['pages']['login']
COMPARISON_PAGE = config['pages']['comparison']

class Scraper():
    def __init__(self):
        #self.chrome_options = Options().add_argument("--start-maximized")
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.chrome_options = Options().add_argument("--start-maximized") #tbc if it's working
        #super().__init__(DRIVER_PATH, options = self.chrome_options)


    def handle_cookies(self):
        try:
            time.sleep(5)
            #        cookie_accept_button = WebDriverWait(webdriver, 10).until(
            #            EC.presence_of_element_located((By.ID, 'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'))
            #        )
            cookie_accept_button = self.driver.find_element_by_id('CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll')
            if cookie_accept_button.is_displayed():
                print('cookie button found!')
            else:
                time.sleep(2)
            cookie_accept_button.click()
        except Exception as e:
            time.sleep(1)
            print(f"Exception occurred: {e}")
        finally:
            pass

    def login(self):
        self.driver.get(LOGIN_PAGE)
        self.handle_cookies()
        print('logging in...')
        time.sleep(2)
        email_box = self.driver.find_element_by_name('username')
        email_box.send_keys(email)
        time.sleep(0.5)

        password_box = self.driver.find_element_by_name('password')
        password_box.send_keys(pw)
        time.sleep(0.5)

        login_button = self.driver.find_element_by_class_name('buttons')
        login_button.click()
        time.sleep(2)
        print('login_successful')


#intercept filters and remove active ones

    def clear_filters(self):
        time.sleep(5)
        column_filter = self.driver.find_element_by_css_selector("a.btn.btn-outline.buttons-collection.buttons-colvis")

        #https://stackoverflow.com/questions/21713280/find-div-element-by-multiple-class-names
        #popup menu opens
        column_filter.click()
        active_filters = self.driver.find_elements_by_css_selector("li.dt-button.buttons-columnVisibility.active")

        for fil in active_filters:
            fil.click()
            time.sleep(0.5)

        options = self.driver.find_elements_by_css_selector("li.dt-button.buttons-columnVisibility")
        to_tick = config["filters_indexes"]

        for i, opt in enumerate(options):
            if i in to_tick:
                opt.click()
            time.sleep(0.2)

        #restore
        self.restore()


#click out of the way
    def restore(self):
        navbar = self.driver.find_element_by_css_selector('div.navbar-brand')
        webdriver.ActionChains(self.driver).move_to_element(navbar).move_by_offset(100,100).click().perform()


    def results_filter(self):
        page_len = self.driver.find_element_by_css_selector('a.btn.btn-outline.buttons-collection.buttons-page-length')
        page_len.click()
        time.sleep(1)
        max_results = self.driver.find_element_by_css_selector('li.dt-button.button-page-length:last-child')
        max_results.click()
        time.sleep(5)


    def get_table(self):
        print('gathering results...')
        etf_table_html = self.driver.find_element_by_css_selector('div.dataTables_scroll').get_attribute('innerHTML')
        try:
            df = pd.read_html(etf_table_html, header=None)[1] #accessing the second dataframe in the list
            print('Printing csv...')
            df.to_csv('test.csv')
        except Exception as e:
            time.sleep(1)
            print(f"Exception occurred: {e}")


    def quit(self):
        self.driver.quit()


#reset all filters
# dont forget
#'''try:
#    active_filters = driver.find_element_by_class_name('dt-button buttons-columnVisibility active')
#    print('Successfully logged in')
#except NoSuchElementException:
#    print('Incorrect login/password')
#'''

    def launch_scraper(self):
        print('going to comparison page')
        self.driver.get(COMPARISON_PAGE)
        print('step 2 handling cookies')
        self.handle_cookies()
        print('step 3 handling filters')
        self.clear_filters()
        self.results_filter()
        print('step 4 getting table')
        self.get_table()
        print('quit scraper')
        self.quit()