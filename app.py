import sympy as sp
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Entry, Button, Frame, PanedWindow, messagebox
from tkinter import font as tkFont
import re
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy.utilities.lambdify import lambdify
import numpy as np

# Ensure that the symbol 'Q' is defined in the local dictionary for sympy
Q = sp.Symbol('Q')


# Function to preprocess user input by adding multiplication signs where necessary
def preprocess_input(expr):
    print(f"Preprocessing input: {expr}")
    # Ensure multiplication is explicit
    expr = re.sub(r'(\d)([A-Za-z])', r'\1*\2', expr)  # e.g., 2Q -> 2*Q
    expr = re.sub(r'([A-Za-z])(\d)', r'\1*\2', expr)  # e.g., Q2 -> Q*2
    expr = re.sub(r'([A-Za-z\d]+)\s*\/\s*([A-Za-z\d]+)', r'(\1) / (\2)', expr)  # Handle divisions with parentheses
    print(f"Processed input: {expr}")
    return expr


# Function to validate user input
def validate_input(expression, allow_constant=False):
    """ Ensures the input is a valid mathematical expression containing 'Q'. """
    print(f"Validating input: {expression}")

    if not allow_constant and 'Q' not in expression:
        print("Validation failed: Q is missing in a required expression")
        return False

    try:
        sp.sympify(expression, locals={'Q': Q})  # Use Q from the local dictionary
    except sp.SympifyError:
        print("Validation failed: Invalid sympy expression")
        return False

    print("Validation passed")
    return True


# Function to calculate the profit-maximizing statistics and surpluses
def calculate_profit_maximization(inverse_demand_str, cost_function_str):
    """ Calculates the profit-maximizing price, quantity, producer and consumer surplus. """
    print("Parsing inputs for calculation...")
    P = sp.sympify(inverse_demand_str, locals={'Q': Q})
    C = sp.sympify(cost_function_str, locals={'Q': Q})

    # Total Revenue, Profit, Marginal Revenue, and Marginal Cost
    TR = P * Q
    profit = TR - C
    MR = sp.diff(TR, Q)
    MC = sp.diff(C, Q)

    # Solve for Q* where MR = MC (profit-maximizing quantity)
    profit_maximizing_quantity = sp.solve(sp.Eq(MR, MC), Q)[0]
    profit_maximizing_price = P.subs(Q, profit_maximizing_quantity)

    total_profit = profit.subs(Q, profit_maximizing_quantity)
    total_revenue = TR.subs(Q, profit_maximizing_quantity)
    total_cost = C.subs(Q, profit_maximizing_quantity)
    marginal_revenue = MR.subs(Q, profit_maximizing_quantity)
    marginal_cost = MC.subs(Q, profit_maximizing_quantity)

    # Compute Consumer Surplus (CS) and Producer Surplus (PS)
    consumer_surplus = sp.integrate(P, (Q, 0, profit_maximizing_quantity)) - (
                profit_maximizing_price * profit_maximizing_quantity)
    producer_surplus = (profit_maximizing_price * profit_maximizing_quantity) - sp.integrate(MC, (
    Q, 0, profit_maximizing_quantity))

    print("Calculation successful")
    return (profit_maximizing_quantity, profit_maximizing_price, total_profit, total_revenue, total_cost,
            marginal_revenue, marginal_cost, consumer_surplus, producer_surplus)


# Function to set up plots for the graphs
def setup_plot(ax, x_values, y_values, title, xlabel, ylabel):
    """ Sets up a matplotlib plot for a given set of data. """
    ax.plot(x_values, y_values)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)


# Function to update UI with calculated statistics
def update_labels(stats):
    """ Updates the displayed labels with the calculated statistics. """
    (profit_maximizing_quantity, profit_maximizing_price, total_profit, total_revenue, total_cost,
     marginal_revenue, marginal_cost, consumer_surplus, producer_surplus) = stats

    price_label.config(text=f"Profit Maximizing Price: {profit_maximizing_price:.2f}")
    quantity_label.config(text=f"Profit Maximizing Quantity: {profit_maximizing_quantity:.2f}")
    mc_label.config(text=f"Marginal Cost: {marginal_cost:.2f}")
    mr_label.config(text=f"Marginal Revenue: {marginal_revenue:.2f}")
    total_cost_label.config(text=f"Total Cost: {total_cost:.2f}")
    total_revenue_label.config(text=f"Total Revenue: {total_revenue:.2f}")
    total_profit_label.config(text=f"Total Profit: {total_profit:.2f}")
    ts_label.config(text=f"Total Surplus: {consumer_surplus+producer_surplus:.2f}")
    cs_label.config(text=f"Consumer Surplus: {consumer_surplus:.2f}")
    ps_label.config(text=f"Producer Surplus: {producer_surplus:.2f}")


# Function to generate plots based on the calculations
def generate_plots():
    # Preprocess and validate inputs
    inverse_demand_str = preprocess_input(inverse_demand_entry.get())
    cost_function_str = preprocess_input(cost_function_entry.get())

    if not validate_input(inverse_demand_str) or not validate_input(cost_function_str, allow_constant=True):
        messagebox.showerror("Invalid Input",
                             "Please enter valid mathematical expressions for demand and cost functions.")
        return

    try:
        # Status update
        status_label.config(text="Processing...", fg="blue")
        root.update_idletasks()

        # Calculate the statistics
        stats = calculate_profit_maximization(inverse_demand_str, cost_function_str)
        profit_maximizing_quantity, profit_maximizing_price, total_profit, total_revenue, total_cost, marginal_revenue, marginal_cost, consumer_surplus, producer_surplus = stats
        update_labels(stats)

        # Create lambdified functions for numerical evaluation
        P_sym = sp.sympify(inverse_demand_str, locals={'Q': Q})
        C_sym = sp.sympify(cost_function_str, locals={'Q': Q})

        # Lambdify the sympy expressions
        P_func = lambdify(Q, P_sym, "numpy")
        C_func = lambdify(Q, C_sym, "numpy")
        profit_func = lambdify(Q, P_sym * Q - C_sym, "numpy")

        # Generate data points for plotting
        Q_values = np.linspace(0, float(profit_maximizing_quantity) * 1.5, 500)
        P_values = P_func(Q_values)
        profit_values = profit_func(Q_values)

        # Clear previous plots
        for ax in axs.flatten():
            ax.clear()

        # Set up plots
        # 1. Inverse Demand Curve Plot (Consumer and Producer Surplus)
        setup_plot(axs[0], Q_values, P_values, 'Inverse Demand Curve', 'Quantity (Q)', 'Price (P)')
        axs[0].fill_between(Q_values, P_values, float(profit_maximizing_price),
                            where=(Q_values <= profit_maximizing_quantity),
                            color='green', alpha=0.3, label='Consumer Surplus')

        axs[0].fill_between(Q_values, float(profit_maximizing_price), 0,
                            where=(Q_values <= profit_maximizing_quantity),
                            color='blue', alpha=0.3, label='Producer Surplus')

        axs[0].scatter([float(profit_maximizing_quantity)], [float(profit_maximizing_price)],
                       color='red', label=f'Max Profit Point: (Q*={float(profit_maximizing_quantity):.2f}, P*={float(profit_maximizing_price):.2f})')

        axs[0].legend()

        # 2. Profit Function Plot
        setup_plot(axs[1], Q_values, profit_values, 'Profit as a Function of Quantity', 'Quantity (Q)', 'Profit')
        axs[1].scatter([float(profit_maximizing_quantity)], [float(total_profit)], color='red',
                       label=f'Max Profit: {float(total_profit):.2f} at Q*={float(profit_maximizing_quantity):.2f}')
        axs[1].legend()

        # Update the canvas with new plots
        canvas.draw()

        # Status update
        status_label.config(text="Done!", fg="green")

    except Exception as e:
        print(f"Error in generate_plots: {e}")
        messagebox.showerror("Error", f"An error occurred: {e}")


# Close the window and stop the script
def close_app():
    root.destroy()  # This will close the window and end the script

# UI setup
root = Tk()
root.title("Profit Maximization and Surplus Calculator")

# Define modern, minimalist fonts
label_font = tkFont.Font(family="Helvetica", size=20)
entry_font = tkFont.Font(family="Helvetica", size=20)
button_font = tkFont.Font(family="Helvetica", size=20)

# Create a PanedWindow for resizable layout
paned_window = PanedWindow(root, orient='vertical', sashwidth=5)
paned_window.pack(fill='both', expand=True)

# Frame for inputs and statistics
frame = Frame(paned_window, padx=20, pady=20, bg='#F6F8FA')  # Soft grey background
paned_window.add(frame)

# Inverse Demand Function Entry
Label(frame, text="Enter Inverse Demand Function P(Q):", font=label_font, fg='#333333', bg='#F6F8FA').grid(row=0, column=0, sticky="w", pady=10)
inverse_demand_entry = Entry(frame, width=50, font=entry_font, relief='flat', bd=1, highlightbackground='#E2E8ED', highlightcolor='#E2E8ED', fg='#333333', bg='#FFFFFF')
inverse_demand_entry.grid(row=0, column=1, padx=10, pady=10)

# Cost Function Entry
Label(frame, text="Enter Cost Function C(Q):", font=label_font, fg='#333333', bg='#F6F8FA').grid(row=1, column=0, sticky="w", pady=10)
cost_function_entry = Entry(frame, width=50, font=entry_font, relief='flat', bd=1, highlightbackground='#E2E8ED', highlightcolor='#E2E8ED', fg='#333333', bg='#FFFFFF')
cost_function_entry.grid(row=1, column=1, padx=10, pady=10)

# Status label
status_label = Label(frame, text="", font=label_font, bg='#F6F8FA', fg='green')
status_label.grid(row=2, column=0, columnspan=2)

# Button to start the calculation and plot generation
submit_button = Button(frame, text="Start", font=button_font, bg='#D1D5DB', fg='#333333', padx=20, pady=10,
                       relief='flat', bd=0, activebackground='#E2E8ED', width=15, anchor='center')
submit_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')
submit_button.config(command=generate_plots)

# Add the Close button below the other widgets
close_button = Button(frame, text="Close", font=button_font, bg='#D1D5DB', fg='#333333', padx=20, pady=10,
                      relief='flat', bd=0, activebackground='#E2E8ED', width=15, anchor='center')
close_button.grid(row=1, column=2, padx=10, pady=10, sticky='e')
close_button.config(command=close_app)

# Labels for statistics (now in two columns)
price_label = Label(frame, text="Profit Maximizing Price: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
price_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)

quantity_label = Label(frame, text="Profit Maximizing Quantity: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
quantity_label.grid(row=5, column=0, sticky="w", padx=5, pady=5)

mc_label = Label(frame, text="Marginal Cost: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
mc_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)

mr_label = Label(frame, text="Marginal Revenue: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
mr_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)

total_cost_label = Label(frame, text="Total Cost: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
total_cost_label.grid(row=4, column=1, sticky="w", padx=5, pady=5)

total_revenue_label = Label(frame, text="Total Revenue: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
total_revenue_label.grid(row=5, column=1, sticky="w", padx=5, pady=5)

total_profit_label = Label(frame, text="Total Profit: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
total_profit_label.grid(row=6, column=1, sticky="w", padx=5, pady=5)

ts_label = Label(frame, text="Total Surplus: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
ts_label.grid(row=7, column=1, sticky="w", padx=5, pady=5)

cs_label = Label(frame, text="Consumer Surplus: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
cs_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)

ps_label = Label(frame, text="Producer Surplus: N/A", font=label_font, fg='#333333', bg='#F6F8FA')
ps_label.grid(row=8, column=1, sticky="w", padx=5, pady=5)

# Create a separate frame for the graphs
graph_frame = Frame(paned_window)
paned_window.add(graph_frame)

# Set up the matplotlib figure with 1x2 grid for the two remaining plots
fig, axs = plt.subplots(1, 2, figsize=(10, 5))  # Now only two subplots

# Initially populate with empty plots
for ax in axs:
    ax.set_title('Empty Plot')
    ax.grid(True)

# Embed the matplotlib figure in Tkinter window using FigureCanvasTkAgg
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()
canvas.get_tk_widget().pack(fill='both', expand=True)

# Run the Tkinter main loop
root.mainloop()
