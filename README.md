
# Expense Tracker

A simple expense-tracking application developed in Python for the Introduction to Software Engineering course.

This project allows users to record daily expenses, store expense data in CSV format, and visualize spending distributions through category-based pie charts.

## Features

### 1. Expense Input (Member A)

- Add multiple expense records.
- Enter expense date, amount, and category.
- Add optional notes.
- Validate date format and expense amount.
- Prevent empty categories.
- Automatically save records to a CSV file.
- Preserve previously recorded expenses.

### 2. Expense Visualization (Member B)

- Load expense records from CSV.
- Group expenses by category.
- Calculate total spending for each category.
- Generate a category-based pie chart.

## Project Structure

```text
expense-tracker/
│
├── input.py          # Expense input and CSV storage
├── visualize.py      # Expense visualization (Member B)
├── expenses.csv      # Generated expense data
├── README.md         # Project documentation
└── .gitignore        # Git ignore configuration
```

Note: expenses.csv is generated automatically when the input module is executed. It is excluded from Git tracking.

## Requirements

- Python 3.7 or later
- Matplotlib (for pie chart visualization)

The input module uses only Python standard libraries.

Install the visualization dependency:

```bash
python -m pip install matplotlib
```

## Installation

Clone the repository:

```bash
git clone https://github.com/1y0u1y0u/expense-tracker.git
```

Navigate to the project directory:

```bash
cd expense-tracker
```

## How to Run

### 1. Run the Input Module

Execute:

```bash
python input.py
```

Enter the following information:

- Date (YYYY-MM-DD)
- Amount
- Category
- Notes (optional)

The program validates the input and saves expense records to `expenses.csv`.

Users can continue adding expenses by entering `y` or finish by entering `n`.

### 2. Run the Visualization Module

After adding expense records, execute:

```bash
python visualize.py
```

The visualization module reads `expenses.csv` and generates a pie chart showing the distribution of total expenses by category.

Note: The visualization module is developed by Member B.

## CSV Data Format

All expense records are stored using the following columns:

| Column | Description |
|---|---|
| date | Expense date (YYYY-MM-DD) |
| amount | Expense amount |
| category | Expense category |
| notes | Optional description |

Example:

```csv
date,amount,category,notes
2026-11-17,120,Food,Lunch
2026-11-17,35,Transport,Bus
2026-11-18,500,Education,Books
```

## Sample Pie Chart

The following section will contain a screenshot of the generated category-based pie chart.

<!-- Add the screenshot at images/sample_pie_chart.png after integrating the visualization module. -->

## Team Collaboration

This project is developed collaboratively using Git and GitHub.

- Member A: Expense input module and CSV data storage.
- Member B: Expense visualization and pie chart generation.

Both members work on separate feature branches, which are integrated through Git merging.

## Course Information

Course: Introduction to Software Engineering

Assignment 1: Version Control Practice
