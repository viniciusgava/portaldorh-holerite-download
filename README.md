# Portal do RH Download
Download holerite PDF using python at Portal do RH.


**⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️**

**⚠️⚠️⚠️⚠️⚠️⚠️ PROJECT ARCHIVE ⚠️⚠️⚠️⚠️⚠️⚠️**

**⚠️⚠️⚠️⚠️⚠️ NO LONGER MAINTAINED ⚠️⚠️⚠️⚠️**


**⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️**

**I no longer have access to Portal do RH, so I cannot follow maintaining this project anymore.**


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

File name is the search year + search month, ``YYYY-MM.pdf``.

**example:**

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

**Default:** https://www.portaldorh.com.br/portal_rckt/auto_default.aspx

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

## Usage - Local
Makefile and instruction bellow expected you uses python3. 
 
1. Clone repository
2. Run ``make prepare-local``
3. Edit ``src/settings/local.py`` file with your information.
4. Run ``python3 src/app.py local``

## Integrations Placeholder
Some integration fields accept placeholder, that means you can use internal fields used on integration on your texts.

Fields that accept placeholders are marked on **Env Variables** of each integration.

### Placeholder syntax
``%(placeholderName)s``
Example:
``This is my holerite at %(search_year)s/%(search_month)s``

### Available placeholders
- search_year
- search_month

## Crontab
First create bash like this:
````bash
#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

# print current date at log
date

# GET LAST MONTH YEAR AND MONTH
LAST_MONTH_YEAR=$(date +'%Y' -d 'last month')
LAST_MONTH_MONTH=$(date +'%m' -d 'last month')

echo "search year: $LAST_MONTH_YEAR"
echo "search month: $LAST_MONTH_MONTH"

# try 5 times
n=0
until [ $n -ge 2 ]
do
    echo "trying $n"
    /usr/bin/docker run --env-file "$SCRIPTPATH/env-configs" \
    -e RH_SEARCH_YEAR="$LAST_MONTH_YEAR" \
    -e RH_SEARCH_MONTH="$LAST_MONTH_MONTH" \
    --rm
    viniciusgava/portaldorh-holerite-download:latest 2>&1 && break
    n=$[$n+1]
    sleep 15
done

````
**Mac tip:** You must to pass docker full path to works at crontab
``/usr/local/bin/docker``

Second add all env variables at ``env-configs``.
Example:
 ````bash
RH_USERNAME=YOUR USERNAME HERE
RH_PASSWORD=YOUR PASSWORD HERE
````
**DO NOT** use quotation to define values on env files.

Then run ``crontab -e`` and add the follow cron.
Example:
````bash
0 8 7 * * sh /home/username/automate/holerite/run.sh  >> /home/username/automate/holerite/log.log
````
The example bellow runs 8am of day 7 of every month. 

You can generate a different crontab config on [https://crontab-generator.org](https://crontab-generator.org) 

## Links
- [GitHub](https://github.com/viniciusgava/portaldorh-holerite-download)
- [Docker Hub](https://hub.docker.com/r/viniciusgava/portaldorh-holerite-download/)
