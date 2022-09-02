
import streamlit as st
import os
import json
import csv
import pandas as pd
import openpyxl
import numpy as np


from H2H_round import Round_statistics
from transfers import transfers_GW, transfers_update


def overalldf(content):
    overall = []
    for team in content:
        played = 0
        won = 0
        draw = 0
        lost = 0
        exp_points = 0
        exp_linear = 0
        exp_poly = 0
        total_points = 0
        Score = 0
        for data in team["pretinieki"]:
            if data["game_status"] == "WON":
                won += 1
            elif data["game_status"] == "LOST":
                lost += 1
            elif data["game_status"] == "DREW":
                draw += 1
            if data["played"] == True:
                played += 1
            try:
                # exp_poly+=data["exp_points_poly"]
                # exp_linear += data["exp_points_linear"]
                exp_points += data["exp_points"]
                total_points += data["points"]
                Score += data["Round Score"]
            except (TypeError, KeyError):
                exp_poly += 0
                exp_linear += 0
                exp_points += 0
                total_points += 0
                Score += 0
        overall.append(
            {"Team": team["team_name"], "Played": played, "Won": won, "Drawn": draw, "Lost": lost, "Score": Score,
             "Points": total_points, "xP": exp_points,
             "xP Linear": exp_linear, "xP Poly": exp_poly})
    return overall
import matplotlib.pylab as plab
import matplotlib.pyplot as plt
from matplotlib import cm
st.set_page_config(layout="wide")
st.write("""
# FPL SIGULDA
Let's **gooooo**!
""")
def main():
    st.write("Head-to-Head league id: ")

    # only allow strings
    league_id = st.number_input('Insert id (fpl Sigulda=619338)', value=0, step=1)

    # conditional statement to check if the input is a string
    if type(league_id) == int and league_id!=0:
        @st.cache
        def load_data(league_id):
            from Team_Fixtures import Team_History_Data
            result=Team_History_Data(league_id)
            content = result[0]
            finished_gw=result[1]
            things=[content,finished_gw]
            return things
        need=load_data(league_id)
        data=need[0]
        finished_gws=need[1]
        col1, col2 = st.columns([6, 6])
        col1.markdown("""
        Yo here this n that!
        * **Data source:** [fantasy.premierleague.com](https://fantasy.premierleague.com/).
        """)
        check = col2.checkbox("Show Overall Stats")
        if check:
            overall_df = pd.DataFrame(overalldf(data))
            col2.dataframe(overall_df)
        st.sidebar.header('User Input Features')
        gws = list((range(1, 39)))
        overall = ["Overall"]
        big_list = overall + gws
        # print(big_list)
        selected_gw = st.sidebar.selectbox('Gameweek', gws)
        col1.dataframe(Round_statistics(league_id, selected_gw))

        @st.cache
        def load_transfers(league_id):
            tr_content=None
            transfers=[]
            is_in_file=False
            for filename in os.listdir("history"):

                id = filename.split("_")[-1]
                id = int(id.split(".")[0])
                if league_id==id:
                    is_in_file = True
                    print("league is in file")
                    with open(os.path.join("history", filename), 'r', encoding='utf8') as f:
                        dict_reader=csv.DictReader(f,delimiter=',')
                        items=list(dict_reader)
                        i=0
                        for item in items:
                            if int(item.get("GW"))==selected_gw:
                                i+=1
                                transfers.append(item)
                        if i>1:print("these transfers are added to file")
                        if len(transfers)==0:
                            print("this gw wasn't in league file, uploading transfers")
                            if finished_gws - selected_gw <-1:
                                tr_content=None
                            else:
                                try:
                                    # print(finished_gws,selected_gw)
                                    tr_content = transfers_GW(selected_gw, league_id)
                                    if finished_gws>=selected_gw:
                                        transfers_update(selected_gw,league_id,tr_content)
                                        print('updating file...')
                                    else:print("but we won't update file, because gw isn't finished yet")
                                except KeyError as e:
                                    print(e)
            if is_in_file==False:
                print("this league wasn't in our archive")
                if finished_gws - selected_gw <-1:
                    tr_content=None
                else:
                    try:
                        tr_content = transfers_GW(selected_gw, league_id)
                        if finished_gws >= selected_gw:
                            print("adding it now...")
                            with open(f"history\league_transfers_{league_id}.csv", "w",encoding='utf8') as file:
                                df=pd.DataFrame(tr_content)
                                df.to_csv(file, header=True,encoding="utf8")
                        else:print("but we won't add it now because this gw is not finished yet")
                    except KeyError as e:
                        print(e)
            if len(transfers)>0:
                tr_content=transfers
            return tr_content
        
        transfers_data=load_transfers(league_id)
        col1.write("Gameweek Transfers")
        col1.dataframe(transfers_data)
        from visuals_faster import visuals_round
        visuals_round(data,league_id,selected_gw)
    else:
        st.write("Please enter a number")

if __name__ == "__main__":
    main()
