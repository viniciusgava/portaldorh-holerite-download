# coding=utf-8
import os
import tempfile
import re
import requests
from html.parser import HTMLParser


class GenericWebFormsParser(HTMLParser):

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.inputs = {}

    def handle_startendtag(self, tag, attrs):
        if tag != 'input':
            return
        attr = dict(attrs)
        if not attr['name'].startswith('__'):
            return
        if 'value' not in attr:
            return

        self.inputs[attr['name']] = attr['value']


class Downloader:
    tmp_download_path = tempfile.mkdtemp()

    def __init__(self, settings, logger):
        self.session = requests.Session()
        self.settings = settings
        self.logger = logger

    def run(self):
        self.logger.info("Initializing Holerite download")
        self.logger.info("Download path: " + self.settings.default_download_path)
        self.logger.info("Temporary download path: " + self.tmp_download_path)
        self.logger.info("Portal do RH URL: " + self.settings.portal_rh.url)
        self.logger.info("Portal do RH username: " + self.settings.portal_rh.username)
        self.logger.info("Holerite year: " + self.settings.search_year)
        self.logger.info("Holerite month: " + self.settings.search_month)

        self.session = requests.Session()
        self.session.verify = False

        # Login
        if self.login() is False:
            return False

        # Search document
        response = self.search_document()

        # Check result
        result = self.check_result(response)

        self.logger.info("download finished")

        return result

    def login(self):
        # Open login page
        home_response = self.session.get(self.settings.portal_rh.url)

        # Fetch webforms validation fields
        parser = GenericWebFormsParser()
        parser.feed(home_response.text)
        form_data = parser.inputs

        # Input username and password
        form_data['CtrlLogin1$txtIDNumerico'] = self.settings.portal_rh.username
        form_data['CtrlLogin1$txtSenhaAlfanumerico'] = self.settings.portal_rh.password
        form_data['CtrlLogin1$btnIniciar'] = 'Iniciar'

        self.logger.info("Username and password has been filled. Logging..")

        # Sign-in
        login_response = self.session.post(self.settings.portal_rh.url, data=form_data, allow_redirects=False)

        # Sign-in?
        if login_response.status_code == 302:
            return True

        # Process login error
        m = re.search('<span id="CtrlLogin1_lblMensagemAcesso".+>(.+)</span>', login_response.text)
        error_msg = m.group(1)

        self.logger.warning('Username or password invalid - "%s"' % error_msg)

        return False

    def search_document(self):

        # Open Search page
        search_page_url = self.settings.portal_rh.url
        search_page_url = search_page_url.replace('auto_default.aspx', 'Auto_PrincipalConteudo.aspx')
        search_page_response = self.session.get(search_page_url)

        # Fetch webforms validation fields
        parser = GenericWebFormsParser()
        parser.feed(search_page_response.text)

        # Fill required fields to fetch PDF
        form_data = parser.inputs
        form_data['controlsAscx111$cboFolha'] = 'MENSAL	1'
        form_data['controlsAscx111$txtDataRef'] = self.get_search_date()
        form_data['controlsAscx111$btnDemoConsultar'] = 'Consultar'
        form_data['controlsAscx113$cboAno'] = '2018'
        form_data['PG'] = ''
        form_data['scrollLeft'] = 0
        form_data['scrollTop'] = 0

        # Fetch PDF
        pdf_response = self.session.post(search_page_url, data=form_data)

        return pdf_response

    def check_result(self, response):
        # Regex to check if given date is invalid
        invalid_date_pattern = re.compile(
            "Demonstrativo de Pagamento (.+) não liberado para emissão!. Será liberado a partir do dia ([0-9]{2}\/[0-9]{2}\/[0-9]{4})\.")

        # is a invalid date?
        if invalid_date_pattern.search(response.text) is not None:
            self.logger.warning("Invalid search date: " + self.get_search_date())
            return False

        # It is a valid date

        # Pdf file name
        pdf_file_name = "%s-%s.pdf" % (self.settings.search_year, self.settings.search_month)

        # Final file path
        pdf_file_path = os.path.abspath(self.settings.default_download_path)
        pdf_file_path = os.path.join(pdf_file_path, pdf_file_name)

        # Save PDF
        with open(pdf_file_path, 'wb') as f:
            f.write(response.content)
        f.close()
        self.logger.info("File saved at: " + pdf_file_path)

        return True

    def get_search_date(self):
        return "%s/%s" % (self.settings.search_month, self.settings.search_year)
