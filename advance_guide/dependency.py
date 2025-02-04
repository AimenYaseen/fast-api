"""
Advanced Dependencies
Previously, We used class and functional dependencies
Here we will use the class function as a dependency
"""

from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


class FixedContentQueryChecker:
    def __init__(self, fixed_content: str):
        self.fixed_content = fixed_content

    def __call__(self, q: str = ""):
        if q:
            return self.fixed_content in q
        return False


checker = FixedContentQueryChecker("bar")


@app.get("/query-checker/")
async def read_query_checker(fixed_content_included: Annotated[bool, Depends(checker)]):
    return {
        "fixed_content_in_query": fixed_content_included,
    }
