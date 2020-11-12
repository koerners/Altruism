from models.basic_model import ExampleModel
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    NUMER_OF_AGENTS = 100  # Größe der Population
    NUMBER_OF_ITERATIONS = 500  # Jahre, welche simuliert werden sollen

    df_results = pd.DataFrame()  # Data Frame, in dem die Ergebisse kummuliert werden
    model = ExampleModel(NUMER_OF_AGENTS)
    for i in tqdm(range(NUMBER_OF_ITERATIONS)):
        model.step()
        df_results = df_results.append({'year': model.get_time(), 'population': model.schedule.get_agent_count(),
                                        'median_age': model.get_median_age(),
                                        'median_fitness': model.get_median_fitness(),
                                        'children_per_woman': model.children_per_woman(),
                                        'net_growth': model.get_net_grow(), 'devil_fitness': model.get_devil_fitness(),
                                        'angel_fitness': model.get_angel_fitness(),
                                        'population_angels': model.get_angels(),
                                        'population_devils': model.get_devils()}, ignore_index=True)

    print(df_results)

    fig_population = df_results[['year', 'population', 'population_angels', 'population_devils']].plot(
        x='year').get_figure()
    fig_fitness = df_results[['year', 'devil_fitness', 'angel_fitness', 'median_fitness']].plot(
        x='year').get_figure()
    fig_age_growth = df_results[['year', 'children_per_woman', 'net_growth']].plot(x='year').get_figure()

    fig_population.savefig('./out/population.png')
    fig_fitness.savefig('./out/fitness.png')
    fig_age_growth.savefig('./out/fig_age_growth.png')
    df_results.to_json("./out/results.json")

    # fig_population.show()
    # fig_age_fitness.show()
