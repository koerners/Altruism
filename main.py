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
    NUMBER_OF_ITERATIONS = 300  # Jahre, welche simuliert werden sollen
    SPAWN_DEVIL = 10  # Spawn Wahrscheinlichkeit von "Devils" in %
    SPAWN_ANGEL = 10  # Spawn Wahrscheinlichkeit von "Angels" in %
    FITNESS_REGENERATION_RATE = 0  # Fitness Regenerationsrate (wird durch Alter geteilt)
    DISASTER_PROBABILITY = 2.5  # Prozentuale Chance, dass ein altruistisches Handeln nötig ist
    FERTILITY = 2 # Fruchtbarkeitsrate
    SEED = 256  # Zufallsseed, gleichlassen für Vergleichbarkeit


if __name__ == '__main__':

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
            df_results = df_results.append({'year': model.get_time(), 'population': model.schedule.get_agent_count(),
                                            'median_age': model.get_median_age(),
                                            'median_fitness': model.get_median_fitness(),
                                            'children_per_woman': model.children_per_woman(),
                                            'net_growth': model.get_net_grow(),
                                            'devil_fitness': model.get_devil_fitness(),
                                            'angel_fitness': model.get_angel_fitness(),
                                            'population_angels': model.get_angels(),
                                            'population_devils': model.get_devils()}, ignore_index=True)

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
