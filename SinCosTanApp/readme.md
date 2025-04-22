# Unit Circle Visualizer (PyQtGraph)

## Description

This is a desktop application written in Python that interactively visualizes the unit circle and the fundamental trigonometric functions (sine, cosine, tangent) using the `pyqtgraph` library. 
## Main Features

*   **Interactive Angle Adjustment:**
    *   Using a slider (range 0-360 degrees with 0.1 precision).
    *   By entering a value in the text box.
    *   Using preset buttons for common angles (e.g., 0°, 30°, 45°, 90°, ..., 360°).
*   **Unit Circle Visualization:**
    *   Displays the unit circle and coordinate axes.
    *   Draws the radius vector (terminal side) for the selected angle.
    *   Highlights the point `(cos(α), sin(α))` on the circle.
    *   Visualizes the `sin(α)` value as a vertical line segment.
    *   Visualizes the `cos(α)` value as a horizontal line segment.
    *   Visualizes the `tan(α)` value as a segment on the tangent line `x=1` and a helper line from the origin.
    *   Draws an arc representing the selected angle `α`.
*   **Trigonometric Function Plots:**
    *   Separate plots for `sin(x)`, `cos(x)`, and `tan(x)` over the range `[0, 2π]`.
    *   Clearly marked asymptotes for the tangent function.
    *   A dynamic marker on each plot indicating the function's value for the current angle.
    *   Helper lines from the x-axis to the marker on the function plots.
*   **Value Display:**
    *   The current angle displayed in both degrees and radians.
    *   Calculated values for `sin(α)`, `cos(α)`, and `tan(α)` with appropriate formatting and colors.

## Program Purpose

The main goal of this application is to provide an **interactive educational tool** that helps in understanding:

1.  The **definition of trigonometric functions** based on the unit circle.
2.  The **relationship between the angle** (in degrees and radians) and the coordinates of the point on the unit circle.
3.  The **visual connection** between the sine, cosine, and tangent values on the circle and their corresponding values on the function graphs.
4.  The **shape and periodicity** of the sine, cosine, and tangent functions.
5.  The **behavior of the tangent function** near its asymptotes.

## Requirements

To run the application, you need Python 3 and the following libraries:

*   **NumPy:** For numerical operations.
*   **PyQtGraph:** For plotting.
*   **A Qt Binding:** One of the following libraries (the script defaults to PyQt6):
    *   **PyQt6** (Recommended)
    *   PyQt5
    *   PySide6

You can install all dependencies using the provided `requirements.txt` file.

## Installing Dependencies

1.  **Clone the repository** or download the script file (`.py`) and the `requirements.txt` file.
2.  **Open your terminal** or command prompt.
3.  **Navigate to the directory** where you downloaded the files.
4.  **Install the required packages** using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The `requirements.txt` file is configured to install `PyQt6`. If you wish to use `PyQt5` or `PySide6`, you need to modify this file (uncomment the desired line and comment out the others) before running the command above.*

## Running the Application

After installing the dependencies, run the Python script from your terminal:

```bash
python main.py