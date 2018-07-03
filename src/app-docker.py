from docker import credentials
from docker import settings
from downloader import *

docker_settings = settings
docker_settings.headless = True

downloader = Downloader(credentials, docker_settings)
downloader.run()
