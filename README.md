# Portal do RH Download
Download holerite PDF using selenium, chrome and python
## Usage
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
 
## ENV Variable availables

| ENV VARIABLE     | REQUIRED | DEFAULT VALUE                                                 | DESCRIPTION                |
| ---------------- |:--------:|---------------------------------------------------------------|----------------------------|
| RH_SEARCHDATE    | yes      |                                                               | Search date. eg(03/2018)   |
| RH_URL           | no       | https://www.portaldorh.com.br/portal_rckt/Auto_Principal.aspx | Portal do RH login page    |
| DOWNLOAD_PATH    | no       | /usr/workspace/downloads                                      | Where files will be saved. |
| RH_USERNAME      | yes      |                                                               | Your username to login     |
| RH_PASSWORD      | yes      |                                                               | Your password to login     |

## Links
- [GitHub](https://github.com/viniciusgava/portaldorh-holerite-download)
- [Docker Hub](https://hub.docker.com/r/viniciusgava/portaldorh-holerite-download/)