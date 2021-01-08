import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import warnings
from scipy.stats import pearsonr

if __name__ == '__main__':
    df = pd.read_csv("./out/results.csv", sep=";", decimal=",").round(2)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('SEED')]
    corr = df.corr()


    def calculate_pvalues(df):
        df = df.dropna()._get_numeric_data()
        dfcols = pd.DataFrame(columns=df.columns)
        pvalues = dfcols.transpose().join(dfcols, how='outer')

        # turn warnings off for the two loops
        # pearsonnr returns a warning, when called with constants
        warnings.filterwarnings("ignore")
        for r in df.columns:
            for c in df.columns:
                pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
        # turn warnings back on
        warnings.filterwarnings("always")
        return pvalues


    p = calculate_pvalues(df.fillna(0)) # Alternative: df.replace(np.nan,0)

    mask_half = np.triu(np.ones_like(corr, dtype=bool)) # -> Values only once -> Dreieck
    mask_sig = np.tril(p < 0.05) # Signifikanz
    mask_combined =  mask_sig | mask_half # Beide Masken kombiniert

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 9))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    # It is important to have the order of graphs and savefig as it is (alternating)
    # otherwise figure gets overwritten every time and results get mixed up
    sns.set_theme(style="white")
    correlation_graph_half = sns.heatmap(corr, mask=mask_half, cmap=cmap, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.figure()
    plt.clf()
    correlation_graph_half.figure.savefig("out/plot_figures/correlation_graph_half.png", bbox_inches='tight')

    correlation_graph_half_sig = sns.heatmap(corr, mask=mask_sig, cmap=cmap, center=0,
                                         square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.figure()
    plt.clf()
    correlation_graph_half_sig.figure.savefig("out/plot_figures/correlation_graph_half_sig.png", bbox_inches='tight')

    correlation_graph_half_combined = sns.heatmap(corr, mask=mask_combined, cmap=cmap, center=0,
                                         square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.figure()
    plt.clf()
    correlation_graph_half_combined.figure.savefig("out/plot_figures/correlation_graph_half_combined.png", bbox_inches='tight')

    """
    correlation_graph_half.figure.show()
    correlation_graph_half_sig.figure.show()
    correlation_graph_half_combined.figure.show()
    """

