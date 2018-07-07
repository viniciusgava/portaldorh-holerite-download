# coding=utf-8
import os
import shutil
import time
import tempfile
import re

import selenium
from selenium.webdriver.support.ui import Select


class Downloader:
    tmp_download_path = tempfile.mkdtemp()

    def __init__(self, settings, logger):
        self.settings = settings
        self.logger = logger

        # Define driver options
        driver_profile = {
            "plugins.plugins_list": [
                {
                    "enabled": False,
                    "name": "Chrome PDF Viewer"
                }
            ],
            "plugins.always_open_pdf_externally": True,
            "download.default_directory": self.tmp_download_path,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }

        driver_options = selenium.webdriver.ChromeOptions()
        driver_options.add_experimental_option("prefs", driver_profile)

        # Should use headless?
        if settings.headless is True:
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--headless')
            driver_options.add_argument('--disable-gpu')

        # Configure driver
        self.driver = selenium.webdriver.Chrome(chrome_options=driver_options)
        self.driver.implicitly_wait(10)

        # Workaround to fix headless problem to set default download path
        if settings.headless is True:
            self.enable_download_in_headless_chrome()

    def run(self):
        self.logger.info("Initializing Holerite download")
        self.logger.info("Download path: " + self.settings.default_download_path)
        self.logger.info("Temporary download path: " + self.tmp_download_path)
        self.logger.info("Portal do RH URL: " + self.settings.portal_rh.url)
        self.logger.info("Portal do RH username: " + self.settings.portal_rh.username)
        self.logger.info("Holerite year: " + self.settings.search_year)
        self.logger.info("Holerite month: " + self.settings.search_month)
        self.logger.info("Headless: %r" % self.settings.headless)

        # Login
        if self.login() is False:
            return False

        # Search document
        if self.search_document() is False:
            return False

        # Check result
        result = self.check_result()

        self.driver.close()
        self.logger.info("download finished")

        return result

    def login(self):
        # Open login page
        self.driver.get(self.settings.portal_rh.url)

        # Input username
        username_element = self.driver.find_element_by_id("CtrlLogin1_txtIDNumerico")
        username_element.clear()
        username_element.send_keys(self.settings.portal_rh.username)

        # Input password
        password_element = self.driver.find_element_by_id("CtrlLogin1_txtSenhaAlfanumerico")
        password_element.clear()
        password_element.send_keys(self.settings.portal_rh.password)

        self.logger.info("Username and password has been filled. Logging..")

        # Sign-in
        self.driver.find_element_by_id("CtrlLogin1_btnIniciar").click()

        home_pattern = re.compile(".*Auto_Default\.aspx.*")

        # Sign-in Fail?
        if home_pattern.match(self.driver.current_url) is not None:
            self.logger.warning('Username or password invalid')
            return False

        return True

    def search_document(self):
        # Select mainFrame, where is the search form
        self.driver.switch_to.frame("mainFrame")

        # Choose document type
        self.logger.info("Choosing document type: MENSAL")
        type_select = Select(self.driver.find_element_by_id("controlsAscx111_cboFolha"))
        type_select.select_by_visible_text("MENSAL")

        # Given search date
        self.logger.info("Inputing search date: " + self.get_search_date())
        date_element = self.driver.find_element_by_id("controlsAscx111_txtDataRef")
        date_element.clear()
        date_element.send_keys(self.get_search_date())

        # Perform search
        self.driver.find_element_by_id("controlsAscx111_btnDemoConsultar").click()

        return True

    def check_result(self):
        # Regex to check if given date is invalid
        invalid_date_pattern = re.compile(
            "Demonstrativo de Pagamento (.+) não liberado para emissão!. Será liberado a partir do dia ([0-9]{2}\/[0-9]{2}\/[0-9]{4})\.")

        # is a invalid date?
        if invalid_date_pattern.search(self.driver.page_source) is not None:
            self.logger.warning("Invalid search date: " + self.get_search_date())
            return False

        # It is a valid date

        # Download file path
        download_file_path = os.path.join(self.tmp_download_path, 'Auto_PrincipalConteudo.aspx')

        # Wait file download
        self.logger.info("Waiting pdf download")
        if self.wait_file_exists(download_file_path) is False:
            return False

        # Success - File downloaded
        self.logger.info("Download finished. Moving file to final path...")

        # Pdf file name
        pdf_file_name = "%s-%s.pdf" % (self.settings.search_year, self.settings.search_month)

        # Final file path
        pdf_file_path = os.path.abspath(self.settings.default_download_path)
        pdf_file_path = os.path.join(pdf_file_path, pdf_file_name)

        # Move
        shutil.move(download_file_path, pdf_file_path)
        self.logger.info("File has been moved to: " + pdf_file_path)

        return True

    def get_search_date(self):
        return "%s/%s" % (self.settings.search_month, self.settings.search_year)

    def wait_file_exists(self, file_path):
        timeout = 0
        timeout_limit = 60
        while not os.path.exists(file_path):
            self.logger.info("Waiting download...")

            time.sleep(3)
            timeout += 3
            if timeout > timeout_limit:
                self.logger.error("timeout - Could not download file")
                return False

        return True

    def enable_download_in_headless_chrome(self):
        # add missing support for chrome "send_command"  to selenium webdriver
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

        params = {'cmd': 'Page.setDownloadBehavior',
                  'params': {'behavior': 'allow', 'downloadPath': self.tmp_download_path}}
        self.driver.execute("send_command", params)
