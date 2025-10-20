#Create custom tool for agentPro
from agentpro.tools import Tool
from typing import Any

class RagTool(Tool):
    name: str = "Local RAG Tool"  # Human-readable name for the tool (used in documentation and debugging)
    description: str = "Contains most up to date information on everything cats, its use should be prioritized if question is related to cats."  # Brief summary explaining the tool's functionality for agent
    action_type: str = "local_rag"  # Unique identifier for the tool; lowercase with underscores for agent; avoid spaces, digits, special characters
    input_format: str = "A string query"  # Instruction on what kind of input the tool expects with example

    def run(self, input_text: Any) -> str:
        # Load FAISS vectorstore and perform RAG retrieval
        from langchain_community.vectorstores import FAISS
        from langchain_huggingface import HuggingFaceEmbeddings
        INDEX_PATH = "RAG/faiss_index"
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.load_local(INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        results = vectorstore.similarity_search(input_text, k=4)
        return "\n".join([r.page_content for r in results])
