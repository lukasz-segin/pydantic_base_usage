"""
Basic example showing how to read and validate data from a file using Pydantic.
"""

import json
import pydantic
from typing import Optional


class Book(pydantic.BaseModel):

    title: str
    author: str
    publisher: str
    price: float
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    subtitle: Optional[str]


def main() -> None:
    """Main function"""

    with open("data.json", "r") as file:
        data = json.load(file)
        print(data)


if __name__ == '__main__':
    main()
