import os
import sys

if os.environ.get('RH_SEARCHDATE') is None:
    sys.exit("Missing ENV VARIABLE RH_SEARCHDATE")

searchDate = os.environ.get('RH_SEARCHDATE')

# Default portal do RH URL, if it is not configured by env variable
portalURL = os.environ.get(
    "RH_URL",
    "https://www.portaldorh.com.br/portal_rckt/Auto_Principal.aspx"
)

# Default download path, if it is not configured by env variable
defaultDownloadPath = os.environ.get(
    "DOWNLOAD_PATH",
    "/usr/workspace/downloads"
)

# Ensure downloads path exists
if os.path.exists(defaultDownloadPath) is False:
    os.makedirs(defaultDownloadPath)
