# Voice-Enabled AI Agent Platform

This project is a comprehensive, voice-enabled AI agent platform featuring a modular architecture with a FastAPI backend, a Python-based frontend, and integrations with large language models (LLMs) and Speech-to-Text (STT) services.

## Directory Structure

-   **`/agent-platform`**: A FastAPI-based multi-agent system with services for intent analysis, copywriting, calendar integration, and more.
-   **`/backend`**: The core backend server that handles WebSocket connections and orchestrates communication between different services.
-   **`/frontend`**: A simple Python-based frontend for interacting with the platform.
-   **`/llm`**: Scripts and configurations for running the Gemma-3-27B language model using vLLM.
-   **`/STT-demos`**: Demonstrations for real-time Speech-to-Text using Google's Gemini.
-   **`/test_tts_client.py`**: A test client for the Text-to-Speech (TTS) service.

---

## Agent Platform

The `agent-platform` is a versatile multi-agent system built with FastAPI. It provides a RESTful API for various AI-driven tasks.

### Key Features

-   **Intent Analysis**: Classifies user text into predefined intents.
-   **Copywriting**: Generates text content based on a brief, tone, and length.
-   **Calendar Integration**: Parses natural language to create and manage calendar events.
-   **FAQ Answering**: Provides answers to frequently asked questions using semantic matching.
-   **Analytics**: Summarizes client events and provides business insights.
-   **Context Management**: Stores and retrieves user-specific context.
-   **Pricing Quotes**: Calculates pricing based on items, quantities, and discounts.
-   **Sentiment Analysis**: Determines the emotional tone of a given text.
-   **Escalation Logic**: Decides whether a conversation needs to be escalated to a human agent.
-   **Follow-up Generation**: Creates follow-up messages based on conversation summaries.

### Getting Started

1.  **Navigate to the directory**:
    ```bash
    cd agent-platform
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the server**:
    ```bash
    uvicorn app.main:app --reload --port 7000
    ```

---

## Backend

The backend server is the central hub of the platform, managing WebSocket connections and routing events between different components.

### Features

-   **WebSocket Communication**: Handles real-time, bidirectional communication with clients.
-   **Dynamic Module Loading**: Automatically discovers and imports all submodules on startup.
-   **CORS Enabled**: Allows cross-origin requests for flexible client integrations.

### Running the Backend

1.  **Navigate to the directory**:
    ```bash
    cd backend
    ```
2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the server**:
    ```bash
    uvicorn app.api.main:app --reload --port 8000
    ```

---

## LLM - Gemma-3-27B with vLLM

This project uses the `google/gemma-3-27b-it` model, served with vLLM for high-performance inference.

### Setup

1.  **Prerequisites**:
    -   Docker
    -   NVIDIA Container Toolkit
    -   Hugging Face Token (`HF_TOKEN`)
2.  **Run the model**:
    -   Navigate to the `/llm` directory.
    -   Ensure your `HF_TOKEN` is set in an `.env` file or as an environment variable.
    -   Execute the script:
        ```bash
        ./run_gemma.sh
        ```

---

## STT Demos - Real-time Speech-to-Text

The `STT-demos` directory contains a demonstration of real-time Speech-to-Text using Google's Gemini `gemini-live-2.5-flash-preview` model.

### Configuration

-   Ensure your `GEMINI_API_KEY` is set in your environment.
-   The script uses PyAudio to capture microphone input and streams it to the Gemini API.

### Running the Demo

-   Execute the `flash.py` script to start the real-time transcription.

---

## TTS Client

The `test_tts_client.py` script is a WebSocket-based client for testing the Text-to-Speech functionality. It connects to the backend, sends text, and plays the received audio.

### Usage

-   Run the script to connect to the WebSocket server and interact with the TTS service.

---

## Getting Started with the Full Project

1.  **Start the LLM**: Follow the instructions in the **LLM** section to get the language model running.
2.  **Start the Backend**: Run the backend server as described in the **Backend** section.
3.  **Start the Agent Platform**: Launch the agent platform as detailed in its section.
4.  **Run the Frontend/Clients**: Use the `frontend/main.py`, `STT-demos`, or `test_tts_client.py` to interact with the platform.

## Technologies Used

-   **Backend**: FastAPI, Uvicorn, WebSockets
-   **LLM**: vLLM, Docker, Gemma-3-27B
-   **STT**: Google Gemini
-   **Data Storage**: JSON (for context), SQLite (optional)
-   **Audio**: PyAudio, playsound

