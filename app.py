import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# --- CONFIGURATION ---
GITHUB_USER = "Rishabh-G-Shetye"
NAME = "Rishabh Gaurish Shetye"
DESCRIPTION = "Cybersecurity Enthusiast | Python Enthusiast | Game Dev"
EMAIL = "rishabhshetye09@gmail.com"
SOCIAL_MEDIA = {
    "LinkedIn": "https://www.linkedin.com/in/rishabh-shetye-3b602b227/",
    "GitHub": f"https://github.com/{GITHUB_USER}"
}
SKILLS = ["Python", "Machine Learning", "Docker", "Cybersecurity", "Godot", "Neuromorphic Computing"]

st.set_page_config(page_title=f"{NAME} Portfolio", page_icon="🚀", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
<style>
    /* Reduce top padding */
    .block-container {padding-top: 2rem;}
    /* Style cards */
    div[data-testid="stMetric"] {
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 10px;
    }
    /* Dark mode adjustments would go here */
</style>
""", unsafe_allow_html=True)


# --- HELPER FUNCTIONS ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def get_github_data(username):
    user_url = f"https://api.github.com/users/{username}"
    repos_url = f"https://api.github.com/users/{username}/repos?sort=updated"

    user_data = requests.get(user_url).json()
    repos_data = requests.get(repos_url).json()
    return user_data, repos_data


# --- LOAD DATA ---
user_data, repos_data = get_github_data(GITHUB_USER)
avatar_url = user_data.get('avatar_url', 'https://via.placeholder.com/150')

# --- SIDEBAR (PROFILE) ---
with st.sidebar:
    st.image(avatar_url, width=150)
    st.title(NAME)
    st.write(DESCRIPTION)
    st.write("📍 " + (user_data.get('location') or "Global"))

    st.markdown("---")
    st.subheader("Skills")
    # Display skills as tags
    st.write("  ".join([f"`{skill}`" for skill in SKILLS]))

    st.markdown("---")
    st.subheader("Contact")
    st.write(f"📧 {EMAIL}")
    for platform, link in SOCIAL_MEDIA.items():
        st.write(f"[{platform}]({link})")

    # Resume Download Button (Placeholder)
    # with open("resume.pdf", "rb") as pdf_file:
    #     st.download_button("Download Resume", data=pdf_file, file_name="resume.pdf")

# --- MAIN CONTENT ---
st.title("🚀 Portfolio & Projects")
st.write("---")

# featured projects in a grid
st.subheader("Recent Work")

# Check if repos exist and are a list
if isinstance(repos_data, list):
    # Filter out forks if you want original work only
    my_repos = [repo for repo in repos_data if not repo.get('fork', False)]

    # Create a grid layout (2 columns)
    cols = st.columns(2)

    for i, repo in enumerate(my_repos[:6]):  # Show top 6
        col = cols[i % 2]
        with col:
            with st.container(border=True):
                st.subheader(f"[{repo['name']}]({repo['html_url']})")
                st.write(repo['description'] or "No description available.")

                # Badge info
                c1, c2, c3 = st.columns(3)
                c1.markdown(f"**⭐ {repo['stargazers_count']}**")
                c2.markdown(f"**🍴 {repo['forks_count']}**")
                c3.markdown(f"**🔵 {repo['language'] or 'Text'}**")
else:
    st.error("Rate limit exceeded or user not found.")

st.write("---")
st.caption("© 2026 | Built with Streamlit")