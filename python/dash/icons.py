import dash.html as html

class FontAwesomeIcons:
    # Navigation Icons
    HOME = "fas fa-home"
    ABOUT = "fas fa-user"
    SKILLS = "fas fa-tools"
    PROJECTS = "fas fa-project-diagram"
    CONTACT = "fas fa-envelope"

    # Brand Icons
    GITHUB = "fab fa-github"
    LINKEDIN = "fab fa-linkedin"
    TWITTER = "fab fa-twitter"
    INSTAGRAM = "fab fa-instagram"
    STACKOVERFLOW = "fab fa-stack-overflow"

    # Technology Icons
    PYTHON = "fab fa-python"
    REACT = "fab fa-react"
    NODE_JS = "fab fa-node-js"
    DOCKER = "fab fa-docker"
    AWS = "fab fa-aws"
    GOOGLE_CLOUD = "fab fa-google"

    # Development Icons
    CODE = "fas fa-code"
    LAPTOP_CODE = "fas fa-laptop-code"
    SERVER = "fas fa-server"
    CLOUD = "fas fa-cloud"
    DATABASE = "fas fa-database"

    # Personal Icons
    USER = "fas fa-user"
    ENVELOPE = "fas fa-envelope"
    PHONE = "fas fa-phone"
    LOCATION = "fas fa-map-marker-alt"

    # Project Icons
    PROJECT = "fas fa-project-diagram"
    ROCKET = "fas fa-rocket"
    BRIEFCASE = "fas fa-briefcase"

    # Skill Icons
    SKILLS_ICON = "fas fa-tools"
    CERTIFICATE = "fas fa-certificate"

    # Status Icons
    CHECK = "fas fa-check"
    STAR = "fas fa-star"
    TROPHY = "fas fa-trophy"

    # Download Icon
    DOWNLOAD = "fas fa-download"

def create_icon(icon_class, additional_classes="", style=None):
    """
    Create a font icon element with optional styling

    Args:
        icon_class (str): Base icon class
        additional_classes (str, optional): Additional CSS classes
        style (dict, optional): Inline styles

    Returns:
        html.I: Dash HTML icon element
    """
    # Default style if not provided
    default_style = {
        "margin-right": "10px",
        "color": "#3b82f6"  # Tailwind primary blue
    }

    # Merge default and provided styles
    merged_style = {**default_style, **(style or {})}

    return html.I(
        className=f"{icon_class} {additional_classes}",
        style=merged_style
    )

# Icon Mapping for Quick Reference
ICON_MAP = {
    "github": FontAwesomeIcons.GITHUB,
    "linkedin": FontAwesomeIcons.LINKEDIN,
    "python": FontAwesomeIcons.PYTHON,
    "react": FontAwesomeIcons.REACT,
    "project": FontAwesomeIcons.PROJECT,
    "home": FontAwesomeIcons.HOME,
    "about": FontAwesomeIcons.ABOUT,
    "skills": FontAwesomeIcons.SKILLS,
    "contact": FontAwesomeIcons.CONTACT
}

def get_icon(name, **kwargs):
    """
    Retrieve an icon by name with optional customization

    Args:
        name (str): Icon name from ICON_MAP
        **kwargs: Additional styling or classes

    Returns:
        html.I: Dash HTML icon element
    """
    icon_class = ICON_MAP.get(name, FontAwesomeIcons.CODE)
    return create_icon(icon_class, **kwargs)
