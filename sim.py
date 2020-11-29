import matplotlib
import pandas as pd
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from tqdm import trange

from agents import Devil, Angel

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


def run_sim(server=False):
    from main import Parameters

    parameters = Parameters()

    df_results = pd.DataFrame()  # Data Frame, in dem die Ergebisse kummuliert werden

    from models.basic_model import ExampleModel

    model = ExampleModel(parameters)
    if server:
        def agent_portrayal(agent):
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "blue",
                         "r": 0.5}

            if isinstance(agent, Devil):
                portrayal["Color"] = "red"
            if isinstance(agent, Angel):
                portrayal["Color"] = "grey"
            return portrayal

        chart = ChartModule([{"Label": "Angels",
                              "Color": "Blue"}, {"Label": "Devils",
                                                 "Color": "Red"}],
                            data_collector_name='datacollector_a_d')
        chart2 = ChartModule([{"Label": "Fitness",
                               "Color": "Blue"}, {"Label": "Angels",
                                                  "Color": "Green"}, {"Label": "Devils",
                                                                      "Color": "Red"}],
                             data_collector_name='datacollector_fitness')
        chart3 = ChartModule([{"Label": "Birthrate",
                               "Color": "Blue"}],
                             data_collector_name='datacollector_birthrate')
        chart4 = ChartModule([{"Label": "Population",
                               "Color": "Blue"}],
                             data_collector_name='datacollector_population')

        grid = CanvasGrid(agent_portrayal, 100, 100, 600, 600)
        server = ModularServer(ExampleModel,
                               [grid, chart, chart2, chart3, chart4],
                               "Altriusm Model",
                               {"parameters": parameters})
        server.port = 8521  # The default
        server.launch()
    else:

        # Model wird ausgeführt
        with trange(parameters.NUMBER_OF_ITERATIONS) as t:
            for i in t:
                model.step()
                t.set_description('YEAR %i' % model.get_time())
                t.set_postfix(population=str(model.schedule.get_agent_count()))
                df_results = df_results.append(
                    {'year': model.get_time(), 'population': model.schedule.get_agent_count(),
                     'median_age': model.get_median_age(),
                     'median_fitness': model.get_median_fitness(),
                     'children_per_woman': model.children_per_woman(),
                     'net_growth': model.get_net_grow(),
                     'devil_fitness': model.get_devil_fitness(),
                     'angel_fitness': model.get_angel_fitness(),
                     'population_angels': model.get_angels(),
                     'population_devils': model.get_devils()}, ignore_index=True)

        print(df_results[['population_angels', 'population_devils', 'population']])

        #gini = model.datacollector_a_d.get_model_vars_dataframe()
        #print(gini)

        fig_population = df_results[['year', 'population', 'population_angels', 'population_devils']].plot(
            x='year').get_figure()
        fig_angel_devil = df_results[['year', 'population_angels', 'population_devils']].plot(
            x='year').get_figure()
        fig_fitness = df_results[['year', 'devil_fitness', 'angel_fitness', 'median_fitness']].plot(
            x='year').get_figure()
        fig_birthrate = df_results[['year', 'children_per_woman']].plot(x='year').get_figure()
        fig_age = df_results[['year', 'median_age']].plot(x='year').get_figure()

        fig_population.savefig('./out/population.png')
        fig_angel_devil.savefig('./out/angel_devil.png')
        fig_fitness.savefig('./out/fitness.png')
        fig_birthrate.savefig('./out/birthrate.png')
        fig_age.savefig('./out/avg_age.png')
        df_results.to_json("./out/results.json", orient="records")
        get_params(Parameters).to_json("./out/params.json", orient="records")

