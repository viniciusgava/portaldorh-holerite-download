import os
import time
import tempfile
import input

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from credentials import *


# TODO use a timeout mechanism
def wait_file_exists(file_path):
    while not os.path.exists(file_path):
        time.sleep(0.1)


defaultDownloadPath = tempfile.mkdtemp()

profile = {
    "plugins.plugins_list": [
        {
            "enabled": False,
            "name": "Chrome PDF Viewer"
        }
    ],
    "download.default_directory": defaultDownloadPath
}

options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", profile)

driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=options)
driver.get(input.portalURL)
assert "Portal RH - Logon" in driver.title

# LOGIN

# Input username
usernameElement = driver.find_element_by_id("CtrlLogin1_txtIDNumerico")
usernameElement.clear()
usernameElement.send_keys(username)

# Input password
passwordElement = driver.find_element_by_id("CtrlLogin1_txtSenhaAlfanumerico")
passwordElement.clear()
passwordElement.send_keys(password)

# sign-in
driver.find_element_by_id("CtrlLogin1_btnIniciar").click()

# CHOOSE DOCUMENT AND INPUT DATE
driver.switch_to.frame("mainFrame")

# Select type
typeSelect = Select(driver.find_element_by_id("controlsAscx111_cboFolha"))
typeSelect.select_by_visible_text("MENSAL")

# Given search date
dateElement = driver.find_element_by_id("controlsAscx111_txtDataRef")
dateElement.clear()
dateElement.send_keys(input.searchDate)

# search
driver.find_element_by_id("controlsAscx111_btnDemoConsultar").click()

download_file_path = os.path.join(defaultDownloadPath, 'Auto_PrincipalConteudo.aspx')
pdf_file_path = os.path.abspath(input.defaultDownloadPath)

wait_file_exists(download_file_path)

# Rename
os.rename(
    os.path.join(download_file_path),
    os.path.join(pdf_file_path, (input.searchDate.replace("/", "-") + ".pdf")),
)
