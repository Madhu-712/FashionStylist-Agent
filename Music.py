import streamlit as st
from gtts import gTTS
import os

# Streamlit App
def main():
    st.title("Text-to-Speech Generator 🎵")
    st.write("Enter your text and download the generated audio as speech or music.")

    # Input Text
    user_input = st.text_area("Enter the text below:", placeholder="Type your text here...")

    # Choose Audio Type
    audio_type = st.radio(
        "Choose the type of audio to generate:",
        ("Speech", "Music"),
        help="Speech generates a text-to-speech audio. Music generation requires additional configurations."
    )

    if st.button("Generate Audio"):
        if user_input.strip():
            # Generate Speech
            if audio_type == "Speech":
                tts = gTTS(user_input, lang="en")
                output_file = "speech_output.mp3"
                tts.save(output_file)
                st.success("Speech audio generated successfully!")
                
                # Provide download link
                with open(output_file, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                    st.download_button(
                        label="Download Speech Audio",
                        data=audio_bytes,
                        file_name="speech_output.mp3",
                        mime="audio/mpeg"
                    )

                # Clean up
                os.remove(output_file)

            # Placeholder for Music Generation
            elif audio_type == "Music":
                st.warning("Music generation is not implemented in this example.")
        else:
            st.error("Please enter some text to generate audio!")

if __name__ == "__main__":
    main()
