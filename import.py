import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from credentials import *
from input import *

defaultDownloadPath = os.path.abspath(defaultDownloadPath)

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
driver.get(portalURL)
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
dateElement.send_keys(searchDate)

# search
driver.find_element_by_id("controlsAscx111_btnDemoConsultar").click()

time.sleep(3)

# Rename
os.rename(
    os.path.join(defaultDownloadPath, "Auto_PrincipalConteudo.aspx"),
    os.path.join(defaultDownloadPath, (searchDate.replace("/", "-") + ".pdf")),
)
