def talk(agent, other_agent):
    """
    Simulates a conversation and relationship building.
    """
    print(f"{agent.name} talks to {other_agent.name}.")
    agent.interact(other_agent)
    agent.update_relationship(other_agent, value=10)
    print(f"The relationship between {agent.name} and {other_agent.name} improved!")
