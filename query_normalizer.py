import re


class QueryNormalizer:
    """
    Cleans and standardizes user queries before retrieval.
    """

    def normalize(
        self,
        query: str,
    ) -> str:

        if not query:
            return ""

        query = query.strip()

        query = re.sub(
            r"\s+",
            " ",
            query,
        )

        query = re.sub(
            r"([!?.,])\1+",
            r"\1",
            query,
        )

        return query

    def process(
        self,
        query: str,
    ) -> str:

        normalized = self.normalize(
            query
        )

        if len(normalized) < 2:
            raise ValueError(
                "Please provide a valid query."
            )

        return normalized