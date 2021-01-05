import pandas as pd
import seaborn as sns

if __name__ == '__main__':
    df = pd.read_csv("./out/results.csv", sep=";", decimal=",").round(2)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('SEED')]
    corr = df.corr()
    print(corr)
    sns.set(rc={'figure.figsize': (11.7, 8.27)})
    correlation_graph = sns.heatmap(corr,
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values)

    correlation_graph.figure.show()