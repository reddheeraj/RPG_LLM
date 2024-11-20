import streamlit as st
from agent import GenerativeAgent
from world import GameWorld
from battle import fight
import random
from LLM_Integration import LLMIntegration
from Agent_Logger import AgentLogger
from visualize import start_visualization


logger = AgentLogger()

def setup_game():
    llm = LLMIntegration()
    knight_attributes = {"health": 100, "strength": 8, "intelligence": 5, "dexterity": 6, "personality": "brave"}
    wizard_attributes = {"health": 80, "strength": 4, "intelligence": 9, "dexterity": 5, "personality": "wise"}
    
    knight = GenerativeAgent("Knight", llm, knight_attributes, initial_info={"Knows the castle is locked."})
    wizard = GenerativeAgent("Wizard", llm, wizard_attributes, initial_info={"Knows about treasure in the dungeon."})

    world = GameWorld(["Village", "Forest", "Castle", "Dungeon"])
    world.add_agent(knight)
    world.add_agent(wizard)
    return world, knight, wizard

def main():
    # Set up the game world and agents
    world, knight, wizard = setup_game()

    # Start Streamlit UI
    st.title("RPG World Simulation")

    # Simulate the game turn by turn
    # if st.button("Run Simulation"):
    events = ["A dragon appears in the forest.", "The castle gates are locked.", "A treasure chest is found in the dungeon."]
    
    # Randomly trigger an event
    event = random.choice(events)
    st.write(f"**Event:** {event}")
    world.trigger_event(event)
    
    # Agents act on the event
    for agent in world.agents:
        action = agent.act(event)
        logger.log_action(agent.name, action, event)
        if "fight" in action.lower():
            fight(agent, "Dragon", {"health": 150, "strength": 10})
        else:
            print(" ---------------- ")
            st.write(f"**{agent.name}** said: {action}.")
    
    # Update world dynamics: random interactions and agent movements
    world.random_interactions()
    world.dynamic_walk()

    # Visualize the world and agents
    world.visualize_world()
    start_visualization(world)
    # Optionally: Save logs after each turn
    logger.save_logs()

if __name__ == "__main__":
    main()
