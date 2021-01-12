import itertools
import multiprocessing as mp

import pandas as pd

from sim import run_sim


class Parameters:
    NUMBER_OF_AGENTS = 100  # Größe der Anfangs-Population
    NUMBER_OF_ITERATIONS = 200  # Jahre, welche simuliert werden sollen
    SPAWN_NONALTRUIST = 10  # Spawn Wahrscheinlichkeit von "NonAltruists" in % -> 5 er Steps
    SPAWN_ALTRUIST = 10  # Spawn Wahrscheinlichkeit von "Altruists" in % -> 5 er Steps
    MUTATION_RATE = 5  # Mutationsrate
    FITNESS_REGENERATION_RATE = 0  # Fitness Regenerationsrate (wird durch Alter geteilt)
    CHANCE_TO_HELP_PROBABILITY = 10  # Prozentuale Chance, dass ein altruistisches Handeln nötig ist
    FERTILITY = 2  # Fruchtbarkeitsrate
    COST_REDUCTION_ALTRUISTIC_ACT = 1  # Anteil der Punkte, welche man selbst verliert wenn man altruistisch handelt
    SEED = 545654  # Zufallsseed, gleichlassen für Vergleichbarkeit
    ID = None

    def __init__(self, permutation_list=None, id_=None):
        if id_ is not None:
            self.SPAWN_NONALTRUIST = permutation_list[0]
            self.SPAWN_ALTRUIST = permutation_list[1]
            self.CHANCE_TO_HELP_PROBABILITY = permutation_list[2]
            self.COST_REDUCTION_ALTRUISTIC_ACT = permutation_list[3]
            self.ID = id_


def run(pl):
    try:
        print("\n Running: ", pl.ID)
        sim_df = run_sim(pl.ID, pl, no_img=True).round(
            2)  # Mit no_img = False wird ein Graph pro Runde generiert
        return sim_df

    except Exception as e:
        print(e)


if __name__ == '__main__':
    BATCH = True  # Wenn True werden die Parameter oben genutzt, Sonst werden die Parameter aus batch_parameter.csv eingelesen und überschreiben oben

    if not BATCH:
        parameters = Parameters()
        print(run_sim(0, parameters))

    else:
        params = []
        import random

        seeds = []
        for i in range(0, 5):
            n = random.randint(1, 999999)
            seeds.append(n)

        df_results = pd.DataFrame()
        df_batch = pd.read_csv("batch_parameters.csv", sep=";")

        batch_test = df_batch.copy().drop(columns=['ID'])
        param_list_dirty = []  # dirty means the parameters including Nan values
        param_list = []  # the final list, cleaned without the Nans
        for column in ['SPAWN_NONALTRUIST', 'SPAWN_ALTRUIST', 'CHANCE_TO_HELP_PROBABILITY',
                       'COST_REDUCTION_ALTRUISTIC_ACT']:
            param_list_dirty.append(batch_test[column].values.tolist())

        for param_list_current in param_list_dirty:
            param_list.append([x for x in param_list_current if str(x) != 'nan'])
        params_permutations = list(itertools.product(*param_list))

        final_params = []
        for id_, permutation in enumerate(params_permutations):
            for seed in seeds:
                params = Parameters(permutation, id_)
                params.SEED = seed
                final_params.append(params)

        pool = mp.Pool(mp.cpu_count())
        print("Running", len(final_params), "iterations")
        result = pool.map(run, final_params)
        pool.terminate()

        for res in result:
            df_results = df_results.append(res)

        df_results.to_csv("./out/results.csv", sep=";")
