"""Prompt Optimization Tool CLI"""
import click, json, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@click.group()
def cli():
    """Prompt Optimization Tool - Find the best prompt automatically."""
    pass

@cli.command()
@click.option("--prompt", "-p", required=True, help="Base prompt to optimize")
@click.option("--goal", "-g", required=True, help="What the optimized prompt should achieve")
@click.option("--variants", "-n", default=10, help="Number of variants to test (default: 10)")
@click.option("--output", "-o", default="results/latest.json", help="Output file")
def optimize(prompt, goal, variants, output):
    """Generate and test prompt variations, returning the best performer."""
    click.echo(f"🔍 Optimizing prompt with {variants} variants...")
    from generator import PromptGenerator
    from evaluator import PromptEvaluator
    from cache import Cache

    cache = Cache()
    generator = PromptGenerator()
    evaluator = PromptEvaluator()

    variations = generator.generate(prompt, goal, count=variants)
    click.echo(f"✓ Generated {len(variations)} variations")

    results = []
    with click.progressbar(variations, label="Testing variants") as bar:
        for variant in bar:
            cached = cache.get(variant)
            if cached:
                results.append(cached)
                continue
            score = evaluator.score(variant, goal)
            result = {"prompt": variant, "score": score}
            cache.set(variant, result)
            results.append(result)

    results.sort(key=lambda x: x["score"]["overall"], reverse=True)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w") as f:
        json.dump(results, f, indent=2)

    click.echo(f"\n🏆 Best prompt (score: {results[0]['score']['overall']:.2f}):")
    click.echo(f"   {results[0]['prompt'][:100]}...")
    click.echo(f"\n📄 Full results saved to {output}")

@cli.command()
@click.argument("results_file")
def report(results_file):
    """Display a formatted report from a results file."""
    with open(results_file) as f:
        results = json.load(f)
    click.echo("\n📊 Prompt Optimization Report")
    click.echo("=" * 50)
    for i, r in enumerate(results[:5], 1):
        click.echo(f"\n#{i} Score: {r['score']['overall']:.2f}")
        click.echo(f"   {r['prompt'][:80]}...")

if __name__ == "__main__":
    cli()
