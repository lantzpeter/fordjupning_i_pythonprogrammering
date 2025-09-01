import pandas as pd
from etl.transform import transform

def test_convert_columns_to_numeric():
    # Creating some values to test on
    df = pd.DataFrame ({
        'pl_name': ['Kepler-22b', 'Kepler-452b'],
        'pl_rade': ['2.4', '1,6'],
        'pl_bmasse': ['5.0', None],
        'disc_year': [2011, 2015]
    })

    result = transform(df)

    assert result['pl_rade'].dtype == 'float64'
    assert result['pl_bmasse'].dtype == 'float64'
    assert result['pl_bmasse'].isna().sum() == 1
    assert result["pl_name"].equals(df["pl_name"])