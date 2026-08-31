from ingestion import SOURCE_FOLDER, read_file, normalize_schema


shipment_ids = ["SHP1032", "SHP1033", "SHP1037"]


def check_shipment_dates():
    """Find selected shipments and display their shipment and delivery dates."""

    results = []

    for file in SOURCE_FOLDER.iterdir():

        if not file.is_file():
            continue

        df = read_file(file)

        if df is None:
            continue

        df = normalize_schema(df)

        matches = df[df["shipment_id"].isin(shipment_ids)]

        if not matches.empty:

            results.append(
                {
                    "file": file.name,
                    "matches": matches[
                        [
                            "shipment_id",
                            "shipment_date",
                            "delivery_date",
                        ]
                    ],
                }
            )

    return results


if __name__ == "__main__":

    results = check_shipment_dates()

    for result in results:

        print(f"\nFile: {result['file']}")

        print(
            result["matches"].to_string(index=False)
        )