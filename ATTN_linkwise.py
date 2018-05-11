import csv
from _decimal import Decimal
from math import log
from os import listdir
from os.path import isfile, join


def get_all_files(folder_path, edited_file_path):
    onlyfiles = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

    _main_(folder_path, edited_file_path, onlyfiles)


def _main_(folder_path, edited_file_location, csv_file_names):
    is_headers_created = False

    for csv_file_name in csv_file_names:
        # file locations
        csv_file_location = folder_path + csv_file_name

        date_time = csv_file_name.split("_")[3]
        edited_csv_file_location = edited_file_location + date_time


        # open file to read
        with open(csv_file_location, "r") as cml_data_file:

            read_field_names = ["Source1", "Source2","AVG_TSL_FRM_S1", "AVG_RSL_TO_S2", "AVG_TSL_FRM_S2", "AVG_RSL_TO_S1",
                                 "ATTN_S1_S2_Watts", "ATTN_S1_S2_dBm", "ATTN_S2_S1_Watts", "ATTN_S2_S1_dBm"]

            reader = csv.DictReader(cml_data_file, fieldnames=read_field_names)

            links = []
            all_rows = []
            count = 0

            # remove first row which is header
            for row in reader:
                if count < 1:
                    count +=1
                else:
                    if row["Source1"] == "":
                        pass
                    else:
                        link_id = row['Source1'].split("-")
                        print(row)
                        links.append(link_id[2] + "-" + link_id[3])
                        all_rows.append(row)

            # create headers for all the links
            for link in range(0, len(links)):
                if not is_headers_created:
                    file_name_id = links[link].translate(str.maketrans({"-":  r"x", "/":  r"y"}))
                    # create headers in all files
                    edited_csv_file_location = edited_file_location + file_name_id + ".csv"

                    write_field_names = ["Source1", "Source2", "date_time", "AVG_TSL_FRM_S1", "AVG_RSL_TO_S2",
                                         "AVG_TSL_FRM_S2",
                                         "AVG_RSL_TO_S1",
                                         "ATTN_S1_S2_Watts", "ATTN_S1_S2_dBm", "ATTN_S2_S1_Watts",
                                         "ATTN_S2_S1_dBm"]

                    with open(edited_csv_file_location, "w") as edited_cml_data_file:
                        new_data = csv.DictWriter(edited_cml_data_file, fieldnames=write_field_names)
                        new_data.writeheader()

        is_headers_created = True

        # header creation is finished
        for link_end in range(0, len(all_rows)):
            link_end_with_axis = links[link_end]

            file_name_id = link_end_with_axis.translate(str.maketrans({"-": r"x", "/": r"y"}))
            edited_csv_file_location = edited_file_location + file_name_id + ".csv"

            # print(edited_csv_file_location)
            with open(edited_csv_file_location, "a") as edited_cml_data_file:
                new_data = csv.DictWriter(edited_cml_data_file, fieldnames=write_field_names)

                all_rows[link_end]["date_time"] = date_time
                new_data.writerow(all_rows[link_end])

get_all_files("C:\\Users\\Akalanka\\Desktop\\edited files\\",
              "C:\\Users\\Akalanka\\Desktop\\edited files linkwise\\")
