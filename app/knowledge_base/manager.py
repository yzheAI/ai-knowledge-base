import os


class KnowledgeManager:
    def __init__(self, base_path):
        self.base_path = base_path

    def create(self, kb_name):
        kb_path = os.path.join(
            self.base_path,
            kb_name
        )

        os.makedirs(
            kb_path,
            exist_ok=True
        )

        return kb_path

    def get_path(self, kb_name):
        return os.path.join(
            self.base_path,
            kb_name
        )

    def list(self):
        if not os.path.exists(self.base_path):
            return []
        return os.listdir(self.base_path)
