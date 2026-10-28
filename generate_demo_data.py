"""Generate a small fictional quarterly report using only the standard library."""

import argparse
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PERIODS = ("2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31")
SERIES = (
    ("示例银行A", "贷款余额", "亿元", ("120.00", "126.00", "133.50", "141.60")),
    ("示例银行A", "不良贷款率", "%", ("1.20", "1.18", "1.15", "1.10")),
    ("示例银行B", "贷款余额", "亿元", ("80.00", "82.40", "84.00", "88.00")),
    ("示例银行B", "不良贷款率", "%", ("1.50", "1.48", "1.45", "1.42")),
)


def main():
    parser = argparse.ArgumentParser(description="生成虚构季度指标报表。")
    parser.add_argument("--output", type=Path, default=ROOT / "outputs" / "sample_report.csv")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("institution", "period", "metric", "value", "unit"))
        for institution, metric, unit, values in SERIES:
            for period, value in zip(PERIODS, values):
                writer.writerow((institution, period, metric, value, unit))
    print(f"已生成 {len(SERIES) * len(PERIODS)} 条虚构记录：{args.output}")


if __name__ == "__main__":
    main()
