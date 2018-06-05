from matplotlib import pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy as np
import csv


files_loc = "/media/akalanka/Engineering/Final Year Project/edited files linkwise/"
specific_links_list = ["26Gy1310x23"]

def draw_map(x, y, show=False, save_loc=None, title=None):
    plt.ylabel("Time")
    plt.xlabel("Attenuation")
    plt.title(title)
    plt.plot(x,y)

    if show:
        plt.show()
    if save_loc is not None:
        plt.savefig()


def attenuation_maps(files_loc, links=None):
    onlyfiles = [f for f in listdir(files_loc) if isfile(join(files_loc, f))]

    columns = ["Source1",
               "Source2",
               "date_time",
               "AVG_TSL_FRM_S1",
               "AVG_RSL_TO_S2",
               "AVG_TSL_FRM_S2",
               "AVG_RSL_TO_S1",
               "ATTN_S1_S2_Watts",
               "ATTN_S1_S2_dBm",
               "ATTN_S2_S1_Watts",
               "ATTN_S2_S1_dBm"]


    x = ["0000", "0015", "0030", "0045", "0100",
         "0115", "0130", "0145", "0200",
         "0215", "0230", "0245", "0300",
         "0315", "0330", "0345", "0400",
         "0415", "0430", "0445", "0500",
         "0515", "0530", "0545", "0600",
         "0615", "0630", "0645", "0700",
         "0715", "0730", "0745", "0800",
         "0815", "0830", "0845", "0900",
         "0915", "0930", "0945", "1000",
         "1015", "1030", "1045", "1100",
         "1115", "1130", "1145", "1200",
         "1215", "1230", "1245", "1300",
         "1315", "1330", "1345", "1400",
         "1415", "1430", "1445", "1500",
         "1515", "1530", "1545", "1600",
         "1615", "1630", "1645", "1700",
         "1715", "1730", "1745", "1800",
         "1815", "1830", "1845", "1900",
         "1915", "1930", "1945", "2000",
         "2015", "2030", "2045", "2100",
         "2115", "2130", "2145", "2200",
         "2215", "2230", "2245", "2300",
         "2315", "2330", "2345"]

    if links is None:
        for link in onlyfiles:
            with open(files_loc + link, "r") as link_file:

                new_data = csv.DictReader(link_file, fieldnames=columns)
                new_data.__next__()

                y = []
                title = ""
                source_1 = ""
                source_2 = ""
                count = 0

                for row in new_data:
                    if count == 0:
                        source_1 = row["Source1"].split("-")[0] + "-" + row["Source1"].split("-")[1]
                        source_2 = row["Source2"].split("-")[0] + "-" + row["Source1"].split("-")[1]
                        title = "Attenuation graph from " + source_1 + " to " + source_2
                        count += 1
                    if source_1 in row["Source1"]:
                        y.append(row["ATTN_S1_S2_Watts"])
                    else:
                        y.append(row["ATTN_S2_S1_Watts"])

                draw_map(x, y, show=True, title=title)
    else:
        for link in links:
            with open(files_loc + link + ".csv", "r") as link_file:
                new_data = csv.DictReader(link_file, fieldnames=columns)
                new_data.__next__()

                y = []
                title = ""
                source_1 = ""
                source_2 = ""
                count = 0

                for row in new_data:
                    if count == 0:
                        source_1 = row["Source1"].split("-")[0] + "-" + row["Source1"].split("-")[1]
                        source_2 = row["Source2"].split("-")[0] + "-" + row["Source1"].split("-")[1]
                        title = "Attenuation graph from " + source_1 + " to " + source_2
                        count += 1
                    if source_1 in row["Source1"]:
                        y.append(row["ATTN_S1_S2_Watts"])
                    else:
                        y.append(row["ATTN_S2_S1_Watts"])
                print(y)
                draw_map(x, y, show=True, title=title)


attenuation_maps(files_loc, links=["26Gy1310x23"])




