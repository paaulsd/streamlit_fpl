import requests
import json
session = requests.session()

def Multiple_elements(elements):
    """Šī funkcija "iztulkos" komandas sastāvu, kad ir ievadīta LISTE ar spēlētāju id vērtībām (jeb data['element']), pie tam izdalot kapteini ar True/False """
    session = requests.session()
    response = session.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    data = (response.json()["elements"])
    players=[]

    for player in elements:
        is_captain=False
        if (type(player) == str):
            is_captain=True
            multiplier=2
            player = int(player.split(" ")[0])
        elif type(player)==float:
            multiplier=0
        else:
            multiplier=1


        for i in data:
            if i["id"] == player:
                if is_captain:
                    players.append({"name":i["web_name"],"multiplier":multiplier})
                else:
                    players.append({"name":i["web_name"],"multiplier":multiplier})
    return (players)


def Single_Element(element):
    """Šī funkcija "iztulkos" VIENA spēlētāja vārdu,kad ir ievadīts spēlētāja id numurs (jeb data['element'])"""
    session = requests.session()
    response = session.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    data = (response.json()["elements"])

    for i in data:
        if i["id"] == element:
            # print(i)
            return i["web_name"]


# print(Single_Element(233))