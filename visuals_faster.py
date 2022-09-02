from H2H_round import Round_statistics
import json
import pandas as pd
import openpyxl
import numpy as np
import requests
import streamlit as st
import matplotlib.pylab as plab
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
#file1 = open("team_fixtures_current.txt","r",encoding='utf8')
# file1 = open("team_fixtures.txt","r",encoding='utf8')
# content=json.loads(file1.read())

def legends(entry,Gameweek):


    response = requests.get(f'https://fantasy.premierleague.com/api/entry/{entry}/event/{Gameweek}/picks/')

    points=response.json()["entry_history"]["points"]
    deduct=response.json()["entry_history"]["event_transfers_cost"]
    points_total=points-deduct

    Team_score={"Round score":points_total}
    return Team_score
def legends_table(GW):
    legends_id=[2,2128298,56371]
    legends_list=[]
    for data in legends_id:
        response = requests.get(f'https://fantasy.premierleague.com/api/entry/{data}/')
        name=response.json()["player_first_name"]
        surname=response.json()["player_last_name"]
        player={"Team_name":name+" "+surname}
        player.update(legends(data,GW))
        legends_list.append(player)
    table=pd.DataFrame(legends_list)
    return table

def graph_GW_scores(Team_names,Scores,GW,team_colors):
    fig, ax = plt.subplots()
    #plt.style.use("seaborn-dark-palette")
    plt.style.use('dark_background')
    # print(Team_names,team_colors)
    colors1=[]
    #print(colors)
    no_of_colors=int(len(Team_names)/2)
    colormap = cm.get_cmap('Accent', no_of_colors)#Accent, #hsv
    color_array = [colormap(i / no_of_colors) for i in range(no_of_colors)]
    c_array=[]
    for data in color_array:
        c_array.append(data)
        c_array.append(data)
    # print(c_array,len(c_array))
    for data in Team_names:
        for i in range(len(c_array)):
            if team_colors[i]==data:
                colors1.append(c_array[i])
    #print(colors,colors1)
    #colors1.extend(legends)
    x_pos = np.arange(len(Team_names))
    bars = ax.bar(x_pos, Scores, align='center',color=colors1)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(Team_names,rotation=45)
    ax.set_ylabel('Round_Score')
    ax.set_title('Gameweek {} Scores'.format(GW))
    ax.bar_label(bars, fmt='%.0f')
    plt.tight_layout()
    #ax.set_ylim(top=150)  # adjust xlim to fit labels
    # plt.show()
    figure = plt.gcf()
    figure.set_size_inches(13, 5,forward=True)
    st.pyplot(figure)
    # plt.show()



    #plt.savefig(f"fpl_plot{GW}.png", dpi=80)

    #plt.close()
    # wb = openpyxl.load_workbook('output.xlsx')
    # ws=wb[f"GW{GW}"]
    # w_current = ws.active
    #
    # img = openpyxl.drawing.image.Image(f"fpl_plot{GW}.png")
    # ws.add_image(img, "I1")
    # wb.save('output.xlsx')

def visuals_round(content,id,GW):
    #print("Round", GW)
    address = f"https://fantasy.premierleague.com/api/leagues-h2h/{id}/standings/"
    response = requests.get(address)
    data = response.json()["standings"]
    a = []

    for team in data["results"]:
        me = (team["entry_name"])
        if a.count(me) == 0:
            a.append(me)
            for data in content:
                if data["team_name"]==me:
                    for pretinieki in data["pretinieki"]:
                        if pretinieki["gw"] == GW:
                            opp = pretinieki["opposition"]
                            a.append(opp)
    print(a)
    table=pd.DataFrame(Round_statistics(id,GW))
    df1 = table[["Team_name","Round score"]]
    #result=df1.append(legends_table(GW),ignore_index=True)

    #print(result)


    graph_GW_scores(df1["Team_name"],df1["Round score"],GW,a)
    #return fig
def graph_overall(x,y,y1,y2,y3,y4,y5,y6,y7):


    plt.style.use("seaborn-dark-palette")
    plt.plot(x, y, label="MANA", color="crimson")
    plt.plot(x, y1, label="Priedes",color="darkviolet")
    plt.plot(x, y2, label="Stabrid aleshec",color="dodgerblue")
    plt.plot(x, y3, label="SHAWTIME",color="c")
    plt.plot(x, y4, label="Jaunieši FC",color="g")
    plt.plot(x, y5, label="Dinamo Riga",color="darkorange")
    plt.plot(x, y6, label="Tony Hibbert horse",color="red")
    plt.plot(x, y7, label="Robben FC",color="grey")

    # naming the x axis
    plt.xlabel('Gameweek')
    # naming the y axis
    plt.ylabel('Score')
    # giving a title to my graph
    plt.title('Sigulda H2H Overall scores')

    # show a legend on the plot
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    # function to show the plot
    #plt.show()
    figure = plt.gcf()
    figure.set_size_inches(10, 4)
    plt.savefig("Overall.png", dpi=80)
    plt.close()
    wb = openpyxl.load_workbook('FPL.xlsx')

    ws=wb.active

    img = openpyxl.drawing.image.Image("Overall.png")
    ws.add_image(img, "K1")
    wb.save('FPL.xlsx')

def overall_points(GW):
    x=[]
    y=[0]
    y1=[0]
    y2=[0]
    y3=[0]
    y4 = [0]
    y5 = [0]
    y6 = [0]
    y7 = [0]

    New_val=0
    for i in range (1,GW+1):
        x.append(i)
        #print(y)
        for data in Round_statistics(i):
            if data["Team_name"]=="MANA":
                m=data["Round score"]
                y.append(y[i-1]+m)
            if data["Team_name"] == "Priedes":
                m = data["Round score"]
                y1.append(y1[i-1]+m)
            if data["Team_name"] == "Stabrid aleshec":
                m = data["Round score"]
                y2.append(y2[i-1]+m)
            if data["Team_name"] == "SHAWTIME":
                m = data["Round score"]
                y3.append(y3[i-1]+m)
            if data["Team_name"] == "Jaunieši FC":
                m = data["Round score"]
                y4.append(y4[i-1]+m)
            if data["Team_name"] == "Dinamo Riga":
                m = data["Round score"]
                y5.append(y5[i-1]+m)
            if data["Team_name"] == "Tony Hibbert horse":
                m = data["Round score"]
                y6.append(y6[i-1]+m)
            if data["Team_name"] == "Robben FC":
                m = data["Round score"]
                y7.append(y7[i-1]+m)
    y.pop(0);y1.pop(0);y2.pop(0);y3.pop(0);y4.pop(0);y5.pop(0);y6.pop(0);y7.pop(0)
    return (x,y,y1,y2,y3,y4,y5,y6,y7)

def main(id,gw):

    visuals_round(id,gw)


# main(619338,4)

def ov_graph(gw):
    graph_overall(*overall_points(gw))

#ov_graph(20)