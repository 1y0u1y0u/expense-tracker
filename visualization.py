import matplotlib.pyplot as plt
from collections import defaultdict
import input  # 匯入組員的模組 

# ==========================================
# Expense Tracker - Visualization Module
# ==========================================

def aggregate_expenses(expenses):
    """
    接收記憶體中的記帳資料列表，並加總各類別的金額。
    """
    category_totals = defaultdict(float)
    
    for exp in expenses:
        category = exp.get('category', 'Unknown').strip()
        try:
            amount = float(exp.get('amount', 0))
            category_totals[category] += amount
        except ValueError:
            continue
            
    return category_totals

def generate_pie_chart(category_totals):
    """
    根據分類與金額總計生成圓餅圖。
    """
    if not category_totals:
        print("目前沒有可用的記帳資料可以產生圖表。")
        return

    labels = list(category_totals.keys())
    sizes = list(category_totals.values())

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Expenses by Category')
    plt.axis('equal') 
    
    print("\n正在顯示圓餅圖...")
    plt.show()

def main():
    print("=" * 40)
    print("       EXPENSE TRACKER & VISUALIZATION")
    print("=" * 40)
    
    expenses_list = []
    
    # 建立一個迴圈，讓使用者可以連續輸入多筆資料
    while True:
        # 直接呼叫組員寫好的 collect_expense()
        expense = input.collect_expense()
        expenses_list.append(expense)
        
        # 呼叫組員的顯示功能確認輸入
        input.display_expense(expense)
        
        # 詢問是否繼續
        cont = input("\n是否繼續新增另一筆花費？(y/n): ").strip().lower()
        if cont != 'y':
            break

    # 資料收集完畢，將串列傳入彙整函數並畫圖
    totals = aggregate_expenses(expenses_list)
    if totals:
        generate_pie_chart(totals)

if __name__ == "__main__":
    main()