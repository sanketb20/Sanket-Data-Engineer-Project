import pandas as pd


def read_shipments_file(file_path):
    """Read a shipment JSON file and return a DataFrame."""
    return pd.read_json(file_path)


if __name__ == "__main__":

    df = read_shipments_file("source/shipments_day3.json")

    print(df.head())

    print(df.shape)

    print(df.columns)