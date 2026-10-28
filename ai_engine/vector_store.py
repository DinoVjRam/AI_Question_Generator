import chromadb


class VectorStore:


    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="chroma_db"
        )


        self.collection = (
            self.client
            .get_or_create_collection(
                name="syllabus_chunks"
            )
        )



    def add_chunk(
        self,
        chunk_id,
        text,
        embedding,
        metadata=None,
    ):


        self.collection.add(

            ids=[
                str(chunk_id)
            ],

            documents=[
                text
            ],

            embeddings=[
                embedding
            ],

            metadatas=[
                metadata or {}
            ],

        )



    def search(
        self,
        query_embedding,
        material_id,
        units=None,
        top_k=5,
    ):


        # ===============================
        # Search only current syllabus
        # ===============================

        where_filter = {

            "material_id": material_id

        }



        # ===============================
        # Filter selected units
        # ===============================

        if units:


            where_filter = {

                "$and":[

                    {
                        "material_id": material_id
                    },

                    {
                        "unit_no":{
                            "$in": [
                                int(u)
                                for u in units
                            ]
                        }
                    }

                ]

            }



        results = self.collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k,

            where=where_filter

        )


        return results