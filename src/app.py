import os
import shutil
import time
import tempfile
import input
import credentials
import logging
import sys
import re

from selenium import webdriver
from selenium.webdriver.support.ui import Select

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
rootLogger.addHandler(ch)


# TODO use a timeout mechanism
def wait_file_exists(file_path):
    while not os.path.exists(file_path):
        rootLogger.info("Waiting download...")
        time.sleep(3)


def enable_download_in_headless_chrome(browser, download_dir):
    # add missing support for chrome "send_command"  to selenium webdriver
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')

    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


defaultDownloadPath = tempfile.mkdtemp()

rootLogger.info("Initializing Holerite download")
rootLogger.info("Download path: " + input.defaultDownloadPath)
rootLogger.info("Temporary download path: " + defaultDownloadPath)
rootLogger.info("Portal do RH URL: " + input.portalURL)
rootLogger.info("Portal do RH username: " + credentials.username)
rootLogger.info("Holerite date: " + input.searchDate)

profile = {
    "plugins.plugins_list": [
        {
            "enabled": False,
            "name": "Chrome PDF Viewer"
        }
    ],
    "plugins.always_open_pdf_externally": True,
    "download.default_directory": defaultDownloadPath,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", profile)
# options.add_argument('--no-sandbox')
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(10)

enable_download_in_headless_chrome(driver, defaultDownloadPath)

driver.get(input.portalURL)

rootLogger.info("Requesting login page")

assert "Portal RH - Logon" in driver.title

# LOGIN

# Input username
usernameElement = driver.find_element_by_id("CtrlLogin1_txtIDNumerico")
usernameElement.clear()
usernameElement.send_keys(credentials.username)

# Input password
passwordElement = driver.find_element_by_id("CtrlLogin1_txtSenhaAlfanumerico")
passwordElement.clear()
passwordElement.send_keys(credentials.password)

rootLogger.info("Username and password has been filled. Logging..")

# sign-in
driver.find_element_by_id("CtrlLogin1_btnIniciar").click()

# CHOOSE DOCUMENT AND INPUT DATE
driver.switch_to.frame("mainFrame")

rootLogger.info("Choosing document type: MENSAL")

# Select type
typeSelect = Select(driver.find_element_by_id("controlsAscx111_cboFolha"))
typeSelect.select_by_visible_text("MENSAL")

# Given search date
dateElement = driver.find_element_by_id("controlsAscx111_txtDataRef")
dateElement.clear()
dateElement.send_keys(input.searchDate)

rootLogger.info("Inputing search date: " + input.searchDate)

rootLogger.info("Waiting pdf download")

# search
driver.find_element_by_id("controlsAscx111_btnDemoConsultar").click()

invalidDatePattern = re.compile(
    "Demonstrativo de Pagamento (.+) não liberado para emissão!. Será liberado a partir do dia ([0-9]{2}\/[0-9]{2}\/[0-9]{4})\."
)
if invalidDatePattern.search(driver.page_source) != None:
    rootLogger.warning("Invalid search date: " + input.searchDate)
else:
    download_file_path = os.path.join(defaultDownloadPath, 'Auto_PrincipalConteudo.aspx')
    pdf_file_path = os.path.abspath(input.defaultDownloadPath)

    wait_file_exists(download_file_path)

    rootLogger.info("Download finished. Renaming file...")

    # Rename
    shutil.move(
        os.path.join(download_file_path),
        os.path.join(pdf_file_path, (input.searchDate.replace("/", "-") + ".pdf")),
    )

    rootLogger.info(
        "Rename has been finished. Path: " + os.path.join(pdf_file_path, (input.searchDate.replace("/", "-") + ".pdf")))
