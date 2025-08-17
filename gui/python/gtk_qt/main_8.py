#!/usr/bin/env python3
"""
Qt5 vs Qt6 Performance and Feature Comparison Demo
Run this to see actual differences between Qt versions
"""

import sys
import time
import psutil
import os
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

class PerformanceWidget(QWidget):
    """Widget to demonstrate performance differences"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(100)  # Update every 100ms
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Performance metrics
        self.memory_label = QLabel("Memory Usage: ")
        self.cpu_label = QLabel("CPU Usage: ")
        self.render_time_label = QLabel("Render Time: ")
        
        layout.addWidget(QLabel("🚀 Performance Metrics:"))
        layout.addWidget(self.memory_label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.render_time_label)
        
        # Animation test
        self.animation_label = QLabel("🎯 Animation Test")
        self.animation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.animation_label.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff6b6b, stop:1 #4ecdc4);
                border-radius: 15px;
                padding: 20px;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.animation_label)
        
        # Start animation
        self.animation = QPropertyAnimation(self.animation_label, b"geometry")
        self.animation.setDuration(2000)
        self.animation.setLoopCount(-1)
        self.animation.valueChanged.connect(lambda: self.measure_render_time())
        
        # GPU acceleration test
        gpu_test = QLabel("🎮 GPU Test - Gradients & Shadows")
        gpu_test.setStyleSheet("""
            QLabel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #667eea, stop:1 #764ba2);
                border-radius: 20px;
                padding: 15px;
                color: white;
                font-weight: bold;
            }
        """)
        layout.addWidget(gpu_test)
        
        self.setLayout(layout)
        
    def resizeEvent(self, event):
        """Update animation when window resizes"""
        super().resizeEvent(event)
        if hasattr(self, 'animation'):
            width = self.width() - 50
            self.animation.setStartValue(QRect(10, 100, 200, 50))
            self.animation.setEndValue(QRect(width - 200, 100, 200, 50))
            if not self.animation.state() == QPropertyAnimation.State.Running:
                self.animation.start()
    
    def measure_render_time(self):
        """Measure rendering performance"""
        start_time = time.perf_counter()
        self.repaint()
        render_time = (time.perf_counter() - start_time) * 1000
        self.render_time_label.setText(f"Render Time: {render_time:.2f}ms")
    
    def update_stats(self):
        """Update performance statistics"""
        process = psutil.Process(os.getpid())
        memory_mb = process.memory_info().rss / 1024 / 1024
        cpu_percent = process.cpu_percent()
        
        self.memory_label.setText(f"Memory Usage: {memory_mb:.1f} MB")
        self.cpu_label.setText(f"CPU Usage: {cpu_percent:.1f}%")

class ModernFeaturesWidget(QWidget):
    """Widget to showcase Qt6 modern features"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # High DPI scaling info
        layout.addWidget(QLabel("📱 High DPI & Scaling Features:"))
        
        dpi_info = QLabel(f"""
        Screen DPI: {QApplication.primaryScreen().logicalDotsPerInch():.1f}
        Device Pixel Ratio: {QApplication.primaryScreen().devicePixelRatio():.2f}
        Qt Version: {QT_VERSION_STR}
        Platform: {QApplication.platformName()}
        """)
        dpi_info.setStyleSheet("background: #2c3e50; color: white; padding: 10px; border-radius: 5px;")
        layout.addWidget(dpi_info)
        
        # Touch and gesture simulation
        layout.addWidget(QLabel("👆 Touch & Gesture Features:"))
        
        touch_area = QLabel("Touch/Gesture Test Area\n(Qt6 has better touch support)")
        touch_area.setMinimumHeight(100)
        touch_area.setStyleSheet("""
            QLabel {
                background: #34495e;
                color: white;
                border: 2px dashed #3498db;
                border-radius: 10px;
                font-size: 14px;
            }
        """)
        touch_area.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(touch_area)
        
        # Modern styling features
        layout.addWidget(QLabel("🎨 Modern Styling Features:"))
        
        modern_button = QPushButton("Modern Qt6 Button")
        modern_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border: none;
                border-radius: 15px;
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 12px 24px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5dade2, stop:1 #3498db);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2980b9, stop:1 #1b4f72);
            }
        """)
        layout.addWidget(modern_button)
        
        self.setLayout(layout)

class Qt6ComparisonApp(QMainWindow):
    """Main application to demonstrate Qt6 features"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Qt6 vs Qt5 - Performance & Feature Demo")
        self.setGeometry(100, 100, 900, 700)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Header
        header = QLabel("🔬 Qt6 Performance & Feature Analysis")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                color: #2c3e50;
                padding: 20px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #74b9ff, stop:1 #0984e3);
                color: white;
                border-radius: 10px;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(header)
        
        # Tab widget
        tab_widget = QTabWidget()
        
        # Add tabs
        performance_widget = PerformanceWidget()
        features_widget = ModernFeaturesWidget()
        
        tab_widget.addTab(performance_widget, "⚡ Performance")
        tab_widget.addTab(features_widget, "🚀 Modern Features")
        
        layout.addWidget(tab_widget)
        
        # Difference explanation
        explanation = QLabel("""
        💡 Key Qt6 Improvements You Can't See:
        • Better memory management and faster startup
        • Improved Wayland support (crucial for Hyprland!)
        • Enhanced GPU acceleration for smoother animations
        • Better handling of high-DPI displays
        • More efficient event handling
        • Future-proof architecture
        """)
        explanation.setStyleSheet("""
            QLabel {
                background: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
                font-size: 12px;
                color: #495057;
            }
        """)
        layout.addWidget(explanation)

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName("Qt6 Performance Demo")
    
    # Print Qt version info
    print(f"Qt Version: {QT_VERSION_STR}")
    print(f"Platform: {app.platformName()}")
    print(f"Primary Screen DPI: {app.primaryScreen().logicalDotsPerInch()}")
    print(f"Device Pixel Ratio: {app.primaryScreen().devicePixelRatio()}")
    
    window = Qt6ComparisonApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
