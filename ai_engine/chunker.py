class DocumentChunker:
    """
    Splits syllabus content into RAG-friendly chunks.
    Keeps chunks readable for AI question generation.
    """


    @staticmethod
    def split(
        text,
        chunk_size=1000,
        overlap=200
    ):

        chunks = []


        # Clean text

        text = (
            text
            .replace("\r\n", "\n")
            .strip()
        )


        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]


        current_chunk = ""


        for paragraph in paragraphs:


            # Add paragraph

            if len(current_chunk) + len(paragraph) <= chunk_size:

                current_chunk += (
                    paragraph
                    + "\n\n"
                )


            else:

                if current_chunk:

                    chunks.append(
                        current_chunk.strip()
                    )


                # overlap support

                overlap_text = (
                    current_chunk[-overlap:]
                    if current_chunk
                    else ""
                )


                current_chunk = (
                    overlap_text
                    + "\n\n"
                    + paragraph
                    + "\n\n"
                )



        if current_chunk:

            chunks.append(
                current_chunk.strip()
            )


        return chunks