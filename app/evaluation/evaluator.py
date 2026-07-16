import json


class RetrieverEvaluator:
    def __init__(self, dataset_path):
        with open(dataset_path, "r", encoding="utf-8") as f:
            self.dataset = json.load(f)

    def evaluate(self, retriever):
        recall_1 = 0
        recall_3 = 0
        recall_5 = 0

        total = len(self.dataset)

        for item in self.dataset:
            results = retriever.search(
                item["question"],
                top_k=5
            )

            if any(
                item["source"] == r["metadata"]["source"]
                for r in results[:1]
            ):
                recall_1 += 1

            if any(
                item["source"] == r["metadata"]["source"]
                for r in results[:3]
            ):
                recall_3 += 1

            if any(
                item["source"] == r["metadata"]["source"]
                for r in results[:5]
            ):
                recall_5 += 1

        return {
            "total": total,
            "recall_1": recall_1 / total,
            "recall_3": recall_3 / total,
            "recall_5": recall_5 / total
        }


