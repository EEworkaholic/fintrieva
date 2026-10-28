"""Summarize time-series CSV records by institution, metric and unit."""

import argparse
import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FIELDS = {"institution", "period", "metric", "value", "unit"}
OUTPUT_FIELDS = (
    "institution", "metric", "unit", "observations", "start_period", "end_period",
    "start_value", "end_value", "change", "change_unit", "minimum", "maximum", "mean",
)


def summarize(path, metric, institution=None):
    groups = defaultdict(list)
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = REQUIRED_FIELDS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError("缺少字段：" + ", ".join(sorted(missing)))
        for row in reader:
            if row["metric"] != metric or (institution and row["institution"] != institution):
                continue
            key = (row["institution"], row["metric"], row["unit"])
            groups[key].append((date.fromisoformat(row["period"]), Decimal(row["value"])))
    results = []
    for (name, metric_name, unit), records in sorted(groups.items()):
        records.sort(key=lambda record: record[0])
        if len({period for period, _ in records}) != len(records):
            raise ValueError(f"{name} / {metric_name} 同一日期存在重复记录，请先明确统计口径。")
        values = [value for _, value in records]
        result = dict(zip(OUTPUT_FIELDS, (
            name, metric_name, unit, len(records), records[0][0].isoformat(),
            records[-1][0].isoformat(), str(values[0]), str(values[-1]),
            str(values[-1] - values[0]), "百分点" if unit == "%" else unit,
            str(min(values)), str(max(values)), str((sum(values) / len(values)).quantize(Decimal("0.0001"))),
        )))
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description="按机构和指标生成时序摘要。")
    parser.add_argument("file", nargs="?", type=Path, default=ROOT / "examples" / "sample_report.csv")
    parser.add_argument("--metric", default="贷款余额")
    parser.add_argument("--institution", help="仅输出指定机构；默认输出所有机构")
    parser.add_argument("--output", type=Path, help="可选的 CSV 输出路径")
    args = parser.parse_args()
    results = summarize(args.file, args.metric, args.institution)
    if not results:
        parser.error("没有找到匹配的机构和指标")
    for row in results:
        print(f"{row['institution']} | {row['metric']} | {row['start_period']} 至 {row['end_period']}")
        print(f"  期初 {row['start_value']} {row['unit']}；期末 {row['end_value']} {row['unit']}；变化 {row['change']} {row['change_unit']}")
        print(f"  最小 {row['minimum']}；最大 {row['maximum']}；均值 {row['mean']} {row['unit']}；观测数 {row['observations']}")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open("w", encoding="utf-8-sig", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            writer.writerows(results)
        print(f"已保存：{args.output}")


if __name__ == "__main__":
    main()
