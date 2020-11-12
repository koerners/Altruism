from mesa import Agent


class Person(Agent):
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

    def step(self):
        """
        Wird jeden Tick aufgerufen
        """
        self.life_cycle()
        if self.random.randint(0, 100) == 1:
            # Zufällig wird die Option gegeben altruistisch zu handeln
            self.altruistic_act()

    def life_cycle(self):
        """
        Altern, sterben und Fortpflanzen
        """
        self.age = self.age + 1
        if self.age > self.life_expectancy or self.random.randint(0, 1000) < 5 or self.fitness < 0:
            # Wenn die Lebenserwartung erreicht ist, man Pech hat, oder die Fitness unter 0 sinkt
            self.die()

        if 40 > self.age > 18 and (self.random.randint(0, 1000) < (1.2 * self.fitness)):
            # Basierend auf dem Alter, einem Zufallswert und der eigenen Fitness kann sich fortgepflanzt werden
            self.find_partner()
            self.reproduce()

    def die(self):
        # Sterben
        self.model.net_grow = self.model.net_grow - 1
        self.model.schedule.remove(self)

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
            child = self.create_child()
            child.parents = [self, self.partner]
            self.children.append(child)
            self.partner.children.append(child)
            self.model.net_grow = self.model.net_grow + 1
            self.model.schedule.add(child)

    def create_child(self):
        """
        Vererbungsstrategie Devil / Angel / "Normal"
        :return: Child
        """
        # TODO: Was sinnvolleres

        if isinstance(self, Devil) or isinstance(self.partner, Devil):
            return Devil(self.model.next_id(), self.model, age=0, fitness=(self.fitness + self.partner.fitness) / 2)

        if isinstance(self, Angel) or isinstance(self.partner, Angel):
            return Angel(self.model.next_id(), self.model, age=0, fitness=(self.fitness + self.partner.fitness) / 2)

        return Person(self.model.next_id(), self.model, age=0, fitness=(self.fitness + self.partner.fitness) / 2)

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
            self.fitness = self.fitness - cost
            needs_help.fitness = needs_help.fitness + cost
        else:
            needs_help.fitness = needs_help.fitness - cost

    def altruism_check(self, needs_help, cost):
        """
        Prüft, ob der Altruitische Akt ausgeführt wird
        :param needs_help: Agent, der Hilfe benötigt
        :param cost: Kosten
        :return: True oder False
        """
        # TODO: Sinnvolle Implementierung basierend z.B. auf dem Verwandschaftsgrad
        return self.random.choice([True, False])


class Angel(Person):
    """
    Eine durchweg altruistisch handelnde Person
    """

    def __init__(self, unique_id, model, age=None, fitness=100):
        super().__init__(unique_id, model, age=age, fitness=fitness)

    def altruism_check(self, needs_help, cost):
        return True


class Devil(Person):
    """
    Eine durchweg egoistisch handelnde Person
    """

    def __init__(self, unique_id, model, age=None, fitness=100):
        super().__init__(unique_id, model, age=age, fitness=fitness)

    def altruism_check(self, needs_help, cost):
        return False
