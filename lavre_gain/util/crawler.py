import urllib2
from bs4 import BeautifulSoup
import re
import sys
import os


def get_ipca(url):
    ipca_index_file = open("indexes/ipca_index.txt", 'w')

    ipca_index = []

    # connect with the remote server and get the data
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request('http://' + url, headers=hdr)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()

    # extract all tables
    tables = soup.find_all('tbody')

    # for table in tables[0]:
    rows = tables[0].find_all('tr')

    for tr_tags in rows:
        cols = tr_tags.find_all('td')

        # append just the column that will be used by the main script
        ipca_index.append(cols[1].text.encode('utf-8').strip())

        for col in cols:
            line = col.text.encode('utf-8').strip() + '|'
            ipca_index_file.write(line)

        ipca_index_file.write("\n")

    ipca_index_file.close()

    # convert to float before returning
    return convert_to_float(ipca_index[1:])


def get_selic(url):
    selic_index_file = open("indexes/selic_index.txt", 'w')
    selic_index = []

    # connect with the remote server and get the data
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request('http://' + url, headers=hdr)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()

    # extract all tables
    tables = soup.find_all('tbody')

    # for table in tables[0]:
    rows = tables[0].find_all('tr')

    for tr_tags in rows:
        cols = tr_tags.find_all('td')

        # append just the column that will be used by the main script
        selic_index.append(cols[1].text.encode('utf-8').strip())

        for col in cols:
            line = col.text.encode('utf-8').strip() + '|'
            selic_index_file.write(line)

        selic_index_file.write("\n")

    selic_index_file.close()

    # convert to float before returning
    return convert_to_float(selic_index[1:])


def get_cdi(url):
    cdi_index_file = open("indexes/cdi_index.txt", 'w')

    cdi_index = []

    # connect with the remote server and get the data
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request('http://' + url, headers=hdr)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()

    # extract all tables
    tables = soup.find_all('table')

    # for table in tables[0]:
    rows = tables[3].find_all('tr')

    for tr_tags in rows:
        cols = tr_tags.find_all('td')

        # append just the column that will be used by the main script
        cdi_index.append(cols[1].text.encode('utf-8').strip())

        for col in cols:
            line = col.text.encode('utf-8').strip() + '|'
            cdi_index_file.write(line)

        cdi_index_file.write("\n")

    cdi_index_file.close()

    return convert_to_float(cdi_index[1:13])


def get_poup(url):
    poup_index_file = open("indexes/poup_index.txt", 'w')
    poup_index = []

    # connect with the remote server and get the data
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request('http://' + url, headers=hdr)
    html = urllib2.urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    soup.prettify()

    # extract all tables
    tables = soup.find_all('table')

    # for table in tables[0]:
    rows = tables[2].find_all('tr')

    for tr_tags in rows:
        cols = tr_tags.find_all('td')

        for col in cols:
            # This table has another orientation. I need to retunr the whole row 2
            poup_index.append(col.text.encode('utf-8').strip())
            line = col.text.encode('utf-8').strip() + '|'
            poup_index_file.write(line)

        poup_index_file.write("\n")

    poup_index_file.close()

    return convert_to_float(poup_index[14:26])


def get_cart(file_name):
    cart_index = []
    try:
        with open(file_name, "r") as f:
            for line in f:
                cart_index = line.split("\t")
    except IOError:
        print "cannot open", file_name

    return convert_to_float(cart_index)


def create_resume_table(all_indexes):
    resume_index_file = open("indexes/all_indexes.txt", 'w')

    header = "INDEX" + "|" + "JAN" + "|" + "FEV" + "|" + "MAR" + "|" + "ABR" + "|" + "MAI" + "|" + "JUN" + "|" + "JUL" + "|" + "AGO" + "|" + "SET" + "|" + "OUT" + "|" + "NOV" + "|" + "DEZ" + "\n"

    resume_index_file.write(header)

    for indexes in all_indexes:
        for element in indexes:
            resume_index_file.write(str(element) + "|")

        resume_index_file.write("\n")

    return header[6:-1].split("|")


def month_row():
    return ["JAN", "FEV", "MAR", "ABR", "MAI", "JUN", "JUL", "AGO", "SET", "OUT", "NOV", "DEZ"]


def convert_to_float(nums):
    regex = re.compile("[\xc2\xa0]?")
    coma_regex = re.compile(",")
    f_list = []

    for num in nums:
        num = coma_regex.sub(".", num)
        num = regex.sub("", num)

        if num == "-" or num == "":
            num = " "
        else:
            num = float(num)

        f_list.append(num)

    return f_list


def f_exists(file_name):
    if os.path.isfile(file_name):
        return True
    else:
        return False


def load_ipca(file_name):
    ipca_index = []
    try:
        with open(file_name, "r") as f:
            for line in f:
                index = line.split("|")
                ipca_index.append(index[1])
    except IOError:
        print "cannot open", file_name

    return convert_to_float(ipca_index[1:])


def load_selic(file_name):
    selic_index = []
    try:
        with open(file_name, "r") as f:
            for line in f:
                index = line.split("|")
                selic_index.append(index[1])
    except IOError:
        print "cannot open", file_name

    return convert_to_float(selic_index[1:])


def load_cdi(file_name):
    cdi_index = []
    try:
        with open(file_name, "r") as f:
            for i, line in enumerate(f):
                index = line.split("|")
                if i < 12:
                    cdi_index.append(index[1])
                else:
                    break
    except IOError:
        print "cannot open", file_name

    return convert_to_float(cdi_index[1:13])


def load_poup(file_name):
    poup_index = []
    try:
        with open(file_name, "r") as f:
            for i, line in enumerate(f):
                if i == 1:
                    index = line.split("|")
                    poup_index = index
                    break
    except IOError:
        print "cannot open", file_name

    return convert_to_float(poup_index[1:-1])
