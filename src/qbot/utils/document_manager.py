import json
from pathlib import Path
from typing import List, Optional


class DocumentManager:
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path or self._get_default_path()

    def _get_default_path(self) -> str:
        """Get the default path for documents.json"""
        current_dir = Path(__file__).parent.parent
        return str(current_dir / 'documents' / 'documents.json')

    def add_documents(self, documents: List[str]) -> bool:
        """Add multiple documents to the JSON file"""
        try:
            existing_docs = self.get_documents()
            existing_docs.extend(documents)

            with open(self.file_path, 'w') as f:
                json.dump({'documents': existing_docs}, f, indent=4)
            return True
        except Exception as e:
            print(f"Error adding documents: {str(e)}")
            return False

    def get_documents(self) -> List[str]:
        """Get all documents from the JSON file"""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return data.get('documents', [])
        except FileNotFoundError:
            return []

    def clear_documents(self) -> bool:
        """Clear all documents from the JSON file"""
        try:
            with open(self.file_path, 'w') as f:
                json.dump({'documents': []}, f, indent=4)
            return True
        except Exception as e:
            print(f"Error clearing documents: {str(e)}")
            return False