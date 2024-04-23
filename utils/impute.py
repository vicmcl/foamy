import pandas as pd


def remove_nan_columns(df: pd.DataFrame) -> pd.DataFrame:

    cols_to_drop = [
        col for col in df.columns if sum(pd.isnull(df[col])) == df.shape[0]
    ]
    df = df.drop(cols_to_drop, axis=1)
    return df


def impute_data(
    df: pd.DataFrame | None, strategy: str = 'ffill'
) -> pd.DataFrame | None:
    
    if df is None:
        return None
    if strategy == 'ffill':
        return remove_nan_columns(df).ffill()
    else:
        return remove_nan_columns(df).bfill()