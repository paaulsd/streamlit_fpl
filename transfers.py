import requests
import pandas as pd
import numpy as np
import json
import csv
# import re
import os
session = requests.session()
from Elements_translator import Single_Element
from ELement_score import el_points
from Wildcard_freehit_ImmediateGain import WC_FH

def transfers_made(Entry,Gameweek):
    response = session.get(f'https://fantasy.premierleague.com/api/entry/{Entry}/event/{Gameweek}/picks/')
    players_in = []
    players_out=[]
    i=0
    transf_made = response.json()["entry_history"]["event_transfers"]
    active_chip=response.json()["active_chip"]
    #print("Active_chip",Active_chip)



    captain=None
    vice_captain=None

    for data in response.json()["picks"]:
        if data["is_captain"]:
            captain=(data["element"])
        if data["is_vice_captain"]:
            vice_captain=data["element"]
    #print(captain,vice_captain)


    transfer_points_gained=0
    transfer_points_lost = response.json()["entry_history"]["event_transfers_cost"]
    #ŠEIT sāksies JAUNS RESPONE. Visiem iepriekšējiem jāpaliek VIRS šī teksta

    response = session.get(f'https://fantasy.premierleague.com/api/entry/{Entry}/transfers/')

    sum = 0
    for n in response.json():
        if n["event"] == Gameweek:
            sum += 1
            player_out = n["element_out"]
            player_in = n["element_in"]
            #print(Single_Element(player_in), "in for", Single_Element(player_out))
            players_in.append(Single_Element(player_in))
            players_out.append(Single_Element(player_out))
            if player_in == captain:
                transfer_points_gained += 2 * (el_points(player_in, Gameweek)) - el_points(vice_captain, Gameweek)
            else:
                transfer_points_gained += el_points(player_in, Gameweek)
            transfer_points_lost += el_points(player_out, Gameweek)
            #players_in.append(player_in)
            #players_out.append(player_out)
    #print(players_in,players_out)
    #print("Transfers made", sum)

    #while i<sum:


        #return (Single_Element(player_in),"in for",Single_Element(player_out))

        #i += 1

    Immediate_gain = transfer_points_gained - transfer_points_lost
    if (active_chip=="wildcard") or (active_chip=="freehit"):
        #print("Points gained from transfers in this GW (compared to last GW playing 11) =",WC_FH(Entry,Gameweek))
        return (sum, WC_FH(Entry,Gameweek),players_in,players_out)
    else:

        #print("Points gained from transfers in this GW =",Immediate_gain)

        return (sum,Immediate_gain, players_in,players_out)

# print(transfers_made(6460171,4))


def transfers_GW(GW,id):
    address = f"https://fantasy.premierleague.com/api/leagues-h2h/{id}/standings/"
    response = requests.get(address)
    data = response.json()["standings"]
    games_played=data["results"]
    Transfers=[]
    for team in data["results"]:
        Transfers.append({"GW":GW,"Team_name":team["entry_name"],"Players in":", ".join(transfers_made(team["entry"],GW)[2]),"Players out":", ".join(transfers_made(team["entry"],GW)[3]),
                          "Immediate gain":transfers_made(team["entry"],GW)[1]})
        #print(Transfers)
    #print(Transfers)
    # table = pd.DataFrame(Transfers)
    # print(table)
    #print(Transfers)
    return Transfers
    # for team in data["results"]:
    #     d={"Players in":[transfers_made(team["entry"],GW)[2]],
    #        "Players out":[transfers_made(team["entry"],GW)[3]]}
    #     df=pd.DataFrame(data=d)
    #     index = df.index
    #     index.name =team["entry_name"]
    #     df.style.set_table_attributes("style='display:inline'").set_caption(team["entry_name"])
    #     #print(team["entry_name"])
    #     #print(transfers_made(team["entry"],GW))
    #     print(df)
# df=pd.DataFrame(transfers_GW(5,619338))
# print(df)


        # with pd.ExcelWriter('fpl.xlsx', mode='a', engine="openpyxl", if_sheet_exists="replace") as writer:
        #     df.to_excel(writer, sheet_name=f'Current_GW {GW}', index=False)
#transfers_GW(13)

trasfers_list=[]
def transfers_update(Current_GW,id,data):
    with open(f"history\league_transfers_{id}.csv", "a",encoding='utf8') as file:

        df = pd.DataFrame(data)
        df.to_csv(file, header=False,encoding="utf8")

# transfers_update(1,619338)

# f = open('history/league_transfers_619338.csv',encoding='utf8')
# dict_reader=csv.DictReader(f,delimiter=',')
# items=list(dict_reader)
# print(items["GW"])
# for data in items:
#     print(data.get("GW"))




# file1 = open("transfers.txt","r",encoding='utf8')
# transfers_content=json.loads(file1.read())
# GW_transfers = []
# for data in transfers_content:
#     for gw in data:
#         if gw["GW"] == 20:
#             GW_transfers.append(gw)
# df = pd.DataFrame(GW_transfers)
# current_gw_transfers = df.drop(columns=['GW'])
# print(current_gw_transfers)

# file1 = open("history/league_transfers_619338.txt","r",encoding='utf8')
# content=json.loads(file1.read())
# for data in content:
#     print(data["GW"])
# for filename in os.listdir("history"):
#     id = filename.split("_")[-1]
#     id=int(id.split(".")[0])
#     print(id)