from bs4 import BeautifulSoup
import requests

def getSchoolsFromLeague(leagueUrl, gender):
    tempResponse = requests.get(leagueUrl)
    tempContent = BeautifulSoup(tempResponse.content, "html.parser")
    allLinks = tempContent.find_all('a', href=True)
    schoolLinks = []
    for t in allLinks:
        temp = ''.join(t['href'].split())
        if "tfrrs.org/teams" in temp:
            if "college_" + gender + "_" in temp:
                schoolLinks.append(temp[temp.index("tfrrs.org/teams") + 16:])
    return schoolLinks

def getAthletesFromSchool(schoolUrl):
    tempResponse = requests.get(schoolUrl)
    tempContent = BeautifulSoup(tempResponse.content, "html.parser")
    allLinks = tempContent.find_all('a', href=True)
    athleteLinks = []
    for t in allLinks:
        temp = ''.join(t['href'].split())
        if "tfrrs.org/athletes" in temp:
            athleteLinks.append(temp[temp.index("tfrrs.org/athletes") + 19:])
    return athleteLinks


print("Enter a conference or region URL.")
leagueUrl = input()
for school in getSchoolsFromLeague(leagueUrl, 'm'):
    for t in getAthletesFromSchool("http://tfrrs.org/teams/"+school):
        print(t)
        
