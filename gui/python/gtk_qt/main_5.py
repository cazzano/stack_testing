#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import os
import subprocess

class HyprlandSPADemo(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hyprland GTK3 SPA Demo")
        self.set_default_size(800, 600)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Main container
        main_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_container)
        
        # Create navbar
        self.create_navbar(main_container)
        
        # Create main content area with stack
        self.content_stack = Gtk.Stack()
        self.content_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.content_stack.set_transition_duration(300)
        
        # Create different pages
        self.create_home_page()
        self.create_controls_page()
        self.create_system_page()
        self.create_settings_page()
        
        main_container.pack_start(self.content_stack, True, True, 0)
        
        # Status bar
        self.status_bar = Gtk.Statusbar()
        self.status_context = self.status_bar.get_context_id("main")
        self.status_bar.push(self.status_context, "Welcome to GTK3 SPA Demo! 🚀")
        main_container.pack_end(self.status_bar, False, False, 0)
        
        # Connect window close event
        self.connect("destroy", Gtk.main_quit)
        
        # Set initial page
        self.content_stack.set_visible_child_name("home")
        
    def create_navbar(self, parent):
        """Create the navigation bar"""
        navbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        navbar.get_style_context().add_class("navbar")
        
        # App title/logo
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        title_box.set_margin_left(15)
        title_box.set_margin_right(15)
        
        app_icon = Gtk.Label(label="🚀")
        app_title = Gtk.Label()
        app_title.set_markup("<b>Hyprland Demo</b>")
        
        title_box.pack_start(app_icon, False, False, 0)
        title_box.pack_start(app_title, False, False, 0)
        navbar.pack_start(title_box, False, False, 0)
        
        # Navigation buttons
        nav_buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        nav_buttons_box.set_halign(Gtk.Align.CENTER)
        nav_buttons_box.set_hexpand(True)
        
        # Create nav buttons
        nav_items = [
            ("🏠 Home", "home"),
            ("🎮 Controls", "controls"),
            ("💻 System", "system"),
            ("⚙️ Settings", "settings")
        ]
        
        self.nav_buttons = {}
        for label, page_name in nav_items:
            btn = Gtk.Button(label=label)
            btn.get_style_context().add_class("nav-button")
            btn.connect("clicked", self.on_nav_clicked, page_name)
            nav_buttons_box.pack_start(btn, False, False, 0)
            self.nav_buttons[page_name] = btn
            
        navbar.pack_start(nav_buttons_box, True, True, 0)
        
        # User info (placeholder)
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        user_box.set_margin_left(15)
        user_box.set_margin_right(15)
        
        user_label = Gtk.Label(label="👤 User")
        user_box.pack_start(user_label, False, False, 0)
        navbar.pack_end(user_box, False, False, 0)
        
        parent.pack_start(navbar, False, False, 0)
        
    def create_home_page(self):
        """Create the home page"""
        page = Gtk.ScrolledWindow()
        page.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content.set_margin_left(40)
        content.set_margin_right(40)
        content.set_margin_top(30)
        content.set_margin_bottom(30)
        
        # Hero section
        hero_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        hero_box.set_halign(Gtk.Align.CENTER)
        
        hero_title = Gtk.Label()
        hero_title.set_markup("<span size='xx-large' weight='bold'>Welcome to Hyprland! 🎉</span>")
        hero_title.set_halign(Gtk.Align.CENTER)
        
        hero_subtitle = Gtk.Label()
        hero_subtitle.set_markup("<span size='large'>A modern GTK3 demonstration application</span>")
        hero_subtitle.set_halign(Gtk.Align.CENTER)
        hero_subtitle.get_style_context().add_class("subtitle")
        
        hero_box.pack_start(hero_title, False, False, 0)
        hero_box.pack_start(hero_subtitle, False, False, 0)
        content.pack_start(hero_box, False, False, 0)
        
        # Feature cards
        cards_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        cards_box.set_halign(Gtk.Align.CENTER)
        
        features = [
            ("🎮", "Interactive Controls", "Buttons, sliders, and more"),
            ("💻", "System Information", "Real-time system data"),
            ("⚙️", "Customizable Settings", "Personalize your experience")
        ]
        
        for icon, title, desc in features:
            card = self.create_feature_card(icon, title, desc)
            cards_box.pack_start(card, False, False, 0)
            
        content.pack_start(cards_box, False, False, 0)
        
        # Quick stats
        stats_frame = Gtk.Frame(label="Quick Stats")
        stats_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)
        stats_box.set_margin_left(20)
        stats_box.set_margin_right(20)
        stats_box.set_margin_top(15)
        stats_box.set_margin_bottom(15)
        stats_box.set_halign(Gtk.Align.CENTER)
        
        session = os.environ.get('XDG_CURRENT_DESKTOP', 'Unknown')
        compositor = os.environ.get('XDG_SESSION_TYPE', 'Unknown')
        
        stats_items = [
            ("🖥️", "Desktop", session),
            ("🎨", "Session", compositor),
            ("🐧", "OS", "Linux")
        ]
        
        for icon, label, value in stats_items:
            stat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
            stat_box.set_halign(Gtk.Align.CENTER)
            
            stat_icon = Gtk.Label(label=icon)
            stat_icon.get_style_context().add_class("stat-icon")
            
            stat_label = Gtk.Label()
            stat_label.set_markup(f"<b>{label}</b>")
            
            stat_value = Gtk.Label(label=value)
            stat_value.get_style_context().add_class("stat-value")
            
            stat_box.pack_start(stat_icon, False, False, 0)
            stat_box.pack_start(stat_label, False, False, 0)
            stat_box.pack_start(stat_value, False, False, 0)
            
            stats_box.pack_start(stat_box, False, False, 0)
            
        stats_frame.add(stats_box)
        content.pack_start(stats_frame, False, False, 0)
        
        page.add(content)
        self.content_stack.add_named(page, "home")
        
    def create_feature_card(self, icon, title, description):
        """Create a feature card widget"""
        card = Gtk.Frame()
        card.get_style_context().add_class("feature-card")
        card.set_size_request(180, 120)
        
        card_content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        card_content.set_margin_left(15)
        card_content.set_margin_right(15)
        card_content.set_margin_top(15)
        card_content.set_margin_bottom(15)
        card_content.set_halign(Gtk.Align.CENTER)
        
        icon_label = Gtk.Label(label=icon)
        icon_label.get_style_context().add_class("card-icon")
        
        title_label = Gtk.Label()
        title_label.set_markup(f"<b>{title}</b>")
        title_label.set_halign(Gtk.Align.CENTER)
        
        desc_label = Gtk.Label(label=description)
        desc_label.set_halign(Gtk.Align.CENTER)
        desc_label.set_line_wrap(True)
        desc_label.set_max_width_chars(20)
        desc_label.get_style_context().add_class("card-desc")
        
        card_content.pack_start(icon_label, False, False, 0)
        card_content.pack_start(title_label, False, False, 0)
        card_content.pack_start(desc_label, True, True, 0)
        
        card.add(card_content)
        return card
        
    def create_controls_page(self):
        """Create the controls page"""
        page = Gtk.ScrolledWindow()
        page.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content.set_margin_left(40)
        content.set_margin_right(40)
        content.set_margin_top(30)
        content.set_margin_bottom(30)
        
        # Page header
        header = Gtk.Label()
        header.set_markup("<span size='x-large' weight='bold'>🎮 Interactive Controls</span>")
        header.set_halign(Gtk.Align.CENTER)
        content.pack_start(header, False, False, 0)
        
        # Action buttons section
        actions_frame = Gtk.Frame(label="Actions")
        actions_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        actions_box.set_margin_left(20)
        actions_box.set_margin_right(20)
        actions_box.set_margin_top(15)
        actions_box.set_margin_bottom(15)
        
        # Button row
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        button_box.set_halign(Gtk.Align.CENTER)
        
        notify_btn = Gtk.Button(label="📢 Send Notification")
        notify_btn.connect("clicked", self.on_notify_clicked)
        button_box.pack_start(notify_btn, False, False, 0)
        
        screenshot_btn = Gtk.Button(label="📸 Screenshot")
        screenshot_btn.connect("clicked", self.on_screenshot_clicked)
        button_box.pack_start(screenshot_btn, False, False, 0)
        
        actions_box.pack_start(button_box, False, False, 0)
        actions_frame.add(actions_box)
        content.pack_start(actions_frame, False, False, 0)
        
        # Text input section
        input_frame = Gtk.Frame(label="Text Input")
        input_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        input_box.set_margin_left(20)
        input_box.set_margin_right(20)
        input_box.set_margin_top(15)
        input_box.set_margin_bottom(15)
        
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        entry_label = Gtk.Label(label="💬 Type something:")
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Hello Hyprland!")
        self.entry.connect("activate", self.on_entry_activate)
        
        entry_box.pack_start(entry_label, False, False, 0)
        entry_box.pack_start(self.entry, True, True, 0)
        input_box.pack_start(entry_box, False, False, 0)
        
        self.output_label = Gtk.Label(label="Your text will appear here...")
        self.output_label.set_halign(Gtk.Align.START)
        self.output_label.set_line_wrap(True)
        input_box.pack_start(self.output_label, False, False, 0)
        
        input_frame.add(input_box)
        content.pack_start(input_frame, False, False, 0)
        
        # Opacity control
        opacity_frame = Gtk.Frame(label="Window Opacity")
        opacity_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
        opacity_box.set_margin_left(20)
        opacity_box.set_margin_right(20)
        opacity_box.set_margin_top(15)
        opacity_box.set_margin_bottom(15)
        
        opacity_label = Gtk.Label(label="🔍 Opacity:")
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.1, 1.0, 0.1)
        self.scale.set_value(1.0)
        self.scale.connect("value-changed", self.on_scale_changed)
        self.scale.set_draw_value(True)
        
        opacity_box.pack_start(opacity_label, False, False, 0)
        opacity_box.pack_start(self.scale, True, True, 0)
        opacity_frame.add(opacity_box)
        content.pack_start(opacity_frame, False, False, 0)
        
        page.add(content)
        self.content_stack.add_named(page, "controls")
        
    def create_system_page(self):
        """Create the system information page"""
        page = Gtk.ScrolledWindow()
        page.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content.set_margin_left(40)
        content.set_margin_right(40)
        content.set_margin_top(30)
        content.set_margin_bottom(30)
        
        # Page header
        header = Gtk.Label()
        header.set_markup("<span size='x-large' weight='bold'>💻 System Information</span>")
        header.set_halign(Gtk.Align.CENTER)
        content.pack_start(header, False, False, 0)
        
        # Environment info
        env_frame = Gtk.Frame(label="Environment")
        env_grid = Gtk.Grid()
        env_grid.set_margin_left(20)
        env_grid.set_margin_right(20)
        env_grid.set_margin_top(15)
        env_grid.set_margin_bottom(15)
        env_grid.set_row_spacing(10)
        env_grid.set_column_spacing(20)
        
        env_vars = [
            ("Desktop Session", os.environ.get('XDG_CURRENT_DESKTOP', 'Unknown')),
            ("Session Type", os.environ.get('XDG_SESSION_TYPE', 'Unknown')),
            ("Display", os.environ.get('DISPLAY', 'Unknown')),
            ("Wayland Display", os.environ.get('WAYLAND_DISPLAY', 'Not set')),
            ("User", os.environ.get('USER', 'Unknown')),
            ("Home", os.environ.get('HOME', 'Unknown'))
        ]
        
        for i, (key, value) in enumerate(env_vars):
            key_label = Gtk.Label()
            key_label.set_markup(f"<b>{key}:</b>")
            key_label.set_halign(Gtk.Align.START)
            
            value_label = Gtk.Label(label=value)
            value_label.set_halign(Gtk.Align.START)
            value_label.set_selectable(True)
            
            env_grid.attach(key_label, 0, i, 1, 1)
            env_grid.attach(value_label, 1, i, 1, 1)
            
        env_frame.add(env_grid)
        content.pack_start(env_frame, False, False, 0)
        
        # GTK info
        gtk_frame = Gtk.Frame(label="GTK Information")
        gtk_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        gtk_box.set_margin_left(20)
        gtk_box.set_margin_right(20)
        gtk_box.set_margin_top(15)
        gtk_box.set_margin_bottom(15)
        
        gtk_version = f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}"
        
        gtk_info = [
            f"GTK Version: {gtk_version}",
            f"Backend: {Gdk.Display.get_default().get_name() if Gdk.Display.get_default() else 'Unknown'}",
            "Theme: Default GTK3 Theme"
        ]
        
        for info in gtk_info:
            label = Gtk.Label(label=info)
            label.set_halign(Gtk.Align.START)
            gtk_box.pack_start(label, False, False, 0)
            
        gtk_frame.add(gtk_box)
        content.pack_start(gtk_frame, False, False, 0)
        
        page.add(content)
        self.content_stack.add_named(page, "system")
        
    def create_settings_page(self):
        """Create the settings page"""
        page = Gtk.ScrolledWindow()
        page.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content.set_margin_left(40)
        content.set_margin_right(40)
        content.set_margin_top(30)
        content.set_margin_bottom(30)
        
        # Page header
        header = Gtk.Label()
        header.set_markup("<span size='x-large' weight='bold'>⚙️ Settings</span>")
        header.set_halign(Gtk.Align.CENTER)
        content.pack_start(header, False, False, 0)
        
        # Appearance settings
        appearance_frame = Gtk.Frame(label="Appearance")
        appearance_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        appearance_box.set_margin_left(20)
        appearance_box.set_margin_right(20)
        appearance_box.set_margin_top(15)
        appearance_box.set_margin_bottom(15)
        
        # Theme selector
        theme_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        theme_label = Gtk.Label(label="🎨 Theme:")
        theme_combo = Gtk.ComboBoxText()
        theme_combo.append_text("Dark")
        theme_combo.append_text("Light")
        theme_combo.append_text("Auto")
        theme_combo.set_active(0)
        
        theme_box.pack_start(theme_label, False, False, 0)
        theme_box.pack_start(theme_combo, False, False, 0)
        appearance_box.pack_start(theme_box, False, False, 0)
        
        # Font size
        font_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        font_label = Gtk.Label(label="📝 Font Size:")
        font_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 8, 18, 1)
        font_scale.set_value(10)
        font_scale.set_draw_value(True)
        
        font_box.pack_start(font_label, False, False, 0)
        font_box.pack_start(font_scale, True, True, 0)
        appearance_box.pack_start(font_box, False, False, 0)
        
        appearance_frame.add(appearance_box)
        content.pack_start(appearance_frame, False, False, 0)
        
        # Application settings
        app_frame = Gtk.Frame(label="Application")
        app_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        app_box.set_margin_left(20)
        app_box.set_margin_right(20)
        app_box.set_margin_top(15)
        app_box.set_margin_bottom(15)
        
        # Checkboxes
        settings_items = [
            "🔄 Auto-refresh system info",
            "🔔 Enable notifications",
            "💾 Remember window position",
            "🎯 Show tooltips"
        ]
        
        for item in settings_items:
            checkbox = Gtk.CheckButton(label=item)
            checkbox.set_active(True)
            app_box.pack_start(checkbox, False, False, 0)
            
        app_frame.add(app_box)
        content.pack_start(app_frame, False, False, 0)
        
        # About section
        about_frame = Gtk.Frame(label="About")
        about_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        about_box.set_margin_left(20)
        about_box.set_margin_right(20)
        about_box.set_margin_top(15)
        about_box.set_margin_bottom(15)
        
        about_text = """This is a demonstration GTK3 application designed for Hyprland.
Built with Python and GTK3, showcasing native Linux desktop integration.

Version: 1.0.0
License: Open Source"""
        
        about_label = Gtk.Label(label=about_text)
        about_label.set_line_wrap(True)
        about_label.set_halign(Gtk.Align.START)
        
        about_box.pack_start(about_label, False, False, 0)
        about_frame.add(about_box)
        content.pack_start(about_frame, False, False, 0)
        
        page.add(content)
        self.content_stack.add_named(page, "settings")
        
    def on_nav_clicked(self, button, page_name):
        """Handle navigation button clicks"""
        self.content_stack.set_visible_child_name(page_name)
        self.update_status(f"Navigated to {page_name.title()} page")
        
        # Update button states
        for name, btn in self.nav_buttons.items():
            if name == page_name:
                btn.get_style_context().add_class("active")
            else:
                btn.get_style_context().remove_class("active")
                
    def on_notify_clicked(self, button):
        """Send a desktop notification"""
        try:
            subprocess.run([
                "notify-send", 
                "GTK3 SPA Demo", 
                "Hello from your Hyprland GTK3 SPA! 🚀"
            ], check=True)
            self.update_status("Notification sent!")
        except subprocess.CalledProcessError:
            self.update_status("Failed to send notification (is notify-send installed?)")
        except FileNotFoundError:
            self.update_status("notify-send not found. Install libnotify.")
            
    def on_screenshot_clicked(self, button):
        """Take a screenshot using grim (common on Hyprland)"""
        try:
            result = subprocess.run([
                "grim", 
                f"/tmp/hyprland-spa-demo-{subprocess.check_output(['date', '+%s']).decode().strip()}.png"
            ], check=True, capture_output=True, text=True)
            self.update_status("Screenshot saved to /tmp/")
        except subprocess.CalledProcessError:
            try:
                # Fallback to scrot if grim isn't available
                subprocess.run([
                    "scrot", 
                    f"/tmp/spa-demo-{subprocess.check_output(['date', '+%s']).decode().strip()}.png"
                ], check=True)
                self.update_status("Screenshot saved to /tmp/ (using scrot)")
            except:
                self.update_status("Screenshot failed (install grim or scrot)")
        except FileNotFoundError:
            self.update_status("Screenshot tool not found (install grim or scrot)")
            
    def on_entry_activate(self, entry):
        """Handle Enter key in text entry"""
        text = entry.get_text()
        if text:
            self.output_label.set_markup(f"<i>You typed:</i> <b>{text}</b>")
            self.update_status(f"Text updated: {text}")
        else:
            self.output_label.set_text("Type something first!")
            
    def on_scale_changed(self, scale):
        """Handle opacity slider changes"""
        opacity = scale.get_value()
        self.set_opacity(opacity)
        self.update_status(f"Window opacity: {opacity:.1f}")
        
    def update_status(self, message):
        """Update the status bar"""
        self.status_bar.pop(self.status_context)
        self.status_bar.push(self.status_context, message)

def main():
    app = HyprlandSPADemo()
    app.show_all()
    
    # Set initial active nav button
    app.nav_buttons["home"].get_style_context().add_class("active")
    
    # Apply custom CSS styling
    css_provider = Gtk.CssProvider()
    css_data = """
    /* Main window styling */
    window {
        background-color: #1a1a2e;
        color: #eee;
    }
    
    /* Navbar styling */
    .navbar {
        background: linear-gradient(to right, #16213e, #0f3460);
        border-bottom: 2px solid #0e6ba8;
        padding: 10px 0;
    }
    
    /* Navigation buttons */
    .nav-button {
        background: transparent;
        border: none;
        color: #fff;
        padding: 8px 16px;
        margin: 0 2px;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .nav-button:hover {
        background-color: rgba(255, 255, 255, 0.1);
    }
    
    .nav-button.active {
        background: linear-gradient(to bottom, #4299e1, #3182ce);
        border: 1px solid #2b77cb;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Frame styling */
    frame {
        background-color: #16213e;
        border: 1px solid #4a5568;
        border-radius: 8px;
        margin: 5px;
    }
    
    frame > label {
        color: #63b3ed;
        font-weight: bold;
        margin: 0 10px;
        padding: 0 5px;
    }
    
    /* Feature cards */
    .feature-card {
        background: linear-gradient(135deg, #16213e, #1a1a2e);
        border: 1px solid #4299e1;
        border-radius: 12px;
        margin: 10px;
    }
    
    .feature-card:hover {
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
    }
    
    .card-icon {
        font-size: 2em;
    }
    
    .card-desc {
        color: #a0aec0;
        font-size: 0.9em;
    }
    
    /* Buttons */
    button {
        background: linear-gradient(to bottom, #4299e1, #3182ce);
        border: 1px solid #2b77cb;
        border-radius: 6px;
        color: white;
        padding: 10px 20px;
        font-weight: bold;
    }
    
    button:hover {
        background: linear-gradient(to bottom, #63b3ed, #4299e1);
        box-shadow: 0 2px 8px rgba(66, 153, 225, 0.4);
    }
    
    /* Entry fields */
    entry {
        background-color: #2d3748;
        color: #e2e8f0;
        border: 1px solid #4a5568;
        border-radius: 6px;
        padding: 8px 12px;
    }
    
    entry:focus {
        border-color: #4299e1;
        box-shadow: 0 0 0 2px rgba(66, 153, 225, 0.3);
    }
    
    /* Scale/slider */
    scale {
        background-color: #2d3748;
    }
    
    scale trough {
        background-color: #4a5568;
        border-radius: 3px;
        min-height: 6px;
    }
    
    scale slider {
        background: linear-gradient(to bottom, #4299e1, #3182ce);
        border: 1px solid #2b77cb;
        border-radius: 50%;
        min-width: 18px;
        min-height: 18px;
    }
    
    scale slider:hover {
        background: linear-gradient(to bottom, #63b3ed, #4299e1);
    }
    
    /* Checkboxes */
    checkbutton {
        color: #e2e8f0;
    }
    
    checkbutton check {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 3px;
    }
    
    checkbutton check:checked {
        background: linear-gradient(to bottom, #4299e1, #3182ce);
        border-color: #2b77cb;
    }
    
    /* ComboBox */
    combobox {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 6px;
    }
    
    combobox button {
        background-color: transparent;
        border: none;
        color: #e2e8f0;
    }
    
    /* Status bar */
    statusbar {
        background-color: #16213e;
        border-top: 1px solid #4a5568;
        color: #a0aec0;
        padding: 5px 10px;
    }
    
    /* Grid */
    grid {
        background-color: transparent;
    }
    
    /* Scrolled window */
    scrolledwindow {
        background-color: #1a1a2e;
    }
    
    /* Labels */
    .subtitle {
        color: #a0aec0;
    }
    
    .stat-icon {
        font-size: 1.5em;
    }
    
    .stat-value {
        color: #4299e1;
        font-weight: bold;
    }
    
    /* Stack transition */
    stack {
        background-color: #1a1a2e;
    }
    """
    
    css_provider.load_from_data(css_data.encode())
    screen = Gdk.Screen.get_default()
    style_context = Gtk.StyleContext()
    style_context.add_provider_for_screen(
        screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )
    
    try:
        Gtk.main()
    except KeyboardInterrupt:
        print("\nExiting gracefully...")
        Gtk.main_quit()

if __name__ == "__main__":
    main()
