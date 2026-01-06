import tkinter as tk
from tkinter import messagebox
import random

# --- Functions ---

def update_dashboard():
    """Update all dashboard metrics and charts."""
    # Get user inputs (use defaults if empty)
    total_balance = float(balance_entry.get() or 5000)
    monthly_income = float(income_entry.get() or 3000)
    monthly_expenses = float(expense_entry.get() or 2000)
    savings_goal = float(savings_entry.get() or 1000)

    # Compute derived metrics
    savings = total_balance + monthly_income - monthly_expenses
    progress_percent = min(max((savings / savings_goal) * 100, 0), 100)

    # Update metric labels
    balance_value.config(text=f"${total_balance:,.2f}")
    income_value.config(text=f"${monthly_income:,.2f}")
    expense_value.config(text=f"${monthly_expenses:,.2f}")
    savings_value.config(text=f"${savings:,.2f}")
    goal_value.config(text=f"{progress_percent:.1f}%")

    # Draw charts
    draw_gauge(gauge_canvas, 125, 75, 60, progress_percent, "#4CAF50")
    draw_line_chart(line_canvas)
    draw_bar_chart(bar_canvas)


def draw_gauge(canvas, x, y, radius, percent, color):
    """Draw circular gauge showing savings progress."""
    canvas.delete("all")
    canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline="gray", width=3)
    extent = percent / 100 * 360
    canvas.create_arc(x-radius, y-radius, x+radius, y+radius, start=90, extent=-extent, fill=color)
    canvas.create_text(x, y, text=f"{percent:.0f}%", font=("Helvetica", 14, "bold"))
    canvas.create_text(x, y+50, text="Savings Goal Progress", font=("Helvetica", 10))


def draw_line_chart(canvas):
    """Draw line chart of monthly spending trends."""
    canvas.delete("all")
    points = [(10 + i*50, 120 - random.randint(20, 100)) for i in range(12)]  # 12 months
    for i in range(len(points)-1):
        canvas.create_line(points[i], points[i+1], fill="#2196F3", width=2)
    for x, y in points:
        canvas.create_oval(x-4, y-4, x+4, y+4, fill="#2196F3")
    canvas.create_text(300, 140, text="Monthly Spending Trend", font=("Helvetica", 10))


def draw_bar_chart(canvas):
    """Draw stacked bar chart for last 5 months category-wise expenses."""
    canvas.delete("all")
    categories = ["Rent", "Food", "Entertainment"]
    colors = ["#FF5722", "#FFC107", "#03A9F4"]
    
    x_start = 50
    for month in range(5):
        y_base = 150
        heights = [random.randint(20, 60) for _ in categories]
        for h, c in zip(heights, colors):
            canvas.create_rectangle(x_start, y_base-h, x_start+30, y_base, fill=c)
            y_base -= h
        x_start += 70

    # Draw legend
    legend_x = 400
    for i, cat in enumerate(categories):
        canvas.create_rectangle(legend_x, 10+i*20, legend_x+15, 25+i*20, fill=colors[i])
        canvas.create_text(legend_x + 70, 17+i*20, text=cat, anchor="w", font=("Helvetica", 9))
    
    canvas.create_text(250, 160, text="Category-wise Expenses (Last 5 Months)", font=("Helvetica", 10))


# --- Tkinter window setup ---
root = tk.Tk()
root.title("Personal Finance Dashboard")
root.geometry("900x650")
root.configure(bg="#F0F0F0")

# --- Input frame ---
input_frame = tk.Frame(root, bg="#F0F0F0")
input_frame.pack(pady=10)

tk.Label(input_frame, text="Total Balance:").grid(row=0, column=0, padx=5, pady=5)
balance_entry = tk.Entry(input_frame); balance_entry.grid(row=0,column=1, padx=5, pady=5)

tk.Label(input_frame, text="Monthly Income:").grid(row=0, column=2, padx=5, pady=5)
income_entry = tk.Entry(input_frame); income_entry.grid(row=0,column=3, padx=5, pady=5)

tk.Label(input_frame, text="Monthly Expenses:").grid(row=1, column=0, padx=5, pady=5)
expense_entry = tk.Entry(input_frame); expense_entry.grid(row=1,column=1, padx=5, pady=5)

tk.Label(input_frame, text="Savings Goal:").grid(row=1, column=2, padx=5, pady=5)
savings_entry = tk.Entry(input_frame); savings_entry.grid(row=1,column=3, padx=5, pady=5)

tk.Button(root, text="Update Dashboard", command=update_dashboard, bg="#4CAF50", fg="white", font=("Helvetica", 12)).pack(pady=10)

# --- Metric panels ---
panel_frame = tk.Frame(root, bg="#F0F0F0")
panel_frame.pack(pady=10)

def create_metric(parent, row, column, label_text, bg_color):
    """Create a labeled colored metric box."""
    value_label = tk.Label(parent, text="$0", bg=bg_color, width=15, height=3, font=("Helvetica", 12, "bold"))
    value_label.grid(row=row*2, column=column, padx=5)
    tk.Label(parent, text=label_text, bg="#F0F0F0", font=("Helvetica", 10, "bold")).grid(row=row*2+1, column=column)
    return value_label

balance_value = create_metric(panel_frame, 0, 0, "Total Balance", "#FFD54F")
income_value = create_metric(panel_frame, 0, 1, "Monthly Income", "#4FC3F7")
expense_value = create_metric(panel_frame, 0, 2, "Monthly Expenses", "#FF8A65")
savings_value = create_metric(panel_frame, 0, 3, "Savings", "#81C784")
goal_value = create_metric(panel_frame, 0, 4, "Goal Progress", "#DCE775")

# --- Canvases for charts ---
gauge_canvas = tk.Canvas(root, width=250, height=150, bg="#F0F0F0", highlightthickness=0)
gauge_canvas.pack(pady=10)

line_canvas = tk.Canvas(root, width=600, height=150, bg="white")
line_canvas.pack(pady=10)

bar_canvas = tk.Canvas(root, width=600, height=200, bg="white")
bar_canvas.pack(pady=10)

root.mainloop()



