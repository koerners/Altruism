from models.basic_model import ExampleModel
import pandas as pd
from tqdm import tqdm

if __name__ == '__main__':
    NUMER_OF_AGENTS = 100  # Größe der Population
    NUMBER_OF_ITERATIONS = 500  # Jahre, welche simuliert werden sollen

    df_results = pd.DataFrame(columns=['year', 'population', 'median_age', 'median_fitness'])
    model = ExampleModel(NUMER_OF_AGENTS)
    for i in tqdm(range(NUMBER_OF_ITERATIONS)):
        model.step()
        df_results = df_results.append({'year': model.get_time(), 'population': model.schedule.get_agent_count(),
                                        'median_age': model.get_median_age(),
                                        'median_fitness': model.get_median_fitness()}, ignore_index=True)

    print(df_results)

    fig_population = df_results[['year', 'population']].plot(x='year').get_figure()
    fig_age_fitness = df_results[['year', 'median_age', 'median_fitness']].plot(x='year').get_figure()

    fig_population.savefig('./out/population.png')
    fig_age_fitness.savefig('./out/age_fitness.png')
    df_results.to_json("./out/results.json")

    # fig_population.show()
    # fig_age_fitness.show()
