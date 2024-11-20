import json

class AgentLogger:
    def __init__(self, filename="agent_logs.json"):
        self.filename = filename
        self.logs = []

    def log_action(self, agent_name, action, context):
        """
        Log an action taken by an agent.
        """
        self.logs.append({
            "agent": agent_name,
            "action": action,
            "context": context,
            "time": len(self.logs)
        })

    def save_logs(self):
        """
        Save logs to a file.
        """
        with open(self.filename, "w") as f:
            json.dump(self.logs, f)