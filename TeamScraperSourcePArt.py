from itertools import groupby
from operator import itemgetter
from decimal import Decimal
import urllib.request
import sys
import csv

f = open("Teamlist.txt", "r")
contents = f.readlines()
f.close()
school = []
name = []
time = []
print("Analyzing teams in list...")
for i in contents:
    url = i
    teamName = url[url.find('_m_')+3:]
    teamName = " ".join(teamName[:teamName.find('.')].split('_'))
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8', 'ignore')
        html = html[html.find('<td class="name"')+5:]
        html = html[html.find('<td class="name"'):]
        html = html[:html.find('</table>')]
        html_list = html.split()
        html_new = ""
        for x in html_list:
            if x[:1] == "/":
                html_new = html_new + "https://www.tfrrs.org/athletes" + x[:x.find('"')] + "\n"
        runnerList = html_new.split("\n")
        runnerList = runnerList[:-1]
        print("Analyzing " + (" ".join(teamName.split('_'))) + "...")
        for j in runnerList:
            with urllib.request.urlopen(j) as runnerStats:
                runnerStatsString = runnerStats.read().decode('utf-8', 'ignore')
                runnerName = runnerStatsString[runnerStatsString.find('<title>TFRRS | ')+15:]
                runnerName = runnerName[:runnerName.find("\n")]
                runnerStatsString = runnerStatsString[runnerStatsString.find('id="results_data">'):]
                runnerStatsString = "\n".join(runnerStatsString.split())
                runnerStatsString = runnerStatsString[runnerStatsString.find("<tr"):runnerStatsString.find("</table>")]
                races = runnerStatsString.split('<tr')
                races_date = [x[x.find('date">')+6:] for x in races]
                races_date = [x[x.find('-')+1:] for x in races_date]
                races_date = [x[x.find('-')+1:] for x in races_date]
                races_date = [x[0:2] for x in races_date]
                races_event = [x[x.find('event">')+8:] for x in races]
                races_event = [x[:x.find('<')-1] for x in races_event]
                races_time = [x[x.find('mark')+4:] for x in races]
                races_time = [x[x.find('HREF=')+4:] for x in races_time]
                races_time = [x[x.find('>')+1:x.find('<')] for x in races_time]
                best = "NULL"
                races_final = zip(races_event, races_time, races_date)
                for k in races_final:
                    if k[0] == "8K" and k[2] == "17":
                        if best == "NULL" and k[1] != "DNF" and k[1] != "DNS":
                            best = k[1]
                        elif k[1] != "DNF" and k[1] != "DNS":
                            p1, p2 = k[1].split(':')
                            b1, b2 = best.split(':')
                            if (int(p1) * 60) + Decimal(p2) < (int(b1) * 60) + Decimal(b2):
                                best = k[1]
                school.append(teamName)
                name.append(runnerName)
                time.append(best)
results = zip(school, name, time)
sortedResults = sorted(results, key=lambda item: item[2])
schoolList = list(set(school))
print("School\tRunner\tTime\tRunning\tPlace\tTeam Place\tScore(PR)\tScore(-1)\tScore(-5)\t\tTeam\tScore(PR)\tScore(-1)\tScore(-5)")
j = 1
with open('Results.csv', 'w', newline='') as results:
    scoreWriter = csv.writer(results)
    scoreWriter.writerow(["School", "Runner", "Time", "Running?", "Place", "Team Place", "Score(PR)", "Score(-1)", "Score(-5)", "", "", "Score(PR)", "Score(-1)", "Score(-5)"])
    for i in sortedResults:
        if i[2] != "NULL":
            if len(schoolList) >= j:
                schoolW = i[0]
                runnerW = i[1]
                timeW = i[2]
                runningW = 'Y'
                placeW = ('=IF(D'+str(j+1)+'="Y",MAX($E$1:E'+str(j)+')+1,"-")')
                teamPlaceW = ('=IF(D'+str(j+1)+'="Y",IF(COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y")>0,COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y"),"-"),"-")')
                scorePRW = ('=IF(F'+str(j+1)+' <= 7, MAX($G$1:G'+str(j)+')+1, "-")')
                scoreFirstW = ('=IF(F'+str(j+1)+'<>1,IF(F'+str(j+1)+'<=8,MAX($H$1:H'+str(j)+')+1,"-"),"-")')
                scoreFifthW = ('=IF(F'+str(j+1)+'<>5,IF(F'+str(j+1)+'<=8,MAX($I$1:I'+str(j)+')+1,"-"),"-")')
                spaceW = ''
                finalSchoolW = schoolList[j-1]
                finalScorePRW = ('=IF(COUNTIFS($A$2:$A$10000,K'+str(j+1)+',$D$2:$D$10000,"Y")>=5,SUMIFS($G$2:$G$10000,$A$2:$A$10000, K'+str(j+1)+',$F$2:$F$10000, "<=5"),"N/A")')
                finalScoreFirstW = ('=IF(COUNTIFS($A$2:$A$10000,K'+str(j+1)+',$D$2:$D$10000,"Y")>=6,SUMIFS($H$2:$H$10000,$A$2:$A$10000, K'+str(j+1)+',$F$2:$F$10000, "<=6", $F$2:$F$10000, ">1"),"N/A")')
                finalScoreFifthW = ('=IF(COUNTIFS($A$2:$A$10000,K'+str(j+1)+',$D$2:$D$10000,"Y")>=6,SUMIFS($I$2:$I$10000,$A$2:$A$10000, K'+str(j+1)+',$F$2:$F$10000, "<=6", $F$2:$F$10000, "<>5"),"N/A")')
                scoreWriter.writerow([schoolW, runnerW, timeW, runningW, placeW, teamPlaceW, scorePRW, scoreFirstW, scoreFifthW, spaceW, finalSchoolW, finalScorePRW, finalScoreFirstW, finalScoreFifthW])
                print(i[0] + "\t"+ i[1] + "\t" + i[2] + "\t" + "Y" + "\t" + '=IF(D'+str(j+1)+'="Y",MAX($E$1:E'+str(j)+')+1,"-")' + "\t" + '=IF(D'+str(j+1)+'="Y",IF(COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y")>0,COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y"),"-"),"-")' + "\t" + '=IF(F'+str(j+1)+' <= 7, MAX($G$1:G'+str(j)+')+1, "-")' + "\t" + '=IF(F'+str(j+1)+'<>1,IF(F'+str(j+1)+'<=8,MAX($H$1:H'+str(j)+')+1,"-"),"-")' + "\t" + '=IF(F'+str(j+1)+'<>5,IF(F'+str(j+1)+'<=8,MAX($I$1:I'+str(j)+')+1,"-"),"-")' + "\t\t" + schoolList[j-1] + "\t" + '=IF(COUNTIFS($A$2:$A$10000,K'+str(j+1)+',$D$2:$D$10000,"Y")>=5,SUMIFS($G$2:$G$10000,$A$2:$A$10000, K'+str(j+1)+',$F$2:$F$10000, "<=5"),"N/A")' + "\t" + '=IF(COUNTIFS($A$2:$A$10000,K'+str(j+1)+',$D$2:$D$10000,"Y")>=6,SUMIFS($H$2:$H$10000,$A$2:$A$10000, K'+str(j+1)+',$F$2:$F$10000, "<=6", $F$2:$F$10000, ">1"),"N/A")' + "\t" + '=IF(COUNTIFS($A$2:$A$10000,K'+str(j+1)+',$D$2:$D$10000,"Y")>=6,SUMIFS($I$2:$I$10000,$A$2:$A$10000, K'+str(j+1)+',$F$2:$F$10000, "<=6", $F$2:$F$10000, "<>5"),"N/A")')
            else:
                schoolW = i[0]
                runnerW = i[1]
                timeW = i[2]
                runningW = 'Y'
                placeW = ('=IF(D'+str(j+1)+'="Y",MAX($E$1:E'+str(j)+')+1,"-")')
                teamPlaceW = ('=IF(D'+str(j+1)+'="Y",IF(COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y")>0,COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y"),"-"),"-")')
                scorePRW = ('=IF(F'+str(j+1)+' <= 7, MAX($G$1:G'+str(j)+')+1, "-")')
                scoreFirstW = ('=IF(F'+str(j+1)+'<>1,IF(F'+str(j+1)+'<=8,MAX($H$1:H'+str(j)+')+1,"-"),"-")')
                scoreFifthW = ('=IF(F'+str(j+1)+'<>5,IF(F'+str(j+1)+'<=8,MAX($I$1:I'+str(j)+')+1,"-"),"-")')
                print(i[0] + "\t"+ i[1] + "\t" + i[2] + "\t" + "Y" + "\t" + '=IF(D'+str(j+1)+'="Y",MAX($E$1:E'+str(j)+')+1,"-")' + "\t" + '=IF(D'+str(j+1)+'="Y",IF(COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y")>0,COUNTIFS($A$2:A'+str(j+1)+',A'+str(j+1)+',$D$2:D'+str(j+1)+',"Y"),"-"),"-")' + "\t" + '=IF(F'+str(j+1)+' <= 7, MAX($G$1:G'+str(j)+')+1, "-")' + "\t" + '=IF(F'+str(j+1)+'<>1,IF(F'+str(j+1)+'<=8,MAX($H$1:H'+str(j)+')+1,"-"),"-")' + "\t" + '=IF(F'+str(j+1)+'<>5,IF(F'+str(j+1)+'<=8,MAX($I$1:I'+str(j)+')+1,"-"),"-")')
                scoreWriter.writerow([schoolW, runnerW, timeW, runningW, placeW, teamPlaceW, scorePRW, scoreFirstW, scoreFifthW])
        j = j + 1
