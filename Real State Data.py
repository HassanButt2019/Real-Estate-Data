import requests
from bs4 import BeautifulSoup
import re
import pandas

url = "http://web.archive.org/web/20160127020422/http://www.century21.com:80/real-estate/rock-springs-wy/LCWYROCKSPRINGS/#t=0&s=10.html"
req = requests.get(url)
html = req.content
soup = BeautifulSoup(html , 'html.parser')

tag = soup.find_all("div",{"class":"propertyRow"})

l = []
for item in tag:
    d = {}
    d["Price"]=item.find("h4",{"class":"propPrice"}).text. replace("\n","").replace(" ","")
    d["Address"]=item.find_all("span",{"class","propAddressCollapse"})[0].text
    d["Locality"]=item.find_all("span", {"class", "propAddressCollapse"})[1].text
    try:
        d["Bed"]=item.find("span",{"class","infoBed"}).find("b").text
    except:
        d["Bed"]="None"
    try:
        d["Area"]=item.find("span",{"class","infoSqFt"}).find("b").text
    except:
        d["Area"]="None"
    try:
        d["Full Bath"]=item.find("span",{"class","infoValueFullBath"}).find("b").text
    except:
        d["Full Bath"]="None"
    try:
        d["Half Bath"]=item.find("span",{"class","infoValueHalfBath"}).find("b").text
    except:
        d["Half Bath"]= "None"
    for coloum_group in item.find_all("div",{"class","columnGroup"}):
        for feature_group,feature_name in zip(coloum_group.find_all("span",{"class":"featureGroup"}),coloum_group.find_all("span",{"class":"featureName"})):
            if "Lot Size" in feature_group.text:
                d["Lot Size"]=feature_name.text

    l.append(d)

df = pandas.DataFrame(l)
df.to_csv("Output.csv")








