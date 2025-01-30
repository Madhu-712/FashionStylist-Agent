
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

SYSTEM_PROMPTS="""You are an AI Tutor specializing in generating concise explanations and real-world examples for educational topics. Your role is to analyze provided chapter titles or queries, deliver brief and intuitive explanations for each, offer relevant real-world examples, and generate 20 frequently asked questions (FAQs) with answers for each topic. Present all information in a clear, organized, and student-friendly manner.Pls use Markdown format"""

INSTRUCTIONS ="""
* For each provided chapter title:
    1. **Explanation**:
        - Provide a concise and intuitive explanation of the topic, ensuring clarity and accessibility for students.
    2. **Real-World Examples**:
        - Offer relevant real-world examples that illustrate the topic, enhancing understanding and applicability.
    3. **Frequently Asked Questions (FAQs)**:
        - Generate a list of 20 pertinent FAQs related to the each topic.
        - For Math related topic ensure the queries are more on math problems and solution should be solved step wise .(eg.solve for 3x+5=90 , 1step:add -5 to both sides,2step:3x=90,3step:x=30)
        - Provide clear and accurate answers to each question to facilitate student comprehension and engagement.
*For a query on a topic:
    - Ensure that all step by step explanations are provided.
    - Give more such examples to make the concepts clear
    - Provide a tailor  responses to students in an intuitive way. 
*Present the information in a structured format, using headings, bullet points, and numbering to enhance readability.
* Maintain a supportive and encouraging tone throughout, fostering a positive learning environment."""




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
        system_prompt=SYSTEM_PROMPTS,
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

        
def analyze_text(user_text):
    agent = get_agent()
    with st.spinner('Analyzing query text...'):
        response = agent.run(
            "Analyze the provided text",
            inputs={"text": user_text},
        )
        st.markdown(response.content)



def main():
    st.title("📘 AI-Powered Tutor Agent")
    st.write("Upload an image containing chapter names to receive explanations, real-world examples, and FAQs for each topic.")
    # Session state initialization
    if 'selected_uploadimage' not in st.session_state:
        st.session_state.selected_uploadimage = None
    if 'analyze_clicked' not in st.session_state:
        st.session_state.analyze_clicked = False
    if 'selected_entertext' not in st.session_state:
        st.session_state.selected_entertext = False
    
    tab_text,tab_upload, tab_camera = st.tabs([
        "📝 Enter Text",
        "📤 Upload Image",
        "📸 Take Photo"
     ])
    # Upload text
    with tab_text:
        user_text = st.text_area(
            "Enter text to analyze:",
            placeholder="Type your text here...",
            height=200
        )
        if st.button("🔍 Analyze Text"):
            if user_text.strip():
                analyze_text(user_text)
            else:
                #st.warning(".....
                st.error("Please enter some text before clicking 'Analyze Text'")

    # Upload Image Tab
    with tab_upload:
        uploaded_file = st.file_uploader(
            "Upload image of query or chapter names",
            type=["jpg", "jpeg", "png"],
            help="Upload a clear image of query or chapter names"
        )
        if uploaded_file:
            resized_image = resize_image_for_display(uploaded_file)
            st.image(resized_image, caption="Uploaded Image", use_container_width=False, width=MAX_IMAGE_WIDTH)
            if st.button("🔍 Analyze Uploaded Image", key="analyze_upload"):
                temp_path = save_uploaded_file(uploaded_file)
                analyze_image(temp_path)
                os.unlink(temp_path)
        
     # Camera Input Tab
    with tab_camera:
        camera_photo = st.camera_input("Take a picture of your query or chapter names")
        if camera_photo:
            resized_image = resize_image_for_display(camera_photo)
            st.image(resized_image, caption="Captured Photo", use_container_width=False, width=MAX_IMAGE_WIDTH)
            if st.button("Analyze Query", key="analyze_camera"):
                temp_path = save_uploaded_file(camera_photo)
                analyze_image(temp_path)
                os.unlink(temp_path)


    
if __name__ == "__main__":
    st.set_page_config(
        page_title="AI-Powered Tutor Agent",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    main()


