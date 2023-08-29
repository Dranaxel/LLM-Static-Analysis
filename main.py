import typer
import asyncio
from openai_cr import review_directory, display_reviews


def main(regexp: str, path: str):
    reviews = asyncio.run(review_directory(path, regexp))
    display_reviews(reviews, sort_by="codeQuality")


if __name__ == "__main__":
    typer.run(main)
