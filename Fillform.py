
import streamlit as st
from phi.agent import Agent
from phi.model.google import Gemini
from phi.knowledge.pdf import PDFFileKnowledgeBase
from phi.vectordb.pgvector import PgVector, SearchType
import os

# Set up environment variables (add your API key in Streamlit secrets)
os.environ['GOOGLE_API_KEY'] = st.secrets.get('GEMINI_KEY', '')

# PostgreSQL connection for vector storage
DB_URL = "postgresql+psycopg://ai:ai@localhost:5532/ai"

# Initialize knowledge base (PDF-based)
@st.cache_resource
def init_knowledge_base(pdf_path):
    kb = PDFFileKnowledgeBase(
        files=[pdf_path],
        vector_db=PgVector(table_name="synthetic_customers", db_url=DB_URL, search_type=SearchType.hybrid),
    )
    kb.load(upsert=True)
    return kb

# Initialize Phi Agent
@st.cache_resource
def init_agent(knowledge_base):
    return Agent(
        model=Gemini(id="gemini-2.0-pro-vision"),  # Multimodal model
        knowledge=knowledge_base,
        search_knowledge=True,
        read_chat_history=True,
        show_tool_calls=True,
        markdown=True
    )

# Function to fill the form using RAG
def fill_form_with_rag(agent, query):
    response = agent.run(query)
    return response.content if response else "No response generated."

# Streamlit UI
st.set_page_config(page_title="Bank Form Auto-Filler", layout="wide")
st.title("🏦 Bank Account Registration Form Auto-Filler with RAG")

# Tabs for PDF upload and Image-based Form Upload
tab1, tab2 = st.tabs(["📄 Upload Synthetic Data (PDF)", "🖼️ Upload Bank Form (Image)"])

with tab1:
    uploaded_pdf = st.file_uploader("Upload Synthetic Data PDF", type=["pdf"])
    if uploaded_pdf:
        pdf_path = f"/tmp/{uploaded_pdf.name}"
        with open(pdf_path, "wb") as f:
            f.write(uploaded_pdf.read())
        
        st.success("PDF uploaded successfully!")

        # Initialize Knowledge Base & Agent
        knowledge_base = init_knowledge_base(pdf_path)
        agent = init_agent(knowledge_base)

        query = st.text_input("Enter your query to auto-fill the form:", placeholder="e.g., Fill the account form for John Doe")
        if st.button("Generate Form"):
            with st.spinner("Generating form using RAG..."):
                output = fill_form_with_rag(agent, query)
            st.markdown("### 📝 Auto-Filled Form:")
            st.markdown(output)

with tab2:
    uploaded_image = st.file_uploader("Upload Bank Form Image", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        st.image(uploaded_image, caption="Uploaded Bank Form", use_column_width=True)
        
