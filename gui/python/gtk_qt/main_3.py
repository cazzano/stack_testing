#!/usr/bin/env python3
"""
GTK4 Portfolio Application with Hyprland Integration
A modern portfolio showcase built with GTK4 and native Wayland/Hyprland support
"""

import gi
import os
import subprocess
import json
import webbrowser
from pathlib import Path

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Gdk', '4.0')

from gi.repository import Gtk, Adw, Gdk, GLib, Gio, GdkPixbuf


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
            result = subprocess.run(['hyprctl', 'activeworkspace', '-j'], 
                                  capture_output=True, text=True, check=True)
            workspace_info = json.loads(result.stdout)
            
            result = subprocess.run(['hyprctl', 'monitors', '-j'], 
                                  capture_output=True, text=True, check=True)
            monitors_info = json.loads(result.stdout)
            
            return {
                'workspace': workspace_info,
                'monitors': monitors_info
            }
        except (subprocess.CalledProcessError, json.JSONDecodeError, FileNotFoundError):
            return None


class NavigationPage(Gtk.Box):
    """Base class for portfolio pages"""
    
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


class ProjectCard(Gtk.Box):
    """Individual project card component"""
    
    def __init__(self, project_data):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.project_data = project_data
        self.add_css_class("card")
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        
        self.setup_ui()
    
    def setup_ui(self):
        # Project header
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        header_box.set_margin_start(15)
        header_box.set_margin_end(15)
        header_box.set_margin_top(15)
        
        title_label = Gtk.Label(label=self.project_data['title'])
        title_label.add_css_class("heading")
        title_label.set_halign(Gtk.Align.START)
        title_label.set_hexpand(True)
        
        # Status badge
        status_label = Gtk.Label(label=self.project_data['status'])
        status_label.add_css_class("caption")
        if self.project_data['status'] == 'Active':
            status_label.add_css_class("success")
        elif self.project_data['status'] == 'Completed':
            status_label.add_css_class("accent")
        
        header_box.append(title_label)
        header_box.append(status_label)
        self.append(header_box)
        
        # Description
        desc_label = Gtk.Label(label=self.project_data['description'])
        desc_label.set_wrap(True)
        desc_label.set_halign(Gtk.Align.START)
        desc_label.set_margin_start(15)
        desc_label.set_margin_end(15)
        self.append(desc_label)
        
        # Technologies
        tech_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        tech_box.set_margin_start(15)
        tech_box.set_margin_end(15)
        
        for tech in self.project_data['technologies']:
            tech_pill = Gtk.Label(label=tech)
            tech_pill.add_css_class("pill")
            tech_box.append(tech_pill)
        
        self.append(tech_box)
        
        # Links
        if self.project_data.get('links'):
            links_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            links_box.set_margin_start(15)
            links_box.set_margin_end(15)
            links_box.set_margin_bottom(15)
            
            for link_text, url in self.project_data['links'].items():
                link_btn = Gtk.Button(label=link_text)
                link_btn.add_css_class("suggested-action")
                link_btn.connect("clicked", self.open_link, url)
                links_box.append(link_btn)
            
            self.append(links_box)
    
    def open_link(self, button, url):
        """Open link in browser"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Failed to open link: {e}")


class HomePage(NavigationPage):
    """Home page with personal introduction"""
    
    def setup_ui(self):
        # Hero section
        hero_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        hero_box.set_halign(Gtk.Align.CENTER)
        hero_box.set_margin_top(40)
        hero_box.set_margin_bottom(40)
        
        # Profile picture placeholder
        avatar_box = Gtk.Box()
        avatar_box.set_size_request(120, 120)
        avatar_box.add_css_class("avatar")
        avatar_box.set_halign(Gtk.Align.CENTER)
        hero_box.append(avatar_box)
        
        # Name and title
        name_label = Gtk.Label(label="Your Name")
        name_label.add_css_class("title-1")
        hero_box.append(name_label)
        
        title_label = Gtk.Label(label="Full-Stack Developer & Open Source Enthusiast")
        title_label.add_css_class("title-3")
        title_label.add_css_class("dim-label")
        hero_box.append(title_label)
        
        # Bio
        bio_text = """Passionate developer with expertise in modern web technologies, 
desktop applications, and system administration. I love creating efficient, 
user-friendly solutions and contributing to open source projects."""
        
        bio_label = Gtk.Label(label=bio_text)
        bio_label.set_wrap(True)
        bio_label.set_justify(Gtk.Justification.CENTER)
        bio_label.set_max_width_chars(60)
        hero_box.append(bio_label)
        
        # Contact buttons
        contact_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        contact_box.set_halign(Gtk.Align.CENTER)
        
        github_btn = Gtk.Button(label="GitHub")
        github_btn.add_css_class("suggested-action")
        github_btn.connect("clicked", self.open_link, "https://github.com/yourusername")
        
        linkedin_btn = Gtk.Button(label="LinkedIn")
        linkedin_btn.connect("clicked", self.open_link, "https://linkedin.com/in/yourprofile")
        
        email_btn = Gtk.Button(label="Email")
        email_btn.connect("clicked", self.open_link, "mailto:your.email@example.com")
        
        contact_box.append(github_btn)
        contact_box.append(linkedin_btn)
        contact_box.append(email_btn)
        hero_box.append(contact_box)
        
        self.append(hero_box)
        
        # Skills overview
        skills_frame = Gtk.Frame(label="Core Skills")
        skills_frame.set_margin_top(20)
        
        skills_flow = Gtk.FlowBox()
        skills_flow.set_margin_start(20)
        skills_flow.set_margin_end(20)
        skills_flow.set_margin_top(20)
        skills_flow.set_margin_bottom(20)
        skills_flow.set_max_children_per_line(4)
        skills_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        
        skills = [
            "Python", "JavaScript", "TypeScript", "Rust",
            "React", "Vue.js", "GTK", "Qt",
            "Linux", "Docker", "Kubernetes", "AWS",
            "PostgreSQL", "MongoDB", "Git", "CI/CD"
        ]
        
        for skill in skills:
            skill_label = Gtk.Label(label=skill)
            skill_label.add_css_class("pill")
            skill_label.set_margin_start(5)
            skill_label.set_margin_end(5)
            skill_label.set_margin_top(5)
            skill_label.set_margin_bottom(5)
            skills_flow.append(skill_label)
        
        skills_frame.set_child(skills_flow)
        self.append(skills_frame)
        
        # System info for Hyprland users
        if HyprlandIntegration.is_hyprland():
            hypr_frame = Gtk.Frame(label="Developer Environment")
            hypr_frame.set_margin_top(20)
            
            hypr_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            hypr_box.set_margin_start(15)
            hypr_box.set_margin_end(15)
            hypr_box.set_margin_top(15)
            hypr_box.set_margin_bottom(15)
            
            hypr_info = HyprlandIntegration.get_hyprland_info()
            if hypr_info:
                ws_label = Gtk.Label(label=f"🖥️ Current Workspace: {hypr_info['workspace'].get('name', 'Unknown')}")
                ws_label.set_halign(Gtk.Align.START)
                hypr_box.append(ws_label)
                
                monitors = len(hypr_info['monitors'])
                mon_label = Gtk.Label(label=f"📺 Monitors: {monitors} connected")
                mon_label.set_halign(Gtk.Align.START)
                hypr_box.append(mon_label)
            
            env_label = Gtk.Label(label="🏗️ Built on Hyprland + Wayland")
            env_label.set_halign(Gtk.Align.START)
            hypr_box.append(env_label)
            
            hypr_frame.set_child(hypr_box)
            self.append(hypr_frame)
    
    def open_link(self, button, url):
        """Open link in browser"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Failed to open link: {e}")


class ProjectsPage(NavigationPage):
    """Projects showcase page"""
    
    def setup_ui(self):
        header = Gtk.Label(label="My Projects")
        header.add_css_class("title-1")
        header.set_margin_bottom(20)
        self.append(header)
        
        # Sample project data
        projects = [
            {
                'title': 'Modern Web Dashboard',
                'description': 'A responsive dashboard built with React and TypeScript, featuring real-time data visualization and user management.',
                'status': 'Completed',
                'technologies': ['React', 'TypeScript', 'D3.js', 'Node.js', 'PostgreSQL'],
                'links': {
                    'GitHub': 'https://github.com/yourusername/web-dashboard',
                    'Live Demo': 'https://your-demo.com'
                }
            },
            {
                'title': 'GTK4 Portfolio App',
                'description': 'This very application! A modern portfolio built with GTK4 and Python, featuring Hyprland integration.',
                'status': 'Active',
                'technologies': ['Python', 'GTK4', 'Libadwaita', 'Wayland'],
                'links': {
                    'GitHub': 'https://github.com/yourusername/gtk4-portfolio'
                }
            },
            {
                'title': 'Microservices API',
                'description': 'Scalable microservices architecture built with Rust and deployed on Kubernetes.',
                'status': 'Completed',
                'technologies': ['Rust', 'Docker', 'Kubernetes', 'gRPC', 'MongoDB'],
                'links': {
                    'GitHub': 'https://github.com/yourusername/microservices-api',
                    'Documentation': 'https://your-docs.com'
                }
            },
            {
                'title': 'Machine Learning Pipeline',
                'description': 'End-to-end ML pipeline for predictive analytics with automated model training and deployment.',
                'status': 'Active',
                'technologies': ['Python', 'TensorFlow', 'Apache Airflow', 'AWS', 'FastAPI'],
                'links': {
                    'GitHub': 'https://github.com/yourusername/ml-pipeline'
                }
            },
            {
                'title': 'Open Source Contribution',
                'description': 'Regular contributor to various open source projects, including bug fixes and feature implementations.',
                'status': 'Ongoing',
                'technologies': ['Various', 'Git', 'GitHub Actions'],
                'links': {
                    'GitHub Profile': 'https://github.com/yourusername'
                }
            }
        ]
        
        # Projects grid
        projects_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        
        for project in projects:
            card = ProjectCard(project)
            projects_box.append(card)
        
        self.append(projects_box)


class ExperiencePage(NavigationPage):
    """Experience and skills page"""
    
    def setup_ui(self):
        header = Gtk.Label(label="Experience & Skills")
        header.add_css_class("title-1")
        header.set_margin_bottom(20)
        self.append(header)
        
        # Work experience
        exp_frame = Gtk.Frame(label="Work Experience")
        exp_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        exp_box.set_margin_start(20)
        exp_box.set_margin_end(20)
        exp_box.set_margin_top(20)
        exp_box.set_margin_bottom(20)
        
        experiences = [
            {
                'title': 'Senior Full-Stack Developer',
                'company': 'Tech Company Inc.',
                'period': '2022 - Present',
                'description': 'Led development of microservices architecture, mentored junior developers, and implemented CI/CD pipelines.'
            },
            {
                'title': 'Software Developer',
                'company': 'StartUp Solutions',
                'period': '2020 - 2022',
                'description': 'Developed web applications using React and Node.js, designed database schemas, and optimized application performance.'
            },
            {
                'title': 'Junior Developer',
                'company': 'Digital Agency',
                'period': '2019 - 2020',
                'description': 'Built responsive websites, maintained legacy systems, and collaborated with design teams.'
            }
        ]
        
        for exp in experiences:
            exp_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            exp_card.add_css_class("card")
            exp_card.set_margin_bottom(15)
            
            # Header
            exp_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            exp_header.set_margin_start(15)
            exp_header.set_margin_end(15)
            exp_header.set_margin_top(15)
            
            title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            title_label = Gtk.Label(label=exp['title'])
            title_label.add_css_class("heading")
            title_label.set_halign(Gtk.Align.START)
            
            company_label = Gtk.Label(label=exp['company'])
            company_label.add_css_class("caption")
            company_label.set_halign(Gtk.Align.START)
            
            title_box.append(title_label)
            title_box.append(company_label)
            title_box.set_hexpand(True)
            
            period_label = Gtk.Label(label=exp['period'])
            period_label.add_css_class("caption")
            period_label.add_css_class("dim-label")
            
            exp_header.append(title_box)
            exp_header.append(period_label)
            exp_card.append(exp_header)
            
            # Description
            desc_label = Gtk.Label(label=exp['description'])
            desc_label.set_wrap(True)
            desc_label.set_halign(Gtk.Align.START)
            desc_label.set_margin_start(15)
            desc_label.set_margin_end(15)
            desc_label.set_margin_bottom(15)
            exp_card.append(desc_label)
            
            exp_box.append(exp_card)
        
        exp_frame.set_child(exp_box)
        self.append(exp_frame)
        
        # Skills breakdown
        skills_frame = Gtk.Frame(label="Technical Skills")
        skills_frame.set_margin_top(20)
        
        skills_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        skills_box.set_margin_start(20)
        skills_box.set_margin_end(20)
        skills_box.set_margin_top(20)
        skills_box.set_margin_bottom(20)
        
        skill_categories = {
            'Programming Languages': ['Python', 'JavaScript', 'TypeScript', 'Rust', 'Go', 'C++'],
            'Frontend': ['React', 'Vue.js', 'HTML5', 'CSS3', 'Tailwind CSS', 'GTK', 'Qt'],
            'Backend': ['Node.js', 'FastAPI', 'Django', 'Express.js', 'GraphQL', 'REST APIs'],
            'Databases': ['PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'MySQL'],
            'DevOps & Tools': ['Docker', 'Kubernetes', 'AWS', 'Git', 'Linux', 'CI/CD', 'Nginx']
        }
        
        for category, skills in skill_categories.items():
            cat_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            
            cat_label = Gtk.Label(label=category)
            cat_label.add_css_class("heading")
            cat_label.set_halign(Gtk.Align.START)
            cat_box.append(cat_label)
            
            skills_flow = Gtk.FlowBox()
            skills_flow.set_max_children_per_line(6)
            skills_flow.set_selection_mode(Gtk.SelectionMode.NONE)
            
            for skill in skills:
                skill_label = Gtk.Label(label=skill)
                skill_label.add_css_class("pill")
                skill_label.set_margin_start(3)
                skill_label.set_margin_end(3)
                skill_label.set_margin_top(3)
                skill_label.set_margin_bottom(3)
                skills_flow.append(skill_label)
            
            cat_box.append(skills_flow)
            skills_box.append(cat_box)
        
        skills_frame.set_child(skills_box)
        self.append(skills_frame)


class ContactPage(NavigationPage):
    """Contact and social links page"""
    
    def setup_ui(self):
        header = Gtk.Label(label="Get In Touch")
        header.add_css_class("title-1")
        header.set_margin_bottom(20)
        self.append(header)
        
        # Contact intro
        intro_text = """I'm always interested in new opportunities and collaborations. 
Feel free to reach out if you'd like to discuss a project, job opportunity, 
or just want to connect!"""
        
        intro_label = Gtk.Label(label=intro_text)
        intro_label.set_wrap(True)
        intro_label.set_justify(Gtk.Justification.CENTER)
        intro_label.set_margin_bottom(30)
        self.append(intro_label)
        
        # Contact methods
        contact_frame = Gtk.Frame(label="Contact Information")
        contact_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        contact_box.set_margin_start(20)
        contact_box.set_margin_end(20)
        contact_box.set_margin_top(20)
        contact_box.set_margin_bottom(20)
        
        contacts = [
            ('📧', 'Email', 'your.email@example.com', 'mailto:your.email@example.com'),
            ('🐙', 'GitHub', 'github.com/yourusername', 'https://github.com/yourusername'),
            ('💼', 'LinkedIn', 'linkedin.com/in/yourprofile', 'https://linkedin.com/in/yourprofile'),
            ('🐦', 'Twitter', '@yourusername', 'https://twitter.com/yourusername'),
            ('🌐', 'Website', 'yourwebsite.com', 'https://yourwebsite.com')
        ]
        
        for emoji, label, value, url in contacts:
            contact_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=15)
            contact_row.add_css_class("card")
            contact_row.set_margin_bottom(10)
            
            emoji_label = Gtk.Label(label=emoji)
            emoji_label.set_size_request(40, -1)
            emoji_label.set_margin_start(15)
            emoji_label.set_margin_top(15)
            emoji_label.set_margin_bottom(15)
            
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            info_box.set_hexpand(True)
            info_box.set_margin_top(15)
            info_box.set_margin_bottom(15)
            
            label_widget = Gtk.Label(label=label)
            label_widget.add_css_class("heading")
            label_widget.set_halign(Gtk.Align.START)
            
            value_label = Gtk.Label(label=value)
            value_label.add_css_class("caption")
            value_label.set_halign(Gtk.Align.START)
            
            info_box.append(label_widget)
            info_box.append(value_label)
            
            open_btn = Gtk.Button(label="Open")
            open_btn.add_css_class("suggested-action")
            open_btn.set_margin_end(15)
            open_btn.set_margin_top(15)
            open_btn.set_margin_bottom(15)
            open_btn.connect("clicked", self.open_link, url)
            
            contact_row.append(emoji_label)
            contact_row.append(info_box)
            contact_row.append(open_btn)
            
            contact_box.append(contact_row)
        
        contact_frame.set_child(contact_box)
        self.append(contact_frame)
        
        # Location info (with Hyprland workspace info)
        location_frame = Gtk.Frame(label="Location & Setup")
        location_frame.set_margin_top(20)
        
        location_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        location_box.set_margin_start(15)
        location_box.set_margin_end(15)
        location_box.set_margin_top(15)
        location_box.set_margin_bottom(15)
        
        location_label = Gtk.Label(label="📍 Based in Your City, Country")
        location_label.set_halign(Gtk.Align.START)
        location_box.append(location_label)
        
        timezone_label = Gtk.Label(label="🕐 Timezone: UTC+X")
        timezone_label.set_halign(Gtk.Align.START)
        location_box.append(timezone_label)
        
        if HyprlandIntegration.is_hyprland():
            hypr_info = HyprlandIntegration.get_hyprland_info()
            if hypr_info:
                workspace_label = Gtk.Label(label=f"💻 Currently on workspace: {hypr_info['workspace'].get('name', 'Unknown')}")
                workspace_label.set_halign(Gtk.Align.START)
                location_box.append(workspace_label)
        
        os_label = Gtk.Label(label="🐧 Running on Linux with Hyprland")
        os_label.set_halign(Gtk.Align.START)
        location_box.append(os_label)
        
        location_frame.set_child(location_box)
        self.append(location_frame)
    
    def open_link(self, button, url):
        """Open link in browser"""
        try:
            webbrowser.open(url)
        except Exception as e:
            print(f"Failed to open link: {e}")


class PortfolioWindow(Adw.ApplicationWindow):
    """Main portfolio window with SPA navigation"""
    
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Your Name - Portfolio")
        self.set_default_size(900, 700)
        
        # Setup pages
        self.pages = {
            'home': HomePage("Home"),
            'projects': ProjectsPage("Projects"),
            'experience': ExperiencePage("Experience"),
            'contact': ContactPage("Contact")
        }
        self.current_page = None
        
        self.setup_ui()
        self.setup_css()
        self.navigate_to('home')
    
    def setup_css(self):
        """Setup custom CSS styling"""
        css_provider = Gtk.CssProvider()
        css = """
        .pill {
            background: alpha(@accent_color, 0.1);
            border: 1px solid alpha(@accent_color, 0.3);
            border-radius: 12px;
            padding: 6px 12px;
            font-size: 0.9em;
        }
        
        .avatar {
            background: linear-gradient(45deg, @accent_color, @theme_selected_bg_color);
            border-radius: 60px;
            border: 3px solid @borders;
        }
        
        .card {
            background: @view_bg_color;
            border: 1px solid @borders;
            border-radius: 12px;
            box-shadow: 0 2px 4px alpha(@borders, 0.2);
        }
        """
        
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
    
    def setup_ui(self):
        """Setup the main UI structure"""
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(main_box)
        
        # Header bar with navigation
        header_bar = Adw.HeaderBar()
        
        # Navigation buttons
        nav_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        nav_box.add_css_class("linked")
        
        self.nav_buttons = {}
        nav_items = [
            ('home', 'Home', '🏠'),
            ('projects', 'Projects', '🚀'),
            ('experience', 'Experience', '💼'),
            ('contact', 'Contact', '📧')
        ]
        
        for page_id, title, emoji in nav_items:
            btn = Gtk.ToggleButton(label=f"{emoji} {title}")
            btn.connect("clicked", self.on_nav_clicked, page_id)
            nav_box.append(btn)
            self.nav_buttons[page_id] = btn
        
        header_bar.set_title_widget(nav_box)
        
        # Theme toggle button
        theme_btn = Gtk.Button()
        theme_btn.set_icon_name("weather-clear-night-symbolic")
        theme_btn.set_tooltip_text("Toggle Dark Mode")
        theme_btn.connect("clicked", self.toggle_theme)
        header_bar.pack_end(theme_btn)
        
        main_box.append(header_bar)
        
        # Content area
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)
        
        self.content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.content_box.set_margin_start(20)
        self.content_box.set_margin_end(20)
        self.content_box.set_margin_top(20)
        self.content_box.set_margin_bottom(20)
        
        scrolled.set_child(self.content_box)
        main_box.append(scrolled)
    
    def toggle_theme(self, button):
        """Toggle between light and dark themes"""
        style_manager = Adw.StyleManager.get_default()
        if style_manager.get_dark():
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            button.set_icon_name("weather-clear-symbolic")
        else:
            style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
            button.set_icon_name("weather-clear-night-symbolic")
    
    def on_nav_clicked(self, button, page_id):
        """Handle navigation button clicks"""
        if button.get_active():
            self.navigate_to(page_id)
        else:
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
        page_titles = {
            'home': 'Portfolio',
            'projects': 'Projects',
            'experience': 'Experience',
            'contact': 'Contact'
        }
        self.set_title(f"Your Name - {page_titles.get(page_id, 'Portfolio')}")


class PortfolioApplication(Adw.Application):
    """Main portfolio application class"""
    
    def __init__(self):
        super().__init__(application_id="com.yourname.portfolio")
        self.connect("activate", self.on_activate)
        self.setup_actions()
    
    def setup_actions(self):
        """Setup application actions"""
        # Quit action
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>q"])
        
        # Navigation shortcuts
        home_action = Gio.SimpleAction.new("home", None)
        home_action.connect("activate", lambda a, p: self.window.navigate_to('home'))
        self.add_action(home_action)
        self.set_accels_for_action("app.home", ["<Ctrl>1"])
        
        projects_action = Gio.SimpleAction.new("projects", None)
        projects_action.connect("activate", lambda a, p: self.window.navigate_to('projects'))
        self.add_action(projects_action)
        self.set_accels_for_action("app.projects", ["<Ctrl>2"])
        
        experience_action = Gio.SimpleAction.new("experience", None)
        experience_action.connect("activate", lambda a, p: self.window.navigate_to('experience'))
        self.add_action(experience_action)
        self.set_accels_for_action("app.experience", ["<Ctrl>3"])
        
        contact_action = Gio.SimpleAction.new("contact", None)
        contact_action.connect("activate", lambda a, p: self.window.navigate_to('contact'))
        self.add_action(contact_action)
        self.set_accels_for_action("app.contact", ["<Ctrl>4"])
        
        # Theme toggle
        theme_action = Gio.SimpleAction.new("toggle_theme", None)
        theme_action.connect("activate", self.on_toggle_theme)
        self.add_action(theme_action)
        self.set_accels_for_action("app.toggle_theme", ["<Ctrl>t"])
        
        # Hyprland workspace shortcuts (if available)
        if HyprlandIntegration.is_hyprland():
            for i in range(1, 10):
                ws_action = Gio.SimpleAction.new(f"workspace_{i}", None)
                ws_action.connect("activate", self.on_switch_workspace, i)
                self.add_action(ws_action)
                self.set_accels_for_action(f"app.workspace_{i}", [f"<Super>{i}"])
    
    def on_activate(self, app):
        """Application activation"""
        self.window = PortfolioWindow(self)
        self.window.present()
        
        # Show welcome message for Hyprland users
        if HyprlandIntegration.is_hyprland():
            GLib.timeout_add_seconds(1, self.show_hyprland_welcome)
    
    def show_hyprland_welcome(self):
        """Show a welcome toast for Hyprland users"""
        toast = Adw.Toast()
        toast.set_title("🚀 Hyprland detected! Use Super+1-9 for workspace shortcuts")
        toast.set_timeout(3)
        
        # Add toast to window if it has a toast overlay
        if hasattr(self.window, 'toast_overlay'):
            self.window.toast_overlay.add_toast(toast)
        
        return False  # Don't repeat
    
    def on_quit(self, action, param):
        """Quit the application"""
        self.quit()
    
    def on_toggle_theme(self, action, param):
        """Toggle application theme"""
        if hasattr(self, 'window'):
            # Find the theme button and simulate click
            style_manager = Adw.StyleManager.get_default()
            if style_manager.get_dark():
                style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
            else:
                style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
    
    def on_switch_workspace(self, action, param, workspace_id):
        """Switch workspace using Hyprland"""
        if HyprlandIntegration.is_hyprland():
            try:
                subprocess.run(['hyprctl', 'dispatch', 'workspace', str(workspace_id)], 
                              check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass


def main():
    """Main entry point"""
    # Optimize for Wayland
    if os.environ.get('XDG_SESSION_TYPE') == 'wayland':
        os.environ['GDK_BACKEND'] = 'wayland'
    
    # Set application info
    GLib.set_application_name("Portfolio")
    GLib.set_prgname("portfolio")
    
    app = PortfolioApplication()
    return app.run()


if __name__ == "__main__":
    print("🚀 Starting Portfolio App...")
    if HyprlandIntegration.is_hyprland():
        print("🖥️  Hyprland integration enabled")
    else:
        print("🖥️  Running in standard mode")
    
    exit(main())
