import requests


class PushBulletNotification:

    url = 'https://api.pushbullet.com/v2/pushes'

    def __init__(self, settings, logger):
        self.settings = settings.pushbullet
        self.search_year = settings.search_year
        self.search_month = settings.search_month

        self.logger = logger

    def push(self):
        if self.settings.enable is False:
            self.logger.info('Push Bullet Integration is disabled')
            return False

        self.logger.info('Starting Push Bullet Integration...')

        response = requests.post(
            self.url,
            json=self.get_body(),
            headers=self.get_headers()
        )

        self.logger.info('Response status: %d' % response.status_code)
        self.logger.info('Response text:')
        self.logger.info(response.text)

        if response.status_code == 200:
            self.logger.info('Notification has been pushed')
            return True

        self.logger.info('Fail to push notification')
        return False

    def get_body(self):
        return {
            "title": self.replace_placeholders(self.settings.title),
            "body": self.replace_placeholders(self.settings.body),
            "type": "note"
        }

    def get_headers(self):
        return {
            'Access-Token': self.settings.token,
            'Content-Type': 'application/json'
        }

    def replace_placeholders(self, text):
        settings = self.settings
        settings['search_year'] = self.search_year
        settings['search_month'] = self.search_month

        return text % settings
