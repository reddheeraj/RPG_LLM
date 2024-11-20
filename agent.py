import random
import datetime
import json
from langchain.prompts import PromptTemplate
from Memory_System import MemorySystem
import streamlit as st

class GenerativeAgent:
    def __init__(self, name, llm, attributes, initial_info=None):
        self.name = name
        self.llm = llm
        self.attributes = attributes
        self.current_location = None
        self.memory = MemorySystem(self.llm)  # Memory system for storing information
        self.relationships = {}  # Tracks relationships with other agents
        self.knowledge = initial_info or {}  # Initial knowledge
        self.skills = {"combat": 1, "persuasion": 1, "exploration": 1}  # Skill levels
        self.xp = 0  # Experience points
        self.age = 0  # Agent age
        self.fame = 0  # Fame score
        self.fear = 0  # Fear score
        self.group = None  # Group affiliation
        self.logs = []  # Agent logs
        self.lifetime_log = []
        self.alive = True
        self.successor = None  # Successor agent
        self.position = (0, 0)  # Store agent's position for visualization

        

        # def get_session_history():
        #     # Convert memory history to LangChain-compatible format
        #     return messages_to_dict(self.memory.load_memory_variables({}).get("history", []))

        # # Initialize conversation chain with LLM and session history
        # self.conversation_chain = RunnableWithMessageHistory(
        #     runnable=self.llm,
        #     get_session_history=get_session_history,
        # )

        # Optional: Load initial memory info
        if initial_info:
            self.memory.add_memory(initial_info)

    def visualize(self):
        """
        Visualizes the agent's position and movement using Streamlit.
        """
        st.title(f"Agent: {self.name}")
        st.write(f"Position: {self.position}")
        st.write(f"Fame: {self.fame}, Fear: {self.fear}")
        
        # Optionally add a map or grid visualization
        st.write("### Agent Movement")
        st.map([{"lat": self.position[0], "lon": self.position[1]}])

        st.write(f"Relationships: {self.relationships}")

    def move(self, direction):
        """
        Move the agent to a new position.
        Direction is a tuple indicating x and y changes.
        """
        self.position = (self.position[0] + direction[0], self.position[1] + direction[1])
        self.visualize()
        print(f"{self.name} moves to {self.position}")
    
    def age_agent(self):
        """
        Increment the agent's age and possibly trigger lifecycle events (e.g., aging, death).
        """
        self.age += 1
        self.lifetime_log.append(f"{datetime.datetime.now()} - {self.name} has aged. New age: {self.age}")
        print(f"{self.name} is now {self.age} years old.")
        
        if self.age > 50:  # Example threshold for aging
            self.die()
        
        if self.age == 30 and self.successor is None:
            self.birth_successor()
    
    def die(self):
        """
        Mark the agent as dead and potentially create a successor.
        """
        self.alive = False
        self.lifetime_log.append(f"{datetime.now()} - {self.name} has died.")
        print(f"{self.name} has died.")
        if self.successor:
            print(f"{self.successor.name} will carry on {self.name}'s legacy.")
    
    def birth_successor(self):
        """
        Create a successor agent who takes over after the current agent's death.
        """
        # ask llm to give a name to the successor
        name = self.llm.generate_action("Give a name to the successor of " + self.name).get("message").get("content")
        successor_name = name
        successor_attributes = {"health": 100, "strength": 10, "speed": 10}  # Example attributes
        self.successor = GenerativeAgent(successor_name, self.llm, successor_attributes)
        print(f"{self.name} has birthed a successor: {self.successor.name}.")
        self.lifetime_log.append(f"{datetime.now()} - {self.name} birthed a successor: {self.successor.name}.")

    def gain_xp(self, amount):
        """
        Gain experience points and potentially level up.
        """
        self.xp += amount
        if self.xp >= 100:  # Level up threshold
            self.xp -= 100
            for skill in self.skills:
                self.skills[skill] += 1
            print(f"{self.name} leveled up! New skills: {self.skills}")

    def observe_event(self, event):
        """
        Observe and store an event in memory.
        """
        st.write(f"{self.name} observed: {event}")
        print(f"{self.name} observed: {event}")
        self.memory.save_context({"input": f"Observed: {event}"}, {"output": "Acknowledged."})
        self.log_action(f"Observed: {event}")
        
    
    def log_action(self, action):
        """
        Logs an action for later analysis.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append({"timestamp": timestamp, "action": action})

    def act(self, context):
        """
        Decide an action based on memory, context, personality, and current goal.
        """
        # Prepare the action prompt
        prompt = PromptTemplate(
            input_variables=["name", "context", "memory", "goal"],
            template=(
                "You are {name}. Based on your memory:\n{memory}\nand the current context: '{context}' "
                "what action will you take? Respond with a single action."
            )
        )

        # Include the goal in the prompt (fallback to "none" if no goal is set)
        action_prompt = prompt.format(
            name=self.name,
            context=context,
            memory=self.memory.load_memory(),
        )

        # Generate action using LLM
        response = self.llm.generate_action(action_prompt)
        self.log_action(f"Action taken: {response}")
        return response

    def interact(self, other_agent):
        """
        Interact with another agent and share information, influencing relationships.
        """
        dialogue = self.memory.interact_with_agent(other_agent.name)
        st.write(f"{self.name} says to {other_agent.name}: {dialogue}")
        print(f"{self.name} says to {other_agent.name}: {dialogue}")

        # Determine interaction type randomly
        interaction_outcome = random.choice(["positive", "neutral", "negative"])
        self.update_relationship(other_agent, interaction_outcome)

    def reflect(self):
        """
        Reflect on past memories and draw insights.
        """
        prompt = PromptTemplate(
            input_variables=["memory"],
            template="Based on your memory:\n{memory}\nWhat insights can you draw? Reflect in one sentence."
        )
        reflection_prompt = prompt.format(memory=self.memory.load_memory({}))
        reflection = self.llm.generate_action(reflection_prompt)
        print(f"{self.name} reflects: {reflection}")
    
    def update_relationship(self, other_agent, interaction_type):
        """
        Updates relationship scores with another agent based on interaction type.
        """
        score_change = {"positive": 10, "neutral": 2, "negative": -10}
        self.relationships[other_agent.name] = self.relationships.get(other_agent.name, 0) + score_change[interaction_type]
        print(f"{self.name} now has a relationship score of {self.relationships[other_agent.name]} with {other_agent.name}.")
        st.write(f"{self.name} now has a relationship score of {self.relationships[other_agent.name]} with {other_agent.name}.")
    
    def generate_successor(self):
        """
        Generate a new agent (successor) when conditions are met (e.g., age, specific goals).
        """
        if self.age > 50:  # Example: agents can create successors if they are older than 50
            successor_name = f"{self.name}_successor"
            successor = GenerativeAgent(successor_name, self.llm, self.attributes)
            self.log_action(f"Generated successor {successor_name}")
            return successor
        return None


