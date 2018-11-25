from bs4 import BeautifulSoup
import requests

page_link = 'https://www.tfrrs.org/teams/IA_college_m_Simpson.html'
page_response = requests.get(page_link, timeout=5)
page_content = BeautifulSoup(page_response.content, "html.parser")
textContent = page_content.find_all('a', href=True)
for link in textContent:
    temp = link['href']
    if "athletes" in temp:
        print(link.text)
        print(temp)
        
