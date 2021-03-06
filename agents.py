from enum import Enum, auto

from mesa import Agent


class DeathCauses(Enum):
    FITNESS = auto()
    RANDOM = auto()
    OLD_AGE = auto()


class BaseAgent(Agent):
    def __init__(self, unique_id, model, age=None, fitness=100):
        super().__init__(unique_id, model)
        if age is None:
            self.age = self.random.randint(0, 60)  # Für die Initialbevölkerung wird zufällig das Alter bestimmt
        else:
            self.age = age

        self.gender = self.random.choice(["m", "f"])  # Geschlecht
        self.life_expectancy = self.random.randint(70, 100)  # Lebenserwartung
        self.partner = None  # Der eigene Partner
        self.children = []  # Die eigenen Kinder
        self.parents = []  # Die eigenen Eltern
        self.fitness = fitness  # Fitness Wert u.a. für Fortpflanzung
        self.parameters = self.model.parameters
        self.altruistic_acts_agent = 0
        self.cause_of_death = None

    def get_neighbours(self):
        neighbors = []
        x, y = self.pos
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                neighbors.append((x + dx, y + dy))

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        """
        Wird jeden Tick aufgerufen
        """
        if self.pos is not None:
            self.move()
        self.life_cycle()
        if self.random.randint(0, 1000) < self.parameters.CHANCE_TO_HELP_PROBABILITY * 10:
            # Zufällig wird die Option gegeben altruistisch zu handeln
            self.altruistic_act()

    def life_cycle(self):
        """
        Altern, sterben und Fortpflanzen
        """
        self.age = self.age + 1

        self.fitness = self.fitness + (
                self.parameters.FITNESS_REGENERATION_RATE / self.age)  # Fitness wird regeneriert. Wirklich gute Idee?

        if self.age > self.life_expectancy:
            # Wenn die Lebenserwartung erreicht ist, man Pech hat, oder die Fitness unter 0 sinkt
            self.cause_of_death = DeathCauses.OLD_AGE
            self.die()

        elif self.fitness < 0:
            # Wenn die Lebenserwartung erreicht ist, man Pech hat, oder die Fitness unter 0 sinkt
            self.cause_of_death = DeathCauses.FITNESS
            self.die()

        elif self.random.randint(0, 1000) < 1:
            # Wenn die Lebenserwartung erreicht ist, man Pech hat, oder die Fitness unter 0 sinkt
            self.cause_of_death = DeathCauses.RANDOM
            self.die()

        if 40 > self.age > 18 and (self.random.randint(0, 1000) < (self.parameters.FERTILITY * self.fitness)):
            # Basierend auf dem Alter, einem Zufallswert und der eigenen Fitness kann sich fortgepflanzt werden
            self.find_partner()
            self.reproduce()

    def die(self):
        # Sterben
        self.model.net_grow = self.model.net_grow - 1
        self.model.died.append(self)
        self.model.died_this_round.append(self)
        self.model.schedule.remove(self)
        if self.pos is not None:
            self.model.grid.remove_agent(self)

    def find_partner(self):
        if self.partner is None:
            # Wahl des Partners aus dem Partnerpool
            self.model.ready_to_mate.append(self)
            for potential_partner in self.model.ready_to_mate:
                if potential_partner.gender != self.gender:
                    self.partner = potential_partner
                    potential_partner.partner = self
                    self.model.ready_to_mate.remove(self)
                    self.model.ready_to_mate.remove(potential_partner)
                    break

    def reproduce(self):
        """
        Ein Kind wird gezeugt und der Simulation hinzugefügt
        """
        if self.partner is not None:
            if self.gender == "f":
                child = self.create_child()
                child.parents = [self, self.partner]
                self.children.append(child)
                self.partner.children.append(child)
                self.model.net_grow = self.model.net_grow + 1
                self.model.schedule.add(child)
                x = self.random.randrange(self.model.grid.width)
                y = self.random.randrange(self.model.grid.height)
                self.model.grid.place_agent(self, (x, y))

    def create_child(self):
        """
        Vererbungsstrategie NonAltruist / Altruist / "Normal"
        :return: Child
        """
        if self.random.randint(0, 100) <= self.parameters.MUTATION_RATE:
            trait_to_inherit = self.random.choice([Altruist, NonAltruist, BaseAgent])
        else:
            trait_to_inherit = self.random.choice([self, self.partner])

        if isinstance(trait_to_inherit, NonAltruist):
            return NonAltruist(self.model.next_id(), self.model, age=0,
                               fitness=(self.fitness + self.partner.fitness) / 2)
        if isinstance(trait_to_inherit, Altruist):
            return Altruist(self.model.next_id(), self.model, age=0, fitness=(self.fitness + self.partner.fitness) / 2)

        return BaseAgent(self.model.next_id(), self.model, age=0, fitness=(self.fitness + self.partner.fitness) / 2)

    def altruistic_act(self):
        """
        Der Agent kommt in die Situation, altruistisch handeln zu können.
        Tut er dies, verliert er selbst Fitness aber der Hilfsbefürtige gewinnt an Fitness
        """
        if len(self.model.schedule.agents) < 2:
            return

        needs_help = self.random.choice(self.model.schedule.agents)  # Hilfsbedürtige Person
        cost = self.random.randint(1, 10)  # Kosten für einen selbst
        if self.altruism_check(needs_help, cost) and self != needs_help:
            self.fitness = self.fitness - cost * self.parameters.COST_REDUCTION_ALTRUISTIC_ACT
            needs_help.fitness = needs_help.fitness + cost
            self.model.average_fitness_cost.append(cost)
            self.model.average_fitness_cost_round.append(cost)
            self.altruistic_acts_agent += 1

    def altruism_check(self, needs_help, cost):
        """
        Prüft, ob der Altruitische Akt ausgeführt wird
        :param needs_help: Agent, der Hilfe benötigt
        :param cost: Kosten
        :return: True oder False
        """

        return self.random.choice([True, False])


class Altruist(BaseAgent):
    """
    Eine durchweg altruistisch handelnde BaseAgent
    """

    def __init__(self, unique_id, model, age=None, fitness=100):
        super().__init__(unique_id, model, age=age, fitness=fitness)

    def altruism_check(self, needs_help, cost):
        return True


class NonAltruist(BaseAgent):
    """
    Eine durchweg egoistisch handelnde BaseAgent
    """

    def __init__(self, unique_id, model, age=None, fitness=100):
        super().__init__(unique_id, model, age=age, fitness=fitness)

    def altruism_check(self, needs_help, cost):
        return False
