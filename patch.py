import re
import json
import random
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient


### Requesting for Words to Scrape
word_site = "https://www.mit.edu/~ecprice/wordlist.100000"
response = requests.get(word_site)
WORDS = response.content.splitlines()
stringlist = [x.decode('utf-8') for x in WORDS]
first_word = random.choice(stringlist)
second_word = random.choice(stringlist)
print(first_word + " " +  second_word)


### Authenticating ScrapperAPI
client = ScraperAPIClient('6f032d750b8194e55a230a24ad3426ba')
url = f'https://www.google.com/search?q=%22{first_word}+{second_word}%22+%22gmail.com%22&num=90'
result = client.get(url).text


### Using BeautifulSoup for conveting Html to Normal text
soup = BeautifulSoup(result, features="html.parser")
sp =  soup.get_text()
emails_list = re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com", sp)
#print(emails_list)


# Some important variables which are required in both "If" and "Else" statement
lp = 0
emails = ""


# Used if/else statement because Discord has a hard limit of 2000 characters per Message ;)
while lp < len(emails_list):

  emails += f'{emails_list[lp]}\n'
  lp += 1

print(emails)
print(len(emails_list))


air_url = 'https://api.airtable.com/v0/appCe79jTEL5pg9ed/Table%201'
headers = {'Authorization': 'Bearer keyLDD20jdc6kSgf6' ,'content-type': 'application/json'}

myobj = {
  "records": [
    {
      "fields": {
        "Name": datetime.utcnow().strftime("%d/%m/%Y %H:%M:%S"),
        "Notes": emails
      }
    }
  ]
}

requests.post(air_url, data=json.dumps(myobj), headers=headers)