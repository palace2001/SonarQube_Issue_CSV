# SonarQube Python Plugin
# Copyright (C) 2019 Keunpil Kim
# Author(s) : Keunpil Kim
# palacekp92@gmail.com

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software


import csv
import requests



MAX_PAGE_SIZE = 500

def getIssueFromSonar(URL):
    data = requests.get(URL).json()
    total = int(data['total'])
    print('# total issues : ', total)

    if total > MAX_PAGE_SIZE:
        data = []
        for pn in range(1, int(total/MAX_PAGE_SIZE) + 2):
            multiURL = URL +'&p=' + str(pn)
            data += (requests.get(multiURL).json())['issues']

    else:
        data = data['issues']

    return data

def makeCSVFromJson(issueJson, fileName):
    csvFile = open(file=fileName, mode='w', newline='')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['key', 'type', 'rule', 'severity', 'status', 'message', 'file', 'line', 'creationDate'])
    for value in issueJson:
        try:
            csvWriter.writerow([value['key'],
                                value['type'],
                                value['rule'],
                                value['severity'],
                                value['status'],
                                value['message'],
                                value['component'],
                                value['line'],
                                value['creationDate']])
        except KeyError as e:
            if str(e) == '\'line\'':
                csvWriter.writerow([value['key'],
                                    value['type'],
                                    value['rule'],
                                    value['severity'],
                                    value['status'],
                                    value['message'],
                                    value['component'],
                                    0,
                                    value['creationDate']])
            else:
                print('KeyError :' + str(e))



if __name__ == "__main__":
    sonarQubeIP = input('SonarQube IP : ')
    sonarQubeURL = 'http://' + sonarQubeIP + ':9000'
    projectKey = input('Project Key : ')
    requestIssueURL = sonarQubeURL + '/api/issues/search?componentKeys=' + projectKey + '&ps=' + str(MAX_PAGE_SIZE)
    issueJson = getIssueFromSonar(requestIssueURL)
    makeCSVFromJson(issueJson, projectKey + '.csv')
