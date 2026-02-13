import streamlit as st
from utils import generate_poem
from poems import poems

# MUST be first Streamlit command
st.set_page_config(
    page_title="Birthday Wishes 🎂 for your loved ones",
    page_icon="🎉",
    layout="centered"
)

# Background style
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #ffecd2, #fcb69f);
}
</style>
""", unsafe_allow_html=True)

# Query parameters
params = st.query_params
default_lang = params.get("lang", "English")
default_name = params.get("name", "")

# Title
st.title("🎉 Birthday Wishes Generator")
st.write("Developed by Sri Kaleeswarar S - poems by Srikaleeswarar")

# Language selection
language = st.selectbox(
    "Language",
    ["English", "Tamil"],
    index=["English", "Tamil"].index(default_lang) if default_lang in ["English", "Tamil"] else 0
)

# Dynamic relationships
relations = list(poems[language].keys())

default_relation = params.get("relation", relations[0])
relation_index = relations.index(default_relation) if default_relation in relations else 0

relation = st.selectbox("Relationship", relations, index=relation_index)

# Name input
name = st.text_input("Enter Name", value=default_name)

# Generate button
if st.button("Generate Wishes 🎁"):

    if not name:
        st.warning("Please enter a name")
    else:
        poem = generate_poem(language, relation, name)

        st.balloons()

        st.markdown(f"""
        <h1 style='text-align: center; color: #ff4b4b;'>
        🎂 Happy Birthday {name} 🎉
        </h1>
        """, unsafe_allow_html=True)

        st.markdown("---")

        st.markdown(f"""
        <div style='text-align: center; font-size: 20px; line-height: 1.6;'>
        {poem}
        </div>
        """, unsafe_allow_html=True)

        # Share link
        base_url = "https://yourapp.streamlit.app"  # Replace after deployment
        share_link = f"{base_url}/?lang={language}&relation={relation}&name={name}"

        st.markdown("### 🔗 Share this link")
        st.code(share_link)
