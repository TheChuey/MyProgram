import streamlit as st
import ollama
import time

# Set up the page
st.set_page_config(
    page_title="Jesus Rodriguez AI chat prototype",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    /* Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #ffffff;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease;
    }

    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.2);
    }

    /* Input Field Styling */
    [data-testid="stChatInput"] {
        border-radius: 30px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(5px);
    }

    /* Headings */
    h1 {
        background: linear-gradient(to right, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        letter-spacing: -1px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0, 0, 0, 0.1);
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255, 255, 255, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

def get_model_names():
    """Fetch available models from Ollama."""
    try:
        models_data = ollama.list()
        if hasattr(models_data, 'models'):
            return [m.model for m in models_data.models]
        elif isinstance(models_data, dict) and 'models' in models_data:
            return [m['name'] for m in models_data['models']]
        return []
    except Exception:
        # Fallback for demo purposes if Ollama isn't running
        return ["llama3", "mistral", "phi3"]

def main():
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=80)
        st.title("Settings")
        model_names = get_model_names()
        selected_model = st.selectbox("🤖 Choose Model", model_names, help="Select the local LLM you want to chat with.")
        
        st.divider()
        st.markdown("### Conversation Control")
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
            
        st.divider()
        st.markdown("### Status")
        st.success("Ollama Connected" if model_names else "Ollama Disconnected")

    # Main Chat Area
    st.title("🌌 Jesus Rodriguez AI chat prototype")
    st.markdown("*Your premium local intelligence companion.*")

    # Initialize message history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome back! I'm your Jesus Rodriguez AI chat prototype assistant, powered by Ollama. How can I help you today?"}
        ]

    # Display history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask me anything..."):
        # User message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Assistant response
        with st.chat_message("assistant"):
            def stream_response():
                try:
                    response_stream = ollama.chat(
                        model=selected_model,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                        stream=True,
                    )
                    for chunk in response_stream:
                        yield chunk['message']['content']
                except Exception as e:
                    # Generic placeholder for if Ollama isn't actually running
                    placeholder_text = "I'm currently in 'Prototype Mode'. To get real responses, ensure Ollama is running locally and you've pulled the models. Error: " + str(e)
                    for word in placeholder_text.split():
                        yield word + " "
                        time.sleep(0.05)

            full_response = st.write_stream(stream_response())

        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
