# Portal do RH Download
Download holerite PDF using selenium, chrome and python at Portal do RH.

## Additional Integrations
- E-mail with downloaded PDF attachment by Mail Gun
- Execution notification by Push Bullet

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
Mail Gun API Key
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
**Placeholder Available:** Yes

#### MAIL_GUN_TEXT
Mail content as text
**Required:** Yes if ``MAIL_GUN_HTML`` is not setted
**Placeholder Available:** Yes

#### MAIL_GUN_HTML
Mail content as text
**Required:** Yes if ``MAIL_GUN_TEXT`` is not setted
**Placeholder Available:** Yes

### Push Bullet feature - ENV variables
All Required fields bellow are required **only** if ``PUSH_BULLET_ENABLE`` env setted as ``true``

#### PUSH_BULLET_ENABLE
Integrate with push bullet? true or false
**Required:** No
**Default:** false

#### PUSH_BULLET_TOKEN
Push Bullet API Token
**Required:** Yes

#### PUSH_BULLET_TITLE
Notification Title
**Required:** Yes
**Placeholder Available:** Yes

#### PUSH_BULLET_BODY
Notification Body
**Required:** Yes
**Placeholder Available:** Yes

# Usage - Local
Makefile and instruction bellow expected you uses python3. 
It also expected you already have a chrome webdrive installed. 

1. Clone repository
2. Run ``make prepare-local``
3. Edit ``src/settings/local.py`` file with your information.
4. Run ``python3 src/app.py local`

# Integrations Placeholder
Some integration fields accept placeholder, that means you can use internal fields used on integration on your texts.
Fields that accept placeholders are marked on **Env Variables** of each integration.

## Placeholder syntax
``%(placeholderName)s``
Example:
``This is my holerite at %(search_year)s/%(search_month)s``

## Available placeholders
- search_year
- search_month

## Links
- [GitHub](https://github.com/viniciusgava/portaldorh-holerite-download)
- [Docker Hub](https://hub.docker.com/r/viniciusgava/portaldorh-holerite-download/)
