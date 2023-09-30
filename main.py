import typer
import asyncio
import json
from files_utils import glob_files, load_code_from_file
from chains import review_file, review_directory


async def files_analysis(path: str, glob: str):
    files = glob_files(path, glob)
    reviews = await asyncio.gather(
        *[review_file(file, load_code_from_file(file)) for file in files]
    )
    reviews = [json.loads(_) for _ in reviews]
    print(reviews)


def main(mode: str, regexp: str, path: str):
    if mode == "files":
        asyncio.run(files_analysis(path, regexp))
    if mode == "folder":
        review_directory(path, regexp)


if __name__ == "__main__":
    typer.run(main)
