import ollama
import chromadb
import json
import os
import logging
from datetime import datetime
from typing import List, Optional, Dict
from pathlib import Path

logging.basicConfig(level=logging.INFO)


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
            documents = self._load_documents()
            if not documents:
                raise Exception("No documents found in the documents file")

            try:
                self.client.delete_collection(name="docs")
            except:
                pass

            collection = self.client.create_collection(name="docs")

            logging.info(f"Initializing vector database with {len(documents)} documents...")
            for i, doc in enumerate(documents):
                response = ollama.embeddings(model="mxbai-embed-large", prompt=doc)
                embedding = response["embedding"]
                collection.add(
                    ids=[str(i)],
                    embeddings=[embedding],
                    documents=[doc],
                    metadatas=[{'timestamp': datetime.now().isoformat(), 'source_index': i}]
                )
                logging.info(f"Processed document {i + 1}/{len(documents)}")

            logging.info("Vector database initialization complete!")
            return collection

        except Exception as e:
            logging.error(f"Error initializing vector database: {str(e)}")
            raise

    def retrieve_chunks(self, query_embedding: list, n_results: int = 3) -> dict:
        """Retrieve relevant chunks from the vector database"""
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

    def filter_relevant_chunks(self, chunks: dict, threshold: float = 0.7) -> list:
        """Filter chunks based on similarity score"""
        if not chunks['distances'][0]:  # Check if there are any results
            return []

        filtered_chunks = [
            doc for doc, dist in zip(chunks['documents'][0], chunks['distances'][0])
            if dist > threshold
        ]
        return filtered_chunks

    def format_prompt(self, query: str, context: str) -> str:
        """Format the prompt with context and instructions"""
        return f"""Based on the following context, answer the question concisely and specifically.
        Only include information that is directly supported by the context.

        Context: {context}
        Question: {query}

        Important guidelines:
        1. Use simple, clear language
        2. Reference specific details from the context
        3. If information is not in the context, say so
        4. Keep responses focused and relevant to the question"""

    def verify_response(self, response: str, context: str) -> str:
        """Verify if the response is supported by the context with improved logic"""
        try:
            # Break into sentences for more granular verification
            response_sentences = response.lower().split('.')
            context_lower = context.lower()

            verified_sentences = []
            for sentence in response_sentences:
                sentence = sentence.strip()
                if not sentence:  # Skip empty sentences
                    continue

                # Check if key words from the sentence appear in context
                words = set(sentence.split())
                # Remove common words that might inflate similarity
                common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
                key_words = words - common_words

                if len(key_words) == 0:
                    continue

                # Count how many key words appear in context
                matching_words = sum(1 for word in key_words if word in context_lower)
                similarity_ratio = matching_words / len(key_words)

                # More lenient threshold (0.2 instead of 0.3)
                if similarity_ratio > 0.2:
                    verified_sentences.append(sentence)

            if verified_sentences:
                return ' '.join(verified_sentences).capitalize() + '.'
            else:
                return ("Based on the available context, I cannot provide a fully verified response. "
                        "Please rephrase your question or provide more specific details.")

        except Exception as e:
            logging.error(f"Error in response verification: {str(e)}")
            return response  # Return original response if verification fails

    def add_document(self, document: str) -> bool:
        """Add a new document to both the JSON file and vector database"""
        try:
            documents = self._load_documents()
            documents.append(document)

            with open(self.documents_path, 'w') as f:
                json.dump({'documents': documents}, f, indent=4)

            response = ollama.embeddings(model="mxbai-embed-large", prompt=document)
            embedding = response["embedding"]
            self.collection.add(
                ids=[str(len(documents) - 1)],
                embeddings=[embedding],
                documents=[document],
                metadatas=[{'timestamp': datetime.now().isoformat(), 'source_index': len(documents) - 1}]
            )

            return True
        except Exception as e:
            logging.error(f"Error adding document: {str(e)}")
            return False

    def generate_response(self, prompt: str) -> str:
        """Generate response for user input with improved context handling"""
        try:
            # Generate embedding for the prompt
            response = ollama.embeddings(
                prompt=prompt,
                model="mxbai-embed-large"
            )

            # Retrieve and filter chunks
            results = self.retrieve_chunks(response["embedding"])
            filtered_chunks = self.filter_relevant_chunks(results)

            if not filtered_chunks:
                return "I couldn't find relevant information to answer your question."

            # Combine filtered chunks into context
            context = " ".join(filtered_chunks)

            # Format prompt with context
            formatted_prompt = self.format_prompt(prompt, context)

            # Generate response
            output = ollama.generate(
                model="llama3.2",
                prompt=formatted_prompt
            )

            # Verify response
            verified_response = self.verify_response(output['response'], context)

            return verified_response

        except Exception as e:
            logging.error(f"Error generating response: {str(e)}")
            return "I encountered an error while processing your request."

    def generate_structured_response(self, prompt: str) -> dict:
        """Generate structured JSON response for user input with improved context handling"""
        try:
            # Generate embedding for the prompt
            response = ollama.embeddings(
                prompt=prompt,
                model="mxbai-embed-large"
            )

            # Retrieve and filter chunks
            results = self.retrieve_chunks(response["embedding"], n_results=3)
            filtered_chunks = self.filter_relevant_chunks(results)

            if not filtered_chunks:
                return {
                    "answer": "I couldn't find relevant information to answer your question.",
                    "source": "none",
                    "confidence": 0.0
                }

            # Combine filtered chunks into context
            context = " ".join(filtered_chunks)

            # Create an enhanced formatted prompt for structured output
            formatted_prompt = f"""
            Based ONLY on the provided context, generate a response in valid JSON format following this exact structure:
            {{
                "answer": "<your detailed answer, stating 'Information not found in context' if you can't answer>",
                "source": "<relevant parts of the context used>",
                "confidence": <float between 0 and 1, based on how well the context matches the question>
            }}

            Context: {context}
            Question: {prompt}

            Guidelines:
            1. Only use information from the provided context
            2. Set confidence to 0.0 if answer cannot be found in context
            3. Include specific quotes or references from the context
            4. Return ONLY valid JSON, no additional text

            Remember to ONLY return valid JSON.
            """

            # Generate response using retrieved data
            output = ollama.generate(
                model="llama3.2",
                prompt=formatted_prompt
            )

            try:
                # Parse and verify the response
                json_response = json.loads(output['response'])

                # Verify response against context
                verified_response = self.verify_response(json_response["answer"], context)

                if verified_response != json_response["answer"]:
                    return {
                        "answer": verified_response,
                        "source": json_response.get("source", "Unable to verify source"),
                        "confidence": 0.3  # Lower confidence for unverified responses
                    }

                # Ensure all required fields are present with improved validation
                return {
                    "answer": json_response.get("answer", ""),
                    "source": json_response.get("source", ""),
                    "confidence": min(max(float(json_response.get("confidence", 0.0)), 0.0), 1.0),
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "num_chunks_retrieved": len(filtered_chunks),
                        "context_length": len(context)
                    }
                }

            except json.JSONDecodeError:
                logging.error("Failed to parse JSON response from LLM")
                # Enhanced fallback response
                return {
                    "answer": "I encountered an error processing the response. Here's the raw output: " +
                              output['response'][:200] + "...",  # Truncate long responses
                    "source": "error_handler",
                    "confidence": 0.0,
                    "metadata": {
                        "error_type": "json_decode_error",
                        "timestamp": datetime.now().isoformat()
                    }
                }

        except Exception as e:
            logging.error(f"Error in generate_structured_response: {str(e)}")
            return {
                "answer": "I encountered an error while processing your request. Please try again.",
                "source": "error_handler",
                "confidence": 0.0,
                "metadata": {
                    "error_type": str(type(e).__name__),
                    "error_message": str(e),
                    "timestamp": datetime.now().isoformat()
                }
            }