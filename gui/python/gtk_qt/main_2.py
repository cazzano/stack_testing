#!/usr/bin/env python3
"""
GTK4 Single Page Application with Hyprland Integration
A demonstration of modern GTK4 app architecture with native Wayland/Hyprland support
"""

import gi
import os
import subprocess
import json
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Adw, Gdk, GLib, Gio


class HyprlandIntegration:
    """Handle Hyprland-specific functionality"""
    
    @staticmethod
    def is_hyprland():
        """Check if running under Hyprland"""
        return os.environ.get('HYPRLAND_INSTANCE_SIGNATURE') is not None
    
    @staticmethod
    def get_hyprland_info():
        """Get current Hyprland workspace and window info"""
        if not HyprlandIntegration.is_hyprland():
            return None
            
        try:
            # Get active workspace
            result = subprocess.run(['hyprctl', 'activeworkspace', '-j'], 
                                  capture_output=True, text=True, check=True)
            workspace_info = json.loads(result.stdout)
            
            # Get monitors info
            result = subprocess.run(['hyprctl', 'monitors', '-j'], 
                                  capture_output=True, text=True, check=True)
            monitors_info = json.loads(result.stdout)
            
            return {
                'workspace': workspace_info,
                'monitors': monitors_info
            }
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
            return None
    
    @staticmethod
    def switch_workspace(workspace_id):
        """Switch to a specific workspace in Hyprland"""
        if not HyprlandIntegration.is_hyprland():
            return False
            
        try:
            subprocess.run(['hyprctl', 'dispatch', 'workspace', str(workspace_id)], 
                          check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False


class NavigationPage(Gtk.Box):
    """Base class for SPA pages"""
    
    def __init__(self, title, **kwargs):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, **kwargs)
        self.title = title
        self.setup_ui()
    
    def setup_ui(self):
        """Override in subclasses"""
        pass
    
    def on_show(self):
        """Called when page becomes active"""
        pass
    
    def on_hide(self):
        """Called when page becomes inactive"""
        pass


class HomePage(NavigationPage):
    """Home page with Hyprland status"""
    
    def setup_ui(self):
        header = Gtk.Label(label="Welcome to GTK4 SPA")
        header.add_css_class("title-1")
        self.append(header)
        
        # Hyprland status section
        if HyprlandIntegration.is_hyprland():
            hypr_frame = Gtk.Frame(label="Hyprland Status")
            hypr_frame.set_margin_top(20)
            
            self.status_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            self.status_box.set_margin_start(10)
            self.status_box.set_margin_end(10)
            self.status_box.set_margin_top(10)
            self.status_box.set_margin_bottom(10)
            
            hypr_frame.set_child(self.status_box)
            self.append(hypr_frame)
            
            # Add refresh button
            refresh_btn = Gtk.Button(label="Refresh Hyprland Info")
            refresh_btn.connect("clicked", self.refresh_hyprland_info)
            refresh_btn.set_margin_top(10)
            self.append(refresh_btn)
            
            self.refresh_hyprland_info()
        else:
            no_hypr_label = Gtk.Label(label="Not running under Hyprland")
            no_hypr_label.add_css_class("dim-label")
            no_hypr_label.set_margin_top(20)
            self.append(no_hypr_label)
    
    def refresh_hyprland_info(self, widget=None):
        """Update Hyprland status information"""
        # Clear existing status
        child = self.status_box.get_first_child()
        while child:
            next_child = child.get_next_sibling()
            self.status_box.remove(child)
            child = next_child
        
        hypr_info = HyprlandIntegration.get_hyprland_info()
        if hypr_info:
            # Workspace info
            ws_info = hypr_info['workspace']
            ws_label = Gtk.Label(label=f"Active Workspace: {ws_info.get('name', 'Unknown')}")
            ws_label.set_halign(Gtk.Align.START)
            self.status_box.append(ws_label)
            
            # Monitor info
            monitors = hypr_info['monitors']
            mon_label = Gtk.Label(label=f"Monitors: {len(monitors)} connected")
            mon_label.set_halign(Gtk.Align.START)
            self.status_box.append(mon_label)
            
            for monitor in monitors:
                if monitor.get('focused'):
                    focused_label = Gtk.Label(label=f"Focused Monitor: {monitor.get('name', 'Unknown')}")
                    focused_label.set_halign(Gtk.Align.START)
                    self.status_box.append(focused_label)
                    break
        else:
            error_label = Gtk.Label(label="Failed to get Hyprland information")
            error_label.add_css_class("error")
            self.status_box.append(error_label)


class SettingsPage(NavigationPage):
    """Settings page with window controls"""
    
    def setup_ui(self):
        header = Gtk.Label(label="Application Settings")
        header.add_css_class("title-1")
        self.append(header)
        
        # Theme selection
        theme_frame = Gtk.Frame(label="Appearance")
        theme_frame.set_margin_top(20)
        
        theme_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        theme_box.set_margin_start(10)
        theme_box.set_margin_end(10)
        theme_box.set_margin_top(10)
        theme_box.set_margin_bottom(10)
        
        # Theme switcher
        theme_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        theme_label = Gtk.Label(label="Color Scheme:")
        theme_label.set_halign(Gtk.Align.START)
        
        theme_dropdown = Gtk.DropDown()
        theme_model = Gtk.StringList()
        theme_model.append("Follow System")
        theme_model.append("Light")
        theme_model.append("Dark")
        theme_dropdown.set_model(theme_model)
        theme_dropdown.connect("notify::selected", self.on_theme_changed)
        
        theme_row.append(theme_label)
        theme_row.append(theme_dropdown)
        theme_box.append(theme_row)
        
        theme_frame.set_child(theme_box)
        self.append(theme_frame)
        
        # Window controls (Hyprland specific)
        if HyprlandIntegration.is_hyprland():
            window_frame = Gtk.Frame(label="Window Controls")
            window_frame.set_margin_top(20)
            
            window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            window_box.set_margin_start(10)
            window_box.set_margin_end(10)
            window_box.set_margin_top(10)
            window_box.set_margin_bottom(10)
            
            # Workspace switcher
            ws_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            ws_label = Gtk.Label(label="Switch Workspace:")
            
            for i in range(1, 6):  # Workspaces 1-5
                ws_btn = Gtk.Button(label=str(i))
                ws_btn.connect("clicked", self.switch_workspace, i)
                ws_row.append(ws_btn)
            
            window_box.append(Gtk.Label(label="Quick Workspace Switch:"))
            window_box.append(ws_row)
            
            window_frame.set_child(window_box)
            self.append(window_frame)
    
    def on_theme_changed(self, dropdown, pspec):
        """Handle theme change"""
        selected = dropdown.get_selected()
        style_manager = Adw.StyleManager.get_default()
        
        if selected == 0:  # Follow System
            style_manager.set_color_scheme(Adw.ColorScheme.DEFAULT)
        elif selected == 1:  # Light
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        elif selected == 2:  # Dark
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
    
    def switch_workspace(self, button, workspace_id):
        """Switch to workspace using Hyprland"""
        if HyprlandIntegration.switch_workspace(workspace_id):
            print(f"Switched to workspace {workspace_id}")
        else:
            print(f"Failed to switch to workspace {workspace_id}")


class AboutPage(NavigationPage):
    """About page with app information"""
    
    def setup_ui(self):
        header = Gtk.Label(label="About This App")
        header.add_css_class("title-1")
        self.append(header)
        
        info_text = """This is a demonstration of a GTK4 Single Page Application with native Hyprland support.

Features:
• Modern GTK4/Libadwaita UI
• SPA navigation pattern
• Native Wayland integration
• Hyprland workspace management
• Adaptive theming
• Responsive design

Built with Python and GTK4."""
        
        info_label = Gtk.Label(label=info_text)
        info_label.set_wrap(True)
        info_label.set_halign(Gtk.Align.START)
        info_label.set_margin_top(20)
        self.append(info_label)
        
        # System info
        sys_frame = Gtk.Frame(label="System Information")
        sys_frame.set_margin_top(20)
        
        sys_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        sys_box.set_margin_start(10)
        sys_box.set_margin_end(10)
        sys_box.set_margin_top(10)
        sys_box.set_margin_bottom(10)
        
        # Display server
        display_server = os.environ.get('XDG_SESSION_TYPE', 'Unknown')
        display_label = Gtk.Label(label=f"Display Server: {display_server}")
        display_label.set_halign(Gtk.Align.START)
        sys_box.append(display_label)
        
        # Desktop environment
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', 'Unknown')
        desktop_label = Gtk.Label(label=f"Desktop: {desktop}")
        desktop_label.set_halign(Gtk.Align.START)
        sys_box.append(desktop_label)
        
        # Hyprland status
        hypr_status = "Yes" if HyprlandIntegration.is_hyprland() else "No"
        hypr_label = Gtk.Label(label=f"Running under Hyprland: {hypr_status}")
        hypr_label.set_halign(Gtk.Align.START)
        sys_box.append(hypr_label)
        
        sys_frame.set_child(sys_box)
        self.append(sys_frame)


class SPAWindow(Adw.ApplicationWindow):
    """Main application window with SPA navigation"""
    
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("GTK4 SPA - Hyprland Edition")
        self.set_default_size(800, 600)
        
        # Enable native window decorations for better Wayland integration
        self.set_decorated(True)
        
        # Setup pages
        self.pages = {
            'home': HomePage("Home"),
            'settings': SettingsPage("Settings"),
            'about': AboutPage("About")
        }
        self.current_page = None
        
        self.setup_ui()
        self.navigate_to('home')
    
    def setup_ui(self):
        """Setup the main UI structure"""
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # Header bar with navigation
        header_bar = Adw.HeaderBar()
        
        # Navigation buttons in header
        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        nav_box.add_css_class("linked")
        
        self.nav_buttons = {}
        for page_id, page in self.pages.items():
            btn = Gtk.ToggleButton(label=page.title)
            btn.connect("clicked", self.on_nav_clicked, page_id)
            nav_box.append(btn)
            self.nav_buttons[page_id] = btn
        
        header_bar.set_title_widget(nav_box)
        
        # Add menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        
        # Create menu
        menu = Gio.Menu()
        menu.append("Preferences", "app.preferences")
        menu.append("About", "app.about")
        menu.append("Quit", "app.quit")
        
        menu_button.set_menu_model(menu)
        header_bar.pack_end(menu_button)
        
        main_box.append(header_bar)
        
        # Content area with scrolling
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        # Content container
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.set_margin_start(20)
        self.content_box.set_margin_end(20)
        self.content_box.set_margin_top(20)
        self.content_box.set_margin_bottom(20)
        
        scrolled.set_child(self.content_box)
        main_box.append(scrolled)
    
    def on_nav_clicked(self, button, page_id):
        """Handle navigation button clicks"""
        if button.get_active():
            self.navigate_to(page_id)
        else:
            # Prevent deactivating current page
            button.set_active(True)
    
    def navigate_to(self, page_id):
        """Navigate to a specific page"""
        if page_id not in self.pages:
            return
        
        # Hide current page
        if self.current_page:
            self.current_page.on_hide()
            self.content_box.remove(self.current_page)
        
        # Show new page
        new_page = self.pages[page_id]
        self.content_box.append(new_page)
        new_page.on_show()
        self.current_page = new_page
        
        # Update navigation buttons
        for btn_id, btn in self.nav_buttons.items():
            btn.set_active(btn_id == page_id)
        
        # Update window title
        self.set_title(f"GTK4 SPA - {new_page.title}")


class SPAApplication(Adw.Application):
    """Main application class"""
    
    def __init__(self):
        super().__init__(application_id="com.example.gtk4spa")
        self.connect("activate", self.on_activate)
        
        # Setup actions
        self.setup_actions()
    
    def setup_actions(self):
        """Setup application actions"""
        # Quit action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])
        
        # Preferences action
        prefs_action = Gio.SimpleAction.new("preferences", None)
        prefs_action.connect("activate", self.on_preferences)
        self.add_action(prefs_action)
        self.set_accels_for_action("app.preferences", ["<Ctrl>comma"])
        
        # About action
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.add_action(about_action)
    
    def on_activate(self, app):
        """Application activation"""
        self.window = SPAWindow(self)
        self.window.present()
    
    def on_quit(self, action, param):
        """Quit the application"""
        self.quit()
    
    def on_preferences(self, action, param):
        """Show preferences"""
        if hasattr(self, 'window'):
            self.window.navigate_to('settings')
    
    def on_about(self, action, param):
        """Show about page"""
        if hasattr(self, 'window'):
            self.window.navigate_to('about')


def main():
    """Main entry point"""
    # Set up better Wayland integration
    if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
        os.environ['GDK_BACKEND'] = 'wayland'
    
    app = SPAApplication()
    return app.run()


if __name__ == "__main__":
    exit(main())
