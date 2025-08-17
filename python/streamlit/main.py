import streamlit as st
import base64
from PIL import Image
import requests

# First Streamlit command - Page Configuration
st.set_page_config(
    page_title="Developer Portfolio",
    page_icon="👨‍💻",
    layout="wide"
)

# Custom CSS for Tailwind-like styling
st.markdown("""
<style>
.tailwind-container {
    background-color: #f3f4f6;
    padding: 2rem;
}
.profile-card {
    background-color: white;
    border-radius: 0.75rem;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    transition: transform 0.3s ease;
}
.profile-card:hover {
    transform: scale(1.02);
}
.skill-badge {
    background-color: #3b82f6;
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 9999px;
    margin-right: 0.5rem;
    margin-bottom: 0.5rem;
    display: inline-block;
}
</style>
""", unsafe_allow_html=True)

# Utility Functions
def load_lottie(url):
    try:
        response = requests.get(url)
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error loading Lottie animation: {e}")
        return None

def load_profile_image(path):
    try:
        return Image.open(path)
    except Exception as e:
        st.error(f"Error loading profile image: {e}")
        return None

# Page Sections
def home_page():
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("# 👋 Hello, I'm [Your Name]")
        st.markdown("### Software Engineer & Full Stack Developer")

        st.markdown("""
        Passionate developer creating innovative solutions
        with cutting-edge technologies. Transforming ideas
        into elegant, efficient code.
        """)

        # Social Links
        st.markdown("""
        <div style="display: flex; gap: 10px;">
            <a href="#" style="background-color: #3b82f6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Download CV
            </a>
            <a href="#" style="background-color: #gray-200; color: black; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Contact Me
            </a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        profile_image = load_profile_image("profile.png")
        if profile_image:
            st.image(profile_image, width=300, caption="Developer Profile")

def about_page():
    st.markdown("## 🚀 About Me")
    st.write("""
    I'm a passionate software engineer with expertise in:
    - Full Stack Web Development
    - Cloud Architecture
    - Machine Learning
    - DevOps Engineering

    Committed to creating scalable, efficient solutions
    that drive technological innovation.
    """)

def skills_page():
    skills = {
        "Frontend": ["React", "Vue", "Tailwind", "Next.js"],
        "Backend": ["Python", "Node.js", "FastAPI", "Django"],
        "DevOps": ["Docker", "Kubernetes", "AWS", "CI/CD"]
    }

    st.markdown("## 💻 Technical Skills")

    for category, skill_list in skills.items():
        st.markdown(f"### {category}")
        skill_html = " ".join([
            f'<span class="skill-badge">{skill}</span>'
            for skill in skill_list
        ])
        st.markdown(skill_html, unsafe_allow_html=True)

def projects_page():
    projects = [
        {
            "name": "AI Chatbot",
            "description": "Advanced conversational AI",
            "technologies": ["Python", "GPT-3", "FastAPI"],
            "link": "https://github.com/username/project"
        },
        {
            "name": "E-commerce Platform",
            "description": "Full-stack online marketplace",
            "technologies": ["React", "Node.js", "MongoDB"],
            "link": "https://github.com/username/project"
        }
    ]

    st.markdown("## 📦 Featured Projects")

    for project in projects:
        with st.expander(project['name']):
            st.markdown(f"""
            ### {project['name']}
            {project['description']}

            **Technologies:** {', '.join(project['technologies'])}

            [View Project]({project['link']})
            """)

def contact_page():
    st.markdown("## 📞 Contact Me")

    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        message = st.text_area("Your Message")
        submit_button = st.form_submit_button("Send Message")

        if submit_button:
            # Add actual form submission logic
            st.success("Message sent successfully!")

def main():
    # Sidebar Navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Explore",
        ["Home", "About", "Skills", "Projects", "Contact"]
    )

    # Page Routing
    if page == "Home":
        home_page()
    elif page == "About":
        about_page()
    elif page == "Skills":
        skills_page()
    elif page == "Projects":
        projects_page()
    elif page == "Contact":
        contact_page()

    # Optional: Add footer
    st.markdown("---")
    st.markdown("© 2024 Your Name. All rights reserved.")

# Application Entry Point
if __name__ == "__main__":
    main()
