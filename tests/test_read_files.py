import pandas as pd

from read_files import read_shipments_file


def test_read_shipments_file(tmp_path):

    json_file = tmp_path / "shipments.json"

    data = [
        {
            "shipment_id": "SHP9999",
            "customer_id": "CUST999",
            "status": "Delivered",
        }
    ]

    pd.DataFrame(data).to_json(json_file, orient="records")

    result = read_shipments_file(json_file)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 1
    assert result.iloc[0]["shipment_id"] == "SHP9999"
    assert result.iloc[0]["status"] == "Delivered"