#!/usr/bin/env python3
"""
Hyprland Qt6 Demo Application
Demonstrates Hyprland/Wayland integration features
"""

import sys
import json
import subprocess
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QTextEdit, 
                             QListWidget, QTabWidget, QGroupBox, QSlider,
                             QCheckBox, QComboBox, QSpinBox, QProgressBar)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor

class HyprlandAPI:
    """Interface to Hyprland IPC"""
    
    @staticmethod
    def run_hyprctl(command):
        """Execute hyprctl command and return output"""
        try:
            result = subprocess.run(['hyprctl', '-j'] + command.split(), 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return json.loads(result.stdout)
            return None
        except (subprocess.SubprocessError, json.JSONDecodeError, FileNotFoundError):
            return None
    
    @staticmethod
    def get_windows():
        """Get list of all windows"""
        return HyprlandAPI.run_hyprctl('clients') or []
    
    @staticmethod
    def get_workspaces():
        """Get list of workspaces"""
        return HyprlandAPI.run_hyprctl('workspaces') or []
    
    @staticmethod
    def get_monitors():
        """Get monitor information"""
        return HyprlandAPI.run_hyprctl('monitors') or []
    
    @staticmethod
    def dispatch(command):
        """Send dispatch command to Hyprland"""
        try:
            subprocess.run(['hyprctl', 'dispatch'] + command.split(), 
                          capture_output=True)
            return True
        except subprocess.SubprocessError:
            return False

    @staticmethod
    def is_hyprland_running():
        """Check if running under Hyprland"""
        return os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') is not None

class WorkspaceWidget(QWidget):
    """Widget for workspace management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Workspace list
        self.workspace_list = QListWidget()
        layout.addWidget(QLabel("Active Workspaces:"))
        layout.addWidget(self.workspace_list)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.switch_btn = QPushButton("Switch to Workspace")
        self.switch_btn.clicked.connect(self.switch_workspace)
        controls_layout.addWidget(self.switch_btn)
        
        self.new_workspace_spin = QSpinBox()
        self.new_workspace_spin.setRange(1, 10)
        self.new_workspace_btn = QPushButton("Create Workspace")
        self.new_workspace_btn.clicked.connect(self.create_workspace)
        controls_layout.addWidget(QLabel("ID:"))
        controls_layout.addWidget(self.new_workspace_spin)
        controls_layout.addWidget(self.new_workspace_btn)
        
        layout.addLayout(controls_layout)
        self.setLayout(layout)
        
    def update_workspaces(self):
        """Update workspace list"""
        self.workspace_list.clear()
        workspaces = HyprlandAPI.get_workspaces()
        
        for ws in workspaces:
            ws_id = ws.get('id', 'Unknown')
            ws_name = ws.get('name', f'Workspace {ws_id}')
            windows_count = ws.get('windows', 0)
            item_text = f"ID: {ws_id} | {ws_name} | Windows: {windows_count}"
            self.workspace_list.addItem(item_text)
    
    def switch_workspace(self):
        """Switch to selected workspace"""
        current_item = self.workspace_list.currentItem()
        if current_item:
            # Extract workspace ID from the item text
            text = current_item.text()
            ws_id = text.split('|')[0].replace('ID:', '').strip()
            HyprlandAPI.dispatch(f'workspace {ws_id}')
    
    def create_workspace(self):
        """Create and switch to new workspace"""
        ws_id = self.new_workspace_spin.value()
        HyprlandAPI.dispatch(f'workspace {ws_id}')

class WindowWidget(QWidget):
    """Widget for window management"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Window list
        self.window_list = QListWidget()
        layout.addWidget(QLabel("Open Windows:"))
        layout.addWidget(self.window_list)
        
        # Window controls
        controls_layout = QHBoxLayout()
        
        self.focus_btn = QPushButton("Focus Window")
        self.focus_btn.clicked.connect(self.focus_window)
        controls_layout.addWidget(self.focus_btn)
        
        self.close_btn = QPushButton("Close Window")
        self.close_btn.clicked.connect(self.close_window)
        controls_layout.addWidget(self.close_btn)
        
        self.fullscreen_btn = QPushButton("Toggle Fullscreen")
        self.fullscreen_btn.clicked.connect(self.toggle_fullscreen)
        controls_layout.addWidget(self.fullscreen_btn)
        
        layout.addLayout(controls_layout)
        
        # Move to workspace
        move_layout = QHBoxLayout()
        self.move_workspace_spin = QSpinBox()
        self.move_workspace_spin.setRange(1, 10)
        self.move_btn = QPushButton("Move to Workspace")
        self.move_btn.clicked.connect(self.move_to_workspace)
        
        move_layout.addWidget(QLabel("Move to workspace:"))
        move_layout.addWidget(self.move_workspace_spin)
        move_layout.addWidget(self.move_btn)
        layout.addLayout(move_layout)
        
        self.setLayout(layout)
        
    def update_windows(self):
        """Update window list"""
        self.window_list.clear()
        windows = HyprlandAPI.get_windows()
        
        for window in windows:
            title = window.get('title', 'Untitled')
            app_class = window.get('class', 'Unknown')
            workspace = window.get('workspace', {}).get('name', 'Unknown')
            address = window.get('address', '')
            
            item_text = f"{app_class} | {title} | WS: {workspace}"
            self.window_list.addItem(item_text)
            # Store address for later use - Qt6 compatible method
            item = self.window_list.item(self.window_list.count() - 1)
            item.setData(Qt.ItemDataRole.UserRole, address)
    
    def get_selected_window_address(self):
        """Get address of selected window"""
        current_item = self.window_list.currentItem()
        if current_item:
            return current_item.data(Qt.ItemDataRole.UserRole)
        return None
    
    def focus_window(self):
        """Focus selected window"""
        address = self.get_selected_window_address()
        if address:
            HyprlandAPI.dispatch(f'focuswindow address:{address}')
    
    def close_window(self):
        """Close selected window"""
        address = self.get_selected_window_address()
        if address:
            HyprlandAPI.dispatch(f'closewindow address:{address}')
    
    def toggle_fullscreen(self):
        """Toggle fullscreen for selected window"""
        address = self.get_selected_window_address()
        if address:
            HyprlandAPI.dispatch(f'fullscreen address:{address}')
    
    def move_to_workspace(self):
        """Move selected window to workspace"""
        address = self.get_selected_window_address()
        workspace = self.move_workspace_spin.value()
        if address:
            HyprlandAPI.dispatch(f'movetoworkspace {workspace},address:{address}')

class MonitorWidget(QWidget):
    """Widget for monitor information"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        self.monitor_info = QTextEdit()
        self.monitor_info.setReadOnly(True)
        layout.addWidget(QLabel("Monitor Information:"))
        layout.addWidget(self.monitor_info)
        
        self.setLayout(layout)
        
    def update_monitors(self):
        """Update monitor information"""
        monitors = HyprlandAPI.get_monitors()
        
        info_text = ""
        for monitor in monitors:
            name = monitor.get('name', 'Unknown')
            width = monitor.get('width', 0)
            height = monitor.get('height', 0)
            refresh = monitor.get('refreshRate', 0)
            scale = monitor.get('scale', 1.0)
            focused = monitor.get('focused', False)
            
            info_text += f"Monitor: {name}\n"
            info_text += f"Resolution: {width}x{height}@{refresh}Hz\n"
            info_text += f"Scale: {scale}x\n"
            info_text += f"Focused: {'Yes' if focused else 'No'}\n"
            info_text += "-" * 30 + "\n"
        
        self.monitor_info.setPlainText(info_text)

class HyprlandDemoApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        self.setWindowTitle("Hyprland Qt6 Demo")
        self.setGeometry(100, 100, 800, 600)
        
        # Check if running under Hyprland
        if not HyprlandAPI.is_hyprland_running():
            self.show_not_hyprland_warning()
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Status label
        self.status_label = QLabel("Hyprland Integration Demo")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.status_label.setFont(font)
        layout.addWidget(self.status_label)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Add tabs
        self.workspace_widget = WorkspaceWidget()
        self.window_widget = WindowWidget()
        self.monitor_widget = MonitorWidget()
        
        self.tab_widget.addTab(self.workspace_widget, "Workspaces")
        self.tab_widget.addTab(self.window_widget, "Windows")
        self.tab_widget.addTab(self.monitor_widget, "Monitors")
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("Refresh All")
        self.refresh_btn.clicked.connect(self.refresh_all)
        controls_layout.addWidget(self.refresh_btn)
        
        self.auto_refresh_cb = QCheckBox("Auto Refresh")
        self.auto_refresh_cb.setChecked(True)
        controls_layout.addWidget(self.auto_refresh_cb)
        
        layout.addLayout(controls_layout)
        
        # Apply dark theme
        self.apply_dark_theme()
        
        # Initial refresh
        self.refresh_all()
    
    def show_not_hyprland_warning(self):
        """Show warning if not running under Hyprland"""
        self.status_label = QLabel("⚠️ Not running under Hyprland - Limited functionality")
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")
    
    def apply_dark_theme(self):
        """Apply dark theme to the application"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(dark_palette)
    
    def setup_timer(self):
        """Setup auto-refresh timer"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(2000)  # Refresh every 2 seconds
    
    def auto_refresh(self):
        """Auto refresh if enabled"""
        if self.auto_refresh_cb.isChecked():
            self.refresh_all()
    
    def refresh_all(self):
        """Refresh all widgets"""
        self.workspace_widget.update_workspaces()
        self.window_widget.update_windows()
        self.monitor_widget.update_monitors()

def main():
    # Set up for Wayland
    os.environ['QT_QPA_PLATFORM'] = 'wayland'
    
    app = QApplication(sys.argv)
    app.setApplicationName("Hyprland Qt6 Demo")
    app.setApplicationVersion("1.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    window = HyprlandDemoApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
