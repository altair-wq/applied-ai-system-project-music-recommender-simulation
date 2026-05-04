import os
import re
from typing import List

class RagAssistant:
    def __init__(self, kb_path: str):
        self.kb_path = kb_path
        self.chunks = self._load_knowledge_base()

    def _load_knowledge_base(self) -> List[str]:
        if not os.path.exists(self.kb_path):
            return []
        with open(self.kb_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by numbered list or newlines
        chunks = []
        for line in content.split('\n'):
            line = line.strip()
            if line and not line.lower().startswith('music recommender knowledge base'):
                # Remove leading numbers like "1. "
                line = re.sub(r'^\d+\.\s*', '', line)
                chunks.append(line)
        return chunks

    def retrieve(self, query: str, top_k: int = 2) -> List[str]:
        if not self.chunks:
            return []
        
        query_words = set(re.findall(r'\w+', query.lower()))
        
        scored_chunks = []
        for chunk in self.chunks:
            chunk_words = set(re.findall(r'\w+', chunk.lower()))
            # Simple keyword overlap
            overlap = len(query_words.intersection(chunk_words))
            scored_chunks.append((chunk, overlap))
        
        # Sort by overlap score descending
        scored_chunks.sort(key=lambda x: x[1], reverse=True)
        
        # Return top_k chunks
        return [chunk for chunk, score in scored_chunks[:top_k] if score > 0]

    def generate_response(self, query: str, recommendations: List[tuple], context: List[str], confidence: float) -> str:
        """
        Template-based assistant response generation.
        """
        response = []
        response.append(f"Music Assistant Response for: '{query}'")
        response.append(f"Confidence: {confidence:.2f}\n")
        
        if context:
            response.append("Knowledge Base Context:")
            for c in context:
                response.append(f"- {c}")
            response.append("")
            
        if recommendations:
            response.append("Here are your top song recommendations:")
            for i, (song, score, explanation) in enumerate(recommendations, 1):
                response.append(f"{i}. {song['title']} by {song['artist']} (Score: {score:.2f})")
                response.append(f"   Reason: {explanation}")
        else:
            response.append("I couldn't find any good recommendations for your request.")
            
        return "\n".join(response)
