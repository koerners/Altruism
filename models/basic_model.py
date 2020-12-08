from mesa import Model, Agent
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation, BaseScheduler

from agents import Person, Angel, Devil
from main import Parameters
from mesa.space import MultiGrid
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
        self.person_fitness = None
        self.birthrate = None
        self.angels = None
        self.devils = None
        self.persons = None
        self.parameters = parameters
        self.population = 0
        self.datacollector_a_d = DataCollector(
            model_reporters={"Angels": "angels", "Devils": "devils"})
        self.datacollector_fitness = DataCollector(
            model_reporters={"Fitness": "average_fitness", "Angels": "angel_fitness", "Devils": "devil_fitness"})
        self.datacollector_birthrate = DataCollector(
            model_reporters={"Birthrate": "birthrate"})
        self.datacollector_population = DataCollector(
            model_reporters={"Population": "population"})
        
        self.altruistic_acts_angels = 0
        self.altruistic_acts_persons = 0

        self.reset_randomizer(seed=self.parameters.SEED)  # Zufallsseed

        self.grid = MultiGrid(100, 100, True)

        # Initiale Agenten werden angelegt
        self.initial_agents = []
        i = 0
        while len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
            # Mit einer x% Chance spawnt ein spezieller Charakter
            rand = self.random.randint(0, 100)
            appended = False

            if rand < self.parameters.SPAWN_DEVIL and len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
                a = Devil(i, self)
                self.initial_agents.append(a)
                i += 1
                appended = True

            if rand < self.parameters.SPAWN_ANGEL and len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
                b = Angel(i, self)
                self.initial_agents.append(b)
                i += 1

                appended = True

            if not appended and len(self.initial_agents) < self.parameters.NUMBER_OF_AGENTS:
                c = Person(i, self)
                self.initial_agents.append(c)
                i += 1

        for agent in self.initial_agents:
            self.schedule.add(agent)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

    def step(self):
        # Schritt, der jeden "Tick" ausgeführt wird

        self.ready_to_mate = []
        self.net_grow = 0
        self.average_age = None
        self.average_fitness = None
        self.devil_fitness = None
        self.angel_fitness = None
        self.person_fitness = None
        self.birthrate = None
        self.angels = None
        self.devils = None
        self.persons = None
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
            devil_fitness = 0
            angel_fitness = 0
            person_fitness = 0
            angels = 0
            devils = 0
            persons = 0
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
                    self.altruistic_acts_angels += agent.altruistic_acts_agent
                if isinstance(agent, Person):
                    person_fitness += agent.fitness
                    persons = persons + 1
                    self.altruistic_acts_persons += agent.altruistic_acts_agent
                fitness += agent.fitness

                if agent.gender == "f":
                    children += len(agent.children)
                    woman = woman + 1
                
                #self.altruistic_acts += agent.altruistic_acts_agent

            self.average_age = age / len(self.schedule.agents)
            self.average_fitness = fitness / len(self.schedule.agents)
            if devils > 0:
                self.devil_fitness = devil_fitness / devils
            if angels > 0:
                self.angel_fitness = angel_fitness / angels
            
            self.person_fitness = person_fitness / persons
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
    
    def get_person_fitness(self):
        """
        Berechnet die Durschnittsfitness der persons
        :return: Durschnittsfitness oder None
        """
        return self.person_fitness

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

    def get_altruistic_acts_angels(self):
        return self.altruistic_acts_angels
    
    def get_altruistic_acts_persons(self):
        return self.altruistic_acts_persons