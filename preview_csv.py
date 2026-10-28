"""Preview CSV fields and records without third-party dependencies."""

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description="查看 CSV 字段、总行数和前几条记录。")
    parser.add_argument("file", nargs="?", type=Path, default=ROOT / "examples" / "sample_report.csv")
    parser.add_argument("--limit", type=int, default=5, help="显示的记录数，默认 5")
    args = parser.parse_args()
    if args.limit < 0:
        parser.error("--limit 不能为负数")
    with args.file.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        print("字段：" + " | ".join(reader.fieldnames or []))
        count = 0
        for count, row in enumerate(reader, start=1):
            if count <= args.limit:
                print(" | ".join(str(value) for value in row.values()))
        print(f"数据行数：{count}")


if __name__ == "__main__":
    main()
