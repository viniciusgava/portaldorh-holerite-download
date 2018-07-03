# coding=utf-8
import os
import shutil
import time
import tempfile
import logging
import sys
import re

import selenium
from selenium.webdriver.support.ui import Select


class Downloader:
    tmp_download_path = tempfile.mkdtemp()

    def __init__(self, credentials, settings):
        self.settings = settings
        self.credentials = credentials

        # Configure logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

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
        if hasattr(settings, 'headless') and settings.headless is True:
            driver_options.add_argument('--no-sandbox')
            driver_options.add_argument('--headless')
            driver_options.add_argument('--disable-gpu')

        # Configure driver
        self.driver = selenium.webdriver.Chrome(chrome_options=driver_options)
        self.driver.implicitly_wait(10)

        # Workaround to fix headless problem to set default download path
        if hasattr(settings, 'headless') and settings.headless is True:
            self.enable_download_in_headless_chrome()

    def run(self):
        self.logger.info("Initializing Holerite download")
        self.logger.info("Download path: " + self.settings.default_download_path)
        self.logger.info("Temporary download path: " + self.tmp_download_path)
        self.logger.info("Portal do RH URL: " + self.settings.portal_rh)
        self.logger.info("Portal do RH username: " + self.credentials.username)
        self.logger.info("Holerite date: " + self.settings.search_date)

        # Login
        self.login()

        # Search document
        self.search_document()

        # Check result
        self.check_result()

        self.driver.close()
        self.logger.info("Script finished")

    def login(self):
        # Open login page
        self.driver.get(self.settings.portal_rh)

        # Input username
        username_element = self.driver.find_element_by_id("CtrlLogin1_txtIDNumerico")
        username_element.clear()
        username_element.send_keys(self.credentials.username)

        # Input password
        password_element = self.driver.find_element_by_id("CtrlLogin1_txtSenhaAlfanumerico")
        password_element.clear()
        password_element.send_keys(self.credentials.password)

        self.logger.info("Username and password has been filled. Logging..")

        # Sign-in
        self.driver.find_element_by_id("CtrlLogin1_btnIniciar").click()

    def search_document(self):
        # Select mainFrame, where is the search form
        self.driver.switch_to.frame("mainFrame")

        # Choose document type
        self.logger.info("Choosing document type: MENSAL")
        type_select = Select(self.driver.find_element_by_id("controlsAscx111_cboFolha"))
        type_select.select_by_visible_text("MENSAL")

        # Given search date
        self.logger.info("Inputing search date: " + self.settings.search_date)
        date_element = self.driver.find_element_by_id("controlsAscx111_txtDataRef")
        date_element.clear()
        date_element.send_keys(self.settings.search_date)

        # Perform search
        self.driver.find_element_by_id("controlsAscx111_btnDemoConsultar").click()

    def check_result(self):
        # Regex to check if given date is invalid
        invalid_date_pattern = re.compile("Demonstrativo de Pagamento (.+) não liberado para emissão!. Será liberado a partir do dia ([0-9]{2}\/[0-9]{2}\/[0-9]{4})\.")

        # is a invalid date?
        if invalid_date_pattern.search(self.driver.page_source) is not None:
            self.logger.warning("Invalid search date: " + self.settings.search_date)
            return

        # It is a valid date
        download_file_path = os.path.join(self.tmp_download_path, 'Auto_PrincipalConteudo.aspx')
        pdf_file_path = os.path.abspath(self.settings.default_download_path)

        print(download_file_path)
        print(pdf_file_path )

        # Wait file download
        self.logger.info("Waiting pdf download")
        if self.wait_file_exists(download_file_path) is False:
            return

        # Success - File downloaded
        self.logger.info("Download finished. Moving file to final path...")

        # Move
        shutil.move(
            os.path.join(download_file_path),
            os.path.join(pdf_file_path, (self.settings.search_date.replace("/", "-") + ".pdf")),
        )
        self.logger.info(
            "File has been moved to: " +
            os.path.join(pdf_file_path, (self.settings.search_date.replace("/", "-") + ".pdf"))
        )

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
