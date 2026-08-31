import pandas as pd

import check_dates


def test_check_shipment_dates_finds_matching_shipments(tmp_path, monkeypatch):
    csv_file = tmp_path / "shipments.csv"

    df = pd.DataFrame({
        "shipment_id": ["SHP1032", "SHP9999"],
        "shipment_date": ["2026-08-29", "2026-08-30"],
        "delivery_date": ["2026-09-01", "2026-09-02"],
    })

    df.to_csv(csv_file, index=False)

    monkeypatch.setattr(check_dates, "SOURCE_FOLDER", tmp_path)

    results = check_dates.check_shipment_dates()

    assert len(results) == 1
    assert results[0]["file"] == "shipments.csv"

    matches = results[0]["matches"]

    assert len(matches) == 1
    assert matches.iloc[0]["shipment_id"] == "SHP1032"


def test_check_shipment_dates_skips_directory_and_unsupported_file(
    tmp_path,
    monkeypatch
):
    csv_file = tmp_path / "shipments.csv"

    df = pd.DataFrame({
        "shipment_id": ["SHP9999"],
        "shipment_date": ["2026-08-30"],
        "delivery_date": ["2026-09-02"],
    })

    df.to_csv(csv_file, index=False)

    # Directory → tests "if not file.is_file(): continue"
    (tmp_path / "some_folder").mkdir()

    # Unsupported file → read_file() returns None
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("unsupported file")

    monkeypatch.setattr(check_dates, "SOURCE_FOLDER", tmp_path)

    results = check_dates.check_shipment_dates()

    assert results == []


def test_check_shipment_dates_skips_file_without_matching_shipment(
    tmp_path,
    monkeypatch
):
    csv_file = tmp_path / "other_shipments.csv"

    df = pd.DataFrame({
        "shipment_id": ["SHP9999"],
        "shipment_date": ["2026-08-30"],
        "delivery_date": ["2026-09-02"],
    })

    df.to_csv(csv_file, index=False)

    monkeypatch.setattr(check_dates, "SOURCE_FOLDER", tmp_path)

    results = check_dates.check_shipment_dates()

    assert results == []