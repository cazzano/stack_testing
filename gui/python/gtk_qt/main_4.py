#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk
import os
import subprocess

class HyprlandDemoApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Hyprland GTK3 Demo")
        self.set_default_size(600, 400)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Set up the main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        main_box.set_margin_left(20)
        main_box.set_margin_right(20)
        main_box.set_margin_top(20)
        main_box.set_margin_bottom(20)
        self.add(main_box)
        
        # Header
        header = Gtk.Label()
        header.set_markup("<span size='large' weight='bold'>🚀 Hyprland GTK3 Demo App</span>")
        header.set_halign(Gtk.Align.CENTER)
        main_box.pack_start(header, False, False, 0)
        
        # Info section
        info_frame = Gtk.Frame(label="System Info")
        info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        info_box.set_margin_left(10)
        info_box.set_margin_right(10)
        info_box.set_margin_top(10)
        info_box.set_margin_bottom(10)
        
        # Display current compositor
        compositor_label = Gtk.Label()
        compositor_label.set_markup("<b>Compositor:</b> Hyprland (hopefully! 😄)")
        compositor_label.set_halign(Gtk.Align.START)
        info_box.pack_start(compositor_label, False, False, 0)
        
        # Display current desktop session
        session_label = Gtk.Label()
        session = os.environ.get('XDG_CURRENT_DESKTOP', 'Unknown')
        session_label.set_markup(f"<b>Desktop Session:</b> {session}")
        session_label.set_halign(Gtk.Align.START)
        info_box.pack_start(session_label, False, False, 0)
        
        info_frame.add(info_box)
        main_box.pack_start(info_frame, False, False, 0)
        
        # Interactive elements
        controls_frame = Gtk.Frame(label="Controls")
        controls_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        controls_box.set_margin_left(10)
        controls_box.set_margin_right(10)
        controls_box.set_margin_top(10)
        controls_box.set_margin_bottom(10)
        
        # Button row
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        button_box.set_halign(Gtk.Align.CENTER)
        
        # Notification button
        notify_btn = Gtk.Button(label="Send Notification")
        notify_btn.connect("clicked", self.on_notify_clicked)
        button_box.pack_start(notify_btn, False, False, 0)
        
        # Screenshot button
        screenshot_btn = Gtk.Button(label="Screenshot")
        screenshot_btn.connect("clicked", self.on_screenshot_clicked)
        button_box.pack_start(screenshot_btn, False, False, 0)
        
        controls_box.pack_start(button_box, False, False, 0)
        
        # Entry and label
        entry_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        entry_label = Gtk.Label(label="Type something:")
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Hello Hyprland!")
        self.entry.connect("activate", self.on_entry_activate)
        
        entry_box.pack_start(entry_label, False, False, 0)
        entry_box.pack_start(self.entry, True, True, 0)
        controls_box.pack_start(entry_box, False, False, 0)
        
        # Output label
        self.output_label = Gtk.Label(label="Your text will appear here...")
        self.output_label.set_halign(Gtk.Align.START)
        self.output_label.set_line_wrap(True)
        controls_box.pack_start(self.output_label, False, False, 0)
        
        # Scale/slider
        scale_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        scale_label = Gtk.Label(label="Opacity:")
        self.scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0.1, 1.0, 0.1)
        self.scale.set_value(1.0)
        self.scale.connect("value-changed", self.on_scale_changed)
        
        scale_box.pack_start(scale_label, False, False, 0)
        scale_box.pack_start(self.scale, True, True, 0)
        controls_box.pack_start(scale_box, False, False, 0)
        
        controls_frame.add(controls_box)
        main_box.pack_start(controls_frame, True, True, 0)
        
        # Status bar
        self.status_bar = Gtk.Statusbar()
        self.status_context = self.status_bar.get_context_id("main")
        self.status_bar.push(self.status_context, "Ready! Welcome to your GTK3 app on Hyprland 🎉")
        main_box.pack_end(self.status_bar, False, False, 0)
        
        # Connect window close event
        self.connect("destroy", Gtk.main_quit)
        
    def on_notify_clicked(self, button):
        """Send a desktop notification"""
        try:
            subprocess.run([
                "notify-send", 
                "GTK3 Demo", 
                "Hello from your Hyprland GTK3 app! 🚀"
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
                f"/tmp/hyprland-gtk-demo-{subprocess.check_output(['date', '+%s']).decode().strip()}.png"
            ], check=True, capture_output=True, text=True)
            self.update_status("Screenshot saved to /tmp/")
        except subprocess.CalledProcessError:
            try:
                # Fallback to scrot if grim isn't available
                subprocess.run([
                    "scrot", 
                    f"/tmp/gtk-demo-{subprocess.check_output(['date', '+%s']).decode().strip()}.png"
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
    app = HyprlandDemoApp()
    app.show_all()
    
    # Set some nice styling
    css_provider = Gtk.CssProvider()
    css_data = """
    window {
        background-color: #2d3748;
        color: #e2e8f0;
    }
    
    frame {
        border: 1px solid #4a5568;
        border-radius: 6px;
    }
    
    button {
        background: linear-gradient(to bottom, #4299e1, #3182ce);
        border: 1px solid #2b77cb;
        border-radius: 4px;
        color: white;
        padding: 8px 16px;
    }
    
    button:hover {
        background: linear-gradient(to bottom, #63b3ed, #4299e1);
    }
    
    entry {
        background-color: #4a5568;
        color: #e2e8f0;
        border: 1px solid #718096;
        border-radius: 4px;
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
