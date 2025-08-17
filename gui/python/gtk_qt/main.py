#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Gdk', '4.0')
from gi.repository import Gtk, Adw, GLib, Gio, Gdk

class ProjectCard(Gtk.Box):
    def __init__(self, title, description, tech_stack, github_url=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.set_margin_top(12)
        self.set_margin_bottom(12)
        self.set_margin_start(16)
        self.set_margin_end(16)
        
        # Add card styling
        self.add_css_class("card")
        
        # Project title
        title_label = Gtk.Label(label=title)
        title_label.add_css_class("title-3")
        title_label.set_halign(Gtk.Align.START)
        self.append(title_label)
        
        # Description
        desc_label = Gtk.Label(label=description)
        desc_label.set_wrap(True)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_xalign(0)
        self.append(desc_label)
        
        # Tech stack
        tech_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        tech_box.set_margin_top(8)
        
        for tech in tech_stack:
            pill = Gtk.Label(label=tech)
            pill.add_css_class("pill")
            pill.set_margin_end(4)
            tech_box.append(pill)
        
        self.append(tech_box)
        
        # GitHub button if URL provided
        if github_url:
            btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            btn_box.set_halign(Gtk.Align.END)
            btn_box.set_margin_top(8)
            
            github_btn = Gtk.Button(label="View on GitHub")
            github_btn.add_css_class("suggested-action")
            github_btn.connect("clicked", lambda x: print(f"Opening: {github_url}"))
            btn_box.append(github_btn)
            
            self.append(btn_box)

class SkillBar(Gtk.Box):
    def __init__(self, skill_name, level):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        self.set_margin_bottom(8)
        
        # Skill name and level
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        header_box.set_margin_start(8)
        header_box.set_margin_end(8)
        
        skill_label = Gtk.Label(label=skill_name)
        skill_label.set_halign(Gtk.Align.START)
        header_box.append(skill_label)
        
        level_label = Gtk.Label(label=f"{level}%")
        level_label.set_halign(Gtk.Align.END)
        level_label.set_hexpand(True)
        level_label.add_css_class("dim-label")
        header_box.append(level_label)
        
        self.append(header_box)
        
        # Progress bar
        progress = Gtk.ProgressBar()
        progress.set_fraction(level / 100.0)
        progress.set_margin_start(8)
        progress.set_margin_end(8)
        self.append(progress)

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Window properties
        self.set_default_size(800, 600)
        self.set_title("Portfolio - Your Name")
        
        # Create header bar with menu button
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        
        # Theme toggle button
        theme_btn = Gtk.Button()
        theme_btn.set_icon_name("weather-clear-night-symbolic")
        theme_btn.connect("clicked", self.toggle_theme)
        theme_btn.set_tooltip_text("Toggle Dark Mode")
        self.header.pack_end(theme_btn)
        
        # Create main scrolled window
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        self.set_child(scrolled)
        
        # Main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        main_box.set_margin_top(24)
        main_box.set_margin_bottom(24)
        main_box.set_margin_start(48)
        main_box.set_margin_end(48)
        scrolled.set_child(main_box)
        
        # Hero section
        self.create_hero_section(main_box)
        
        # About section
        self.create_about_section(main_box)
        
        # Skills section
        self.create_skills_section(main_box)
        
        # Projects section
        self.create_projects_section(main_box)
        
        # Contact section
        self.create_contact_section(main_box)
        
        self.dark_mode = False
    
    def create_hero_section(self, parent):
        hero_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        hero_box.set_halign(Gtk.Align.CENTER)
        
        # Name
        name_label = Gtk.Label(label="John Developer")
        name_label.add_css_class("title-1")
        hero_box.append(name_label)
        
        # Title
        title_label = Gtk.Label(label="Full-Stack Developer & Linux Enthusiast")
        title_label.add_css_class("title-3")
        title_label.add_css_class("dim-label")
        hero_box.append(title_label)
        
        # Tagline
        tagline = Gtk.Label(label="Building awesome applications with modern technologies\nArch Linux • Hyprland • Python • Web Development")
        tagline.set_justify(Gtk.Justification.CENTER)
        tagline.set_margin_top(16)
        hero_box.append(tagline)
        
        parent.append(hero_box)
    
    def create_about_section(self, parent):
        about_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        # Section title
        about_title = Gtk.Label(label="About Me")
        about_title.add_css_class("title-2")
        about_title.set_halign(Gtk.Align.START)
        about_box.append(about_title)
        
        # About text
        about_text = """I'm a passionate developer who loves creating efficient and beautiful applications. 
I use Arch Linux with Hyprland as my daily driver and enjoy working with modern technologies 
like Python, JavaScript, and various frameworks. When I'm not coding, you can find me 
contributing to open-source projects or exploring new technologies."""
        
        about_label = Gtk.Label(label=about_text)
        about_label.set_wrap(True)
        about_label.set_xalign(0)
        about_label.set_margin_start(16)
        about_box.append(about_label)
        
        parent.append(about_box)
    
    def create_skills_section(self, parent):
        skills_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        # Section title
        skills_title = Gtk.Label(label="Skills")
        skills_title.add_css_class("title-2")
        skills_title.set_halign(Gtk.Align.START)
        skills_box.append(skills_title)
        
        # Skills container
        skills_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        skills_container.add_css_class("card")
        skills_container.set_margin_start(16)
        
        # Sample skills
        skills_data = [
            ("Python", 90),
            ("JavaScript", 85),
            ("GTK4/PyGObject", 80),
            ("Linux/Bash", 95),
            ("Git", 88),
            ("HTML/CSS", 92),
            ("React", 75),
            ("Docker", 70)
        ]
        
        for skill, level in skills_data:
            skill_bar = SkillBar(skill, level)
            skills_container.append(skill_bar)
        
        skills_box.append(skills_container)
        parent.append(skills_box)
    
    def create_projects_section(self, parent):
        projects_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        # Section title
        projects_title = Gtk.Label(label="Projects")
        projects_title.add_css_class("title-2")
        projects_title.set_halign(Gtk.Align.START)
        projects_box.append(projects_title)
        
        # Projects container
        projects_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        projects_container.set_margin_start(16)
        
        # Sample projects
        projects_data = [
            {
                "title": "Hyprland Config Manager",
                "description": "A GTK4 application for managing Hyprland window manager configurations with a beautiful GUI interface.",
                "tech_stack": ["Python", "GTK4", "JSON", "Linux"],
                "github_url": "https://github.com/user/hyprland-config"
            },
            {
                "title": "System Monitor Dashboard",
                "description": "Real-time system monitoring dashboard built with Python and modern web technologies.",
                "tech_stack": ["Python", "Flask", "JavaScript", "Chart.js"],
                "github_url": "https://github.com/user/sys-monitor"
            },
            {
                "title": "Arch Package Helper",
                "description": "Command-line tool to help manage Arch Linux packages with AUR integration and dependency tracking.",
                "tech_stack": ["Python", "Click", "SQLite", "AUR API"],
                "github_url": "https://github.com/user/arch-helper"
            }
        ]
        
        for project in projects_data:
            card = ProjectCard(
                project["title"],
                project["description"],
                project["tech_stack"],
                project.get("github_url")
            )
            projects_container.append(card)
        
        projects_box.append(projects_container)
        parent.append(projects_box)
    
    def create_contact_section(self, parent):
        contact_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        
        # Section title
        contact_title = Gtk.Label(label="Get In Touch")
        contact_title.add_css_class("title-2")
        contact_title.set_halign(Gtk.Align.START)
        contact_box.append(contact_title)
        
        # Contact info
        contact_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        contact_container.add_css_class("card")
        contact_container.set_margin_start(16)
        
        contacts = [
            "📧 john.developer@email.com",
            "🐙 github.com/johndeveloper",
            "💼 linkedin.com/in/johndeveloper",
            "🌐 johndeveloper.dev"
        ]
        
        for contact in contacts:
            contact_label = Gtk.Label(label=contact)
            contact_label.set_halign(Gtk.Align.START)
            contact_label.set_margin_top(8)
            contact_label.set_margin_bottom(8)
            contact_label.set_margin_start(16)
            contact_container.append(contact_label)
        
        contact_box.append(contact_container)
        parent.append(contact_box)
    
    def toggle_theme(self, button):
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            button.set_icon_name("weather-clear-symbolic")
        else:
            Adw.StyleManager.get_default().set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            button.set_icon_name("weather-clear-night-symbolic")

class PortfolioApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        
        # Add custom CSS
        self.setup_css()
    
    def setup_css(self):
        css_provider = Gtk.CssProvider()
        css = """
        .pill {
            background-color: alpha(@accent_color, 0.1);
            color: @accent_color;
            border-radius: 12px;
            padding: 4px 8px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .card {
            background-color: alpha(@window_bg_color, 0.05);
            border-radius: 12px;
            border: 1px solid alpha(@borders, 0.5);
        }
        """
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

def main():
    app = PortfolioApp(application_id="com.example.PortfolioApp")
    return app.run()

if __name__ == '__main__':
    main()
