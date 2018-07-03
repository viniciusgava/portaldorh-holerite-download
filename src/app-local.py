from local import credentials
from local import settings
from downloader import *

downloader = Downloader(credentials, settings)
downloader.run()
