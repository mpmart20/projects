"""Parallel prompt execution across all models."""
import concurrent.futures, json, time
from models.claude import ClaudeModel

class Executor:
    def __init__(self, models=None):
        self.models = models or [ClaudeModel()]

    def run_prompt(self, prompt: str) -> list[dict]:
        results = []
        def execute(model):
            try:
                resp = model.complete(prompt)
                return {"success": True, "response": resp.__dict__}
            except Exception as e:
                return {"success": False, "error": str(e), "model_name": str(model.model)}

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.models)) as executor:
            futures = {executor.submit(execute, m): m for m in self.models}
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
        return results

    def run_suite(self, prompts: list[str], output_file: str = "results/latest.json"):
        all_results = []
        for i, prompt in enumerate(prompts, 1):
            print(f"Running prompt {i}/{len(prompts)}: {prompt[:50]}...")
            results = self.run_prompt(prompt)
            all_results.append({"prompt": prompt, "results": results})
            time.sleep(0.5)  # Rate limiting

        import os
        os.makedirs("results", exist_ok=True)
        with open(output_file, "w") as f:
            json.dump(all_results, f, indent=2)
        print(f"✓ Results saved to {output_file}")
        return all_results
