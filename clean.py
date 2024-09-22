import polars as pl
from polars import DataFrame


def extract_gender(df: DataFrame) -> DataFrame:
    """
    Extracts gender from the subtitle column and adds a new column 'gender' to the dataframe.
    """

    subtitles = df["subtitle"].str.split(" ")
    new_subtitle = []
    genders = []
    for subtitle in subtitles:
        if len(subtitle) == 1:
            genders.append("Unisex")
        else:
            genders.append(subtitle[0])
        new_subtitle.append(subtitle[-1])
    df = df.drop("subtitle")
    df = df.with_columns(pl.Series(name="gender", values=genders))
    df = df.with_columns(pl.Series(name="subtitle", values=new_subtitle))
    return df
