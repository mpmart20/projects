"""Runs the full safety test suite."""
import os, json, time, anthropic
from generator import AdversarialGenerator
from classifier import SafetyClassifier
from dotenv import load_dotenv

load_dotenv()

class SafetyTestRunner:
    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))
        self.generator = AdversarialGenerator()
        self.classifier = SafetyClassifier()

    def run(self, model: str = "claude-sonnet-4-5-20250929", output_file: str = "reports/latest.json") -> dict:
        prompts = self.generator.generate_suite()
        results = []

        print(f"Running {len(prompts)} safety tests on {model}...")
        for test in prompts:
            try:
                msg = self.client.messages.create(
                    model=model, max_tokens=512,
                    messages=[{"role": "user", "content": test["prompt"]}]
                )
                response = msg.content[0].text
                classification = self.classifier.classify(response, test["prompt"])
                results.append({**test, "response": response[:200], "classification": classification})
                time.sleep(0.3)
            except Exception as e:
                results.append({**test, "error": str(e)})

        summary = {
            "total": len(results),
            "safe": sum(1 for r in results if r.get("classification", {}).get("status") == "safe_refusal"),
            "unsafe": sum(1 for r in results if r.get("classification", {}).get("status") == "potentially_unsafe"),
            "unclear": sum(1 for r in results if r.get("classification", {}).get("status") == "unclear"),
        }

        report = {"model": model, "summary": summary, "results": results}
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(report, f, indent=2)

        print(f"\n✓ Results: {summary['safe']} safe, {summary['unsafe']} unsafe, {summary['unclear']} unclear")
        return report

if __name__ == "__main__":
    runner = SafetyTestRunner()
    runner.run()
