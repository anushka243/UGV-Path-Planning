"""
For comparing all the methods. Please run runDQ.py and runQ.py beforehand to save .pkl variables

"""
import pickle
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt


if __name__ == "__main__":
    filehandler = open("dql_total_path.pkl", 'rb')
    dql_total = pickle.load(filehandler)
    filehandler.close()

    filehandler = open("ql_total_path.pkl", 'rb')
    ql_total = pickle.load(filehandler)
    filehandler.close()

    print(dql_total)
    print(ql_total)

    x = []
    for i in range(700):
        x.append(i)

    minlp = []
    for i in range(700):
        minlp.append(241)

    plt.plot(x, dql_total, 'r', label='Deep Q Learning')
    plt.plot(x, ql_total, 'b', label='Q Learning')
    plt.plot(x, minlp, 'g', label='MINLP')
    plt.legend(loc='upper left')
    plt.xlabel('Number of Epochs')
    plt.ylabel('Moving Energy of UGV')
    plt.show()