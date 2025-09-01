from etl.extract import extract_data

def test_extract_data():
    df = extract_data()
    assert (len(df)> 0)

def test_expected_columns():
    df = extract_data()
    expected_columns = {"pl_name", "pl_rade", "pl_bmasse", "disc_year"}
    assert expected_columns.issubset(df.columns)