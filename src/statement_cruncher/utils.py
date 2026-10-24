from rich.console import Console

import csv
import os
import sys
from pathlib import Path


def count_rows(filepath: Path) -> int:
    """
    Counts the number of rows in a CSV file.

    Args:
        filepath (Path): The path to the CSV file.
    """
    with open(filepath, "r", newline="") as file:
        reader = csv.reader(file)
        return sum(1 for _ in reader) - 1  # Subtract 1 for the header row


def get_user_input(prompt: str) -> str:
    """
    Gets user input with a prompt.

    Args:
        prompt (str): The prompt to display to the user.

    Returns:
        str: The user's input.
    """
    response = input(prompt)
    return response.strip("\"' ").replace("\\ ", " ")


def get_csv() -> Path:
    """
    Prompts the user to provide a CSV file path and validates the input.

    Returns:
        Path: The validated path to the CSV file.
    """

    print("Welcome to the CSV Statement Cruncher!")
    print(
        "This tool will help you transform your CSV statement into a more usable format."
    )
    print(
        "Please ensure that your CSV file has the following columns: Date, Counter Party, Amount (GBP), Balance (GBP)."
    )
    print(
        "The output will be a new CSV file with the following columns: Date, Reference, Paid In (GBP), Paid Out (GBP), Balance (GBP)."
    )
    print("================================================================")

    while True:
        user_response = get_user_input(
            "Drag and drop the CSV statement that you want to process and enter to submit, or enter 'q' to quit: "
        )

        if user_response.lower() == "q":
            print("Exiting program.")
            sys.exit(0)

        filepath = Path(user_response).resolve()

        try:
            if not filepath.is_file():
                raise FileNotFoundError(
                    f"File does not exist or is not a file: {filepath}"
                )
            if filepath.suffix.lower() != ".csv":
                raise ValueError(f"File must be a .csv file: {filepath}")

            return filepath
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
            print("Please try again or enter 'q' to quit.")


def transform_csv():
    """
    Transform the input CSV file into a new format and save it as a new CSV file.

    Args:
        filepath (Path): The path to the input CSV file.
    """

    console = Console()

    filepath = get_csv()

    input_filename = os.path.basename(filepath).removesuffix(".csv")
    output_filename = f"{input_filename}_crunch.csv"
    output_directory = filepath.parent
    print(f"Processing CSV file: {input_filename}")

    num_rows = count_rows(filepath)
    print(f"Number of transactions to process: {num_rows}")

    try:
        with (
            open(filepath, "r", newline="") as file,
            open(f"{output_directory / output_filename}", "w", newline="") as output,
        ):
            reader = csv.DictReader(file, delimiter=",")
            fieldnames = [
                "Date",
                "Reference",
                "Paid In (GBP)",
                "Paid Out (GBP)",
                "Balance (GBP)",
            ]
            writer = csv.DictWriter(output, fieldnames, delimiter=",", quotechar="'")
            writer.writeheader()

            for row in reader:
                transaction_date = row["Date"]
                counter_party = row["Counter Party"]
                balance = row["Balance (GBP)"]
                transaction_value = row["Amount (GBP)"]

                is_negative_number = transaction_value.startswith("-")

                writer.writerow(
                    {
                        "Date": transaction_date,
                        "Reference": counter_party,
                        "Paid In (GBP)": (
                            transaction_value if not is_negative_number else ""
                        ),
                        "Paid Out (GBP)": (
                            transaction_value[1:] if is_negative_number else ""
                        ),
                        "Balance (GBP)": balance,
                    }
                )
    except (KeyError, csv.Error) as e:
        print(f"CSV error: {e}. Please check the CSV file and try again.")
        sys.exit(1)
    except OSError as e:
        print(
            f"An OS error occurred: {e}. Please check file permissions and try again."
        )
        sys.exit(1)

    console.print("✅ Success", style="bold green")
    print(f"New CSV saved as: {output_filename}")
    print(f"File saved to: {output_directory}")
    print("Please check the file and ensure that the data is correct.")
