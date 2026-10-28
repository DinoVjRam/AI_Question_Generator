from .embedding_service import EmbeddingService
from .vector_store import VectorStore


class RetrievalService:


    def __init__(self):

        self.embedder = EmbeddingService()

        self.store = VectorStore()



    def build_query(
        self,
        units,
        difficulty,
        bloom,
    ):
        """
        Build semantic search query.
        """


        return f"""

Generate university examination questions.

Selected Units:

{", ".join(map(str, units))}


Difficulty:

{difficulty}


Bloom Level:

{bloom}

"""



    def retrieve(
        self,
        material_id,
        units,
        difficulty,
        bloom,
        top_k=5,
    ):


        # ===============================
        # Create semantic query
        # ===============================

        query = self.build_query(

            units,

            difficulty,

            bloom

        )

        # ===============================
        # Create embedding
        # ===============================

        query_vector = self.embedder.embed(
            query
        )



        # ===============================
        # Search ChromaDB
        # ===============================

        results = self.store.search(

            query_embedding=query_vector,

            material_id=material_id,

            units=units,

            top_k=top_k

        )



        documents = results.get(
            "documents",
            [[]]
        )



        if documents:

            context = "\n\n".join(
                documents[0]
            )

        else:

            context = ""
            
        return context