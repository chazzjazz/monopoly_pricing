# Profit Maximization and Surplus Calculator

This Python-based graphical application computes the profit-maximizing price and quantity, as well as the consumer surplus, producer surplus, and total profit from given inverse demand and cost functions. The application provides a user-friendly graphical interface (built with Tkinter) to input functions, visualize results through plots (generated with Matplotlib), and displays important economic metrics.

![image](https://github.com/user-attachments/assets/f50c13c8-1e96-4503-a7a1-f561d7c96b67)


## Features

- Graphical User Interface (GUI): Easily input functions and see the results displayed in real-time.
- Plots:
  - Inverse Demand Curve with shaded Consumer Surplus (green) and Producer Surplus (blue).
  - Profit Function plot showing the relationship between quantity and profit.
- Displays key economic metrics such as:
  - Profit-maximizing price and quantity
  - Marginal cost and marginal revenue
  - Total profit
  - Consumer surplus and producer surplus

## Technologies Used

- SymPy: Symbolic mathematics library for handling algebraic functions.
- Matplotlib: For plotting graphs in the Tkinter GUI.
- Tkinter: GUI toolkit for rendering the user interface.
- NumPy: For numerical operations.
- Python 3.x

## How the Script Works

1. Input Functions: 
   - The user inputs an inverse demand function and a cost function into the provided entry fields.
   - The script processes the input, ensuring it is valid and can be evaluated using SymPy.

2. Computation: 
   - Using the inputted functions, the script calculates the profit-maximizing quantity where Marginal Revenue (MR) equals Marginal Cost (MC).
   - The profit-maximizing price is determined by substituting the quantity into the inverse demand function.

3. Visualization:
   - Two key plots are generated:
     - Inverse Demand Curve: Shows the relationship between quantity and price, with shaded regions for consumer surplus and producer surplus.
     - Profit Function: Shows the profit as a function of quantity, with a marker on the maximum profit point.
   
4. Display of Results: 
   - The GUI displays key metrics like profit-maximizing price, quantity, total profit, marginal revenue, marginal cost, and both surpluses.

## Installation

1. Clone the Repository:
   ```bash
   git clone https://github.com/yourusername/profit-maximization-calculator.git
   cd profit-maximization-calculator
   ```

2. Install Dependencies:
   Make sure you have Python 3.x installed. Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

   If you don’t have the `requirements.txt`, manually install these dependencies:
   ```bash
   pip install sympy matplotlib numpy
   ```

3. Run the Script:
   Start the application by running the following command in your terminal:
   ```bash
   python profit_maximization.py
   ```

## Usage

1. Input the Inverse Demand Function in terms of `Q` (quantity). Example: `12 - Q / 1000`.
2. Input the Cost Function in terms of `Q`. Example: `1.4Q` or `1.4`.
3. Click Start to perform the calculations and generate the plots.
4. View the results in the form of plots and key metrics displayed in the UI.
5. Click Close to exit the application.

## Example

- Inverse Demand Function: `P(Q) = 12 - (Q / 1000)`
- Cost Function: `C(Q) = 1.4`

After hitting Start, the application will calculate the profit-maximizing price and quantity, along with the consumer surplus, producer surplus, and total profit. The Inverse Demand Curve will display the shaded consumer and producer surpluses, and the Profit Function will show the profit curve with a highlighted maximum point.

## File Structure

```
├── profit_maximization.py   # Main script for running the calculator
├── README.md                # This README file
└── requirements.txt         # Required Python packages
```

## Dependencies
- SymPy
- NumPy
- Matplotlib
- Tkinter (included in Python standard library)
