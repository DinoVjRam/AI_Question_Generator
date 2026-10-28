from .chunker import DocumentChunker
from .embedding_service import EmbeddingService
from .vector_store import VectorStore
from .syllabus_parser import SyllabusParser


class IndexService:


    def __init__(self):

        self.chunker = DocumentChunker()

        self.embedder = EmbeddingService()

        self.store = VectorStore()



    def index_document(
        self,
        material_id,
        text
    ):


        # ==================================
        # Split syllabus into units first
        # ==================================

        syllabus_units = (
            SyllabusParser.split_into_units(text)
        )


        chunks = []


        # ==================================
        # Chunk each unit separately
        # ==================================

        for unit in syllabus_units["units"]:


            unit_chunks = self.chunker.split(
                unit["content"]
            )


            for chunk in unit_chunks:

                chunks.append(
                    {
                        "unit_no": unit["unit_no"],
                        "text": chunk
                    }
                )



        # ==================================
        # Create embeddings
        # ==================================

        for i, item in enumerate(chunks):

            vector = self.embedder.embed(
                item["text"]
            )


            self.store.add_chunk(

                chunk_id=f"{material_id}_{i}",

                text=item["text"],

                embedding=vector,

                metadata={

                    "material_id": material_id,

                    "unit_no": item["unit_no"]

                }

            )