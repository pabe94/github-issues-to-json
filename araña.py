import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

def main():
    data = []

    elementos = int(input("Cuantos elementos vas a introducir: "))

    for i in range(elementos):
        owner = raw_input("Inserte owner: ")
        repository = raw_input("Inserte repository: ")
        data.append(owner + "/" + repository)

    tamano = len(data)  
    
    for a in range(tamano):
        nuevo = (data[a])
        trade_spider(5, nuevo)
    theend()    

def trade_spider(max_pages, nuevo):
    #mzet-/linux-exploit-suggester/
    #iblancasa/GitHubRankingsSpain

    page=1
    while page <= max_pages:
        url="https://github.com/"+ nuevo + "/issues?page=" + str(page) + "&q=is%3Aissue&utf8=%E2%9C%93"
        source_code = requests.get(url)
        plain_text =source_code.text
        soup = BeautifulSoup(plain_text)
        for link in soup.findAll('a',{'class': 'link-gray-dark v-align-middle no-underline h4 js-navigation-open'}):
            href = "https://github.com/" + link.get('href')
            get_single_item_data(href)
        page += 1

def get_single_item_data(item_url):

    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    
    id = soup.find('span',{'class': 'gh-header-number'}).get_text(strip=True)
    id=remove_firstcharacter(id)
    print(id)

    state = soup.find('div',{'class': 'TableObject-item'}).get_text(strip=True)
    print(state)
    
    name = soup.find('span',{'class': 'js-issue-title'}).get_text(strip=True)
    print(name)
    
    owner = soup.find('a',{'data-pjax': '#js-repo-pjax-container'}).attrs['href']
    owner=remove_firstcharacter(owner)
    print(owner)

    date = soup.find('relative-time',datetime=True).attrs['datetime']
    print(date)

    issues.append({'id': id, 'state':state, 'name': name, 'owner': owner, 'date': date})
    
def remove_firstcharacter(character):
    return character[1:]

def theend():
    issues.sort(reverse=True)
    finaljson = {'issues':issues }
    example = json.dumps(finaljson, indent=3, sort_keys=True) 

    example2 = json.loads(example)  

    count = 0
    count_final = 0
    last_date = datetime.strptime('2050-01-01', '%Y-%m-%d')
    last_date = last_date.strftime('%Y-%m-%d')
    
    date_final = datetime.strptime('1994-01-01', '%Y-%m-%d')
    date_final = date_final.strftime('%Y-%m-%d')

    for item in example2['issues']:
        date = item['date'][:10]

        date = datetime.strptime(date, '%Y-%m-%d')
        date = date.strftime('%Y-%m-%d')

        count += 1
        if date < last_date:
            last_date = date
            if count_final < count:
                count_final = count
                date_final = last_date
                count = 0

    for item in example2['issues']:
        date = item['date'][:10]
        user =item['owner']

        date = datetime.strptime(date, '%Y-%m-%d')
        date = date.strftime('%Y-%m-%d')

        if date_final == date:
            topday.append({'day': date_final, user: count_final})

    finaljson = {'issues':issues,'topday':topday } 
    final= json.dumps(finaljson, indent=3, sort_keys=True)   
    print(final)    

   

#Global variable
issues = []
topday = []

#Call Main
main()
