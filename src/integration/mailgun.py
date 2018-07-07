import requests
from requests.auth import HTTPBasicAuth


class Mailgun:

    def __init__(self, settings):
        self.settings = settings.mailgun
        self.search_year = settings.search_year
        self.search_month = settings.search_month
        self.default_download_path = settings.default_download_path

    def send(self):
        if self.settings.enable is False:
            return False

        response = requests.post(
            self.get_url(),
            data=self.get_data(),
            files=self.get_files(),
            auth=HTTPBasicAuth('api', self.settings.api_key)
        )

        if response.status_code == 200:
            return True

        return False

    def get_url(self):
        return "https://api.mailgun.net/v3/%s/messages" % self.settings.domain

    def get_files(self):
        path = "%s/%s-%s.pdf" % (self.default_download_path, self.search_year, self.search_month)

        return {
            'attachment': open(path, 'rb')
        }

    def get_data(self):
        data = {
            'from': self.settings['from'],
            'to': self.settings.to,
            'subject': self.replace_placeholders(self.settings.subject),
        }

        if hasattr(self.settings, 'text'):
            data['text'] = self.replace_placeholders(self.settings.text)

        if hasattr(self.settings, 'html'):
            data['html'] = self.replace_placeholders(self.settings.html)

        return data

    def replace_placeholders(self, text):
        settings = self.settings
        settings['search_year'] = self.search_year
        settings['search_month'] = self.search_month

        return text % settings
