# Portal do RH Download
Download holerite PDF using selenium, chrome and python at Portal do RH
## Usage - Docker

```
docker run -v $(pwd):/usr/workspace/downloads \
    -e RH_USERNAME='YOUR USERNAME HERE' \
    -e RH_PASSWORD='YOUR PASSWORD HERE' \
    -e RH_SEARCH_YEAR='2018' \
    -e RH_SEARCH_MONTH='03' \
    viniciusgava/portaldorh-holerite-download:latest
```
The above command will save pdf in ``$(pwd)``, it means the directory where you run it.
File name is the search date, ``YYYY-MM.pdf``.

**eg:**

``2018-03.pdf``
 
### Download feature - ENV variables

#### RH_SEARCH_YEAR
Search Year
**Required:** Yes

#### RH_SEARCH_MONTH
Search Month
**Required:** Yes

### RH_USERNAME
Your username to login
**Required:** Yes

### RH_PASSWORD
Your password to login
**Required:** Yes

#### RH_URL
Portal do RH URL
**Required:** No
**Default:** https://www.portaldorh.com.br/portal_rckt/Auto_Principal.aspx

### DOWNLOAD_PATH
Where files will be saved.
**Required:** No
**Default:** /usr/workspace/downloads

### Mail Gun feature - ENV variables
All Required fields bellow are required **only** if ``MAIL_GUN_ENABLE`` env setted as ``true``

#### MAIL_GUN_ENABLE
Integrate with mail gun? true or false
**Required:** No
**Default:** false

#### MAIL_GUN_KEY
Mail Gun Api Key
**Required:** Yes

#### MAIL_GUN_DOMAIN
Mail Gun Domain
**Required:** Yes

#### MAIL_GUN_FROM
Mail origin
**Required:** Yes
**Example:**: Name <name@mail.com>

#### MAIL_GUN_TO
Mail destination
**Required:** Yes
**Example:**: Name <name@mail.com>

#### MAIL_GUN_SUBJECT
Mail subject
**Required:** Yes

#### MAIL_GUN_TEXT
Mail content as text
**Required:** Yes if ``MAIL_GUN_HTML`` is not setted

#### MAIL_GUN_HTML
Mail content as text
**Required:** Yes if ``MAIL_GUN_TEXT`` is not setted

# Usage - Local
Makefile and instruction bellow expected you uses python3. 
It also expected you already have a chrome webdrive installed. 

1. Clone repository
2. Run ``make prepare-local``
3. Edit ``src/settings/local.py`` file with your information.
4. Run ``python3 src/app-local.py local``

## Links
- [GitHub](https://github.com/viniciusgava/portaldorh-holerite-download)
- [Docker Hub](https://hub.docker.com/r/viniciusgava/portaldorh-holerite-download/)
