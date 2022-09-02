
from Elements_translator import Single_Element,Multiple_elements
import requests
import json
session = requests.session()

def pre_wildcard_points(elements,round):
    """Šī funkcija "iztulkos" komandas sastāvu, kad ir ievadīta LISTE ar spēlētāju id vērtībām (jeb data['element']), pie tam izdalot kapteini ar True/False """
    possible_points=0
    for player in elements:
        if (type(player) == str):
            is_captain = True
            player = int(player.split(" ")[0])
        else:
            is_captain = False

        session = requests.session()
        response = session.get(f"https://fantasy.premierleague.com/api/element-summary/{player}/")
        data=(response.json())
        for i in (data["history"]):
            #print(i["round"])
            if i["round"]==round:
                #print(Single_Element(player)," ",i["total_points"])
                if is_captain:
                    possible_points+=2*i["total_points"]
                else:
                    possible_points+=i["total_points"]
                break

    # print(possible_points)
    return (possible_points)

def WC_FH(Entry,GW):
    """Funkcija, kas parādīs datus par konkrēto komandu konkrētajā GW un 1 GW iepriekš. Šis TIKAI priekš WC,FH (transfer cost=0"""

    response = session.get(f'https://fantasy.premierleague.com/api/entry/{Entry}/event/{GW}/picks/')
    players = []
    # print(response.json())
    GW_points=response.json()["entry_history"]["points"]
    # print(GW_points)
    #print("Bench points", response.json()["entry_history"]["points_on_bench"])
    response = session.get(f'https://fantasy.premierleague.com/api/entry/{Entry}/event/{GW-1}/picks/')
    for data in (response.json()["picks"]):
        # print(data["element"])
        if (data["multiplier"] == 2):
            Captain = str(data["element"]) + " Captain"
            players.append(Captain)
        elif (data["multiplier"] == 0):
            pass
        else:
            players.append(data["element"])
    # print(players)
    #print("Possible points =",pre_wildcard_points(players,GW))
    #print("points gained =",GW_points - pre_wildcard_points(players,GW))
    return(GW_points - pre_wildcard_points(players,GW))

# print(WC_FH(6460171,4))