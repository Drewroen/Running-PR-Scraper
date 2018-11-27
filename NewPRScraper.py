from bs4 import BeautifulSoup
import requests
import csv
import re

def getSchoolsFromLeague(leagueUrl, gender):
    tempResponse = requests.get(leagueUrl)
    tempContent = BeautifulSoup(tempResponse.content, "html.parser")
    allLinks = tempContent.find_all('a', href=True)
    schoolLinks = []
    for t in allLinks:
        temp = ''.join(t['href'].split())
        if "tfrrs.org/teams" in temp:
            if "college_" + gender + "_" in temp:
                schoolLinks.append("http://" + temp[temp.index("tfrrs.org/teams"):])
    return schoolLinks

def getAthletesFromSchool(schoolUrl):
    tempResponse = requests.get(schoolUrl)
    tempContent = BeautifulSoup(tempResponse.content, "html.parser")
    allLinks = tempContent.find_all('a', href=True)
    athleteLinks = []
    for t in allLinks:
        temp = ''.join(t['href'].split())
        if "tfrrs.org/athletes" in temp:
            athleteLinks.append("http://" + temp[temp.index("tfrrs.org/athletes"):])
    return athleteLinks

def getDataFromAthlete(athleteUrl):
    tempResponse = requests.get(athleteUrl)
    tempContent = BeautifulSoup(tempResponse.content, "html.parser")
    athleteName = tempContent.find('h3').text
    allResults = tempContent.find('div', attrs={'id':'meet-results'})
    athleteResults = []
    dateRegex = re.compile("[a-zA-Z]{3} [0-9]{1,2}(-[0-9]{1,2})?, [0-9]{4}")
    for race in allResults.find_all('div'):
        if race.find('thead'):
            meetInfo = ' '.join(race.find('thead').text.split())
            meetName = meetInfo[:dateRegex.search(meetInfo).start()].rstrip()
            meetDate = meetInfo[dateRegex.search(meetInfo).start():]
            tempResult = [athleteName, meetName, meetDate]
            i = 0
            for info in race.find_all('td'):
                if i == 3:
                    athleteResults.append(tempResult)
                    tempResult = [athleteName, meetName, meetDate]
                    i = 0
                tempResult.append(''.join(info.text.split()))
                i = i + 1
            athleteResults.append(tempResult)
    return athleteResults

print("Enter a league URL.")
leagueUrl = input()
finalPRList = []


print("Writing...")
with open("final.csv","w+") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=",", lineterminator='\n')
    for school in getSchoolsFromLeague(leagueUrl, 'm'):
        print(school)
        for athlete in getAthletesFromSchool(school):
            print(athlete)
            csvWriter.writerows(getDataFromAthlete(athlete))
finalPRList.sort(key=lambda x: x[1])
        
