from mesa import Model
from mesa.time import RandomActivation

from agents import Person, Angel, Devil


class ExampleModel(Model):
    def __init__(self, n_agents):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.ready_to_mate = []
        for i in range(n_agents):
            if self.random.randint(0, 100) == 1:
                # Mit einer 1% Chance spawnt ein speizieller Charakter
                a = self.random.choice([Angel(i, self), Devil(i, self)])
            else:
                # Sonst wird eine normale Person hinzugefügt
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

    def get_median_fitness(self):
        """
        Berechnet die Durschnittsfitness der Bevölkerung
        :return: Durchschnittsalter oder None
        """
        if len(self.schedule.agents) > 0:
            fitness = 0
            for agent in self.schedule.agents:
                fitness += agent.fitness

            return fitness / len(self.schedule.agents)
        return None
