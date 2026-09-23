"""Knowledge loading utilities.

The loader converts existing conjecture sources into a stable internal format.
No source is treated as truth without provenance metadata.
"""

from pathlib import Path
import json


class KnowledgeBase:
    def __init__(self, root: str):
        self.root = Path(root)
        self.items = []

    def load_json(self, path: str):
        file = self.root / path
        if not file.exists():
            return []
        data = json.loads(file.read_text(encoding="utf-8"))
        self.items.extend(data if isinstance(data, list) else [data])
        return self.items

    def add_source(self, name: str, status: str, source: str):
        self.items.append({
            "name": name,
            "status": status,
            "source": source,
        })

    def export(self, path: str):
        Path(path).write_text(
            json.dumps(self.items, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )
