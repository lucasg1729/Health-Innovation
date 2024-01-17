import httplib2
from bs4 import BeautifulSoup, SoupStrainer

url = 'https://www.sec.gov/Archives/edgar/data/1587143/000095012322010974/0000950123-22-010974-index.htm'

http = httplib2.Http() #opens link

response, content = http.request(url) #returns a tuple so puts both values into variable

links = []

for link in BeautifulSoup(content).find_all('a', href=True): #appends every link to links
    links.append(link['href'])

for link in links:
    print(link)