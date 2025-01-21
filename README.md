# FashionStylist-Agent App 👠👟🩰👞🧥👗👔👜🎒
App link: https://kj32igqrqkckk7ttgpeaft.streamlit.app/

**Multimodal Agentic Workflow - Phidata**

This app gives styling and brand recommendations based on uploaded images.

## Features 🌟

* **Example Products:** Pre-loaded examples of common products
* **Image Upload:** Upload your own product images
* **Camera Capture:** Take photos directly through the app
* **AI Analysis:** Powered by Google's Gemini 2.0 Flash and Tavily Search
* **Fashion Insights:** Get detailed analysis of product, branding, and styling tips.


## Installation 🚀

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/FashionStylist-Agent.git
   cd FashionStylist-Agent
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration ⚙️

1. **Create a `.env` file in the project root:**

   ```
   TAVILY_API_KEY = your_tavily_api_key
   GOOGLE_API_KEY = your_gemini_api_key
   ```

2. **Add your example images in the `images/` directory:**

   ```
   images/
   ├── Coat.jpg
   ├── Pant.jpg
   ├── Shoe.jpg
   └── Slidders.jpg
   ```

## Usage 💡

1. **Run the Streamlit app:**

   ```bash
   streamlit run App.py
   ```

2. **Open your browser and navigate to `http://localhost:8501`**

3. **Choose one of three options to analyze a product:**
    * Select from example products
    * Upload your own image
    * Take a photo using your camera


## Project Structure 📁

```
FashionStylist-Agent/
├── App.py          # Main Streamlit application
├── Constants.py     # System prompts and constants
├── requirements.txt # Project dependencies
├── images/         # Example product images
└── README.md       # Project documentation
```

## Dependencies 📚📚

* `streamlit`
* `phidata`
* `pillow`
* `tavily-python`
* `google-generativeai`


## Contributing 🤝

⭐️ STAR the Phidata repository: [https://github.com/phidatahq/phidata](https://github.com/phidatahq/phidata)


## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


## Acknowledgments 👏

* **Phidata** for building Multimodal Agent
* **Google Gemini AI** for powering the analysis
* **Streamlit** for the web interface
* **Tavily** for search capabilities 
