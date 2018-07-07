import os
import sys

from util.ObjectDic import ObjectDic

portal_rh = ObjectDic({})

# Portal do RH username
if os.environ.get('RH_USERNAME') is None:
    sys.exit("Missing ENV VARIABLE RH_USERNAME")

portal_rh['username'] = os.environ.get('RH_USERNAME')

# Portal do RH password
if os.environ.get('RH_PASSWORD') is None:
    sys.exit("Missing ENV VARIABLE RH_PASSWORD")

portal_rh['password'] = os.environ.get('RH_PASSWORD')

# Portal do RH Search Date
if os.environ.get('RH_SEARCH_YEAR') is None:
    sys.exit("Missing ENV VARIABLE RH_SEARCH_YEAR")

search_year = os.environ.get('RH_SEARCH_YEAR')

# Portal do RH Search Date
if os.environ.get('RH_SEARCH_MONTH') is None:
    sys.exit("Missing ENV VARIABLE RH_SEARCH_MONTH")

search_month = os.environ.get('RH_SEARCH_MONTH')

# Portal do RH URL
portal_rh['url'] = os.environ.get(
    "RH_URL",
    "https://www.portaldorh.com.br/portal_rckt/Auto_Principal.aspx"
)

# Download Path
default_download_path = os.environ.get(
    "DOWNLOAD_PATH",
    "/usr/workspace/downloads"
)
# Ensure downloads path exists
if os.path.exists(default_download_path) is False:
    os.makedirs(default_download_path)

headless = True

# Mail Gun - Enable?
mailgun = ObjectDic({
    'enable': os.environ.get("MAIL_GUN_ENABLE", 'false')
})
mailgun.enable = mailgun.enable != 'false'

# Mail Gun
if mailgun.enable:
    # Mail Gun - Api Key
    if os.environ.get('MAIL_GUN_KEY') is None:
        sys.exit("Missing ENV VARIABLE MAIL_GUN_KEY")

    mailgun['api_key'] = os.environ.get('MAIL_GUN_KEY')

    # Mail Gun - Api Domain
    if os.environ.get('MAIL_GUN_DOMAIN') is None:
        sys.exit("Missing ENV VARIABLE MAIL_GUN_DOMAIN")

    mailgun['domain'] = os.environ.get('MAIL_GUN_DOMAIN')

    # Mail Gun - From
    if os.environ.get('MAIL_GUN_FROM') is None:
        sys.exit("Missing ENV VARIABLE MAIL_GUN_FROM")

    mailgun['from'] = os.environ.get('MAIL_GUN_FROM')

    # Mail Gun - To
    if os.environ.get('MAIL_GUN_TO') is None:
        sys.exit("Missing ENV VARIABLE MAIL_GUN_TO")

    mailgun['to'] = os.environ.get('MAIL_GUN_TO')

    # Mail Gun - Subject
    if os.environ.get('MAIL_GUN_SUBJECT') is None:
        sys.exit("Missing ENV VARIABLE MAIL_GUN_SUBJECT")

    mailgun['subject'] = os.environ.get('MAIL_GUN_SUBJECT')

    # Mail Gun - Text or Html
    if (os.environ.get('MAIL_GUN_TEXT') is None and
        os.environ.get('MAIL_GUN_HTML') is None):
        sys.exit("Missing ENV VARIABLE MAIL_GUN_TEXT or MAIL_GUN_HTML")

    # Mail Gun - Text
    if os.environ.get('MAIL_GUN_TEXT') is not None:
        mailgun['text'] = os.environ.get('MAIL_GUN_TEXT')

    # Mail Gun - Html
    if os.environ.get('MAIL_GUN_HTML') is not None:
        mailgun['html'] = os.environ.get('MAIL_GUN_HTML')
