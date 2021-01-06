import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

if __name__ == '__main__':
    df = pd.read_csv("./out/results.csv", sep=";", decimal=",").round(2)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('SEED')]
    corr = df.corr()

    from scipy.stats import pearsonr


    def calculate_pvalues(df):
        df = df.dropna()._get_numeric_data()
        dfcols = pd.DataFrame(columns=df.columns)
        pvalues = dfcols.transpose().join(dfcols, how='outer')
        for r in df.columns:
            for c in df.columns:
                pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
        return pvalues

    p = calculate_pvalues(df.fillna(0))

    mask_half = np.triu(np.ones_like(corr, dtype=bool)) # -> Values only once -> Dreieck
    mask_sig = np.tril(p < 0.05) # Signifikanz
    mask_combined =  mask_sig | mask_half # Beide Masken kombiniert

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio

    sns.set_theme(style="white")
    correlation_graph = sns.heatmap(corr, mask=mask_combined, cmap=cmap, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})

    correlation_graph.figure.show()
    correlation_graph.figure.savefig("output.png")



