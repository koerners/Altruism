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


def run_sim(id_, parameters=None, no_img=False):
    df_results = pd.DataFrame(columns=['ID'])  # Data Frame, in dem die Ergebisse kummuliert werden

    from models.basic_model import ExampleModel

    model = ExampleModel(parameters)

    # Model wird ausgeführt
    with trange(parameters.NUMBER_OF_ITERATIONS) as t:
        for i in t:
            if not len(model.schedule.agents) > 0:
                continue
            model.step()
            t.set_description('YEAR %i' % model.get_time())
            t.set_postfix(population=str(model.schedule.get_agent_count()))
            df_results = df_results.append(
                {'SEED': parameters.SEED,
                 'SPAWN_NONALTRUIST': parameters.SPAWN_NONALTRUIST,
                 'SPAWN_ALTRUIST': parameters.SPAWN_ALTRUIST,
                 'CHANCE_TO_HELP_PROBABILITY': parameters.CHANCE_TO_HELP_PROBABILITY,
                 'COST_REDUCTION_ALTRUISTIC_ACT': parameters.COST_REDUCTION_ALTRUISTIC_ACT,
                 'year': model.get_time(), 'population': model.schedule.get_agent_count(),
                 'median_age': model.get_median_age(),
                 'median_fitness': model.get_median_fitness(),
                 'children_per_woman': model.children_per_woman(),
                 'net_growth': model.get_net_grow(),
                 'nonAltruist_fitness': model.get_nonAltruist_fitness(),
                 'altruist_fitness': model.get_altruist_fitness(),
                 'population_altruists': model.get_altruists(),
                 'population_nonAltruists': model.get_nonAltruists(),
                 'altruistic_acts_altruists': model.get_altruistic_acts_altruists(),
                 'altruistic_acts_base_agents': model.get_altruistic_acts_base_agents(),
                 'average_fitness_cost': model.get_average_cost(),
                 'average_fitness_cost_round': model.get_average_fitness_cost_round(),
                 'fitness_at_death': model.get_all_death_fitness(), 'age_at_death': model.get_all_death_age(),
                 'died_of_fitness_loss': model.get_died_fitness(),
                 'died_of_chance': model.get_died_random(),
                 'died_of_old_age': model.get_died_age()
                 },
                ignore_index=True)

        if not no_img:
            fig_population = df_results[['year', 'population', 'population_altruists', 'population_nonAltruists']].plot(
                x='year').get_figure()
            fig_altruist_nonAltruist = df_results[['year', 'population_altruists', 'population_nonAltruists']].plot(
                x='year').get_figure()
            fig_fitness = df_results[['year', 'nonAltruist_fitness', 'altruist_fitness', 'median_fitness']].plot(
                x='year').get_figure()
            fig_fitness_death = df_results[['year', 'median_fitness', 'fitness_at_death']].plot(
                x='year').get_figure()
            fig_birthrate = df_results[['year', 'children_per_woman']].plot(x='year').get_figure()
            fig_age = df_results[['year', 'median_age', 'age_at_death']].plot(x='year').get_figure()
            fig_cost = df_results[['year', 'average_fitness_cost_round', 'average_fitness_cost']].plot(
                x='year').get_figure()
            fig_altruistic_acts = df_results[['year', 'altruistic_acts_altruists', 'altruistic_acts_base_agents']].plot(
                x='year').get_figure()

            fig_cause_of_death = df_results[['year', 'died_of_fitness_loss', 'died_of_chance', 'died_of_old_age']].plot(
                x='year').get_figure()

            directory = "./out/" + str(id_) + "-" + str(parameters.SEED) + "/"
            from pathlib import Path
            Path(directory).mkdir(parents=True, exist_ok=True)

            fig_population.savefig(directory + 'population.png')
            fig_altruist_nonAltruist.savefig(directory + 'altruist_nonAltruist.png')
            fig_fitness.savefig(directory + 'fitness.png')
            fig_birthrate.savefig(directory + 'birthrate.png')
            fig_fitness_death.savefig(directory + 'fig_fitness_death.png')
            fig_age.savefig(directory + 'avg_age.png')
            fig_cost.savefig(directory + 'fig_cost.png')
            fig_altruistic_acts.savefig(directory + 'altruistic_acts.png')
            fig_cause_of_death.savefig(directory + 'fig_cause_of_death.png')
            df_results.iloc[[-1]].to_json(directory + "results.json", orient="records")
            # get_params(Parameters).to_json(directory + "params.json", orient="records")
            matplotlib.pyplot.close('all')
        df_results.iloc[-1, df_results.columns.get_loc('ID')] = id_
        return df_results.iloc[[-1]]
