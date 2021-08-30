from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time


class EasyApplyer:

    def __init__(self, data):
        self.email = data['email']
        self.password = data['password']
        self.keywords = data['keywords']
        self.location = data['location']
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--window-size=2560,1440")
        chrome_options.add_argument("--window-position=0,0")

        self.driver = webdriver.Chrome(data['driver_path'],
                                       chrome_options=chrome_options)

    def login(self):
        login_url = 'https://www.linkedin.com/login'
        self.driver.get(login_url)

        # Input login info
        login_email = self.driver.find_element_by_name('session_key')
        login_email.clear()
        login_email.send_keys(self.email)
        login_password = self.driver.find_element_by_name('session_password')
        login_password.clear()
        login_password.send_keys(self.password)
        login_password.send_keys(Keys.RETURN)

    def search_jobs(self):
        jobs_link = self.driver.find_element_by_link_text('Jobs')
        jobs_link.click()

        time.sleep(3)
        job_xpa_rule = "//input[starts-with(@id, 'jobs-search-box-keyword')]"
        job_keyword = self.driver.find_element_by_xpath(job_xpa_rule)
        job_keyword.clear()
        job_keyword.send_keys(self.keywords)

        time.sleep(2)

        loc_xpa_rule = "//input[starts-with(@id, 'jobs-search-box-location')]"
        job_location = self.driver.find_element_by_xpath(loc_xpa_rule)
        job_location.clear()
        job_location.send_keys(self.location)

        btn_rule = "//button[starts-with(@class, 'jobs-search-box__submit')]"
        search_button = self.driver.find_element_by_xpath(btn_rule)
        search_button.click()

    def add_filters(self):
        # easy apply
        easy_rule = "//button[starts-with(@aria-label, 'Easy Apply filter')]"
        easy_apply_btn = self.driver.find_element_by_xpath(easy_rule)
        easy_apply_btn.click()
        time.sleep(2)

        # All filters, Entry level experience:
        allF_rule = "//button[starts-with(@aria-label, 'All filters')]"
        all_f_btn = self.driver.find_element_by_xpath(allF_rule)
        all_f_btn.click()
        time.sleep(2)

        entry_level_rule = "//label[starts-with(@for,\
                                            'advanced-filter-experience-2')]"
        entry_level_btn = self.driver.find_element_by_xpath(entry_level_rule)
        entry_level_btn.click()
        time.sleep(2)

        show_rule = "//button[starts-with(@aria-label,\
                                            'Apply current filters to show')]"
        show_results_btn = self.driver.find_element_by_xpath(show_rule)
        show_results_btn.click()
        time.sleep(2)

    def find_offers(self):
        offers_class_name = 'disabled.ember-view.job-card-container__link.job-card-list__title'
        offers = self.driver.find_elements_by_class_name(offers_class_name)
        index = 0
        for offer in offers:
            # hover = ActionChains(self.driver).move_to_element(offer)
            # hover.perform()
            offer.click()
            time.sleep(1)
            self.click_on_easy_apply(offer, index)
            time.sleep(2)
            index += 1
            if index == 3:
                break

    def click_on_easy_apply(self, offer, index):
        try:
            easy_apl_rule = "//button[@data-control-name = \
                              'jobdetails_topcard_inapply']"
            easy_apl_button = self.driver.find_element_by_xpath(easy_apl_rule)
            easy_apl_button.click()
            self.submit_application()

            s = 'Applying to : '
        except NoSuchElementException:
            s = 'Already Applyed, or application needs more steps to '

        company_name = self.driver.find_elements_by_class_name(
                                    'job-card-container__link.job-card-container__company-name.ember-view'
                                    )[index].text
        job_name_and_company = str(offer.text) + ' at ' + str(company_name)
        s += job_name_and_company

        self.add_to_log(s)
        time.sleep(1)

    def submit_application(self):
        try:
            submit_btn_rule = "//button[@aria-label = 'Submit application']"
            submit_button = self.driver.find_element_by_xpath(submit_btn_rule)
            submit_button.click()
        # Not a direct application .. discard !
        except NoSuchElementException:
            try:
                self.answer_question()
            except NoSuchElementException:
                self.discard_offer()

    def click_next(self):
        try:
            next_rule = "//button[@aria-label = 'Continue to next step']"
            next_button = self.driver.find_element_by_xpath(next_rule)
            next_button.click()
        except NoSuchElementException:
            pass

    def click_review(self):
        try:
            review_rule = "//button[@aria-label = 'Review your application']"
            review_button = self.driver.find_element_by_xpath(review_rule)
            review_button.click()
            time.sleep(1)
            self.submit_application()
        except NoSuchElementException:
            pass

    def answer_question(self):
        for i in range(5):
            try:
                self.click_next()
                time.sleep(1)
            except NoSuchElementException:
                pass

        try:
            self.click_review()
        except NoSuchElementException:
            pass

    def discard_offer(self):
        try:
            discard = self.driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
            discard.send_keys(Keys.RETURN)
            time.sleep(1)
            discard_confirm = self.driver.find_element_by_xpath("//button[@data-test-dialog-primary-btn]")
            discard_confirm.send_keys(Keys.RETURN)
            time.sleep(1)
        except NoSuchElementException:
            pass
        raise NoSuchElementException

    def add_to_log(self, s):
        with open('src/logs/applications_logs.txt', 'a') as log_file:
            log_file.write(s)
            log_file.write('\n')

    def run(self):
        self.login()
        # One problem is that the script tries to access
        # the elements before they are loaded, so sleep
        time.sleep(5)
        self.search_jobs()

        time.sleep(5)
        self.add_filters()

        time.sleep(3)
        self.find_offers()
