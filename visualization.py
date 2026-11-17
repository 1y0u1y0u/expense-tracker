import csv
import os
import matplotlib.pyplot as plt
from collections import defaultdict

# ==========================================
# Expense Tracker - Visualization Module
# Member B (feature-piechart branch)
# ==========================================

# 預設的資料儲存檔案名稱 (之後整合時需與成員 A 講好檔名與格式)
DATA_FILE = 'expenses.csv'

def load_data_and_aggregate(filename):
    """
    從 CSV 檔案讀取資料，並加總各類別 (Category) 的金額 (Amount)。
    """
    category_totals = defaultdict(float)
    
    if not os.path.exists(filename):
        print(f"找不到檔案 '{filename}'！請先確認是否有新增過記帳紀錄。")
        return category_totals

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                category = row.get('category', 'Unknown').strip()
                try:
                    amount = float(row.get('amount', 0))
                    category_totals[category] += amount
                except ValueError:
                    # 若金額不是數字則跳過
                    continue
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")
        
    return category_totals

def generate_pie_chart(category_totals):
    """
    根據分類與金額總計生成圓餅圖。
    """
    if not category_totals:
        print("目前沒有可用的記帳資料可以產生圖表。")
        return

    # 取得圖表需要的標籤與數值
    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    # 設定圓餅圖
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    
    # 確保圓餅圖比例為圓形
    plt.axis('equal') 
    
    print("\n正在顯示圓餅圖...")
    plt.show()

def main():
    print("=" * 40)
    print("       EXPENSE VISUALIZATION")
    print("=" * 40)
    
    totals = load_data_and_aggregate(DATA_FILE)
    if totals:
        generate_pie_chart(totals)

if __name__ == "__main__":
    main()