import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QTextEdit, QSlider, QProgressBar, QCheckBox, 
                             QRadioButton, QButtonGroup, QComboBox, QSpinBox,
                             QMessageBox, QFileDialog, QMenuBar, QStatusBar,
                             QGroupBox, QTabWidget)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QFont, QIcon
import os

class DemoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Qt6 Demo Application")
        self.setGeometry(100, 100, 800, 600)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_basic_controls_tab()
        self.create_text_tab()
        self.create_interactive_tab()
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        open_action = QAction('Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_basic_controls_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Title
        title = QLabel("Basic Controls")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Input section
        input_group = QGroupBox("Input Controls")
        input_layout = QVBoxLayout(input_group)
        
        # Text input
        input_layout.addWidget(QLabel("Text Input:"))
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter some text here...")
        self.text_input.textChanged.connect(self.on_text_changed)
        input_layout.addWidget(self.text_input)
        
        # Combo box
        input_layout.addWidget(QLabel("Dropdown:"))
        self.combo = QComboBox()
        self.combo.addItems(["Option 1", "Option 2", "Option 3", "Custom Option"])
        self.combo.currentTextChanged.connect(self.on_combo_changed)
        input_layout.addWidget(self.combo)
        
        # Spin box
        spin_layout = QHBoxLayout()
        spin_layout.addWidget(QLabel("Number:"))
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.setValue(50)
        self.spin_box.valueChanged.connect(self.on_spin_changed)
        spin_layout.addWidget(self.spin_box)
        input_layout.addLayout(spin_layout)
        
        layout.addWidget(input_group)
        
        # Checkbox and radio buttons
        choice_group = QGroupBox("Choice Controls")
        choice_layout = QVBoxLayout(choice_group)
        
        self.checkbox = QCheckBox("Enable advanced features")
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        choice_layout.addWidget(self.checkbox)
        
        # Radio buttons
        choice_layout.addWidget(QLabel("Select mode:"))
        self.radio_group = QButtonGroup()
        
        self.radio1 = QRadioButton("Beginner")
        self.radio2 = QRadioButton("Intermediate")
        self.radio3 = QRadioButton("Advanced")
        
        self.radio_group.addButton(self.radio1, 1)
        self.radio_group.addButton(self.radio2, 2)
        self.radio_group.addButton(self.radio3, 3)
        
        self.radio1.setChecked(True)
        self.radio_group.buttonClicked.connect(self.on_radio_changed)
        
        choice_layout.addWidget(self.radio1)
        choice_layout.addWidget(self.radio2)
        choice_layout.addWidget(self.radio3)
        
        layout.addWidget(choice_group)
        
        self.tab_widget.addTab(tab, "Basic Controls")
        
    def create_text_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Title
        title = QLabel("Text Editor")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Text editor
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Enter your text here...\n\nThis is a multi-line text editor.")
        layout.addWidget(self.text_edit)
        
        # Buttons for text operations
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Clear Text")
        clear_btn.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_btn)
        
        sample_btn = QPushButton("Insert Sample Text")
        sample_btn.clicked.connect(self.insert_sample_text)
        button_layout.addWidget(sample_btn)
        
        word_count_btn = QPushButton("Word Count")
        word_count_btn.clicked.connect(self.show_word_count)
        button_layout.addWidget(word_count_btn)
        
        layout.addLayout(button_layout)
        
        self.tab_widget.addTab(tab, "Text Editor")
        
    def create_interactive_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Title
        title = QLabel("Interactive Elements")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Slider and progress bar
        slider_group = QGroupBox("Slider & Progress")
        slider_layout = QVBoxLayout(slider_group)
        
        slider_layout.addWidget(QLabel("Adjust the slider:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.on_slider_changed)
        slider_layout.addWidget(self.slider)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(30)
        slider_layout.addWidget(self.progress_bar)
        
        self.slider_label = QLabel("Value: 30")
        slider_layout.addWidget(self.slider_label)
        
        layout.addWidget(slider_group)
        
        # Action buttons
        button_group = QGroupBox("Actions")
        button_layout = QVBoxLayout(button_group)
        
        # Timer demo
        timer_layout = QHBoxLayout()
        self.timer_btn = QPushButton("Start Timer Demo")
        self.timer_btn.clicked.connect(self.toggle_timer)
        timer_layout.addWidget(self.timer_btn)
        
        self.timer_label = QLabel("Timer: Stopped")
        timer_layout.addWidget(self.timer_label)
        button_layout.addLayout(timer_layout)
        
        # Message box demo
        msg_btn = QPushButton("Show Message Box")
        msg_btn.clicked.connect(self.show_message_box)
        button_layout.addWidget(msg_btn)
        
        # File dialog demo
        file_btn = QPushButton("Open File Dialog")
        file_btn.clicked.connect(self.show_file_dialog)
        button_layout.addWidget(file_btn)
        
        layout.addWidget(button_group)
        
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_count = 0
        self.timer_running = False
        
        self.tab_widget.addTab(tab, "Interactive")
        
    # Event handlers
    def on_text_changed(self, text):
        self.status_bar.showMessage(f"Text changed: {len(text)} characters")
        
    def on_combo_changed(self, text):
        self.status_bar.showMessage(f"Selected: {text}")
        
    def on_spin_changed(self, value):
        self.status_bar.showMessage(f"Number changed to: {value}")
        
    def on_checkbox_changed(self, state):
        status = "enabled" if state == Qt.CheckState.Checked else "disabled"
        self.status_bar.showMessage(f"Advanced features {status}")
        
    def on_radio_changed(self, button):
        mode = button.text()
        self.status_bar.showMessage(f"Mode changed to: {mode}")
        
    def on_slider_changed(self, value):
        self.progress_bar.setValue(value)
        self.slider_label.setText(f"Value: {value}")
        self.status_bar.showMessage(f"Slider value: {value}")
        
    def clear_text(self):
        self.text_edit.clear()
        self.status_bar.showMessage("Text cleared")
        
    def insert_sample_text(self):
        sample = """This is sample text for the Qt6 demo application.

This application demonstrates various Qt6 widgets including:
- Text input and editing
- Buttons and interactive controls
- Sliders and progress bars
- Menus and dialogs
- Tabs and groupboxes

Qt6 is a powerful framework for creating cross-platform desktop applications with Python!"""
        self.text_edit.setPlainText(sample)
        self.status_bar.showMessage("Sample text inserted")
        
    def show_word_count(self):
        text = self.text_edit.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        QMessageBox.information(self, "Word Count", 
                               f"Words: {words}\nCharacters: {chars}")
        
    def toggle_timer(self):
        if not self.timer_running:
            self.timer.start(1000)  # 1 second interval
            self.timer_btn.setText("Stop Timer Demo")
            self.timer_running = True
            self.timer_count = 0
        else:
            self.timer.stop()
            self.timer_btn.setText("Start Timer Demo")
            self.timer_running = False
            self.timer_label.setText("Timer: Stopped")
            
    def update_timer(self):
        self.timer_count += 1
        self.timer_label.setText(f"Timer: {self.timer_count} seconds")
        
    def show_message_box(self):
        reply = QMessageBox.question(self, "Demo Message", 
                                   "This is a demo message box.\n\nDo you like Qt6?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Great!", "Excellent choice! Qt6 is awesome!")
        else:
            QMessageBox.information(self, "That's OK", "Maybe you'll like it more as you use it!")
            
    def show_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
                                                  "Text Files (*.txt);;Python Files (*.py);;All Files (*)")
        if file_path:
            self.status_bar.showMessage(f"Selected file: {os.path.basename(file_path)}")
            QMessageBox.information(self, "File Selected", f"You selected:\n{file_path}")
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", 
                                                  "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                self.status_bar.showMessage(f"Opened: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file:\n{str(e)}")
                
    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", 
                                                  "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                self.status_bar.showMessage(f"Saved: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
                
    def show_about(self):
        QMessageBox.about(self, "About Qt6 Demo", 
                         "Qt6 Demo Application\n\n"
                         "This is a simple demonstration of Qt6 capabilities with Python.\n\n"
                         "Features demonstrated:\n"
                         "• Basic input controls\n"
                         "• Text editing\n"
                         "• Interactive elements\n"
                         "• Menus and dialogs\n"
                         "• Timers and events\n\n"
                         "Built with PyQt6")

def main():
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Qt6 Demo")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Demo Company")
    
    # Create and show main window
    window = DemoApp()
    window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main()