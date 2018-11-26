from bs4 import BeautifulSoup
import requests

def getSchoolFromLeague(leagueUrl, gender):
    tempResponse = requests.get(leagueUrl)
    tempContent = BeautifulSoup(tempResponse.content, "html.parser")
    allLinks = tempContent.find_all('a', href=True)
    schoolLinks = []
    for t in allLinks:
        temp = ''.join(t['href'].split())
        if "tfrrs.org/teams" in temp:
            print(temp)
    return

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
    
    

page_link = 'https://www.tfrrs.org/teams/IA_college_m_Simpson.html'
page_response = requests.get(page_link)
page_content = BeautifulSoup(page_response.content, "html.parser")
textContent = page_content.find_all('a', href=True)

tempLinks = getAthletesFromSchool(page_link)

for t in tempLinks:
    print(t)
print("\n")
getSchoolFromLeague('https://www.tfrrs.org/leagues/1400.html')
        
