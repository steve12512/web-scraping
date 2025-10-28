import polars as pl
from polars import col


listings = [
    "Kraken Technologies",
    "Software Engineer",
    "2  yrs",
    "London, EN, United Kingdom | an hour ago",
    "4,3\xa0χιλ. | N/A | N/A",
]
listings = [listings]
df = pl.DataFrame(
    listings,
    [
        "company_name",
        "title",
        "years_of_experience",
        "city_and_country",
        "total_compensation",
    ],
)

df = df.with_columns(
    [
        col("city_and_country").str.split(",").list.get(0).alias("City"),
        col("city_and_country").str.split(",").list.slice(1, 2).list.eval(pl.element().str.split('|'))
        .alias("Country"),
        col("total_compensation")
            .cast(pl.Utf8)  
            .str.extract(r"(\d+,\d+)") 
            .alias("salary")
    ]
)

print(df.row(0))