import streamlit as st
from main import check_api_key, get_ai_response
import time

# Page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .ai-title {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            filter: drop-shadow(0 0 5px #667eea);
        }
        to {
            filter: drop-shadow(0 0 20px #764ba2);
        }
    }
    
    .subtitle {
        text-align: center;
        color: #888;
        font-size: 1.1rem;
        margin-top: 0;
    }
    
    .thinking-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
    
    .thinking-text {
        font-size: 1.5rem;
        color: #667eea;
        font-weight: bold;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<h1 class="ai-title">⚡ NeuralChat AI ⚡</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by OpenAI | Your Intelligent Assistant</p>', unsafe_allow_html=True)
st.markdown("---")

# Check API key on startup
if 'api_key_checked' not in st.session_state:
    api_key = check_api_key()
    if api_key:
        st.session_state.api_key_checked = True
    else:
        st.error("❌ OPENAI_API_KEY not found. Please check your .env file.")
        st.stop()

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar with settings
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Model selection
    model_option = st.selectbox(
        "Select Model",
        options=["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="Choose the AI model to use"
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=0.0,
        step=0.1,
        help="Controls randomness. Lower = more focused, Higher = more creative"
    )
    
    # Timeout input
    timeout = st.number_input(
        "Timeout (seconds)",
        min_value=30,
        max_value=600,
        value=300,
        step=30,
        help="Maximum time to wait for a response"
    )
    
    st.markdown("---")
    
    # Display current settings
    st.markdown("### Current Settings")
    st.info(f"""
    **Model:** {model_option}  
    **Temperature:** {temperature}  
    **Timeout:** {timeout}s
    """)
    
    st.markdown("---")
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 Chat Stats")
    st.metric("Messages", len(st.session_state.messages))

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get AI response with centered thinking indicator
    with st.chat_message("assistant"):
        # Create centered thinking animation
        thinking_placeholder = st.empty()
        thinking_placeholder.markdown(
            '<div class="thinking-container"><div class="thinking-text">🤔 Thinking...</div></div>',
            unsafe_allow_html=True
        )
        
        # Get response from AI
        response = get_ai_response(
            user_message=prompt,
            model=model_option,
            temperature=temperature,
            timeout=timeout
        )
        
        # Clear thinking indicator and show response
        thinking_placeholder.empty()
        st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    