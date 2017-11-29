from bs4 import BeautifulSoup
import urllib.request
import re

PROBLEM_NAMES = ['oving', 'ov', 'ex']
SOLUTION_NAMES = ['lf', 'sol', 'solution']
PROB_SOL_NAMES = PROBLEM_NAMES + SOLUTION_NAMES

def is_subject_active(page):
    resp = urllib.request.urlopen(page)
    soup = BeautifulSoup(resp, "lxml",
    from_encoding=resp.info().get_param('charset'))
    return not soup(text=re.compile("Emnet er"))

def find_subjects():
    resp = urllib.request.urlopen("https://wiki.math.ntnu.no/emner")
    soup = BeautifulSoup(resp, "lxml",
    from_encoding=resp.info().get_param('charset'))
    subjects = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.startswith("/ma") or url.startswith("/tma"):
            if url not in subjects:
                subjects.append(url)
    return subjects

def latest_year_url(subject):
    try:
        resp = urllib.request.urlopen(subject)
    except:
        return ""
    soup = BeautifulSoup(resp, "lxml",
    from_encoding=resp.info().get_param('charset'))
    subjects = []

    years = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.endswith('start'):
            years.append(url)
    years.sort(reverse=True)
    return years

def find_assignment_url(subject_year):
    resp = urllib.request.urlopen(subject_year)
    soup = BeautifulSoup(resp, "lxml",
    from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', href=True):
        url = link['href']
        if any(name in url for name in ['oving', 'assignment', 'exercise']):
            if "exam" not in url:
                return url
    return ""

def find_assignments(assignment_url):
    resp = urllib.request.urlopen(assignment_url)
    soup = BeautifulSoup(resp, "lxml",
    from_encoding=resp.info().get_param('charset'))
    problem_and_solutions = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.endswith("pdf"):
            problem_and_solutions.append(url)
    return problem_and_solutions

def find_mainpage_assignments(mainpage_url):
    resp = urllib.request.urlopen(mainpage_url)
    soup = BeautifulSoup(resp, "lxml",
    from_encoding=resp.info().get_param('charset'))
    problem_and_solutions = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if url.endswith("pdf"):
            if any(word in url for word in PROB_SOL_NAMES):
                problem_and_solutions.append(url)
    return problem_and_solutions


# resp = urllib.request.urlopen("https://wiki.math.ntnu.no/ma0001/2017h/oving")
# soup = BeautifulSoup(resp, "lxml", from_encoding=resp.info().get_param('charset'))

# for link in soup.find_all('a', href=True):
#     url = link['href']
#     if url.endswith("pdf"):
#         print(url)

yeas = ["/ma3301", "/ma2301", "/ma1201"]

baseurl = "https://wiki.math.ntnu.no"
year_url = latest_year_url(baseurl + yeas[2])

# print(year_url)
y = baseurl + yeas[0]
# print(is_subject_active(y))
# print(find_mainpage_assignments(baseurl + year_url[0]))

# assignments = find_assignment_url(baseurl + year_url[0])
# print(assignments)
def get_assignments_from_subject(subject):
    # print("="*30)
    # print(subject)
    # print("="*30 + '\n')
    baseurl = "https://wiki.math.ntnu.no"
    subjecturl = baseurl + subject
    # print(subjecturl, is_subject_active(subjecturl))
    if not is_subject_active(subjecturl):
        return []
    # try:
    years_url = latest_year_url(subjecturl)
    if len(year_url)>0:
        problem_and_solutions = []
        current_year_url = baseurl + years_url[0]
        assignments = find_assignment_url(current_year_url)
        if assignments.endswith("pdf"):
            problem_and_solutions += find_mainpage_assignments(current_year_url)
        else:
            problem_and_solutions += find_assignments(baseurl + assignments)
    return problem_and_solutions

def get_first_existing_substring(filename, list_of_numberstring, year, subject):
    no_year = filename.replace(year,"").replace(year[-2::],"")
    no_subject = no_year.replace(subject,"").replace(subject[-4::],"")
    for numberstr in list_of_numberstring:
        if numberstr in no_subject:
            return numberstr
    return ""

def get_new_filename(filename, numbers, year, subjectname):
    ex_or_sol = ""
    if any(s in filename for s in ["sol", "lf", "oppg"]):
        ex_or_sol = "lf"
    elif any(e in filename for e in ["assignment", "ex", "prob", "ov", "hw",
                                     "_ving", "l_osning"]):
        ex_or_sol = "ex"
    if ex_or_sol:
        str_num = get_first_existing_substring(filename, numbers, year, subjectname)
        if str_num:
            return '{}-{}-{}-{}.pdf'.format(subjectname,
                                            year,
                                            ex_or_sol,
                                            str_num.zfill(2))
    return ""

def get_all_urls():
    baseurl = "https://wiki.math.ntnu.no"
    numbers = list(map(str,range(15,-1,-1)))
    for subject in find_subjects():
        years = latest_year_url(baseurl + subject)
        try:
            year = get_year(years[0])
        except:
            continue
        try:
            if subject[0:3] == "/ma":
                subjectname = subject[1:7]
            elif subject[0:4] == "/tma":
                subjectname = subject[1:8]
            else:
                continue
            for pdf in get_assignments_from_subject(subject):
                filename = pdf.rsplit('/', 1)[-1]
                print('{:50}'.format(filename), end="")
                new_filename = get_new_filename(filename, numbers, year,
                                                subjectname)
                if new_filename:
                    print(new_filename, end="")
                print()
        except:
            pass

def get_all_urls_from_subject(subject):
    baseurl = "https://wiki.math.ntnu.no"
    numbers = list(map(str,range(15,-1,-1)))
    exercises_and_solutions = []

    subj = {}

    years = latest_year_url(baseurl + subject)
    try:
        year = get_year(years[0])
    except:
        return ""
    subj["year"] = year
    try:
        if subject[0:3] == "/ma":
            subjectname = subject[1:7]
        elif subject[0:4] == "/tma":
            subjectname = subject[1:8]
        else:
            return ""
        subj["name"] = subjectname
        subj["paths"] = list()
        subj["filenames"] = list()
        for pdf in get_assignments_from_subject(subject):
            subj["paths"].append(baseurl + pdf)
            filename = pdf.rsplit('/', 1)[-1]
            new_filename = get_new_filename(filename, numbers, year,
                                                subjectname)
            if new_filename and new_filename not in subj["filenames"]:
                subj["filenames"].append(new_filename)
            else:
                subj["filenames"].append(filename)

        return subj
    except:
        pass

def get_year(url):
    try:
        centuryIdx = url.index("ma")
    except:
        try:
            centuryIdx = url.index("tma")
        except:
            return ""
    try:
        yearIdx = url.index("20", centuryIdx+5)
        return url[yearIdx:yearIdx+4]
    except:
        return ""

# get_all_urls()
