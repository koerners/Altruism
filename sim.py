import matplotlib
import pandas as pd
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from tqdm import trange

from agents import NonAltruist, Altruist

matplotlib.use('Agg')  # Fix für SSH


class ParamsElement(TextElement):
    def __init__(self):
        super().__init__()

    def render(self, model):
        from main import Parameters
        params = get_params(Parameters)

        return params.T.to_html()


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

    if server:
        def agent_portrayal(agent):
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "blue",
                         "r": 0.5}

            if isinstance(agent, NonAltruist):
                portrayal["Color"] = "red"
            if isinstance(agent, Altruist):
                portrayal["Color"] = "green"
            return portrayal

        chart = ChartModule([{"Label": "Altruists",
                              "Color": "Green"}, {"Label": "NonAltruists",
                                                  "Color": "Red"}],
                            data_collector_name='datacollector_a_d')
        chart2 = ChartModule([{"Label": "Fitness",
                               "Color": "Blue"}, {"Label": "Altruists",
                                                  "Color": "Green"}, {"Label": "NonAltruists",
                                                                      "Color": "Red"}],
                             data_collector_name='datacollector_fitness')
        chart3 = ChartModule([{"Label": "Birthrate",
                               "Color": "Blue"}],
                             data_collector_name='datacollector_birthrate')
        chart4 = ChartModule([{"Label": "Population",
                               "Color": "Blue"}],
                             data_collector_name='datacollector_population')

        grid = CanvasGrid(agent_portrayal, 100, 100, 600, 600)

        params = ParamsElement()
        server = ModularServer(ExampleModel,
                               [params, grid, chart, chart2, chart3, chart4],
                               "Altruism Model",
                               {"parameters": parameters})

        server.port = 8521  # The default
        server.launch()
    else:
        model = ExampleModel(parameters)

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
                     'nonAltruist_fitness': model.get_nonAltruist_fitness(),
                     'altruist_fitness': model.get_altruist_fitness(),
                     'population_altruists': model.get_altruists(),
                     'population_nonAltruists': model.get_nonAltruists(),
                     'altruistic_acts_angels': model.get_altruistic_acts_angels(),
                     'altruistic_acts_persons': model.get_altruistic_acts_persons()}, ignore_index=True)}, ignore_index=True)

        print(df_results[['population_altruists', 'population_nonAltruists', 'population']])

        fig_population = df_results[['year', 'population', 'population_altruists', 'population_nonAltruists']].plot(
            x='year').get_figure()
        fig_altruist_nonAltruist = df_results[['year', 'population_altruists', 'population_nonAltruists']].plot(
            x='year').get_figure()
        fig_fitness = df_results[['year', 'nonAltruist_fitness', 'altruist_fitness', 'median_fitness']].plot(
            x='year').get_figure()
        fig_birthrate = df_results[['year', 'children_per_woman']].plot(x='year').get_figure()
        fig_age = df_results[['year', 'median_age']].plot(x='year').get_figure()
        fig_altruistic_acts = df_results[['year', 'altruistic_acts_angels', 'altruistic_acts_persons']].plot(x='year').get_figure()

        fig_population.savefig('./out/population.png')
        fig_altruist_nonAltruist.savefig('./out/altruist_nonAltruist.png')
        fig_fitness.savefig('./out/fitness.png')
        fig_birthrate.savefig('./out/birthrate.png')
        fig_age.savefig('./out/avg_age.png')
        fig_altruistic_acts.savefig('./out/altruistic_acts.png')
        df_results.to_json("./out/results.json", orient="records")
        get_params(Parameters).to_json("./out/params.json", orient="records")
