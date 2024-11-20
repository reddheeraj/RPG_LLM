from agent import GenerativeAgent
import sched
import time
import random
import streamlit as st

class GameWorld:
    def __init__(self, locations):
        self.locations = locations
        self.agents = []  # List of agents
        self.events = []  # Tracks ongoing events
        self.resources = {"gold": 100, "food": 200}  # Village resources
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def schedule_event(self, delay, event_description):
        """
        Schedule a future event.
        """
        self.scheduler.enter(delay, 1, self.trigger_event, (event_description,))

    def run_scheduled_events(self):
        """
        Run the event loop.
        """
        self.scheduler.run(blocking=False)

    def add_agent(self, agent: GenerativeAgent):
        self.agents.append(agent)
        agent.current_location = random.choice(self.locations)  # Randomly assign an initial location

    def trigger_event(self, event):
        """
        Triggers an event and notifies all agents.
        """
        print(f"Event: {event}")
        self.events.append(event)
        for agent in self.agents:
            agent.observe_event(event)

    def random_interactions(self):
        """
        Simulates random interactions between agents.
        """
        import random
        if len(self.agents) > 1:
            agent1, agent2 = random.sample(self.agents, 2)
            agent1.interact(agent2)

    def dynamic_walk(self):
        """
        Simulates agents moving between locations.
        """
        import random
        for agent in self.agents:
            location = random.choice(self.locations)
            print(f"{agent.name} walks to the {location}.")
            st.write(f"{agent.name} walks to the {location}.")
            agent.observe_event(f"Arrived at the {location}.")
            if location == "Village":
                agent.gain_xp(10)
            elif location == "Forest":
                agent.gain_xp(20)
            elif location == "Castle":
                agent.gain_xp(30)
            elif location == "Dungeon":
                agent.gain_xp(40)

    def trade(self, agent1, agent2):
        """
        Simulates a trade between two agents.
        """
        import random
        trade_value = random.randint(1, 10)
        print(f"{agent1.name} trades {trade_value} gold with {agent2.name}.")
    
    def visualize_world(self):
        """
        Visualize the world and agents in Streamlit.
        """
        st.title("Game World Visualization")
        for agent in self.agents:
            agent.visualize()

    def move_agents(self):
        """
        Simulate the movement of agents and update visualization.
        """
        for agent in self.agents:
            direction = (random.choice([-1, 1]), random.choice([-1, 1]))  # Random move direction
            agent.move(direction)
