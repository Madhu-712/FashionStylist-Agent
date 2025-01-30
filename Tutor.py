# Required installations:
# pip install phidata google-generativeai tavily-python
# pip install streamlit

import streamlit as st
import os
from PIL import Image
from io import BytesIO
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.tavily import TavilyTools
from tempfile import NamedTemporaryFile

# Define system prompt and instructions
SYSTEM_PROMPT = """
You are an AI-powered Tutor Agent. Your role is to analyze images containing chapter names from educational materials, generate brief and intuitive explanations about each topic, provide real-world examples, and formulate 20 frequently asked questions (FAQs) for each chapter. Present your responses in a clear and organized manner suitable for students.
"""

INSTRUCTIONS = """
* Analyze the uploaded image to extract chapter names.
* For each chapter:
    * Provide a concise explanation of the topic.
    * Offer real-world examples to illustrate the concepts.
    * Generate 20 relevant FAQs along with their answers.
* Present the information in a structured format using headings and bullet points for clarity.
* Ensure the content is student-friendly and easy to understand.
"""

# Set API keys from Streamlit secrets
os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_KEY']
os.environ['GOOGLE_API_KEY'] = st.secrets['GEMINI_KEY']

MAX_IMAGE_WIDTH = 300

def resize_image_for_display(image_file):
    """Resize image for display purposes."""
    img = Image.open(image_file)
    aspect_ratio = img.height / img.width
    new_height = int(MAX_IMAGE_WIDTH * aspect_ratio)
    img = img.resize((MAX_IMAGE_WIDTH, new_height), Image.Resampling.LANCZOS)
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

@st.cache_resource
def get_agent():
    """Initialize and cache the AI agent."""
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
        tools=[TavilyTools(api_key=os.getenv("TAVILY_API_KEY"))],
        markdown=True,
    )

def analyze_image(image_path):
    """Analyze the image to extract chapter names and generate educational content."""
    agent = get_agent()
    with st.spinner('Analyzing image and generating content...'):
        response = agent.run(
            "Analyze the given image to extract chapter names and generate educational content.",
            images=[image_path],
        )
        st.markdown(response.content)

def save_uploaded_file(uploaded_file):
    """Save the uploaded image to a temporary file."""
    with NamedTemporaryFile(dir='.', suffix='.jpg', delete=False) as f:
        f.write(uploaded_file.getbuffer())
        return f.name

def main():
    st.title("📘 AI-Powered Tutor Agent")
    st.write("Upload an image containing chapter names to receive explanations, real-world examples, and FAQs for each topic.")

    uploaded_file = st.file_uploader(
        "Upload an image with chapter names", 
        type=["jpg", "jpeg", "png"],
        help="Ensure the image is clear and the text is legible."
    )

    if uploaded_file:
        resized_image = resize_image_for_display(uploaded_file)
        st.image(resized_image, caption="Uploaded Image", use_container_width=False, width=MAX_IMAGE_WIDTH)
        if st.button("📖 Generate Educational Content"):
            temp_path = save_uploaded_file(uploaded_file)
            analyze_image(temp_path)
            os.unlink(temp_path)
    else:
        st.info("Please upload an image to proceed.")

if __name__ == "__main__":
    st.set_page_config(
        page_title="AI-Powered Tutor Agent",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()


