import os
import sys

if os.environ.get('RH_SEARCHDATE') is None:
    sys.exit("Missing ENV VARIABLE RH_SEARCHDATE")

search_date = os.environ.get('RH_SEARCHDATE')

# Default portal do RH URL, if it is not configured by env variable
portal_rh = os.environ.get(
    "RH_URL",
    "https://www.portaldorh.com.br/portal_rckt/Auto_Principal.aspx"
)

# Default download path, if it is not configured by env variable
default_download_path = os.environ.get(
    "DOWNLOAD_PATH",
    "/usr/workspace/downloads"
)

# Ensure downloads path exists
if os.path.exists(default_download_path) is False:
    os.makedirs(default_download_path)
