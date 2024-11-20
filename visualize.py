import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random

# Simulated World
class WorldVisualizer:
    def __init__(self, world):
        self.world = world

    def render_world(self):
        """
        Render the world map with agents at their current locations.
        """
        # Create a graph of locations
        G = nx.Graph()
        for location in self.world.locations:
            G.add_node(location)

        # Add connections between locations (for simplicity, random connections)
        for i in range(len(self.world.locations) - 1):
            G.add_edge(self.world.locations[i], self.world.locations[i + 1])

        # Plot the world map
        pos = nx.spring_layout(G)
        plt.figure(figsize=(8, 6))
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10)

        # Add agents to the map
        for agent in self.world.agents:
            agent_location = agent.current_location
            if agent_location in pos:
                x, y = pos[agent_location]
                plt.text(x, y + 0.05, agent.name, fontsize=12, color="red", ha="center")

        st.pyplot(plt)

# Visualization loop
def start_visualization(world):
    st.title("RPG World Simulation")
    world_vis = WorldVisualizer(world)

    # Add a button to advance the simulation to the next turn
    if st.button("Next Turn"):
        # Simulate world and agent updates for the next turn
        for agent in world.agents:
            agent.age_agent()  # Increment agent's age (or any other updates)
            # Update agent's position or make them perform actions
            direction = (random.choice([-1, 1]), random.choice([-1, 1]))  # Example movement
            agent.move(direction)
        
        # Render the world and agents' status
        st.header("World Map")
        world_vis.render_world()

        st.header("Agent Information")
        for agent in world.agents:
            st.write(f"**{agent.name}**")
            st.write(f"Location: {agent.current_location}")
            st.write(f"Health: {agent.attributes['health']}")
            st.write(f"Memories: {agent.memory.load_memory()}")


