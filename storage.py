import csv
import os


CSV_FILE = "ehr_data.csv"

FIELDNAMES = [
    "patient_id",
    "encrypted_data",
    "data_hash",
    "block_hash",
    "previous_hash",
    "timestamp"
]


def initialize_storage():
    """Create the CSV file if it does not exist."""

    if not os.path.exists(CSV_FILE):

        with open(
            CSV_FILE,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=FIELDNAMES
            )

            writer.writeheader()


def get_all_records():
    """Read all patient records from CSV."""

    initialize_storage()

    with open(
        CSV_FILE,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def patient_id_exists(patient_id):
    """Check whether a patient ID already exists."""

    records = get_all_records()

    return any(
        record["patient_id"] == patient_id
        for record in records
    )


def save_record(
    patient_id,
    encrypted_data,
    data_hash,
    block_hash,
    previous_hash,
    timestamp
):
    """Save an encrypted patient record."""

    initialize_storage()

    with open(
        CSV_FILE,
        "a",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        writer.writerow({
            "patient_id": patient_id,
            "encrypted_data": encrypted_data,
            "data_hash": data_hash,
            "block_hash": block_hash,
            "previous_hash": previous_hash,
            "timestamp": timestamp
        })


def find_record(patient_id):
    """Find a patient record using Patient ID."""

    records = get_all_records()

    for record in records:

        if record["patient_id"] == patient_id:
            return record

    return None