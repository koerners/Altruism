import pandas as pd
from sim import run_sim
import itertools


class Parameters:
    NUMBER_OF_AGENTS = 100  # Größe der Anfangs-Population
    NUMBER_OF_ITERATIONS = 250  # Jahre, welche simuliert werden sollen
    SPAWN_NONALTRUIST = 10  # Spawn Wahrscheinlichkeit von "NonAltruists" in % -> 5 er Steps
    SPAWN_ALTRUIST = 10  # Spawn Wahrscheinlichkeit von "Altruists" in % -> 5 er Steps
    MUTATION_RATE = 5  # Mutationsrate
    FITNESS_REGENERATION_RATE = 0  # Fitness Regenerationsrate (wird durch Alter geteilt)
    CHANCE_TO_HELP_PROBABILITY = 10  # Prozentuale Chance, dass ein altruistisches Handeln nötig ist
    FERTILITY = 2  # Fruchtbarkeitsrate
    COST_REDUCTION_ALTRUISTIC_ACT = 1  # Anteil der Punkte, welche man selbst verliert wenn man altruistisch handelt
    SEED = 545654  # Zufallsseed, gleichlassen für Vergleichbarkeit

    def __init__(self, permutation_list):
        self.SPAWN_NONALTRUIST = permutation_list[0]
        self.SPAWN_ALTRUIST = permutation_list[1]
        self.CHANCE_TO_HELP_PROBABILITY = permutation_list[2]
        self.COST_REDUCTION_ALTRUISTIC_ACT = permutation_list[3]


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
        # print(str(df_batch))

        batch_test = df_batch.copy().drop(columns = ['ID'])
        # batch_test = batch_test.values.tolist()
        param_list_dirty = [] # dirty means the parameters including Nan values
        param_list = [] # the final list, cleaned without the Nans
        param_list_dirty.append(batch_test['SPAWN_NONALTRUIST'].values.tolist())
        param_list_dirty.append(batch_test['SPAWN_ALTRUIST'].values.tolist())
        param_list_dirty.append(batch_test['CHANCE_TO_HELP_PROBABILITY'].values.tolist())
        param_list_dirty.append(batch_test['COST_REDUCTION_ALTRUISTIC_ACT'].values.tolist())
        for param_list_current in param_list_dirty:
            param_list.append([x for x in param_list_current if str(x) != 'nan'])
        # print(str(param_list))
        params_permutations = list(itertools.product(*param_list))

        for id_, permutation in enumerate(params_permutations):
            # print("current Permutation: " + str(permutation))
            params = Parameters(permutation)

            for seed in seeds:
                setattr(params, "SEED", seed)
                try:
                    print(id_, "von", len(params_permutations), seed)
                    sim_df = run_sim(id_, params, no_img=True).round(2) # Mit no_img = False wird ein Graph pro Runde generiert
                    df_results = df_results.append(sim_df)
                    df_results.to_csv("./out/results.csv", sep=";")
                except Exception as e:
                    print(e)
