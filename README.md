# 泛睿 Fintrieva

面向金融监管制度与统计报表的可信问答助手。

泛睿将制度查询、报表分析和来源定位放在同一工作流程中，帮助使用者从业务问题找到相关条款、数据与计算依据。

## 项目功能

- **监管制度查询**：围绕业务问题查找制度条款，查看相关内容及出处。
- **统计报表分析**：按机构、期间和指标查找数据，辅助完成比较与变化分析。
- **答案来源定位**：将回答与文件、条款或表格位置关联，方便回看原始依据。
- **资料协同使用**：结合制度说明与统计数据，支持业务查询和材料整理。

## 数据工具

本仓库提供报表预览、示例数据生成和指标摘要工具，使用 Python 标准库即可运行，无需安装第三方依赖。

| 工具 | 功能 |
| --- | --- |
| `scripts/preview_csv.py` | 查看 CSV 的字段、行数和前几条记录 |
| `scripts/generate_demo_data.py` | 生成两家示例银行的季度指标数据 |
| `scripts/summarize_report.py` | 按机构与指标输出期初、期末、变化值和区间统计 |

## 快速开始

使用 Python 3.10 或更新版本，在仓库根目录执行：

```bash
# 查看示例报表
python scripts/preview_csv.py

# 汇总贷款余额
python scripts/summarize_report.py

# 查看指定机构的不良贷款率
python scripts/summarize_report.py --institution "示例银行A" --metric "不良贷款率"

# 将摘要保存为 CSV
python scripts/summarize_report.py --output outputs/loan_summary.csv
```

也可以传入自己的 CSV 文件：

```bash
python scripts/preview_csv.py path/to/report.csv --limit 8
python scripts/summarize_report.py path/to/report.csv --metric "贷款余额"
```

所有命令均支持 `--help`。数据工具在本地读写文件。

## 数据格式

`examples/sample_report.csv` 包含以下字段：

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `institution` | 机构名称 | 示例银行A |
| `period` | 统计时点，使用 YYYY-MM-DD | 2025-03-31 |
| `metric` | 指标名称 | 贷款余额 |
| `value` | 指标值 | 120.00 |
| `unit` | 指标单位 | 亿元 |

示例数据由脚本生成，机构和数值均为虚构，用于演示工具的使用方式。可用以下命令重新生成：

```bash
python scripts/generate_demo_data.py --output outputs/sample_report.csv
```

摘要按机构、指标和单位分别计算，不合并不同单位。期初和期末按统计日期排序；余额的变化值沿用原单位，百分比指标的变化值以百分点表示。区间均值为各观测值的算术平均值。

## 目录

```text
fintrieva/
├── README.md
├── LICENSE
├── examples/
│   └── sample_report.csv
└── scripts/
    ├── generate_demo_data.py
    ├── preview_csv.py
    └── summarize_report.py
```

## 许可

本仓库代码采用 [MIT License](LICENSE)。
