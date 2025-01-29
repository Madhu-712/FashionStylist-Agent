
import streamlit as st
import os
from phi.agent import Agent
from phi.model.google import Gemini
from tempfile import NamedTemporaryFile

# Set your API keys
os.environ['TAVILY_API_KEY'] = st.secrets['TAVILY_KEY']
os.environ['GOOGLE_API_KEY'] = st.secrets['GEMINI_KEY']

# System prompt and instructions
SYSTEM_PROMPT = """You are a state-of-the-art AI model specializing in text-to-audio conversion. Your goal is to take input text, convert it into natural-sounding speech, and provide a downloadable audio output."""

INSTRUCTIONS = """Convert the provided text into natural-sounding audio. The output should match the tone, language, and clarity expected for human-like speech."""

# Function to cache and retrieve the Gemini agent
@st.cache_resource
def get_agent():
    return Agent(
        model=Gemini(id="gemini-2.0-flash-exp"),
        system_prompt=SYSTEM_PROMPT,
        instructions=INSTRUCTIONS,
    )



def generate_audio(text_input):
    agent = get_agent()
    with st.spinner("Generating audio..."):
        response = agent.run("Convert the following text to audio", inputs={"text": text_input})
        st.write(response)  # Debugging line
        if hasattr(response, 'outputs') and "audio" in response.outputs:
            audio_content = response.outputs["audio"]
            return audio_content
        else:
            st.error("The response does not contain 'audio'. Please check the response structure.")
            return None







# Save audio to a temporary file
def save_audio(audio_bytes):
    with NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
        audio_file.write(audio_bytes)
        return audio_file.name


def main():
    st.title("🎤 Text-to-Audio Generator")
    st.write("Enter text below and convert it to high-quality audio.")

    # Text input
    user_text = st.text_area("Enter your text:", placeholder="Type here...", height=200)

    if st.button("🎧 Generate Audio"):
        if user_text.strip():
            # Generate audio from the entered text
            audio_bytes = generate_audio(user_text)
            if audio_bytes:
                # Save the generated audio
                audio_file_path = save_audio(audio_bytes)

                # Provide a download button for the generated audio
                with open(audio_file_path, "rb") as audio_file:
                    st.audio(audio_bytes, format="audio/mp3", start_time=0)
                    st.download_button(
                        label="📥 Download Audio",
                        data=audio_file,
                        file_name="generated_audio.mp3",
                        mime="audio/mpeg",
                    )

                # Clean up the temporary audio file
                os.unlink(audio_file_path)
        else:
            st.error("Please enter some text before generating audio!")






if __name__ == "__main__":
    st.set_page_config(
        page_title="Text-to-Audio Generator",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    main()
