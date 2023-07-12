
#pip install PySide2 matplotlib pytest pytest-qt




import sys
from math import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import pytest
from pytestqt import qtbot


class FunctionPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Function Plotter")
        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout(self)

        self.function_label = QLabel("Enter function (use 'x' as the variable):")
        self.function_text = QLineEdit()
        self.function_text.setPlaceholderText("e.g., 5*x**3 + 2*x")

        self.range_label = QLabel("Enter the range for x:")
        self.x_min = QLineEdit()
        self.x_min.setPlaceholderText("Minimum x")
        self.x_max = QLineEdit()
        self.x_max.setPlaceholderText("Maximum x")

        self.plot_button = QPushButton("Plot")

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.function_label)
        self.layout.addWidget(self.function_text)
        self.layout.addWidget(self.range_label)
        self.layout.addWidget(self.x_min)
        self.layout.addWidget(self.x_max)
        self.layout.addWidget(self.plot_button)
        self.layout.addWidget(self.canvas)

        self.plot_button.clicked.connect(self.plot)

    def validate_inputs(self):
        function = self.function_text.text()
        x_min = self.x_min.text()
        x_max = self.x_max.text()

        # Check if any input is empty
        if not function or not x_min or not x_max:
            QMessageBox.critical(self, "Error", "Please enter all the values.")
            return False

        # Check if x_min and x_max are valid floats
        try:
            float(x_min)
            float(x_max)
        except ValueError:
            QMessageBox.critical(self, "Error", "Invalid range for x.")
            return False

        return True

    def plot(self):
        if not self.validate_inputs():
            return

        function = self.function_text.text()
        x_min = float(self.x_min.text())
        x_max = float(self.x_max.text())

        try:
            x = []
            y = []

            step = (x_max - x_min) / 100  # Adjust the step size as needed for smoother curves

            while x_min <= x_max:
                x.append(x_min)
                y.append(eval(function.replace('x', str(x_min))))
                x_min += step

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(x, y)
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title('Function Plot')
            self.canvas.draw()

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


@pytest.fixture
def function_plotter(qtbot):
    plotter = FunctionPlotter()
    qtbot.addWidget(plotter)
    return plotter


def test_plot_button_click(function_plotter, qtbot):
    function_plotter.function_text.setText("x**2")
    function_plotter.x_min.setText("0")
    function_plotter.x_max.setText("10")

    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)

    assert len(function_plotter.figure.axes) == 1


def test_empty_input(function_plotter, qtbot, capsys):
    function_plotter.function_text.setText("")
    function_plotter.x_min.setText("0")
    function_plotter.x_max.setText("10")

    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)

    captured = capsys.readouterr()
    assert "Please enter all the values." in captured.err


def test_invalid_range(function_plotter, qtbot, capsys):
    function_plotter.function_text.setText("x**2")
    function_plotter.x_min.setText("A")
    function_plotter.x_max.setText("10")

    qtbot.mouseClick(function_plotter.plot_button, Qt.LeftButton)

    captured = capsys.readouterr()
    assert "Invalid range for x." in captured.err


if __name__ == '__main__':
    app = QApplication(sys.argv)
    plotter = FunctionPlotter()
    plotter.show()
    sys.exit(app.exec_())

