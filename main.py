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


if __name__ == '__main__':
    batch = False  # Wenn True werden die Parameter oben genutzt, Sonst werden die Parameter aus batch_parameter.csv eingelesen und überschreiben oben

    if not batch:
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
        for col in df_batch:
            parameters = Parameters()
            if col != "ID":
                for index, value in df_batch[col].items():
                    if not pd.isnull(value):
                        setattr(parameters, col, float(value))
                        for col_ in df_batch:
                            if col_ != "ID" and col_ != col:
                                for index_, value_ in df_batch[col_].items():
                                    if not pd.isnull(value_):
                                        setattr(parameters, col_, float(value_))
                                        params.append(parameters)
                                        parameters = Parameters()

        for id_, param in enumerate(params):
            for seed in seeds:
                setattr(param, "SEED", seed)
                try:
                    print(id_, "von", len(params), seed)
                    sim_df = run_sim(id_, param).round(2)
                    df_results = df_results.append(sim_df)
                    df_results.to_csv("./out/results.csv", sep=";")
                except Exception as e:
                    print(e)
