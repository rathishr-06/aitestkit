from aitestkit import Evaluator

evaluator = Evaluator()

results = evaluator.run(
    prompt="What is RAG in AI?",
    response="RAG stands for Retrieval Augmented Generation. It combines document search with LLM generation.",
    reference="Retrieval Augmented Generation combines retrieval mechanisms with generative LLM models.",
    contexts=["Retrieval Augmented Generation combines search engines with generative AI models."],
    export_json_path="reports/demo_result.json"
)

print("\n--- Unified Evaluation Output ---")
print(results)