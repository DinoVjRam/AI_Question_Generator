import re


class SyllabusParser:
    """
    Parses the syllabus section from extracted text and splits it into units.

    Supports formats such as:

    UNIT I
    UNIT - I
    UNIT – II
    UNIT: III
    UNIT 1
    """

    # Match complete UNIT blocks
    UNIT_PATTERN = re.compile(
        r"(UNIT\s*[-–:]?\s*[IVX0-9]+\b.*?)(?=UNIT\s*[-–:]?\s*[IVX0-9]+\b|$)",
        re.IGNORECASE | re.DOTALL,
    )

    # Match UNIT heading
    TITLE_PATTERN = re.compile(
        r"UNIT\s*[-–:]?\s*([IVX0-9]+)\s*(.*)",
        re.IGNORECASE,
    )

    @staticmethod
    def split_into_units(text):
        """
        Returns:

        {
            "units":[
                {
                    "unit_no":1,
                    "roman":"I",
                    "title":"Introduction",
                    "content":"..."
                }
            ]
        }
        """

        if not text:
            return {"units": []}

        matches = SyllabusParser.UNIT_PATTERN.findall(text)

        units = []

        for index, block in enumerate(matches, start=1):

            block = block.strip()

            lines = [
                line.strip()
                for line in block.splitlines()
                if line.strip()
            ]

            if not lines:
                continue

            header = lines[0]

            match = SyllabusParser.TITLE_PATTERN.search(header)

            if match:

                roman = match.group(1).strip()

                title = (
                    match.group(2)
                    .strip(" :-–")
                    .strip()
                )

            else:

                roman = str(index)
                title = f"Unit {index}"

            units.append(
                {
                    "unit_no": index,
                    "roman": roman,
                    "title": title,
                    "content": block,
                }
            )

        return {"units": units}

    @staticmethod
    def get_syllabus_only(text):
        """
        Returns only the syllabus portion.

        Stops before detailed notes if they begin with:

        Unit 1
        1.1
        Chapter 1
        """

        if not text:
            return ""

        markers = [
            r"\n\s*Unit\s+1\s*$",
            r"\n\s*1\.1\s+",
            r"\n\s*Chapter\s+1",
        ]

        end = len(text)

        for marker in markers:

            m = re.search(marker, text, re.IGNORECASE | re.MULTILINE)

            if m:
                end = min(end, m.start())

        return text[:end].strip()
