from mesa import Agent


class Person(Agent):
    def __init__(self, unique_id, model, age=None):
        super().__init__(unique_id, model)
        if age is None:
            self.age = self.random.randint(0, 60)
        else:
            self.age = age

        self.gender = self.random.choice(["m", "f"])
        self.life_expectancy = self.random.randint(60, 100)
        self.partner = None
        self.children = []

    def step(self):
        """
        Wird jeden Tick aufgerufen
        """
        self.life_cycle()

    def life_cycle(self):
        """
        Altern, sterben und Fortpflanzen
        """
        self.age = self.age + 1
        if self.age > self.life_expectancy or self.random.randint(0, 1000)<5:
            # Wenn die Lebenserwartung erreicht ist, stirbt man
            self.die()

        if 40 > self.age > 18 and self.random.randint(0, 100) < 0:
            self.reproduce()

    def die(self):
        self.model.schedule.remove(self)

    def reproduce(self):
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

        if self.partner is not None and len(self.children) < 5:
            child = Person(self.model.next_id(), self.model, age=0)
            self.model.schedule.add(child)
            self.children.append(child)

