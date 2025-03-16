import polars as pl


def format_tournament_metadata_frame(df: pl.DataFrame) -> pl.DataFrame:

    df = df.with_columns(
        pl.col("champion_earnings").str.replace("", "0").cast(float),
        pl.col("purse").str.replace("", "0").cast(float),
        pl.col("tour_standing_value")
        .str.split(" pts")
        .list.get(0)
        .str.replace(",", "")
        .cast(float),
    )

    return df


def format_tournament_results_frame(df: pl.DataFrame) -> pl.DataFrame:

    df = df.with_columns(
        pl.col("round_1").replace("-", None).replace("None", None).cast(float),
        pl.col("round_2").replace("-", None).replace("None", None).cast(float),
        pl.col("round_3").replace("-", None).replace("None", None).cast(float),
        pl.col("round_4").replace("-", None).replace("None", None).cast(float),
        pl.col("round_1_rel")
        .replace("-", None)
        .replace("None", None)
        .replace("E", "0")
        .cast(float),
        pl.col("round_2_rel")
        .replace("-", None)
        .replace("None", None)
        .replace("E", "0")
        .cast(float),
        pl.col("round_3_rel")
        .replace("-", None)
        .replace("None", None)
        .replace("E", "0")
        .cast(float),
        pl.col("round_4_rel")
        .replace("-", None)
        .replace("None", None)
        .replace("E", "0")
        .cast(float),
        pl.col("total")
        .replace("-", None)
        .replace("None", None)
        .replace("E", "0")
        .cast(float),
        pl.col("total_relative")
        .replace("-", None)
        .replace("None", None)
        .replace("E", "0")
        .cast(float),
        pl.col("tournament_year").str.split("-").list.get(0).alias("year").cast(float),
        pl.col("final_position").alias("str_final_position"),
        pl.col("final_position").str.extract_all("\d+").explode().cast(float),
    )

    return df
