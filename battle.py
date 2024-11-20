import random

def fight(agent, enemy_name, enemy_stats):
    """
    Simulates a fight between an agent and an enemy (e.g., dragon).
    """
    print(f"{agent.name} is fighting {enemy_name}!")
    agent_health = agent.attributes["health"]
    enemy_health = enemy_stats["health"]

    while agent_health > 0 and enemy_health > 0:
        agent_attack = random.randint(1, agent.attributes["strength"])
        enemy_attack = random.randint(1, enemy_stats["strength"])

        # Apply damage
        enemy_health -= agent_attack
        agent_health -= enemy_attack

        print(f"{agent.name} deals {agent_attack} damage. {enemy_name} has {enemy_health} health left.")
        print(f"{enemy_name} deals {enemy_attack} damage. {agent.name} has {agent_health} health left.")

    if agent_health > 0:
        print(f"{agent.name} wins the fight!")
    else:
        print(f"{agent.name} is defeated by {enemy_name}.")
