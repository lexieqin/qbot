import ollama
import chromadb
import json
import os
from typing import List, Optional
from pathlib import Path


class VectorStore:
    def __init__(self, documents_path: Optional[str] = None):
        self.client = chromadb.Client()
        self.documents_path = documents_path or self._get_default_documents_path()
        self.collection = self._initialize_collection()

    def _get_default_documents_path(self) -> str:
        """Get the default path for documents.json"""
        current_dir = Path(__file__).parent.parent
        return str(current_dir / 'documents' / 'documents.json')

    def _load_documents(self) -> List[str]:
        """Load documents from JSON file"""
        try:
            with open(self.documents_path, 'r') as f:
                data = json.load(f)
                return data.get('documents', [])
        except FileNotFoundError:
            raise Exception(f"Documents file not found at {self.documents_path}")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON format in documents file at {self.documents_path}")

    def _initialize_collection(self):
        """Initialize and populate the vector database"""
        try:
            # Load documents from file
            documents = self._load_documents()
            if not documents:
                raise Exception("No documents found in the documents file")

            # Delete existing collection if it exists
            try:
                self.client.delete_collection(name="docs")
            except:
                pass

            collection = self.client.create_collection(name="docs")

            print(f"Initializing vector database with {len(documents)} documents...")
            for i, doc in enumerate(documents):
                response = ollama.embeddings(model="mxbai-embed-large", prompt=doc)
                embedding = response["embedding"]
                collection.add(
                    ids=[str(i)],
                    embeddings=[embedding],
                    documents=[doc]
                )
                print(f"Processed document {i + 1}/{len(documents)}")

            print("Vector database initialization complete!")
            return collection

        except Exception as e:
            print(f"Error initializing vector database: {str(e)}")
            raise

    def add_document(self, document: str) -> bool:
        """Add a new document to both the JSON file and vector database"""
        try:
            # Add to JSON file
            documents = self._load_documents()
            documents.append(document)

            with open(self.documents_path, 'w') as f:
                json.dump({'documents': documents}, f, indent=4)

            # Add to vector database
            response = ollama.embeddings(model="mxbai-embed-large", prompt=document)
            embedding = response["embedding"]
            self.collection.add(
                ids=[str(len(documents) - 1)],
                embeddings=[embedding],
                documents=[document]
            )

            return True
        except Exception as e:
            print(f"Error adding document: {str(e)}")
            return False

    def generate_response(self, prompt: str) -> str:
        """Generate response for user input"""
        # Generate embedding for the prompt
        response = ollama.embeddings(
            prompt=prompt,
            model="mxbai-embed-large"
        )

        # Query vector database
        results = self.collection.query(
            query_embeddings=[response["embedding"]],
            n_results=1
        )
        data = results['documents'][0][0]

        # Generate response using retrieved data
        output = ollama.generate(
            model="llama3.2",
            prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
        )
        return output['response']

    def generate_structured_response(self, prompt: str) -> dict:
        """Generate structured JSON response for user input"""
        try:
            # Generate embedding for the prompt
            response = ollama.embeddings(
                prompt=prompt,
                model="mxbai-embed-large"
            )

            # Query vector database
            results = self.collection.query(
                query_embeddings=[response["embedding"]],
                n_results=1
            )
            data = results['documents'][0][0]

            # Create a formatted prompt for structured output
            formatted_prompt = f"""
            You must respond in valid JSON format following this exact structure:
            {{
                "answer": "<your detailed answer>",
                "source": "<the source document used>",
                "confidence": <float between 0 and 1>
            }}

            Using this context: {data}
            Respond to this prompt: {prompt}

            Remember to ONLY return valid JSON.
            """

            # Generate response using retrieved data
            output = ollama.generate(
                model="llama3.2",
                prompt=formatted_prompt
            )

            try:
                # Parse the response as JSON
                json_response = json.loads(output['response'])

                # Ensure all required fields are present
                return {
                    "answer": json_response.get("answer", ""),
                    "confidence": json_response.get("confidence", 0.0)
                }

            except json.JSONDecodeError:
                # Fallback if response isn't valid JSON
                return {
                    "answer": output['response'],
                    "confidence": 0.0
                }

        except Exception as e:
            return {
                "answer": f"Error generating response: {str(e)}",
                "confidence": 0.0
            }