import sys
import numpy as np
import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore, QtGui
import math

pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class UnitCircleVisualizerPyQtGraph(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initial_angle_deg = 30.0
        self.current_angle_deg = self.initial_angle_deg
        self.current_angle_rad = math.radians(self.current_angle_deg)
        self.tan_limit = 5

        self._setup_ui()
        self._setup_plots()
        self._connect_signals()
        self._update_visuals(self.current_angle_deg)
        self.show()

    def _setup_ui(self):
        self.setWindowTitle("SinCosTanApp")
        self.setGeometry(100, 100, 1300, 850)

        self.main_layout = QtWidgets.QGridLayout(self)

        control_widget = QtWidgets.QWidget()
        control_layout = QtWidgets.QVBoxLayout(control_widget)

        slider_layout = QtWidgets.QHBoxLayout()
        slider_label = QtWidgets.QLabel("Angle [deg]:")
        self.angle_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.angle_slider.setRange(0, 3600)
        self.angle_slider.setValue(int(self.initial_angle_deg * 10))
        self.angle_slider.setSingleStep(1)
        self.angle_slider.setTickInterval(900)
        self.angle_slider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksBelow)
        self.slider_value_label = QtWidgets.QLabel(f"{self.initial_angle_deg:.1f}")
        self.slider_value_label.setMinimumWidth(40)
        self.slider_value_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignVCenter)
        slider_layout.addWidget(slider_label)
        slider_layout.addWidget(self.angle_slider)
        slider_layout.addWidget(self.slider_value_label)
        control_layout.addLayout(slider_layout)

        textbox_layout = QtWidgets.QHBoxLayout()
        textbox_label = QtWidgets.QLabel("Set Angle:")
        self.angle_textbox = QtWidgets.QLineEdit(str(self.initial_angle_deg))

        double_validator = QtGui.QDoubleValidator(0.0, 360.0, 2, self)
        double_validator.setNotation(QtGui.QDoubleValidator.Notation.StandardNotation)
        self.angle_textbox.setValidator(double_validator)
        self.angle_textbox.setMaximumWidth(80)
        textbox_layout.addWidget(textbox_label)
        textbox_layout.addWidget(self.angle_textbox)
        textbox_layout.addStretch()
        control_layout.addLayout(textbox_layout)

        self.reset_button = QtWidgets.QPushButton("Reset")
        control_layout.addWidget(self.reset_button, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        common_angles = [0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 225, 240, 270, 300, 315, 330, 360]
        button_grid = QtWidgets.QGridLayout()
        buttons_per_row = 9
        self.angle_buttons = []
        for i, angle in enumerate(common_angles):
            row = i // buttons_per_row
            col = i % buttons_per_row
            button = QtWidgets.QPushButton(f"{angle}\u00b0")
            button.clicked.connect(lambda checked=False, a=angle: self._set_angle(float(a)))
            button_grid.addWidget(button, row, col)
            self.angle_buttons.append(button)
        control_layout.addLayout(button_grid)
        control_layout.addStretch()

        self.win = pg.GraphicsLayoutWidget()

        self.plot_circle = self.win.addPlot(row=0, col=0, rowspan=3, title="Unit Circle")
        self.plot_circle.setAspectLocked(True)
        self.plot_circle.setXRange(-1.7, 1.7)
        self.plot_circle.setYRange(-1.7, 1.7)
        self.plot_circle.showGrid(x=True, y=True, alpha=0.3)
        self.plot_circle.getViewBox().setLimits(xMin=-1.8, xMax=1.8, yMin=-1.8, yMax=1.8)
        self.plot_circle.getViewBox().disableAutoRange()

        self.text_widget = QtWidgets.QWidget()
        self.text_layout = QtWidgets.QVBoxLayout(self.text_widget)
        self.text_layout.addStretch()
        self.angle_deg_label = QtWidgets.QLabel("Angle [deg]: -")
        self.angle_rad_label = QtWidgets.QLabel("Angle [rad]: -")
        self.sin_label = QtWidgets.QLabel("Sine: -")
        self.cos_label = QtWidgets.QLabel("Cosine: -")
        self.tan_label = QtWidgets.QLabel("Tangent: -")

        font = QtGui.QFont()
        font.setPointSize(12)
        for label in [self.angle_deg_label, self.angle_rad_label, self.sin_label, self.cos_label, self.tan_label]:
            label.setFont(font)
            self.text_layout.addWidget(label, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        self.text_layout.addStretch()

        self.plot_sine = self.win.addPlot(row=0, col=1, title="Sine Function")
        self.plot_cosine = self.win.addPlot(row=1, col=1, title="Cosine Function")
        self.plot_tangent = self.win.addPlot(row=2, col=1, title="Tangent Function")

        major_ticks_x = [
            (0, '0'), (np.pi/2, 'π/2'), (np.pi, 'π'),
            (3*np.pi/2, '3π/2'), (2*np.pi, '2π')
        ]

        for plot in [self.plot_sine, self.plot_cosine, self.plot_tangent]:
            plot.setXRange(0, 2 * np.pi)
            plot.showGrid(x=True, y=True, alpha=0.3)
            ax = plot.getAxis('bottom')
            ax.setTicks([major_ticks_x])
            plot.getAxis('left').setLabel('Value', units=None)

        self.plot_sine.setYRange(-1.1, 1.1)
        self.plot_cosine.setYRange(-1.1, 1.1)
        self.plot_tangent.setYRange(-self.tan_limit*1.1, self.tan_limit*1.1)

        tan_asymptote_pen = pg.mkPen(color=(180, 180, 180), style=QtCore.Qt.PenStyle.DashLine, width=1)
        self.tan_asymptote1 = pg.InfiniteLine(pos=np.pi/2, angle=90, pen=tan_asymptote_pen)
        self.tan_asymptote2 = pg.InfiniteLine(pos=3*np.pi/2, angle=90, pen=tan_asymptote_pen)
        self.plot_tangent.addItem(self.tan_asymptote1)
        self.plot_tangent.addItem(self.tan_asymptote2)
        self.plot_tangent.getViewBox().setLimits(yMin=-self.tan_limit*1.2, yMax=self.tan_limit*1.2)

        self.main_layout.addWidget(self.win, 0, 0)
        self.main_layout.addWidget(self.text_widget, 0, 1)
        self.main_layout.addWidget(control_widget, 1, 0, 1, 2)

        self.main_layout.setColumnStretch(0, 3)
        self.main_layout.setColumnStretch(1, 1)
        self.main_layout.setRowStretch(0, 1)
        self.main_layout.setRowStretch(1, 0)

    def _setup_plots(self):
        theta = np.linspace(0, 2*np.pi, 200)
        self.circle_item = pg.PlotDataItem(np.cos(theta), np.sin(theta), pen=pg.mkPen('blue', width=2))
        self.plot_circle.addItem(self.circle_item)
        axis_pen = pg.mkPen(color=(150, 150, 150), width=1)
        self.plot_circle.addItem(pg.InfiniteLine(pos=0, angle=90, pen=axis_pen))
        self.plot_circle.addItem(pg.InfiniteLine(pos=0, angle=0, pen=axis_pen))

        self.angle_line_item = pg.PlotDataItem(pen=pg.mkPen('red', width=2.5))
        self.point_item = pg.PlotDataItem(pen=None, symbol='o', symbolBrush='red', symbolSize=9)
        self.sin_line_item = pg.PlotDataItem(pen=pg.mkPen('purple', style=QtCore.Qt.PenStyle.SolidLine, width=2.5))
        self.cos_line_item = pg.PlotDataItem(pen=pg.mkPen('green', style=QtCore.Qt.PenStyle.SolidLine, width=2.5))

        tangent_color = QtGui.QColor(165, 42, 42)
        tangent_extend_color = QtGui.QColor(165, 42, 42, 180)

        self.tangent_line_item = pg.PlotDataItem(pen=pg.mkPen(tangent_color, style=QtCore.Qt.PenStyle.SolidLine, width=2.5))
        self.tangent_point_item = pg.PlotDataItem(pen=None, symbol='s', symbolBrush=tangent_color, symbolSize=8)
        self.tangent_extend_item = pg.PlotDataItem(pen=pg.mkPen(tangent_extend_color, style=QtCore.Qt.PenStyle.DotLine, width=2.0))

        self.angle_arc_item = pg.PlotDataItem(pen=pg.mkPen(color=(255, 0, 0, 180), width=2.0))
        self.angle_label_item = pg.TextItem(text='α', color='red', anchor=(0.5, 0.5))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.angle_label_item.setFont(font)

        self.plot_circle.addItem(self.angle_line_item)
        self.plot_circle.addItem(self.point_item)
        self.plot_circle.addItem(self.sin_line_item)
        self.plot_circle.addItem(self.cos_line_item)
        self.plot_circle.addItem(self.tangent_line_item)
        self.plot_circle.addItem(self.tangent_point_item)
        self.plot_circle.addItem(self.tangent_extend_item)
        self.plot_circle.addItem(self.angle_arc_item)
        self.plot_circle.addItem(self.angle_label_item)

        x_vals = np.linspace(0, 2*np.pi, 500)
        self.sine_curve_item = pg.PlotDataItem(x_vals, np.sin(x_vals), pen=pg.mkPen('purple', width=2))
        self.cosine_curve_item = pg.PlotDataItem(x_vals, np.cos(x_vals), pen=pg.mkPen('green', width=2))
        y_tan = np.tan(x_vals)
        y_tan[:-1][np.abs(np.diff(y_tan)) > 2 * self.tan_limit * 5] = np.nan
        self.tangent_curve_item = pg.PlotDataItem(x_vals, y_tan, pen=pg.mkPen(tangent_color, width=2), connect='finite')

        self.plot_sine.addItem(self.sine_curve_item)
        self.plot_cosine.addItem(self.cosine_curve_item)
        self.plot_tangent.addItem(self.tangent_curve_item)

        common_symbol = 'o'
        common_symbol_size = 9
        line_style = QtCore.Qt.PenStyle.DashLine
        self.current_sine_point_item = pg.PlotDataItem(pen=None, symbol=common_symbol, symbolBrush='red', symbolSize=common_symbol_size)
        self.sine_height_line_item = pg.PlotDataItem(pen=pg.mkPen('purple', style=line_style, width=1.5))
        self.current_cosine_point_item = pg.PlotDataItem(pen=None, symbol=common_symbol, symbolBrush='red', symbolSize=common_symbol_size)
        self.cosine_height_line_item = pg.PlotDataItem(pen=pg.mkPen('green', style=line_style, width=1.5))
        self.current_tan_point_item = pg.PlotDataItem(pen=None, symbol=common_symbol, symbolBrush='red', symbolSize=common_symbol_size)
        self.tan_height_line_item = pg.PlotDataItem(pen=pg.mkPen(tangent_color, style=line_style, width=1.5))

        self.plot_sine.addItem(self.current_sine_point_item)
        self.plot_sine.addItem(self.sine_height_line_item)
        self.plot_cosine.addItem(self.current_cosine_point_item)
        self.plot_cosine.addItem(self.cosine_height_line_item)
        self.plot_tangent.addItem(self.current_tan_point_item)
        self.plot_tangent.addItem(self.tan_height_line_item)

    def _connect_signals(self):
        self.angle_slider.valueChanged.connect(self._slider_changed)
        self.angle_textbox.returnPressed.connect(self._text_submitted)
        self.angle_textbox.editingFinished.connect(self._text_submitted)
        self.reset_button.clicked.connect(self._reset_angle)

    def _slider_changed(self, value):
        angle_deg = value / 10.0
        current_text = self.angle_textbox.text().replace(',', '.')
        new_text = f"{angle_deg:.1f}"
        if current_text != new_text:
             if not self.angle_textbox.hasFocus():
                 self.angle_textbox.setText(new_text)

        self.slider_value_label.setText(f"{angle_deg:.1f}")
        self._update_visuals(angle_deg)

    def _text_submitted(self):
        try:
            angle_deg_str = self.angle_textbox.text().replace(',', '.')
            angle_deg = float(angle_deg_str)

            if 0.0 <= angle_deg <= 360.0:
                angle_deg = round(angle_deg, 1)
                self.angle_slider.blockSignals(True)
                self.angle_slider.setValue(int(round(angle_deg * 10)))
                self.angle_slider.blockSignals(False)
                formatted_angle = f"{angle_deg:.1f}"
                if self.angle_textbox.text() != formatted_angle:
                    self.angle_textbox.setText(formatted_angle)
                self.slider_value_label.setText(formatted_angle)
                self._update_visuals(angle_deg)
            else:
                self.angle_textbox.setText(f"{self.current_angle_deg:.1f}")
        except ValueError:
            self.angle_textbox.setText(f"{self.current_angle_deg:.1f}")

    def _set_angle(self, angle_deg):
        angle_deg = float(angle_deg)
        self.angle_slider.setValue(int(round(angle_deg * 10)))
        formatted_angle = f"{angle_deg:.1f}"
        self.angle_textbox.setText(formatted_angle)

    def _reset_angle(self):
        self._set_angle(self.initial_angle_deg)

    def _update_visuals(self, angle_deg):
        self.current_angle_deg = angle_deg
        self.current_angle_rad = math.radians(angle_deg)

        cos_a = np.cos(self.current_angle_rad)
        sin_a = np.sin(self.current_angle_rad)

        angle_mod_2pi = self.current_angle_rad % (2 * np.pi)
        is_near_pi_half = math.isclose(angle_mod_2pi, np.pi / 2, abs_tol=1e-8)
        is_near_3pi_half = math.isclose(angle_mod_2pi, 3 * np.pi / 2, abs_tol=1e-8)
        is_pole = is_near_pi_half or is_near_3pi_half

        self.angle_line_item.setData([0, cos_a], [0, sin_a])
        self.point_item.setData([cos_a], [sin_a])
        self.sin_line_item.setData([cos_a, cos_a], [0, sin_a])
        self.cos_line_item.setData([0, cos_a], [0, 0])

        show_tangent = False
        tan_text_val = "undefined"

        if not is_pole and abs(cos_a) > 1e-9:
            try:
                tan_a = math.tan(self.current_angle_rad)
                tan_display = np.clip(tan_a, -self.tan_limit, self.tan_limit)

                self.tangent_line_item.setData([1, 1], [0, tan_display])
                self.tangent_point_item.setData([1], [tan_display])
                self.tangent_extend_item.setData([0, 1], [0, tan_display])

                show_tangent = True
                tan_text_val = f"{tan_a:.4f}"

            except OverflowError:
                tan_text_val = "undefined (Overflow)"
                show_tangent = False
        else:
            tan_text_val = "undefined (≈π/2 + kπ)" if is_pole else "undefined (cos ≈ 0)"
            show_tangent = False

        self.tangent_line_item.setVisible(show_tangent)
        self.tangent_point_item.setVisible(show_tangent)
        self.tangent_extend_item.setVisible(show_tangent)

        arc_radius = 0.35
        arc_points = 50
        theta_arc = np.linspace(0, self.current_angle_rad, arc_points)
        self.angle_arc_item.setData(arc_radius * np.cos(theta_arc), arc_radius * np.sin(theta_arc))

        label_radius = 0.45
        label_angle_rad = self.current_angle_rad / 2.0
        label_x = label_radius * np.cos(label_angle_rad)
        label_y = label_radius * np.sin(label_angle_rad)
        self.angle_label_item.setPos(label_x, label_y)

        sin_color = "purple"
        cos_color = "green"
        tan_color = "saddlebrown"
        self.sin_label.setText(f"Sine: <font color='{sin_color}'>{sin_a:.4f}</font>")
        self.cos_label.setText(f"Cosine: <font color='{cos_color}'>{cos_a:.4f}</font>")
        self.tan_label.setText(f"Tangent: <font color='{tan_color}'>{tan_text_val}</font>")
        self.angle_deg_label.setText(f"Angle [deg]: {angle_deg:.1f}°")
        self.angle_rad_label.setText(f"Angle [rad]: {self.current_angle_rad:.4f}")

        plot_angle_rad = angle_mod_2pi

        self.current_sine_point_item.setData([plot_angle_rad], [sin_a])
        self.sine_height_line_item.setData([plot_angle_rad, plot_angle_rad], [0, sin_a])

        self.current_cosine_point_item.setData([plot_angle_rad], [cos_a])
        self.cosine_height_line_item.setData([plot_angle_rad, plot_angle_rad], [0, cos_a])

        if show_tangent:
            tan_a_for_plot = math.tan(self.current_angle_rad)
            tan_plot_display = np.clip(tan_a_for_plot, -self.tan_limit, self.tan_limit)
            self.current_tan_point_item.setData([plot_angle_rad], [tan_plot_display])
            self.tan_height_line_item.setData([plot_angle_rad, plot_angle_rad], [0, tan_plot_display])
        self.current_tan_point_item.setVisible(show_tangent)
        self.tan_height_line_item.setVisible(show_tangent)

if __name__ == '__main__':
    if hasattr(QtCore.Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
    if hasattr(QtCore.Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)

    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = UnitCircleVisualizerPyQtGraph()

    sys.exit(qapp.exec())