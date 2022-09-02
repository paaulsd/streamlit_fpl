from H2H_round import Round_statistics
import requests #requesto info no specifiskas websaites
import json
from transfers import transfers_GW
import csv
from csv import writer
from csv import reader
import time
Points_delta_list = []
def Get_TeamFixtures(entry,Team_name,GW):
    """Funkcija, kas atgriezīs ievadītās komandas pretiniekus katrā no GW. Kur GW būs beidzies (True/False), parādīs spēles iznākumu,/
    iegūto punktu skaitu (3;1 vai 0), kā arī rezultāta starpību, Expected points"""
    Team_dictionary=[]
    #Points_Total = 0
    #Expected_Total = 0
    for number in range(1,5):
        address=f"https://fantasy.premierleague.com/api/leagues-h2h-matches/league/619338/?page={number}"
        response = requests.get(address)
        #print(response.json()["results"])


        for data in response.json()["results"]:
            if data["event"]==GW:
            #print (data["id"])

                if (data["entry_1_entry"]==entry) or (data["entry_2_entry"]==entry):
                    if data["entry_1_entry"] != entry:
                        users_team=data["entry_2_name"]
                        users_points=data["entry_2_points"]
                        opposition = data["entry_1_name"]
                        opposition_won=data["entry_1_win"]
                        opposition_lost=data["entry_1_loss"]
                        opposition_drew=data["entry_1_draw"]
                    else:
                        users_team=data["entry_1_name"]
                        users_points=data["entry_1_points"]
                        opposition = data["entry_2_name"]
                        opposition_won = data["entry_2_win"]
                        opposition_lost = data["entry_2_loss"]
                        opposition_drew = data["entry_2_draw"]
                    played=False
                    Game_status=""




                    if (data["entry_2_total"] + data["entry_1_total"]) > 0:
                        played=True
                        Points=None
                        for event_score in Round_statistics(619338,data["event"]):

                            if users_points==(event_score["Round score"]):
                                exp_points=round(event_score["Expected Points"],4)
                                exp_points_lin=0#round(event_score["xp_linear"],4)
                                exp_points_poly=0#round(event_score["xP poly"],4)



                        if opposition_won==1:
                            Game_status="LOST"
                            Points=0
                            Score_difference=-1*(abs((data["entry_1_points"])-(data["entry_2_points"])))
                        if opposition_lost==1:
                            Game_status="WON"
                            Points=3
                            Score_difference = abs((data["entry_1_points"]) - (data["entry_2_points"]))
                        if opposition_drew==1:
                            Game_status="DREW"
                            Points=1
                            Score_difference=0

                        #Points_Total+=Points
                        #Expected_Total+=exp_points
                        #print(data["event"], opposition,played, Game_status, Points,Score_difference,exp_points, Points_Total,round(Expected_Total,2))
                        Team_dictionary.append({"gw":data["event"],"opposition":opposition,"played":played,"game_status":Game_status,"Round Score":users_points,
                                               "points":Points,"score_dif":Score_difference,"exp_points":exp_points, "exp_points_linear":exp_points_lin,"exp_points_poly":exp_points_poly})

                    else:
                        adr=f"https://fantasy.premierleague.com/api/entry/4115138/event/{data['event']}/picks/"
                        response=requests.get(adr)
                        if len(response.json().keys())>1:
                            Game_status="ONGOING"
                            Points=None;Score_difference=None;exp_points=None;exp_points_lin=None;exp_points_poly=None
                            Team_dictionary.append({"gw":data["event"],"opposition":opposition,"played":played,"game_status":Game_status,"Round Score":users_points,
                                                     "points":Points,"score_dif":Score_difference,"exp_points":exp_points,"exp_points_linear":exp_points_lin,"exp_points_poly":exp_points_poly})
                        else:
                            pass




        #Points_delta = round(Expected_Total - Points_Total,2)


    #Points_delta_list.append({"Team_name": Team_name, "Expected Total minus Points Total =": Points_delta})
    #Teams_dictionary.append(Team_dictionary)
    return(Team_dictionary)





def Team_History_Data(GW):
    address = f"https://fantasy.premierleague.com/api/leagues-h2h/619338/standings/"
    response = requests.get(address)
    data=response.json()["standings"]
    #print(data.keys())
    History_dict=[]


    for team in data["results"]:
        #print(team)
        #print(team["player_name"],team["entry_name"], team["entry"], "pretinieki: ")
        Team_History_dict = {"player_name":"", "team_name":"", "pretinieki":{}}
        Team_History_dict["player_name"]=(team["player_name"])
        Team_History_dict["team_name"]=(team["entry_name"])
        Team_History_dict["pretinieki"] = Get_TeamFixtures(team["entry"], team["entry_name"],GW)

        History_dict.append(Team_History_dict)
    file = open("team_fixtures_current.txt", "w", encoding='utf8')

    file.write(json.dumps(History_dict, ensure_ascii=False))
    return (History_dict)
print(Team_History_Data(5))

# def update_currentGW(GW):
#     file = open("team_fixtures_current.txt", "w", encoding='utf8')
#     file1=open("transfers_current.txt", "w",encoding='utf8')
#     file1.write(json.dumps(transfers_GW(GW), ensure_ascii=False))
#     file.write(json.dumps(Team_History_Data(GW), ensure_ascii=False))
# update_currentGW(11)