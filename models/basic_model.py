from mesa import Model, Agent
from mesa.time import RandomActivation, BaseScheduler

from agents import Person, Angel, Devil
from main import Parameters


class ExampleModel(Model):
    def __init__(self, parameters: Parameters):
        super().__init__()
        self.schedule = BaseScheduler(self)
        self.ready_to_mate = []

        self.net_grow = None
        self.average_age = None
        self.average_fitness = None
        self.devil_fitness = None
        self.angel_fitness = None
        self.birthrate = None
        self.angels = None
        self.devils = None
        self.parameters = parameters

        self.reset_randomizer(seed=self.parameters.SEED)  # Zufallsseed

        # Initiale Agenten werden angelegt
        self.initial_agents = []
        i = 0
        while len(self.initial_agents) < self.parameters.NUMER_OF_AGENTS:
            # Mit einer x% Chance spawnt ein spezieller Charakter
            rand = self.random.randint(0, 100)
            appended = False

            if rand < self.parameters.SPAWN_DEVIL and len(self.initial_agents) < self.parameters.NUMER_OF_AGENTS:
                a = Devil(i, self)
                self.initial_agents.append(a)
                i += 1
                appended = True

            if rand < self.parameters.SPAWN_ANGEL and len(self.initial_agents) < self.parameters.NUMER_OF_AGENTS:
                b = Angel(i, self)
                self.initial_agents.append(b)
                i += 1

                appended = True

            if not appended and len(self.initial_agents) < self.parameters.NUMER_OF_AGENTS:
                c = Person(i, self)
                self.initial_agents.append(c)
                i += 1

        for agent in self.initial_agents:
            self.schedule.add(agent)

    def step(self):
        # Schritt, der jeden "Tick" ausgeführt wird
        self.ready_to_mate = []
        self.net_grow = 0
        self.average_age = None
        self.average_fitness = None
        self.devil_fitness = None
        self.angel_fitness = None
        self.birthrate = None
        self.angels = None
        self.devils = None

        self.schedule.step()
        self.calculate_statistics()

    def calculate_statistics(self):
        """
        Etwas unschöne Methode um Statistiken zu sammeln aber sonst müsste man die Agenten Liste sehr häufig durchgehen...
        """
        if len(self.schedule.agents) > 0:

            age = 0
            devil_fitness = 0
            angel_fitness = 0
            angels = 0
            devils = 0
            fitness = 0
            woman = 0
            children = 0
            for agent in self.schedule.agents:
                age += agent.age
                if isinstance(agent, Devil):
                    devil_fitness += agent.fitness
                    devils = devils + 1
                if isinstance(agent, Angel):
                    angel_fitness += agent.fitness
                    angels = angels + 1
                fitness += agent.fitness

                if agent.gender == "f":
                    children += len(agent.children)
                    woman = woman + 1

            self.average_age = age / len(self.schedule.agents)
            self.average_fitness = fitness / len(self.schedule.agents)
            if devils > 0:
                self.devil_fitness = devil_fitness / devils
            if angels > 0:
                self.angel_fitness = angel_fitness / angels
            if woman > 0:
                self.birthrate = children / woman

            self.devils = devils
            self.angels = angels

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

    def get_devil_fitness(self):
        """
        Berechnet die Durschnittsfitness der devils
        :return: Durschnittsfitness oder None
        """
        return self.devil_fitness

    def get_angel_fitness(self):
        """
        Berechnet die Durschnittsfitness der angels
        :return: Durschnittsfitness oder None
        """
        return self.angel_fitness

    def children_per_woman(self):
        """
        Berechnet die Durchschnittsanzahl der Kinder pro Frau
        :return: Durchschnittsanzahl oder None
        """
        return self.birthrate

    def get_net_grow(self):
        return self.net_grow

    def get_angels(self):
        return self.angels

    def get_devils(self):
        return self.devils
