from sim import run_sim


class Parameters:
    NUMBER_OF_AGENTS = 100  # Größe der Anfangs-Population
    NUMBER_OF_ITERATIONS = 300  # Jahre, welche simuliert werden sollen
    SPAWN_DEVIL = 10  # Spawn Wahrscheinlichkeit von "Devils" in %
    SPAWN_ANGEL = 10  # Spawn Wahrscheinlichkeit von "Angels" in %
    FITNESS_REGENERATION_RATE = 0  # Fitness Regenerationsrate (wird durch Alter geteilt)
    DISASTER_PROBABILITY = 2.5  # Prozentuale Chance, dass ein altruistisches Handeln nötig ist
    FERTILITY = 2  # Fruchtbarkeitsrate
    COST_REDUCTION_ALTRUISTIC_ACT = 0.8  # Anteil der Punkte, welche man selbst verliert wenn man altruistisch handelt
    SEED = 32  # Zufallsseed, gleichlassen für Vergleichbarkeit


if __name__ == '__main__':
    run_sim(server=False)
