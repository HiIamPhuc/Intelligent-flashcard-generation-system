import os
import uuid
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django.conf import settings
import openai
from .text_processor import TextProcessor
from .vector_store import VectorStore
# Remove the FlashcardEvaluator import
from .gemini_flashcard_evaluator import ImprovedGeminiFlashcardEvaluator


class RAGManager:
    def __init__(self):
        self.text_processor = TextProcessor()
        self.vector_store = VectorStore()
        # Remove the FlashcardEvaluator initialization
        # Initialize only the Gemini evaluator with your API key
        self.gemini_evaluator = ImprovedGeminiFlashcardEvaluator(api_key=settings.GEMINI_API_KEY)
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        
    def process_document(self, file, filename, user_id):
        """Process a document and create a vector store for it"""
        # Extract text from the document
        text = self.text_processor.extract_text_from_file(file, filename)
        
        # Chunk the text
        chunks = self.text_processor.chunk_text(text)

        # Create metadata for each chunk
        metadatas = [{
            "source": filename,
            "chunk_index": i,
            "user_id": user_id
        } for i in range(len(chunks))]
        
        # Create vector store
        self.vector_store.add_texts(chunks, metadatas)
        
        # Save vector store
        store_id = str(uuid.uuid4())
        store_path = os.path.join(settings.MEDIA_ROOT, 'vector_stores', f"{user_id}_{store_id}.pkl")
        self.vector_store.save(store_path)
        
        return {
            "store_id": store_id,
            "chunk_count": len(chunks),
            "store_path": store_path,
            "full_text": text  # Return the full text for evaluation
        }
    
    def process_raw_text(self, text, user_id):
        """
        Process raw text (not from a file), create chunks and build a vector store for it.
        """
        import uuid
        import os

        # Chunk the raw text
        chunks = self.text_processor.chunk_text(text)

        # Create metadata for each chunk
        metadatas = [{
            "source": "raw_text",
            "chunk_index": i,
            "user_id": user_id
        } for i in range(len(chunks))]

        # Add to vector store
        self.vector_store.add_texts(chunks, metadatas)

        # Save vector store
        store_id = str(uuid.uuid4())
        store_path = os.path.join(settings.MEDIA_ROOT, 'vector_stores', f"{user_id}_{store_id}.pkl")
        self.vector_store.save(store_path)

        return {
            "store_id": store_id,
            "chunk_count": len(chunks),
            "store_path": store_path
        }
        
    def load_vector_store(self, store_id, user_id):
        """Load a vector store for a specific user and document"""
        store_path = os.path.join(settings.MEDIA_ROOT, 'vector_stores', f"{user_id}_{store_id}.pkl")
        success = self.vector_store.load(store_path)
        return success
    
    
    
    def generate_flashcards(self, store_id, user_id, num_flashcards):
            """Generate flashcards from document using chunked RAG strategy"""
            import json

            if not self.load_vector_store(store_id, user_id):
                return {
                    "name": '',
                    "flashcards": [],
                    "entities": []
                }

            all_chunks = self.vector_store.texts
            seen_vocab = set()
            all_flashcards = []
            all_entities = set()
            # Xử lý từng nhóm 1-2 chunks để tránh token quá lớn
            for i in range(0, len(all_chunks), 2):
                
                chunk_group = all_chunks[i:i+2]


                chunk_text = "\n\n".join(chunk_group)

                prompt = f"""
                You are a language assistant that helps learners understand new vocabulary from documents.

                First, extract all named entities and key phrases from the text using NER and keyphrase extraction. Return them as a flat list of strings, no duplicates.

                Then, select 2–3 of the most important or educational terms and write short, relevant definitions based on their context.

                Return only a valid JSON in this format:
                {{
                    "name": "Chunk flashcard set",
                    "entities": ["Entity1", "Entity2", ...],
                    "flashcards": [
                        {{
                            "vocabulary": "Entity1",
                            "description": "Its meaning in context."
                        }}
                    ]
                }}
                """

                try:
                    response = self.openai_client.chat.completions.create(
                        model=settings.USED_GPT_MODEL,
                        messages=[
                            {"role": "system", "content": prompt},
                            {"role": "user", "content": chunk_text}
                        ],
                        temperature=0.3,
                    )

                    result = json.loads(response.choices[0].message.content)

                    # Gộp vào tập hợp
                    for entity in result.get("entities", []):
                        all_entities.add(entity)

                    for card in result.get("flashcards", []):
                        if card["vocabulary"] not in seen_vocab:
                            all_flashcards.append(card)
                            seen_vocab.add(card["vocabulary"])

                    if len(all_flashcards) >= num_flashcards:
                        break

                except Exception as e:
                    print(f"[Chunk {i}] Error generating flashcards: {e}")
                    continue

            final_result = {
                "name": "Document Flashcards",
                "entities": list(all_entities),
                "flashcards": all_flashcards[:num_flashcards]
            }

            
            self.evaluate_and_save_flashcards(final_result, "\n\n".join(all_chunks), user_id, store_id)

            return final_result

    
    def evaluate_and_save_flashcards(self, flashcards_data, original_text, user_id, store_id):
        """Evaluate generated flashcards using only Gemini evaluator"""
        try:
            # Create evaluation directories if they don't exist
            eval_dir = os.path.join(settings.MEDIA_ROOT, 'flashcard_evaluations')
            os.makedirs(eval_dir, exist_ok=True)
            
            # Only evaluate with Gemini
            try:
                gemini_evaluation_results = self.gemini_evaluator.evaluate_flashcards(
                    flashcards_data,
                    original_text
                )
                
                # Save Gemini evaluation results
                gemini_output_path = os.path.join(eval_dir, f"{user_id}_{store_id}_gemini_evaluation.png")
                self.gemini_evaluator.visualize_results(gemini_evaluation_results, gemini_output_path)
                
                # Save the results as JSON
                results_json_path = os.path.join(eval_dir, f"{user_id}_{store_id}_gemini_evaluation.json")
                with open(results_json_path, 'w', encoding='utf-8') as f:
                    json.dump(gemini_evaluation_results, f, indent=2)
                
                print(f"Gemini flashcard evaluation completed and saved")
                return True
                
            except Exception as gemini_error:
                print(f"[ERROR] Gemini evaluation failed: {gemini_error}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Flashcard evaluation failed: {e}")
            return False
            
    def answer_question(self, store_id, user_id, question):
        """Answer a question using RAG"""
        # Load the vector store
        if not self.load_vector_store(store_id, user_id):
            return "Sorry, I couldn't find the relevant knowledge base."
            
        # Retrieve relevant chunks
        relevant_chunks = self.vector_store.similarity_search(question, top_k=3)
        
        # Combine retrieved texts
        context = "\n\n---\n\n".join([chunk["text"] for chunk in relevant_chunks])
        
        # Generate answer
        response = self.openai_client.chat.completions.create(
            model=settings.USED_GPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context. If you don't know the answer based on the context, say so."},
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}"}
            ],
            temperature=0.3
        )
        
        return response.choices[0].message.content