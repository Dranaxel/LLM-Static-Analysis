import typer
import asyncio
import json
from chain import review_directory
from files_utils import glob_files, load_code_from_file
from chains import review_file, review_directory
from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table


async def files_analysis(path: str, glob: str):
    files = glob_files(path, glob)
    reviews = await asyncio.gather(
        *[review_file(file, load_code_from_file(file)) for file in files]
    )
    reviews = [json.loads(_) for _ in reviews]
    table = Table(title="files analysis", show_lines=True)

    table.add_column("Filename")
    table.add_column("Code Quality")
    table.add_column("Goods points")
    table.add_column("Bad points")

    for review in reviews:
        color = (
            "green"
            if review["codeQuality"] > 9
            else "bright_green"
            if review["codeQuality"] > 7
            else "yellow"
            if review["codeQuality"] > 5
            else "orange"
            if review["codeQuality"] > 3
            else "red"
        )
        table.add_row(
            str(review["filename"]),
            str(review["codeQuality"]),
            str("\n".join(review["goodPoints"])),
            str("\n".join(review["badPoints"])),
            style=color,
        )

    console = Console()
    console.print(table)

    return reviews


def main(mode: str, regexp: str, path: str):
    if mode == "files":
        asyncio.run(files_analysis(path, regexp))
    if mode == "folder":
        review_directory(path, regexp)


if __name__ == "__main__":
    typer.run(main)
