FashionStylist-Agent App👠👟🩰👞🧥👗👔👜🎒

Multimodal Agentic Workflow - Phidata

This App gives styling and brand  recommendation based on uploaded image.

Features 🌟
Example Products: Pre-loaded examples of common products
Image Upload: Upload your own product images
Camera Capture: Take photos directly through the app
AI Analysis: Powered by Google's Gemini 2.0 Flash and Tavily Search
Fashion Insights: Get a detailed analysis of product ,branding and styling tips.

Installation 🚀
Clone the repository:
git clone https://github.com/yourusername/FashionStylist-Agent.git
cd FashionStylist-Agent
Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt

Configuration ⚙️
Create a .env file in the project root:
TAVILY_API_KEY = your_tavily_api_key
GOOGLE_API_KEY = your_gemini_api_key 
Add your example images in the images/ directory:
images/
├── Coat.jpg
├── Pant.jpg
├── Shoe.jpg
└── Slidders.jpg

Usage 💡
Run the Streamlit app:
streamlit run App.py
Open your browser and navigate to http://localhost:8501

Choose one of three options to analyze a product:

Select from example products
Upload your own image
Take a photo using your camera
Project Structure 📁
FashionStylist-Agent/
├── App.py                 # Main Streamlit application
├── Constants.py           # System prompts and constants
├── requirements.txt       # Project dependencies
├── images/               # Example product images
└── README.md             # Project documentation

Dependencies 📚
streamlit
phidata
pillow
tavily-python
google-generativeai
Contributing 🤝
⭐️ STAR the Phidata repository: https://github.com/phidatahq/phidata

License 📄
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments 👏
Phidata for building Multimodal Agent
Google Gemini AI for powering the analysis
Streamlit for the web interface
Tavily for search capabilities

