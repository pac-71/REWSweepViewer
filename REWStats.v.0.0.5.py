import sys
import os
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, 
    QPushButton, QFileDialog,
    QTextEdit, QSplitter
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# v.0.0.0 Loaded REW export text sweep spectrum files with basic stats. Old version.
# v.0.0.1 Added graph with Matlibplot and numpy 
# v.0.0.2 Added Stats block, Mean 95 percentile
# v.0.0.3 Added spectra lines count
# v.0.0.4 Add 3db, 10db thresholds
# v.0.0.5 Added filename to window titlebar & stats, added resizing.

version = "v.0.0.5"
appname = "REW Sweep Viewer"

class SPLGraphCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.ax.set_xscale('log')
        super().__init__(fig)
        self.setParent(parent)

    def plot_spl(self, freq_hz, spl_db, mean_spl, perc_95):
        self.ax.clear()
        self.ax.set_xscale('log')
        self.ax.plot(freq_hz, spl_db, label="SPL vs Frequency", color='blue')
        self.ax.axhline(mean_spl, color='red', linestyle='--', label=f"Mean SPL: {mean_spl:.2f} dB")
        self.ax.axhline(perc_95, color='green', linestyle=':', label=f"95th Percentile: {perc_95:.2f} dB")
        self.ax.axhline(perc_95-3, color='orange', linestyle=':', label=f"95th -3dB: {perc_95-3:.2f} dB")
        self.ax.axhline(perc_95-10, color='orange', linestyle=':', label=f"95th -10dB: {perc_95-10:.2f} dB")
        self.ax.set_xlabel("Frequency (Hz)")
        self.ax.set_ylabel("SPL (dB)")
        self.ax.set_title("SPL vs Frequency (Log Scale)")
        self.ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.ax.legend()
        self.draw()

class REWViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{appname} {version}")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        self.load_button = QPushButton("Load REW File")
        self.load_button.clicked.connect(self.load_file)
        main_layout.addWidget(self.load_button)

        splitter = QSplitter(Qt.Vertical)

        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        splitter.addWidget(self.text_output)

        self.stats_box = QTextEdit()
        self.stats_box.setReadOnly(True)
        splitter.addWidget(self.stats_box)

        self.graph_canvas = SPLGraphCanvas(self)
        splitter.addWidget(self.graph_canvas)

        main_layout.addWidget(splitter)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open REW File", "", "Text Files (*.txt)")
        if file_path:
            filename = os.path.basename(file_path)
            self.setWindowTitle(f"{appname} {version} – {filename}")

            freq_hz, spl_db, raw_lines = self.parse_rew_file(file_path)
            self.text_output.setPlainText("\n".join(raw_lines))

            mean_spl = np.mean(spl_db)
            perc_95 = np.percentile(spl_db, 95)
            min_spl = np.min(spl_db)
            max_spl = np.max(spl_db)
            freq_min = np.min(freq_hz)
            freq_max = np.max(freq_hz)
            lines = spl_db.size

            indexes_3db = np.where(spl_db > perc_95 - 3)[0]
            indexes_10db = np.where(spl_db > perc_95 - 10)[0]

            stats_text = (
                f"SPL Stats for REW Sweep File: {filename}\n"
                f"Spectra: {lines} lines\n"
                f"Mean SPL: {mean_spl:.2f} dB\n"
                f"95th Percentile: {perc_95:.2f} dB\n"
                f"Min SPL: {min_spl:.2f} dB\n"
                f"Max SPL: {max_spl:.2f} dB\n"
                f"Frequency Range: {freq_min:.1f} Hz – {freq_max:.1f} Hz\n"
                f"F3 Low: {freq_hz[indexes_3db[0]]:.2f} Hz F3 High: {freq_hz[indexes_3db[-1]]:.2f} Hz\n"
                f"F10 Low: {freq_hz[indexes_10db[0]]:.2f} Hz F10 High: {freq_hz[indexes_10db[-1]]:.2f} Hz"
            )
            self.stats_box.setPlainText(stats_text)

            self.graph_canvas.plot_spl(freq_hz, spl_db, mean_spl, perc_95)

    def parse_rew_file(self, file_path):
        freq_hz = []
        spl_db = []
        raw_lines = []
        with open(file_path, 'r') as f:
            for line in f:
                raw_lines.append(line.strip())
                if line.strip() and not line.startswith("*"):
                    parts = line.strip().split()
                    if len(parts) >= 2:
                        try:
                            freq = float(parts[0])
                            spl = float(parts[1])
                            freq_hz.append(freq)
                            spl_db.append(spl)
                        except ValueError:
                            continue
        return np.array(freq_hz), np.array(spl_db), raw_lines

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = REWViewer()
    viewer.show()
    sys.exit(app.exec_())
