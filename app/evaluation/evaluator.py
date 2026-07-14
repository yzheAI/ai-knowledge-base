import json


class RetrieverEvaluator:
    def __init__(self, dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

    def evaluate(self, retriever):
        hit = 0

        total = len(self.dataset)

        for item in self.dataset:
            results = retriever.search(
                item["question"],
                top_k=5
            )

            if any(
                item["source"] == r["doc_id"]
                for r in results
            ):
                hit += 1

        return {
            "hit": hit,
            "total": total,
            "recall@5": hit / total
        }


