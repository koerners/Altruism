import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr

if __name__ == '__main__':
    df = pd.read_csv("./out/batch_results_2.0 - Rohdaten.csv", sep=",", decimal=".").round(2)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.loc[:, ~df.columns.str.contains('SEED')]
    df = df.loc[:, ~df.columns.str.contains('ID')]


    def calculate_pvalues(df_):
        df_ = df_.dropna()

        dfcols = pd.DataFrame(columns=df_.columns)
        cvalues = dfcols.transpose().join(dfcols, how='outer')
        pvalues = dfcols.transpose().join(dfcols, how='outer')

        warnings.filterwarnings("ignore")
        for r in df.columns:
            for c in df.columns:
                c_, p_ = pearsonr(pd.to_numeric(df_[r], errors='coerce'), pd.to_numeric(df_[c], errors='coerce'))
                pvalues[r][c] = round(p_, 4)
                if np.isnan(p_) or np.isnan(c_) or p_ > 0.01:
                    continue

                c_ = round(c_, 4)
                cvalues[r][c] = c_

        # turn warnings back on
        warnings.filterwarnings("always")

        for col in cvalues:
            cvalues[col] = pd.to_numeric(cvalues[col], errors='coerce')
        for col in pvalues:
            pvalues[col] = pd.to_numeric(pvalues[col], errors='coerce')

        return cvalues, pvalues


    cols_to_fill = ['died_of_chance', 'children_per_woman', 'altruistic_acts_altruists', 'altruistic_acts_base_agents',
                    'died_of_old_age', 'population_nonAltruists', 'population_altruists', 'population',
                    'died_of_fitness_loss',
                    'nonAltruist_fitness', 'net_growth']

    for col in cols_to_fill:
        df[col] = df[col].fillna(0)

    c, p = calculate_pvalues(df)

    mask_half = np.triu(np.ones_like(c, dtype=bool))  # -> Values only once -> Dreieck

    f, ax = plt.subplots(figsize=(11, 9))

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    sns.set_theme(style="white")
    correlation_graph_half = sns.heatmap(c, cmap=cmap, mask=mask_half, center=0,
                                         square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.figure()
    plt.show()

    correlation_graph_half.figure.savefig("out/plot_figures/correlation_graph.png", bbox_inches='tight')

    """
    correlation_graph_half.figure.show()
    correlation_graph_half_sig.figure.show()
    correlation_graph_half_combined.figure.show()
    """
