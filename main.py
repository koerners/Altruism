from mesa.batchrunner import BatchRunner
import matplotlib
from models.basic_model import ExampleModel

if __name__ == '__main__':
    parameters = {"n_agents": range(1, 100)}
    batch_run = BatchRunner(ExampleModel, parameters, max_steps=500,
                            model_reporters={"population": lambda m: m.schedule.get_agent_count(), "median_age": lambda m: m.get_median_age(), "time_passed": lambda m: m.get_time()})
    batch_run.run_all()
    batch_df = batch_run.get_model_vars_dataframe()
    print(batch_df)
    #batch_df.T.plot(x='Run', y='population').get_figure().show()

