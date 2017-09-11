import matplotlib.pyplot as plt
from matplotlib import style


def plot_raw(x_label, raw, corrected, size):
    style.use('seaborn-darkgrid2')
    x = list(range(size - 1))

    fig = plt.figure()
    ax1 = plt.subplot2grid((8, 1), (0, 0),
                           rowspan=3, colspan=1)
    plt.title(r"Rentabilidade da Carteira vs. Indicadores Economicos")
    plt.ylabel("% a.m.")

    ax2 = plt.subplot2grid((8, 1), (4, 0),
                           rowspan=3, colspan=1, sharex=ax1)
    plt.title(r"Rentabilidade da Carteira vs. Indicadores Economicos Corrigidos")
    plt.ylabel("% a.m.")

    for index, i_corrected in zip(raw, corrected):

        plt.xticks(x, x_label)

        # add numbers to each point on the graph
        for i, j in enumerate(x):
            ax1.text(x[i], index[j + 1], str(index[j + 1]))
            ax2.text(x[i], i_corrected[j + 1], str(i_corrected[j + 1]))

        # plot graph
        if index[0] == "MINHA CARTEIRA":

            ax1.plot(x, index[1:size], '-', label=index[0], dashes=[9, 5, 10, 5], color='b')
            ax2.plot(x, i_corrected[1:size], '-', label=i_corrected[0], dashes=[9, 5, 10, 5], color='b')


        else:
            ax1.plot(x, index[1:size], label=index[0], linewidth=1)
            ax2.plot(x, i_corrected[1:size], label=i_corrected[0], linewidth=1)

    # put legend below the graph
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.25),
               fancybox=False, shadow=False, ncol=5)

    # hide x axis legend on ax1
    plt.setp(ax1.get_xticklabels(), visible=False)

    # set the x axis to start at zero
    ax1.set_xlim(xmin=0)
    ax2.set_xlim(xmin=0)
    plt.show()


def table_correction(tables):
    for table in tables:
        culmu = 1
        for i in range(1, len(tables[1])):
            culmu *= (table[i] / 100 + 1)
            table[i] = "{:.2f}".format((culmu - 1) * 100)

    return tables
