from collections import Counter
import math
import requests #requesto info no specifiskas websaites
import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from matplotlib import pyplot
import scipy as sp
import json
def percentage_to_float(value):
    value=float(value.split("%")[0])
    value=value/100
    return value
def percentage(part, whole):
  percentage = round(100 * float(part)/float(whole),2)
  return percentage

#print(percentage(0, 5))
def Expected_Points(win_percentage,draw_percentage):
    Exp_P=((3*win_percentage)+(1*draw_percentage))
    return Exp_P/100

def PlotPolly(model, independent_v, dependent_v, Name):
    x_new = np.linspace(15,55,100)
    y_new = model(x_new)

    plt.plot(independent_v, dependent_v, '.', x_new, y_new, '.')
    plt.title("Polynomial graph")
    ax = plt.gca()
    ax.set_facecolor((0.898, 0.898, 0.898))
    fig = plt.gcf()
    plt.xlabel(Name)
    plt.ylabel('Probability')

    #plt.show()
    plt.close()

def Round_statistics(id,Gameweek):
    print(f"GW{Gameweek}",end=",")
    scores_list = []
    team_list = []

    for number in range(1, 5):
        address = f"https://fantasy.premierleague.com/api/leagues-h2h-matches/league/{id}/?page={number}"
        response = requests.get(address)

        for data in response.json()["results"]:

            if (data["event"] == Gameweek):
                # print(data["entry_1_points"])

                scores_list.append(data["entry_1_points"])
                team_list.append({"Team_name": data["entry_1_name"], "Score":data["entry_1_points"],
                                  "r_points": data["entry_1_total"]})

                scores_list.append(data["entry_2_points"])
                team_list.append({"Team_name": data["entry_2_name"], "Score":data["entry_2_points"],
                                  "r_points": data["entry_2_total"]})
    scores_list.sort()

    # for i,data in enumerate(team_list):
    #     data["r_points"]=i+1
    # print(scores_list)
    ###SĀKAS POLY XP APRĒĶINS
    # first = scores_list[0]
    # last = scores_list[-1]
    # interval = round((last - first) / (len(scores_list) - 1), 3)
    # interval_list = [0]
    # # print(interval)
    # i1 = i2 = i3 = i4 = i5 = i6 = i7 = i8 = 0
    # for i in np.arange(first, (last + 0.05), interval):
    #     interval_list.append((round(i, 3)))
    # if interval_list[-1] < last:
    #     interval_list.pop(-1);
    #     interval_list.append(last)
    #
    # for data in (scores_list):
    #     if data > interval_list[0] and data <= interval_list[1]:
    #         i1 += 1
    #     if data > interval_list[1] and data <= interval_list[2]:
    #         i2 += 1
    #     if data > interval_list[2] and data <= interval_list[3]:
    #         i3 += 1
    #     if data > interval_list[3] and data <= interval_list[4]:
    #         i4 += 1
    #     if data > interval_list[4] and data <= interval_list[5]:
    #         i5 += 1
    #     if data > interval_list[5] and data <= interval_list[6]:
    #         i6 += 1
    #     if data > interval_list[6] and data <= interval_list[7]:
    #         i7 += 1
    #     if data > interval_list[7] and data <= interval_list[8]:
    #         i8 += 1
    #     # for data in scores_list:
    #
    # intervals = [i1, i2, i3, i4, i5, i6, i7, i8]
    #
    # del interval_list[0]
    # # print(interval_list)
    # # print(intervals)
    #
    # #plt.style.use("seaborn-dark-palette")
    #
    # #x = [i for i in range(1, 9)]
    # # plt.plot(x, intervals, label="distr", color="blue", alpha=0.5)
    # # plt.fill_between(x, intervals, where=[(x >= 1) and (x <= 4) for x in x], color="olive")
    # #
    # # plt.title('distr')
    # # plt.xlabel('interval')
    # # plt.ylabel('values')
    # # # plt.show()
    # # plt.close()
    # sq1 = 0;
    # sq2 = (((i2 - i1) / 2)) + i1;
    # sq3 = ((i3 - i2) / 2) + i2;
    # sq4 = ((i4 - i3) / 2) + i3;
    # sq5 = ((i5 - i4) / 2) + i4
    # sq6 = ((i6 - i5) / 2) + i5;
    # sq7 = ((i7 - i6) / 2) + i6;
    # sq8 = ((i8 - i7) / 2) + i7
    # distr_sq = [sq1, sq2, sq3, sq4, sq5, sq6, sq7, sq8]
    # distr_cumulative = [0]
    # for i, data in enumerate(distr_sq):
    #     try:
    #         v = distr_sq[i] + distr_sq[i + 1]
    #     except IndexError:
    #         break
    #     distr_cumulative.append(v + distr_cumulative[i - 1])
    # #print(distr_sq)
    # #print(distr_cumulative)
    # win_pr_list = []
    # for data in distr_cumulative:
    #     win_pr = percentage(data, distr_cumulative[-1])
    #     win_pr_list.append(win_pr)
    # #print(win_pr_list)
    #
    # # calculate polynomial of 6th order
    # x1 = interval_list
    # y1 = win_pr_list
    # print(x1,y1)
    # f = np.polyfit(x1, y1, 6)  # using polyfit funct
    # p = np.poly1d(f)
    # # print(p)
    # coef_list = []
    # for data in p:
    #     coef_list.append(data)
    # # print(coef_list)
    # # coef_list.reverse()
    # # print(coef_list)
    # coef_dict = []
    # # for i,data in enumerate(coef_list):
    # #     coef_dict.append({"Coefficient degree":i,"Value":data})
    # # print(coef_dict)
    # # now plot the function
    # PlotPolly(p, x1, y1, "Scores")
    # xp_poly = []
    # for data in scores_list:
    #     p_win_poly = ((math.pow(data, 6)) * coef_list[0]) + ((math.pow(data, 5)) * coef_list[1]) + (
    #                 (math.pow(data, 4)) * coef_list[2]) \
    #                  + ((math.pow(data, 3)) * coef_list[3]) + ((math.pow(data, 2)) * coef_list[4]) + (
    #                              (math.pow(data, 1)) * coef_list[5]) + (coef_list[6])
    #     xp_poly.append(3 * p_win_poly / 100)
    # #print(xp_poly)
    # ###XP LINEAR aprēķins
    # xp_linear = []
    # #print(interval_list)
    # # print(scores_list)
    #
    #
    # i=0
    # for e,data in enumerate(intervals):
    #     if e==0:
    #         for n in range(data):
    #             xp = ((scores_list[i] - interval_list[e]) / interval) * ((win_pr_list[e] - win_pr_list[e]) / 100) + (win_pr_list[e] / 100)
    #             xp_linear.append(xp*3)
    #             i += 1
    #     else:
    #          for n in range(data):
    #             #print(n,scores_list[i],interval_list[e])
    #             xp=((scores_list[i]-interval_list[e-1])/interval)*((win_pr_list[e]-win_pr_list[e-1])/100)+(win_pr_list[e-1]/100)
    #             xp_linear.append(xp*3)
    #             i+=1
    # #print(intervals)
    # #print(xp_linear)
    # #print(xp_poly)
    # #print(scores_list)
    # # print(team_list)
    # xP_dict = []
    # for i, data in enumerate(scores_list):
    #         xP_dict.append({"Round_score": data, "xP linear": xp_linear[i], "xP poly": xp_poly[i]})
    #
    #
    # # preint(xP_dict)
    #
    Round_scores = []
    i = 0
    # #print(scores_list)
    # #print(team_list)
    # #print(xP_dict)
    for k, v in Counter(scores_list).items():
        # print(k,v)

        if v == 1:
            positive_outcome = len(scores_list[0:i])
            negative_outcome = len(scores_list) - 1
            draw_outcome = 0
            win_pr = percentage(positive_outcome, negative_outcome)
            draw_pr = percentage(draw_outcome, negative_outcome)

            for data in team_list:
                if data["Score"] == k:
                    name = data["Team_name"]
                    round_points = data["r_points"]

            Round_scores.append({"Team_name": name, "Round score": k, "round_points": round_points,
                                 "Win probability": str(win_pr) + "%", "Draw probability": str(draw_pr) + "%",
                                 "Expected Points": Expected_Points(win_pr, draw_pr)})
            i += 1


        else:
            draw_outcome = v - 1
            f_name = ""
            for n in range(1, v + 1):
                positive_outcome = len(scores_list[0:i])
                negative_outcome = len(scores_list) - 1
                win_pr = percentage(positive_outcome, negative_outcome)
                draw_pr = percentage(draw_outcome, negative_outcome)

                for data in team_list:

                    if data["Score"] == scores_list[i]:
                        if data["Team_name"] != f_name:
                            name = data["Team_name"]
                            round_points = data["r_points"]
                f_name = name

                # print(scores_list[i],  "win probability",str(win_pr)+"%","draw probability",str(draw_pr)+"%", Expected_Points(win_pr,draw_pr))
                Round_scores.append(
                    {"Team_name": name, "Round score": scores_list[i], "round_points": round_points,
                     "Win probability": str(win_pr) + "%", "Draw probability": str(draw_pr) + "%",
                     "Expected Points": Expected_Points(win_pr, draw_pr)})

            i += n
    # for score in xP_dict:
    #     for data in Round_scores:
    #         if data["Round score"] == score["Round_score"]:
    #             data["xp_linear"] = score["xP linear"]+percentage_to_float(data['Draw probability'])
    #             data["xP poly"] = score["xP poly"]+percentage_to_float(data['Draw probability'])
    #print(Round_scores)
    return Round_scores
# print(Round_statistics(619338,4))


#print(percentage_to_float("14.54%"))