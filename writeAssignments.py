#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

import getAssignments
from getAssignments import *


numbers = list(map(str,range(15,-1,-1)))
baseurl = "https://wiki.math.ntnu.no"
subject = "/Ma1101"
subjectname = subject[1:]
years = latest_year_url(baseurl + subject)
# year = get_year(years[0])

# print(get_first_existing_substring("lfov3_ma1101_h17.pdf",numbers,year,subjectname))

# get_all_urls()

def create_subject_folder(subject_info):
    path = "../kok/"
    if subject_info["name"][0:2] == "ma":
        path += "/ma/"
    elif subject_info["name"][0:3] == "tma":
        path += "/tma/"
    path += subject_info["name"]
    path += "/kok/"
    path += subject_info["year"]

    os.makedirs(path, exist_ok=True)
    return path

def download_subject_solutions(subject):
    try:
        subject_info = get_all_urls_from_subject(subject)
    except:
        return False
    if not subject_info:
        return False
    elif len(subject_info["paths"])==0:
        return False
    localpath = create_subject_folder(subject_info)

    for (i, file2download) in enumerate(subject_info["paths"]):
        try:
            destination = localpath + "/" + subject_info["filenames"][i]
            urllib.request.urlretrieve(file2download, destination)
        except:
            pass
    return True

# for subject in find_subjects():
#     print(subject)
#     download_subject_solutions(subject)
