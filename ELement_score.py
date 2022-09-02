"""Šī funkcija atgriezīsies konkrētā spēlētāja punktus, kad tiks ievadīt spēlētāja id un GW nr"""
import requests
import json
session = requests.session()
def el_score(element,round):

    response = session.get(f'https://fantasy.premierleague.com/api/element-summary/{element}/')
    history=response.json()["history"]
    for data in history:
        #print(data)
        if data["round"]==round:
            return data["total_points"]
def el_points(element,round):
    if el_score(element,round)==None:
        return 0
    else:
        return el_score(element,round)


    #print(history)
# print(el_points(357,16))
# print(el_points(233,16))