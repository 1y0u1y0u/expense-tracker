"""Expense Tracker - Member B: category-based pie chart visualization."""

import csv
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager


BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "expenses.csv"
OUTPUT_FILE = BASE_DIR / "images" / "sample_pie_chart.png"

COLORS = [
    "#3563E9",  # Blue
    "#14A8A0",  # Teal
    "#F07178",  # Coral
    "#E3A34B",  # Amber
    "#8B63D9",  # Purple
    "#43A87B",  # Green
    "#6D85A5",  # Slate
    "#C56F9A",  # Pink
]
BG_COLOR = "#F8FAFD"
TEXT_COLOR = "#182B49"


def configure_fonts():
    """Select a Chinese-capable font if installed on the computer."""
    preferred = [
        "Microsoft JhengHei", "Microsoft YaHei", "Noto Sans CJK TC",
        "Noto Sans CJK SC", "PingFang TC", "SimHei", "Arial Unicode MS",
    ]
    installed = {font.name for font in font_manager.fontManager.ttflist}
    for name in preferred:
        if name in installed:
            plt.rcParams["font.sans-serif"] = [name, "DejaVu Sans"]
            break
    plt.rcParams["axes.unicode_minus"] = False


def load_data_and_aggregate(filename=DATA_FILE):
    """Read CSV and sum positive, finite expense amounts by category."""
    totals = defaultdict(Decimal)
    valid_count = 0
    skipped_count = 0

    if not filename.exists():
        print("[!] No expenses.csv found. Run 'python input.py' first.")
        return {}, 0, 0

    with filename.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        columns = reader.fieldnames or []
        if "category" not in columns or "amount" not in columns:
            print("[!] CSV must contain the 'category' and 'amount' columns.")
            return {}, 0, 0

        for row in reader:
            try:
                category = (row.get("category") or "").strip()
                amount = Decimal((row.get("amount") or "").strip())
                if not category or not amount.is_finite() or amount <= 0:
                    skipped_count += 1
                    continue
            except (InvalidOperation, TypeError):
                skipped_count += 1
                continue
            totals[category] += amount
            valid_count += 1

    return dict(totals), valid_count, skipped_count


def generate_pie_chart(category_totals, record_count):
    """Create a polished donut-style pie chart and export it as PNG."""
    if not category_totals:
        print("[!] No valid expense records to visualize.")
        return False

    configure_fonts()
    ordered = sorted(category_totals.items(), key=lambda item: item[1], reverse=True)
    labels = [category for category, _ in ordered]
    amounts = [float(amount) for _, amount in ordered]
    total = sum(category_totals.values())

    # Prevent overflow when Decimal values cannot be represented as finite floats.
    if any(not (0 < amount < float("inf")) for amount in amounts):
        print("[!] Some amounts are too large to display in a pie chart.")
        return False

    fig, ax = plt.subplots(figsize=(11, 6.5), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    fig.subplots_adjust(left=0.06, right=0.65, top=0.79, bottom=0.10)

    exploded = [0.035 if idx == 0 and len(amounts) > 1 else 0 for idx in range(len(amounts))]
    wedges, _, pct_texts = ax.pie(
        amounts,
        labels=None,
        colors=[COLORS[idx % len(COLORS)] for idx in range(len(amounts))],
        startangle=90,
        counterclock=False,
        explode=exploded,
        autopct=lambda p: f"{p:.1f}%" if p >= 5 else "",
        pctdistance=0.79,
        wedgeprops={"width": 0.42, "edgecolor": BG_COLOR, "linewidth": 3},
    )

    for idx, text in enumerate(pct_texts):
        text.set_fontsize(9)
        text.set_fontweight("bold")
        text.set_color(TEXT_COLOR if idx % len(COLORS) == 3 else "white")

    ax.text(0, 0.13, "TOTAL SPENT", ha="center", va="center",
            fontsize=11, fontweight="bold", color="#68809D")
    ax.text(0, -0.11, f"{total:,.2f}", ha="center", va="center",
            fontsize=21, fontweight="bold", color=TEXT_COLOR)
    ax.set_aspect("equal")

    fig.text(0.065, 0.94, "EXPENSE TRACKER  /  VISUAL REPORT", fontsize=10,
             fontweight="bold", color="#3563E9")
    fig.text(0.065, 0.885, "Expenses by Category", fontsize=22,
             fontweight="bold", color=TEXT_COLOR)
    fig.text(0.065, 0.83, f"{record_count} expense records  •  Amount distribution",
             fontsize=11, color="#68809D")

    legend_labels = [
        f"{label}   {amount:,.2f}  ({Decimal(amount) / total * 100:.1f}%)"
        for label, amount in ordered
    ]
    ax.legend(
        wedges, legend_labels,
        title="CATEGORY BREAKDOWN",
        loc="center left", bbox_to_anchor=(1.12, 0.5),
        frameon=False, fontsize=10, title_fontsize=11,
        labelspacing=1.35, handlelength=1.1, handleheight=1.1,
    )
    fig.text(0.065, 0.038, "Generated automatically from expenses.csv",
             fontsize=9, color="#8190A4")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_FILE, dpi=180, bbox_inches="tight", facecolor=BG_COLOR)
    print(f"[OK] Pie chart saved: {OUTPUT_FILE}")
    print("[OK] Close the chart window to return to the terminal.")
    plt.show()
    plt.close(fig)
    return True


def main():
    print("=" * 56)
    print("  EXPENSE TRACKER / VISUAL REPORT")
    print("=" * 56)
    try:
        totals, record_count, skipped_count = load_data_and_aggregate()
    except OSError as error:
        print(f"[!] Unable to read CSV: {error}")
        return

    if not totals:
        print("[!] Please add some expenses first.")
        return

    print("\nCATEGORY SUMMARY")
    print("-" * 56)
    for category, amount in sorted(totals.items(), key=lambda item: -item[1]):
        print(f"  {category:<18} {amount:>12,.2f}")
    print("-" * 56)
    print(f"  TOTAL                {sum(totals.values()):>12,.2f}")
    print(f"  Valid records: {record_count}  |  Skipped: {skipped_count}")
    print("\nGenerating chart...")
    generate_pie_chart(totals, record_count)


if __name__ == "__main__":
    main()
