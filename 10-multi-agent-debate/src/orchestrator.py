"""Orchestrates the full debate between agents."""
import json, time
from agents.base import BaseAgent
from agents.moderator import ModeratorAgent

DEFAULT_AGENTS = [
    ("Pragmatist", "practical, cost-benefit focused"),
    ("Idealist",   "principled, ethics-focused"),
    ("Skeptic",    "critical, evidence-demanding"),
]

class DebateOrchestrator:
    def __init__(self, agents=None, rounds: int = 3):
        self.agents = [BaseAgent(name, perspective) for name, perspective in (agents or DEFAULT_AGENTS)]
        self.moderator = ModeratorAgent()
        self.rounds = rounds

    def run_debate(self, topic: str) -> dict:
        print(f"\n🎙️ Debate: {topic}")
        print("=" * 60)
        all_messages = []

        for round_num in range(1, self.rounds + 1):
            print(f"\n--- Round {round_num} ---")
            for agent in self.agents:
                msg = agent.respond(topic, all_messages, round_num)
                all_messages.append(msg)
                print(f"{msg.agent_name}: {msg.content[:100]}...")
                time.sleep(0.5)

        synthesis = self.moderator.synthesize(topic, all_messages)
        print(f"\n📊 Synthesis:\n{synthesis}")

        return {
            "topic": topic,
            "rounds": self.rounds,
            "messages": [{"agent": m.agent_name, "role": m.role, "content": m.content, "round": m.round} for m in all_messages],
            "synthesis": synthesis
        }

if __name__ == "__main__":
    orchestrator = DebateOrchestrator(rounds=2)
    result = orchestrator.run_debate("Should AI development be slowed down for safety?")
    with open("debates/latest.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n✓ Debate saved to debates/latest.json")
