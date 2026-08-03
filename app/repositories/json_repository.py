from typing import Any

from app.utils.file_handler import read_json, write_json


class JsonRepository:
    def __init__(self, file_path: str, model_class=None):
        self.file_path = file_path
        self.model_class = model_class
        self.data = self._load()

    def _load(self):
        return read_json(self.file_path, [])

    def _save(self):
        write_json(self.file_path, self.data)

    def list_all(self):
        return [self.model_class.from_dict(item) for item in self.data] if self.model_class else list(self.data)

    def add(self, item: Any):
        payload = item.to_dict() if hasattr(item, "to_dict") else item
        self.data.append(payload)
        self._save()
        return payload

    def get_by_id(self, item_id: int):
        for item in self.data:
            if item.get("id") == item_id:
                return self.model_class.from_dict(item) if self.model_class else item
        return None

    def update(self, item_id: int, updated: Any):
        for index, item in enumerate(self.data):
            if item.get("id") == item_id:
                self.data[index] = updated.to_dict() if hasattr(updated, "to_dict") else updated
                self._save()
                return self.data[index]
        return None

    def delete(self, item_id: int):
        before_count = len(self.data)
        self.data = [item for item in self.data if item.get("id") != item_id]
        if len(self.data) != before_count:
            self._save()
            return True
        return False
