from mesa import Model
from mesa.time import RandomActivation

from agents import Person


class ExampleModel(Model):
    def __init__(self, n_agents):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.ready_to_mate = []
        for i in range(n_agents):
            a = Person(i, self)
            self.schedule.add(a)

    def step(self):
        # Schritt, der jeden "Tick" ausgeführt wird
        self.ready_to_mate = []
        self.schedule.step()

    def get_time(self):
        """
        :return: Die in der Simulation vergangenen Jahre / Ticks
        """
        return self.schedule.steps

    def get_median_age(self):
        """
        Berechnet das Durchschnittsalter der Bevölkerung
        :return: Durchschnittsalter oder None
        """
        if len(self.schedule.agents) > 0:
            age = 0
            for agent in self.schedule.agents:
                age += agent.age

            return age / len(self.schedule.agents)
        return None
