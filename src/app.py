import argparse
import logging
import sys

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

# Configure logger
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

downloader = Downloader(settings, logger)
result = downloader.run()

if result:
    mailgun = Mailgun(settings, logger)
    mailgun.send()
