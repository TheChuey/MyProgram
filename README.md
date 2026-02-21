# Ollama Streamlit Chatbot

A simple yet powerful chatbot interface built with Streamlit and Ollama.

## Prerequisites

1.  **Ollama**: Ensure Ollama is installed and running on your machine. [Download Ollama](https://ollama.com/).
2.  **Pull a Model**: Make sure you have at least one model pulled (e.g., `ollama pull llama3`).

## Setup

1.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

2.  Run the application:
    ```bash
    streamlit run app.py
    ```

## Features

- **Model Selection**: Choose from any local model available in your Ollama installation.
- **Streaming Responses**: Real-time response generation for a better user experience.
- **Chat History**: Preserves context during your session.
