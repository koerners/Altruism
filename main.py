import time

import matplotlib
import pandas as pd
from tqdm import trange

matplotlib.use('Agg')  # Fix für SSH


def get_params(input_class):
    """
    Helfermethode um die Attribute einer Klasse speichern zu können
    """
    attrs = {}
    for attr, value in input_class.__dict__.items():
        if not "__" in attr:
            attrs.update({attr: value})
    return pd.DataFrame(attrs, index=[0])


class Parameters:
    NUMBER_OF_AGENTS = 100  # Größe der Anfangs-Population
    NUMBER_OF_ITERATIONS = 1000  # Jahre, welche simuliert werden sollen
    SPAWN_DEVIL = 10  # Spawn Wahrscheinlichkeit von "Devils" in %
    SPAWN_ANGEL = 10  # Spawn Wahrscheinlichkeit von "Angels" in %
    FITNESS_REGENERATION_RATE = 0  # Fitness Regenerationsrate (wird durch Alter geteilt)
    DISASTER_PROBABILITY = 2  # Prozentuale Chance, dass ein altruistisches Handeln nötig ist
    FERTILITY = 1.72 # Fruchtbarkeitsrate
    COST_REDUCTION_ALTRUISTIC_ACT = 1  # Anteil der Punkte, welche man selbst verliert wenn man altruistisch handelt
    SEED = 256  # Zufallsseed, gleichlassen für Vergleichbarkeit



def run_sim(lag=False):
    parameters = Parameters()

    df_results = pd.DataFrame()  # Data Frame, in dem die Ergebisse kummuliert werden

    from models.basic_model import ExampleModel

    model = ExampleModel(parameters)

    # Model wird ausgeführt
    with trange(parameters.NUMBER_OF_ITERATIONS) as t:
        for i in t:
            model.step()
            t.set_description('YEAR %i' % model.get_time())
            t.set_postfix(population=str(model.schedule.get_agent_count()))
            data = {'year': model.get_time(), 'population': model.schedule.get_agent_count(),
                                            'median_age': model.get_median_age(),
                                            'median_fitness': model.get_median_fitness(),
                                            'children_per_woman': model.children_per_woman(),
                                            'net_growth': model.get_net_grow(),
                                            'devil_fitness': model.get_devil_fitness(),
                                            'angel_fitness': model.get_angel_fitness(),
                                            'population_angels': model.get_angels(),
                                            'population_devils': model.get_devils()}
            df_results = df_results.append(data, ignore_index=True)
            df_results.to_json("./out/results.json", orient="records")
            if lag:
                agents = {}
                i = 0
                for agent in model.schedule.agents:
                    agents[i] = {"age": agent.age ,"fitness": agent.fitness, "class": agent.__class__.__name__}
                    i = i + 1
                pd.DataFrame.from_dict(agents, "index").to_json("./out/agents.json", orient="records")
                pd.DataFrame(data, index=[0]).to_json("./out/current.json", orient="records")
                time.sleep(0.1)


    print(df_results[['population_angels', 'population_devils', 'population']])
    fig_population = df_results[['year', 'population', 'population_angels', 'population_devils']].plot(
        x='year').get_figure()
    fig_fitness = df_results[['year', 'devil_fitness', 'angel_fitness', 'median_fitness']].plot(
        x='year').get_figure()
    fig_birthrate = df_results[['year', 'children_per_woman']].plot(x='year').get_figure()
    fig_age = df_results[['year', 'median_age']].plot(x='year').get_figure()

    fig_population.savefig('./out/population.png')
    fig_fitness.savefig('./out/fitness.png')
    fig_birthrate.savefig('./out/birthrate.png')
    fig_age.savefig('./out/avg_age.png')
    df_results.to_json("./out/results.json", orient="records")
    get_params(Parameters).to_json("./out/params.json", orient="records")

    # Wegkommentieren, wenn SSH
    # fig_population.show()
    # fig_fitness.show()


if __name__ == '__main__':
    run_sim()
