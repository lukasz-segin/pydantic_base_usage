"""
Basic example showing how to read and validate data from a file using Pydantic.
"""

import json
import pydantic
from typing import Optional, List


class ISBNMissingError(Exception):
    """Custom error that is raised when both ISBN10 and ISBN13 are missing."""

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(message)


class ISBN10FormatError(Exception):
    """Custom error that is raised when ISBN10 doesn't have the right format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)


class Book(pydantic.BaseModel):

    title: str
    author: str
    publisher: str
    price: float
    isbn_10: Optional[str]
    isbn_13: Optional[str]
    subtitle: Optional[str]

    @pydantic.root_validator(pre=True)
    @classmethod
    def check_isbn10_or_isbn13(cls, values):
        """Make sure there is either an isbn10 or isbn13 value defined."""

        if "isbn_10" not in values and "isbn_13" not in values:
            raise ISBNMissingError(
                title=values["title"],
                message="Document should have either an ISBN10 or ISBN13"
            )
        return values

    @pydantic.validator('isbn_10')
    @classmethod
    def isbn_10_valid(cls, value) -> None:
        """Validator to check whether ISBN10 is valid."""
        chars = [c for c in value if c in "0123456789Xx"]
        if len(chars) != 10:
            raise ISBN10FormatError(value=value, message="ISBN10 should be 10 digits.")

        def char_to_int(char: str) -> int:
            if char in "Xx":
                return 10
            return int(char)

        weighted_sum = sum((10 - i) * char_to_int(x) for i, x in enumerate(chars))
        if weighted_sum % 11 != 0:
            raise ISBN10FormatError(value=value, message="ISBN10 digit sum should be divisible by 11.")

    class Config:
        """Pydantic config class"""

        allow_mutation = True
        anystr_lower = False


def main() -> None:
    """Main function"""

    with open("data.json", "r") as file:
        data = json.load(file)
        books: List[Book] = [Book(**item) for item in data]
        print(data)
        print()
        print(books)
        print()
        print(books[0].title)
        print()
        print(books[0].dict())
        print()
        print(books[0].dict(exclude={"title"}))
        print()
        print(books[0].dict(include={"title"}))
        print()
        print(books[0].copy())
        print()
        print(books[0].copy(deep=True))
        print()


if __name__ == '__main__':
    main()
