from pathlib import Path

from cleaning import load_all_files, clean_data


REJECTED_FOLDER = Path("rejected")


MANDATORY_COLUMNS = [
    "shipment_id",
    "customer_id",
    "shipment_date",
    "origin",
    "destination",
    "status",
    "weight_kg",
    "shipping_cost",
]


def validate_data(df):
    """Separate valid and invalid shipment records."""

    rejection_reasons = []

    for _, row in df.iterrows():

        reasons = []

        # Check mandatory fields
        for column in MANDATORY_COLUMNS:
            if row[column] is None or row[column] != row[column]:
                reasons.append(f"Missing {column}")

        # Check weight
        if row["weight_kg"] is not None and row["weight_kg"] == row["weight_kg"]:
            if row["weight_kg"] <= 0:
                reasons.append("Invalid weight_kg")

        # Check shipping cost
        if row["shipping_cost"] is not None and row["shipping_cost"] == row["shipping_cost"]:
            if row["shipping_cost"] < 0:
                reasons.append("Invalid shipping_cost")

        rejection_reasons.append("; ".join(reasons))


    df = df.copy()

    df["rejection_reason"] = rejection_reasons

    invalid_df = df[df["rejection_reason"] != ""].copy()

    valid_df = df[df["rejection_reason"] == ""].copy()

    return valid_df, invalid_df


if __name__ == "__main__":

    # Extract + schema normalization + combine
    df = load_all_files()

    # Clean
    df = clean_data(df)

    print("Total records after cleaning:")
    print(len(df))

    # Validate
    valid_df, invalid_df = validate_data(df)

    print("\nValid records:")
    print(len(valid_df))

    print("\nInvalid records:")
    print(len(invalid_df))

    # Create rejected folder if it doesn't exist
    REJECTED_FOLDER.mkdir(exist_ok=True)

    # Save rejected records
    rejected_file = REJECTED_FOLDER / "rejected_shipments.csv"

    invalid_df.to_csv(rejected_file, index=False)

    print("\nRejected records saved to:")
    print(rejected_file)

    print("\nRejection details:")
    print(
        invalid_df[
            ["shipment_id", "rejection_reason"]
        ].to_string(index=False)
    )