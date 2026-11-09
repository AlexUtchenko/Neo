"""
Частина 2, крок 1: landing -> bronze.

  * завантажує CSV з FTP-сервера;
  * читає CSV через Spark і зберігає у parquet: bronze/<table>.
"""
import argparse
from pathlib import Path

import requests
from pyspark.sql import SparkSession

FTP_URL = "https://ftp.goit.study/neoversity/"
TABLES = ["athlete_bio", "athlete_event_results"]
DEFAULT_LAKE = Path(__file__).resolve().parent / "data"


def download_data(table: str, landing_dir: Path) -> Path:
    """Функція з шаблону, з явним шляхом збереження і таймаутом."""
    downloading_url = FTP_URL + table + ".csv"
    local_file = landing_dir / f"{table}.csv"
    print(f"Downloading from {downloading_url}")
    response = requests.get(downloading_url, timeout=120)

    if response.status_code == 200:
        local_file.write_bytes(response.content)
        print(f"File downloaded successfully and saved as {local_file} "
              f"({len(response.content):,} bytes)")
    else:
        raise SystemExit(
            f"Failed to download the file. Status code: {response.status_code}"
        )
    return local_file


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--lake-root", default=str(DEFAULT_LAKE))
    p.add_argument("--tables", nargs="+", default=TABLES)
    p.add_argument("--skip-download", action="store_true",
                   help="використати вже наявні файли в landing/")
    args = p.parse_args()

    lake = Path(args.lake_root)
    landing_dir = lake / "landing"
    landing_dir.mkdir(parents=True, exist_ok=True)

    spark = SparkSession.builder.appName("LandingToBronze").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    for table in args.tables:
        # 1. завантаження з FTP в оригінальному форматі CSV
        csv_path = landing_dir / f"{table}.csv"
        if not args.skip_download:
            csv_path = download_data(table, landing_dir)

        # 2. читання CSV через Spark (multiLine/escape — у полях description трапляються коми, лапки і переноси рядків)
        df = (
            spark.read.option("header", True)
            .option("inferSchema", False)  # типізація — на рівні silver/gold
            .option("multiLine", True)
            .option("quote", '"')
            .option("escape", '"')
            .csv(str(csv_path))
        )

        # 3. запис у bronze/<table> у форматі parquet
        out = lake / "bronze" / table
        df.write.mode("overwrite").parquet(str(out))
        print(f"[bronze/{table}] rows={df.count()} columns={df.columns}")
        spark.read.parquet(str(out)).show(10, truncate=40)

    spark.stop()


if __name__ == "__main__":
    main()
