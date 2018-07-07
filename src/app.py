import argparse

from automate.downloader import Downloader
from integration.mailgun import Mailgun

parser = argparse.ArgumentParser("app")
parser.add_argument('env', help='local or docker env', default='local')

args = parser.parse_args()
env = args.env

if env == 'docker':
    import settings.docker as settings
else:
    import settings.local as settings

downloader = Downloader(settings)
result = downloader.run()

if (result):
    mailgun = Mailgun(settings)
    mailgun.send()
