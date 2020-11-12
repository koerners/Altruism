import matplotlib

import pandas as pd
from tqdm import tqdm

matplotlib.use('Agg')  # Fix für SSH


class Parameters:
    NUMER_OF_AGENTS = 100  # Größe der Population
    NUMBER_OF_ITERATIONS = 200  # Jahre, welche simuliert werden sollen
    SPAWN_DEVIL = 10  # Spawn Wahrscheinlichkeit von "Devils" in %
    SPAWN_ANGEL = 10  # Spawn Wahrscheinlichkeit von "Angels" in %
    FITNESS_REGENERATION_RATE = 0.05  # Fitness Regeneration
    DISASTER_PROBABILITY = 1  # Prozentuale Chance, dass ein altruistisches Handeln nötig ist
    FERTILITY = 1.2  # Fruchtbarkeitsrate
    SEED = 42  # Zufallsseed


if __name__ == '__main__':

    parameters = Parameters()

    df_results = pd.DataFrame()  # Data Frame, in dem die Ergebisse kummuliert werden
    from models.basic_model import ExampleModel

    model = ExampleModel(parameters)
    for i in tqdm(range(parameters.NUMBER_OF_ITERATIONS)):
        model.step()
        df_results = df_results.append({'year': model.get_time(), 'population': model.schedule.get_agent_count(),
                                        'median_age': model.get_median_age(),
                                        'median_fitness': model.get_median_fitness(),
                                        'children_per_woman': model.children_per_woman(),
                                        'net_growth': model.get_net_grow(), 'devil_fitness': model.get_devil_fitness(),
                                        'angel_fitness': model.get_angel_fitness(),
                                        'population_angels': model.get_angels(),
                                        'population_devils': model.get_devils()}, ignore_index=True)

    print(df_results[['population_angels', 'population_devils', 'population']])

    fig_population = df_results[['year', 'population', 'population_angels', 'population_devils']].plot(
        x='year').get_figure()
    fig_fitness = df_results[['year', 'devil_fitness', 'angel_fitness', 'median_fitness']].plot(
        x='year').get_figure()
    fig_growth = df_results[['year', 'children_per_woman']].plot(x='year').get_figure()

    fig_population.savefig('./out/population.png')
    fig_fitness.savefig('./out/fitness.png')
    fig_growth.savefig('./out/fig_growth.png')
    df_results.to_json("./out/results.json")

    # Wegkommentieren, wenn SSH
    # fig_population.show()
    # fig_age_fitness.show()
