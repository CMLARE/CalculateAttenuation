import csv
from _decimal import Decimal
from math import log
from os import listdir
from os.path import isfile, join


def dBm_to_W(dBm):
    power = 10 ** ((float(dBm)-30)/10)
    return Decimal(power).to_eng_string()


def W_to_dBm(power):
    dBm = 30 + 10 * log(float(power),10)
    return (dBm)


def _main_(folder_path, edited_file_location, csv_file_name):

    # file locations
    csv_file_location = folder_path + csv_file_name
    edited_csv_file_location = edited_file_location + csv_file_name

    # open file to read
    with open(csv_file_location, "r") as cml_data_file:
        data = csv.reader(cml_data_file)

        read_field_names = ["DeviceID", "DeviceName", "ResourceID", "ResourceName", "CollectionTime", "GranularityPeriod", "RSL_MAX", "RSL_MIN",
                       "RSL_AVG", "RSL_CUR", "TLHTT", "TLLTT", "TSL_MAX", "TSL_MIN", "TSL_AVG", "TSL_CUR", "RLHTT", "RLLTT",
                       "ATPC_N_ADJUST", "ATPC_P_ADJUST",	"ODU_SSV_TH"]

        write_field_names = ["Source1", "Source2", "AVG_TSL_FRM_S1", "AVG_RSL_TO_S2", "AVG_TSL_FRM_S2", "AVG_RSL_TO_S1",
                             "ATTN_S1_S2_Watts", "ATTN_S1_S2_dBm", "ATTN_S2_S1_Watts", "ATTN_S2_S1_dBm"]

        reader = csv.DictReader(cml_data_file, fieldnames=read_field_names)

        link_ends = []
        traversed_links = []
        all_rows = []
        count = 0
        for row in reader:
            if count < 2:
                count +=1
            else:
                link_ends.append(row['ResourceName'].split("-"))
                all_rows.append(row)

        with open(edited_csv_file_location, "w") as edited_cml_data_file:
            new_data = csv.DictWriter(edited_cml_data_file, fieldnames=write_field_names)

            new_data.writeheader()
            for link_end in range(0,len(link_ends)):
                # check next element is 23 or 24
                if link_ends[link_end][3] == "24" or link_ends[link_end][3] == "23" \
                        or link_ends[link_end][3] == "25" or link_ends[link_end][3] == "26":
                    link_end_with_axis = link_ends[link_end][2] + "-" + link_ends[link_end][3]
                else:
                    link_end_with_axis = link_ends[link_end][2] + "-" + link_ends[link_end][3] + \
                                         "-" + link_ends[link_end][4]
                if not (traversed_links.__contains__(link_end_with_axis)):
                    traversed_links.append(link_end_with_axis)
                    print(link_end_with_axis)

                    for next_link_end in range(0,len(link_ends)):
                        if not link_ends[next_link_end] == link_ends[link_end]:
                            if link_ends[link_end][3] == "24" or link_ends[link_end][3] == "23" \
                                    or link_ends[link_end][3] == "25" or link_ends[link_end][3] == "26":
                                new_link_end_with_axis = link_ends[link_end][2] + "-" + link_ends[link_end][3]
                                new_next_link_end_with_axis = link_ends[next_link_end][2] + "-" + link_ends[next_link_end][3]
                            else:
                                new_link_end_with_axis = link_ends[link_end][2] + "-" + link_ends[link_end][3] + \
                                                     "-" + link_ends[link_end][4]
                                new_next_link_end_with_axis = link_ends[next_link_end][2] + "-" + link_ends[next_link_end][3] + \
                                                     "-" + link_ends[next_link_end][4]
                            if (new_link_end_with_axis == new_next_link_end_with_axis):
                                attenuation_from_s2_to_s1_in_watts = float(dBm_to_W(float(all_rows[next_link_end]['TSL_AVG']))) - float(dBm_to_W(float(all_rows[link_end]['RSL_AVG'])))
                                print("attenuation_from_s2_to_s1_in_watts " + str(attenuation_from_s2_to_s1_in_watts))

                                if attenuation_from_s2_to_s1_in_watts > 0:
                                    attenuation_from_s2_to_s1_in_dBm = W_to_dBm(
                                        float(dBm_to_W(float(all_rows[next_link_end]['TSL_AVG']))) - float(
                                            dBm_to_W(float(all_rows[link_end]['RSL_AVG']))))
                                    print("attenuation_from_s2_to_s1_in_dBm " + str(attenuation_from_s2_to_s1_in_dBm))
                                else:
                                    attenuation_from_s2_to_s1_in_dBm = "ATTN_NEG"
                                    attenuation_from_s2_to_s1_in_watts = "ATTN_NEG"

                                attenuation_from_s1_to_s2_in_watts = float(dBm_to_W(float(all_rows[link_end]['TSL_AVG']))) - float(dBm_to_W(float(all_rows[next_link_end]['RSL_AVG'])))
                                print("attenuation_from_s1_to_s2_in_watts " + str(attenuation_from_s1_to_s2_in_watts))

                                if attenuation_from_s1_to_s2_in_watts > 0:
                                    attenuation_from_s1_to_s2_in_dBm = W_to_dBm(
                                        float(all_rows[link_end]['TSL_AVG']) - float(
                                            all_rows[next_link_end]['RSL_AVG']))
                                    print("attenuation_from_s1_to_s2_in_dBm " + str(attenuation_from_s1_to_s2_in_dBm))
                                else:
                                    attenuation_from_s1_to_s2_in_watts = "ATTN_NEG"
                                    attenuation_from_s1_to_s2_in_dBm = "ATTN_NEG"

                                new_data.writerow({"Source1": "-".join(link_ends[link_end]),
                                                   "Source2": "-".join(link_ends[next_link_end]),
                                                   "AVG_TSL_FRM_S1": all_rows[link_end]['TSL_AVG'],
                                                   "AVG_RSL_TO_S2": all_rows[next_link_end]['RSL_AVG'],
                                                   "AVG_TSL_FRM_S2": all_rows[next_link_end]['TSL_AVG'],
                                                   "AVG_RSL_TO_S1": all_rows[link_end]['RSL_AVG'],
                                                   "ATTN_S1_S2_Watts": attenuation_from_s1_to_s2_in_watts,
                                                   "ATTN_S1_S2_dBm": attenuation_from_s1_to_s2_in_dBm,
                                                   "ATTN_S2_S1_Watts": attenuation_from_s2_to_s1_in_watts,
                                                   "ATTN_S2_S1_dBm": attenuation_from_s2_to_s1_in_dBm})


def get_all_files(folder_path, edited_file_path):
    onlyfiles = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    for i in onlyfiles:
        _main_(folder_path, edited_file_path, i)

get_all_files("C:\\Users\\Akalanka\\Desktop\\New folder\\drive-download-20180321T185453Z-001\\",
              "C:\\Users\\Akalanka\\Desktop\\edited files\\")
