import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QLineEdit, 
                             QTextEdit, QSlider, QProgressBar, QCheckBox, 
                             QRadioButton, QButtonGroup, QComboBox, QSpinBox,
                             QMessageBox, QFileDialog, QStatusBar,
                             QGroupBox, QTabWidget)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
import os

class DemoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.apply_theme()
        
    def init_ui(self):
        self.setWindowTitle("✨ Beautiful Qt6 Demo")
        self.setGeometry(100, 100, 900, 600)
        
        # Menu bar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('📁 File')
        
        open_action = QAction('🔍 Open', self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction('💾 Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("🚀 Ready!")
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Header
        title = QLabel("🎨 Beautiful Qt6 Showcase")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: white; padding: 20px;")
        main_layout.addWidget(title)
        
        # Tabs
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        self.create_controls_tab()
        self.create_text_tab()
        self.create_interactive_tab()
        
    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #1a1a2e, stop:1 #0f3460);
            }
            QTabWidget::pane {
                border: 2px solid #3a3a5c;
                border-radius: 15px;
                background: rgba(255, 255, 255, 0.05);
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #667eea, stop:1 #764ba2);
                color: white;
                padding: 12px 20px;
                margin-right: 3px;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                           stop:0 #7c8df0, stop:1 #8a5aa8);
            }
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                margin-top: 20px;
                padding-top: 15px;
                background: rgba(255, 255, 255, 0.05);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 5px 15px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #667eea, stop:1 #764ba2);
                border-radius: 8px;
                color: white;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #667eea, stop:1 #764ba2);
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 100px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #7c8df0, stop:1 #8a5aa8);
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox {
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus {
                border: 2px solid #667eea;
                background: rgba(255, 255, 255, 0.15);
            }
            QSlider::groove:horizontal {
                border: none;
                height: 8px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #667eea, stop:1 #764ba2);
                border: 2px solid white;
                width: 18px;
                height: 18px;
                margin: -6px 0;
                border-radius: 10px;
            }
            QSlider::sub-page:horizontal {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #667eea, stop:1 #764ba2);
                border-radius: 4px;
            }
            QProgressBar {
                border: none;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                color: white;
                background: rgba(255, 255, 255, 0.1);
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                           stop:0 #667eea, stop:1 #764ba2);
                border-radius: 10px;
            }
            QCheckBox, QRadioButton {
                color: white;
                font-size: 14px;
                padding: 5px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid rgba(255, 255, 255, 0.5);
                background: rgba(255, 255, 255, 0.1);
            }
            QCheckBox::indicator {
                border-radius: 4px;
            }
            QRadioButton::indicator {
                border-radius: 9px;
            }
            QCheckBox::indicator:checked, QRadioButton::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                           stop:0 #667eea, stop:1 #764ba2);
                border: 2px solid white;
            }
            QLabel { color: white; font-size: 14px; }
            QStatusBar {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                font-size: 14px;
                padding: 5px;
            }
            QMenuBar {
                background: rgba(255, 255, 255, 0.1);
                color: white;
                border: none;
                padding: 5px;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QMenuBar::item:selected {
                background: rgba(102, 126, 234, 0.3);
            }
            QMenu {
                background: rgba(26, 26, 46, 0.95);
                border: 2px solid #667eea;
                border-radius: 8px;
                color: white;
                padding: 5px;
            }
            QMenu::item {
                padding: 8px 15px;
                border-radius: 4px;
            }
            QMenu::item:selected {
                background: #667eea;
            }
        """)
        
    def create_controls_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Input group
        input_group = QGroupBox("🎛️ Input Controls")
        input_layout = QVBoxLayout(input_group)
        
        input_layout.addWidget(QLabel("✍️ Text Input:"))
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter some text...")
        self.text_input.textChanged.connect(self.on_text_changed)
        input_layout.addWidget(self.text_input)
        
        input_layout.addWidget(QLabel("📋 Dropdown:"))
        self.combo = QComboBox()
        self.combo.addItems(["🌟 Option 1", "🎨 Option 2", "🚀 Option 3"])
        self.combo.currentTextChanged.connect(self.on_combo_changed)
        input_layout.addWidget(self.combo)
        
        spin_layout = QHBoxLayout()
        spin_layout.addWidget(QLabel("🔢 Number:"))
        self.spin_box = QSpinBox()
        self.spin_box.setRange(0, 100)
        self.spin_box.setValue(42)
        self.spin_box.valueChanged.connect(self.on_spin_changed)
        spin_layout.addWidget(self.spin_box)
        input_layout.addLayout(spin_layout)
        
        layout.addWidget(input_group)
        
        # Choice group
        choice_group = QGroupBox("⚡ Choices")
        choice_layout = QVBoxLayout(choice_group)
        
        self.checkbox = QCheckBox("🎯 Enable Features")
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        choice_layout.addWidget(self.checkbox)
        
        self.radio_group = QButtonGroup()
        self.radio1 = QRadioButton("🌱 Beginner")
        self.radio2 = QRadioButton("⚡ Intermediate")
        self.radio3 = QRadioButton("🔥 Advanced")
        
        self.radio_group.addButton(self.radio1, 1)
        self.radio_group.addButton(self.radio2, 2)
        self.radio_group.addButton(self.radio3, 3)
        self.radio2.setChecked(True)
        self.radio_group.buttonClicked.connect(self.on_radio_changed)
        
        choice_layout.addWidget(self.radio1)
        choice_layout.addWidget(self.radio2)
        choice_layout.addWidget(self.radio3)
        
        layout.addWidget(choice_group)
        self.tab_widget.addTab(tab, "🎛️ Controls")
        
    def create_text_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        editor_group = QGroupBox("📝 Text Editor")
        editor_layout = QVBoxLayout(editor_group)
        
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("✨ Start writing something amazing...")
        editor_layout.addWidget(self.text_edit)
        
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("🗑️ Clear")
        clear_btn.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_btn)
        
        sample_btn = QPushButton("✨ Sample")
        sample_btn.clicked.connect(self.insert_sample_text)
        button_layout.addWidget(sample_btn)
        
        word_count_btn = QPushButton("📊 Count")
        word_count_btn.clicked.connect(self.show_word_count)
        button_layout.addWidget(word_count_btn)
        
        editor_layout.addLayout(button_layout)
        layout.addWidget(editor_group)
        
        self.tab_widget.addTab(tab, "📝 Editor")
        
    def create_interactive_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(20, 20, 20, 20)
        
        slider_group = QGroupBox("🎚️ Slider & Progress")
        slider_layout = QVBoxLayout(slider_group)
        
        slider_layout.addWidget(QLabel("🎯 Drag the slider:"))
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.slider.valueChanged.connect(self.on_slider_changed)
        slider_layout.addWidget(self.slider)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(50)
        slider_layout.addWidget(self.progress_bar)
        
        self.slider_label = QLabel("✨ Value: 50%")
        self.slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        slider_layout.addWidget(self.slider_label)
        
        layout.addWidget(slider_group)
        
        action_group = QGroupBox("🚀 Actions")
        action_layout = QVBoxLayout(action_group)
        
        timer_layout = QHBoxLayout()
        self.timer_btn = QPushButton("⏰ Start Timer")
        self.timer_btn.clicked.connect(self.toggle_timer)
        timer_layout.addWidget(self.timer_btn)
        
        self.timer_label = QLabel("⏸️ Timer: Stopped")
        timer_layout.addWidget(self.timer_label)
        action_layout.addLayout(timer_layout)
        
        button_row = QHBoxLayout()
        
        msg_btn = QPushButton("💬 Message")
        msg_btn.clicked.connect(self.show_message_box)
        button_row.addWidget(msg_btn)
        
        file_btn = QPushButton("📂 Browse")
        file_btn.clicked.connect(self.show_file_dialog)
        button_row.addWidget(file_btn)
        
        action_layout.addLayout(button_row)
        layout.addWidget(action_group)
        
        # Timer setup
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_count = 0
        self.timer_running = False
        
        self.tab_widget.addTab(tab, "🚀 Interactive")
        
    # Event handlers
    def on_text_changed(self, text):
        self.status_bar.showMessage(f"✍️ {len(text)} characters")
        
    def on_combo_changed(self, text):
        self.status_bar.showMessage(f"🎯 Selected: {text}")
        
    def on_spin_changed(self, value):
        self.status_bar.showMessage(f"🔢 Number: {value}")
        
    def on_checkbox_changed(self, state):
        status = "enabled" if state == Qt.CheckState.Checked else "disabled"
        self.status_bar.showMessage(f"⚡ Features {status}")
        
    def on_radio_changed(self, button):
        self.status_bar.showMessage(f"🎮 Level: {button.text()}")
        
    def on_slider_changed(self, value):
        self.progress_bar.setValue(value)
        emoji = "😴" if value < 25 else "😊" if value < 50 else "🔥" if value < 75 else "✨"
        self.slider_label.setText(f"{emoji} Value: {value}%")
        self.status_bar.showMessage(f"🎚️ Power: {value}%")
        
    def clear_text(self):
        self.text_edit.clear()
        self.status_bar.showMessage("🗑️ Text cleared!")
        
    def insert_sample_text(self):
        sample = """🎨 Welcome to Beautiful Qt6! ✨

This app showcases modern UI design with:
• Glassmorphic backgrounds
• Smooth gradients  
• Interactive controls
• Beautiful animations

Built with PyQt6 and lots of love! 💖"""
        self.text_edit.setPlainText(sample)
        self.status_bar.showMessage("✨ Sample text inserted!")
        
    def show_word_count(self):
        text = self.text_edit.toPlainText()
        words = len(text.split()) if text.strip() else 0
        chars = len(text)
        QMessageBox.information(self, "📊 Stats", f"Words: {words}\nCharacters: {chars}")
        
    def toggle_timer(self):
        if not self.timer_running:
            self.timer.start(1000)
            self.timer_btn.setText("⏹️ Stop")
            self.timer_running = True
            self.timer_count = 0
        else:
            self.timer.stop()
            self.timer_btn.setText("⏰ Start Timer")
            self.timer_running = False
            self.timer_label.setText("⏸️ Timer: Stopped")
            
    def update_timer(self):
        self.timer_count += 1
        self.timer_label.setText(f"⏰ Timer: {self.timer_count}s")
        
    def show_message_box(self):
        reply = QMessageBox.question(self, "✨ Message", 
                                   "Do you love this beautiful design?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "🎉 Great!", "Awesome! Thanks for the love! 💖")
        else:
            QMessageBox.information(self, "💭 OK", "That's fine! Beauty is subjective! 😊")
            
    def show_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "🔍 Choose File", "", 
                                                  "Text Files (*.txt);;All Files (*)")
        if file_path:
            filename = os.path.basename(file_path)
            self.status_bar.showMessage(f"📂 Selected: {filename}")
            QMessageBox.information(self, "📂 File", f"Selected:\n{filename}")
        
    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "🔍 Open File", "", 
                                                  "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_edit.setPlainText(content)
                filename = os.path.basename(file_path)
                self.status_bar.showMessage(f"📖 Opened: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "❌ Error", f"Could not open file:\n{str(e)}")
                
    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "💾 Save File", "", 
                                                  "Text Files (*.txt);;All Files (*)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.text_edit.toPlainText())
                filename = os.path.basename(file_path)
                self.status_bar.showMessage(f"💾 Saved: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "❌ Error", f"Could not save file:\n{str(e)}")

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Beautiful Qt6 Demo")
    app.setApplicationVersion("1.0")
    
    window = DemoApp()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main()