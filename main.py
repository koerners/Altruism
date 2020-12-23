from sim import run_sim


class Parameters:
    NUMBER_OF_AGENTS = 100  # Größe der Anfangs-Population
    NUMBER_OF_ITERATIONS = 200  # Jahre, welche simuliert werden sollen
    SPAWN_NONALTRUIST = 10  # Spawn Wahrscheinlichkeit von "NonAltruists" in %
    SPAWN_ALTRUIST = 10  # Spawn Wahrscheinlichkeit von "Altruists" in %
    MUTATION_RATE = 20  # Mutationsrate
    FITNESS_REGENERATION_RATE = 0  # Fitness Regenerationsrate (wird durch Alter geteilt)
    CHANCE_TO_HELP_PROBABILITY = 2.5  # Prozentuale Chance, dass ein altruistisches Handeln nötig ist
    FERTILITY = 2  # Fruchtbarkeitsrate
    COST_REDUCTION_ALTRUISTIC_ACT = 1  # Anteil der Punkte, welche man selbst verliert wenn man altruistisch handelt
    SEED = 545654  # Zufallsseed, gleichlassen für Vergleichbarkeit


if __name__ == '__main__':
    run_sim(server=False)
