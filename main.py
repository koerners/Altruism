from mesa.batchrunner import BatchRunner

from models.basic_model import ExampleModel

if __name__ == '__main__':
    parameters = {"n_agents": range(1, 20)}
    batch_run = BatchRunner(ExampleModel, parameters, max_steps=10,
                            model_reporters={"n_agents": lambda m: m.schedule.get_agent_count()})
    batch_run.run_all()
    batch_df = batch_run.get_model_vars_dataframe()


