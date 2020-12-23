from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import BaseScheduler

from agents import BaseAgent, Altruist, NonAltruist
from main import Parameters


class ExampleModel(Model):
    def __init__(self, parameters: Parameters):
        super().__init__()
        self.schedule = BaseScheduler(self)
        self.ready_to_mate = []

        self.net_grow = None
        self.average_age = None
        self.average_fitness = None
        self.nonAltruist_fitness = None
        self.altruist_fitness = None
        self.birthrate = None
        self.altruists = None
        self.nonAltruists = None
        self.parameters = parameters
        self.population = 0
        self.datacollector_a_d = DataCollector(
            model_reporters={"Altruists": "altruists", "NonAltruists": "nonAltruists"})
        self.datacollector_fitness = DataCollector(
            model_reporters={"Fitness": "average_fitness", "Altruists": "altruist_fitness",
                             "NonAltruists": "nonAltruist_fitness"})
        self.datacollector_birthrate = DataCollector(
            model_reporters={"Birthrate": "birthrate"})
        self.datacollector_population = DataCollector(
            model_reporters={"Population": "population"})

        self.altruistic_acts_altruists = 0
        self.altruistic_acts_base_agent = 0

        self.average_fitness_cost_round = []
        self.average_fitness_cost = []

        self.reset_randomizer(seed=self.parameters.SEED)  # Zufallsseed

        self.grid = MultiGrid(100, 100, True)

        # Initiale Agenten werden angelegt
        self.initial_agents = []
        i = 0
        while len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
            # Mit einer x% Chance spawnt ein spezieller Charakter
            rand = self.random.randint(0, 100)
            appended = False

            if rand < self.parameters.SPAWN_NONALTRUIST and len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
                a = NonAltruist(i, self)
                self.initial_agents.append(a)
                i += 1
                appended = True

            if rand < self.parameters.SPAWN_ALTRUIST and len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
                b = Altruist(i, self)
                self.initial_agents.append(b)
                i += 1

                appended = True

            if not appended and len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
                c = BaseAgent(i, self)
                self.initial_agents.append(c)
                i += 1

        for agent in self.initial_agents:
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

    def step(self):
        # Schritt, der jeden "Tick" ausgeführt wird
        self.average_fitness_cost_round = []
        self.ready_to_mate = []
        self.net_grow = 0
        self.average_age = None
        self.average_fitness = None
        self.nonAltruist_fitness = None
        self.altruist_fitness = None
        self.birthrate = None
        self.altruists = None
        self.nonAltruists = None
        self.population = len(self.schedule.agents)
        self.schedule.step()
        self.calculate_statistics()
        self.datacollector_a_d.collect(self)
        self.datacollector_fitness.collect(self)
        self.datacollector_birthrate.collect(self)
        self.datacollector_population.collect(self)

    def calculate_statistics(self):
        """
        Etwas unschöne Methode um Statistiken zu sammeln aber sonst müsste man die Agenten Liste sehr häufig durchgehen...
        """
        if len(self.schedule.agents) > 0:

            age = 0
            nonAltruist_fitness = 0
            altruist_fitness = 0
            altruists = 0
            nonAltruists = 0
            fitness = 0
            woman = 0
            children = 0
            for agent in self.schedule.agents:
                age += agent.age
                if isinstance(agent, NonAltruist):
                    nonAltruist_fitness += agent.fitness
                    nonAltruists = nonAltruists + 1
                if isinstance(agent, Altruist):
                    altruist_fitness += agent.fitness
                    altruists = altruists + 1
                    self.altruistic_acts_altruists += agent.altruistic_acts_agent

                if isinstance(agent, BaseAgent):
                    self.altruistic_acts_base_agent += agent.altruistic_acts_agent
                fitness += agent.fitness

                if agent.gender == "f":
                    children += len(agent.children)
                    woman = woman + 1

            self.average_age = age / len(self.schedule.agents)
            self.average_fitness = fitness / len(self.schedule.agents)
            if nonAltruists > 0:
                self.nonAltruist_fitness = nonAltruist_fitness / nonAltruists
            if altruists > 0:
                self.altruist_fitness = altruist_fitness / altruists
            if woman > 0:
                self.birthrate = children / woman

            self.nonAltruists = nonAltruists
            self.altruists = altruists

    def get_time(self):
        """
        :return: Die in der Simulation vergangenen Jahre / Ticks
        """
        return self.schedule.steps

    def get_median_age(self):
        return self.average_age

    def get_median_fitness(self):
        """
        Berechnet die Durschnittsfitness der Bevölkerung
        :return: Durschnittsfitness oder None
        """
        return self.average_fitness

    def get_nonAltruist_fitness(self):
        """
        Berechnet die Durschnittsfitness der nonAltruists
        :return: Durschnittsfitness oder None
        """
        return self.nonAltruist_fitness

    def get_altruist_fitness(self):
        """
        Berechnet die Durschnittsfitness der altruists
        :return: Durschnittsfitness oder None
        """
        return self.altruist_fitness

    def children_per_woman(self):
        """
        Berechnet die Durchschnittsanzahl der Kinder pro Frau
        :return: Durchschnittsanzahl oder None
        """
        return self.birthrate

    def get_net_grow(self):
        return self.net_grow

    def get_altruists(self):
        return self.altruists

    def get_nonAltruists(self):
        return self.nonAltruists

    def get_altruistic_acts_altruists(self):
        return self.altruistic_acts_altruists

    def get_altruistic_acts_base_agents(self):
        return self.altruistic_acts_base_agent

    def get_average_cost(self):
        if len(self.average_fitness_cost) < 1:
            return 0
        cost = 0
        for c in self.average_fitness_cost:
            cost += c

        return cost / len(self.average_fitness_cost)

    def get_average_fitness_cost_round(self):
        if len(self.average_fitness_cost_round) < 1:
            return 0
        cost = 0
        for c in self.average_fitness_cost_round:
            cost += c

        return cost / len(self.average_fitness_cost_round)
