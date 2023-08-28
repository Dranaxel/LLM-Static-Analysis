import openai
import os
import re
import json
from rich.table import Table
from rich.console import Console


def review_code(code, filename):
    prompt = f"""
     Please review the following code according to the criteria outlined below. Your review should be returned as an array of JSON objects. Each JSON object should contain the following keys:

    1. "filename": The name of the file that the code is from.
    2. "codeQuality": A score out of ten that represents the overall quality of the code. Please consider factors such as readability, efficiency, and adherence to best practices when determining this score.
    3. "goodPoints": An array of points that highlight the strengths of the code. This could include things like effective use of data structures, good commenting, efficient algorithms, etc.
    4. "badPoints": An array of points that highlight areas where the code could be improved. This could include things like unnecessary repetition, lack of comments, inefficient algorithms, etc.

    Please ensure that your review is thorough and constructive. Remember, the goal is to help the coder improve, not to criticize them unnecessarily.

    code: {code}

    Example of expected output:
        {{
            "filename": "test1.js",
            "codeQuality": 7,
            "goodPoints": ["Effective use of data structures", "Good commenting"],
            "badPoints": ["Unnecessary repetition"]
        }},
        {{
            "filename": "test2.js",
            "codeQuality": 5,
            "goodPoints": ["Efficient algorithms"],
            "badPoints": ["Lack of comments", "Inefficient data structures"]
        }}

    output only the json
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    content = response.choices[0].message.content
    review = json.loads(content)
    review = review[0]
    review["filename"] = filename
    return review


def load_code_from_file(filename):
    with open(filename, "r") as file:
        return file.read()


def review_directory(directory, extension=None):
    reviews = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if extension is None or file.endswith(extension):
                filename = os.path.join(root, file)
                code = load_code_from_file(filename)
                review = review_code(code, filename)
                reviews.append(review)
    print(reviews)
    return reviews


def display_reviews(reviews, sort_by="filename"):
    reviews.sort(key=lambda review: review[sort_by])
    table = Table(show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("Filename")
    table.add_column("Code Quality")
    table.add_column("Good Points", justify="full")
    table.add_column("Bad Points", justify="full")

    for review in reviews:
        color = (
            "green"
            if review["codeQuality"] > 7
            else "yellow"
            if review["codeQuality"] > 4
            else "red"
        )
        table.add_row(
            review["filename"],
            str(review["codeQuality"]),
            str("\n".join(review["goodPoints"])),
            str("\n".join(review["badPoints"])),
            style=color,
        )

    console = Console()
    console.print(table)
