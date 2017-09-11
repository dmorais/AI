import util.crawler as uc
import util.plotter as pl
import sys
import os
import copy
from datetime import datetime
import matplotlib.pyplot as plt


def get_indexes(file_name):
    ipca_table = list()
    selic_table = list()
    cdi_table = list()
    poup_table = list()
    resume = list()

    create_resume = True

    # Get the month of the last modification of the IPCA index
    ipca_month = datetime.fromtimestamp(os.path.getmtime('indexes/ipca_index.txt')).strftime('%m')

    if uc.f_exists('indexes/ipca_index.txt'):

        if ipca_month == datetime.now().strftime('%m'):
            ipca_table = uc.load_ipca('indexes/ipca_index.txt')
            selic_table = uc.load_selic("indexes/selic_index.txt")
            cdi_table = uc.load_cdi("indexes/cdi_index.txt")
            poup_table = uc.load_poup("indexes/poup_index.txt")

            # Set to false so no all_indexes will be created
            create_resume = False

        else:
            ipca_table = uc.get_ipca("br.advfn.com/indicadores/ipca/2017")
            selic_table = uc.get_selic("br.advfn.com/indicadores/taxa-selic")
            cdi_table = uc.get_cdi("www.magconsultoria.uaivip.com.br/TABFINANCEIRAS.htm")
            poup_table = uc.get_poup("www.portalbrasil.net/poupanca_mensal.htm")

    # Get the user gains data
    cart_table = uc.get_cart(file_name)

    ipca_table.insert(0, "IPCA")
    selic_table.insert(0, "SELIC")
    poup_table.insert(0, "POUPANCA")
    cdi_table.insert(0, "CDI")
    cart_table.insert(0, "MINHA CARTEIRA")

    resume.append(ipca_table)
    resume.append(selic_table)
    resume.append(poup_table)
    resume.append(cdi_table)
    resume.append(cart_table)

    # If needs create the all_indexes file
    if create_resume == True:
        month_row = uc.create_resume_table(resume)
        return resume, month_row, len(selic_table)

    else:
        return resume, uc.month_row(), len(selic_table)


def main():
    if len(sys.argv) < 1:
        print "You must give the Minha carteira file"
        sys.exit(1)

    # Fetch or load data
    resume, month_row, selic_len = get_indexes(sys.argv[1])

    # C_resume need to be a deep copy otherwise it gets modified as well
    c_resume = copy.deepcopy(resume)

    # Get corrected values
    corrected_tables = pl.table_correction(c_resume)

    # Create graphs
    pl.plot_raw(month_row, resume, corrected_tables, selic_len)


if __name__ == '__main__':
    main()
