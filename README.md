# Portal do RH Download
Download holerite PDF using selenium, chrome and python at Portal do RH
## Usage - Docker

```
docker run -v $(pwd):/usr/workspace/downloads \
    -e RH_USERNAME='YOUR USER NAME HERE' \
    -e RH_PASSWORD='YOUR PASSWORD' \
    -e RH_SEARCHDATE='03/2018' \
    viniciusgava/portaldorh-holerite-download:latest
```
The above command will save pdf in ``$(pwd)``, it means the directory where you run it.
File name is the search date, ``MM-YYYY.pdf``.

**eg:**

``03-2018.pdf``
 
### Container ENV variables

| ENV VARIABLE     | REQUIRED | DESCRIPTION                | DEFAULT VALUE                                                 |
| ---------------- |:--------:|----------------------------|---------------------------------------------------------------|
| RH_SEARCHDATE    | yes      | Search date. eg(03/2018)   |                                                               |
| RH_URL           | no       | Portal do RH login page    | https://www.portaldorh.com.br/portal_rckt/Auto_Principal.aspx |
| DOWNLOAD_PATH    | no       | Where files will be saved. | /usr/workspace/downloads                                      |
| RH_USERNAME      | yes      | Your username to login     |                                                               |
| RH_PASSWORD      | yes      | Your password to login     |                                                               |

# Usage - Local
Makefile and instruction bellow expected you uses python3. 
It also expected you already have a chrome webdrive installed. 

1. Clone repository
2. Run ``make prepare-local``
3. Edit both files ``src/local/credentials.py``and ``src/local/settings.py`` with your information.
4. Run ``python3 src/app-local.py``

## Links
- [GitHub](https://github.com/viniciusgava/portaldorh-holerite-download)
- [Docker Hub](https://hub.docker.com/r/viniciusgava/portaldorh-holerite-download/)
