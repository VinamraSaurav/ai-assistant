# AI Assistant

An advanced AI-driven personal assistant designed to assist with a variety of tasks, including web searches, YouTube video lookups, and AI-powered chat responses via Gemini AI. This assistant uses voice commands for natural interaction and supports text-based fallback.

---

## Features

- **Gemini AI Integration**: Offers intelligent chat responses powered by Gemini AI.
- **YouTube Search**: Finds and opens YouTube videos based on user queries.
- **Web Search**: Performs Google searches directly from voice or text commands.
- **Voice Interaction**: Supports speech recognition and text-to-speech synthesis.
- **Fallback Input**: Accepts typed commands if voice input fails.

---

## Installation and Setup

Follow these steps to set up and run the AI Assistant:

### Prerequisites
1. Install [Python](https://www.python.org/downloads/) (version 3.8 or above).
2. Install `virtualenv` for creating isolated environments:
   ```bash
   pip install virtualenv
   ```

### Clone the Repository
Clone the project repository from GitHub:
```bash
git clone https://github.com/VinamraSaurav/ai-assistant.git
cd ai-assistant
```

### Create a Virtual Environment
1. Create a virtual environment:
   ```bash
   virtualenv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

### Install Dependencies
Install the required Python libraries:
```bash
pip install -r requirements.txt
```

### Configure Environment Variables
1. Rename `.env.example` to `.env`:
   ```bash
   mv .env.example .env
   ```
2. Update the `.env` file with your configuration:
   - Gemini AI API Key
   - Email address and password for email-related functionality

### Run the Assistant
Start the assistant by running the following command:
```bash
python assistant.py
```

---

## Usage

- **Voice Command**: Speak commands such as "search the web for Python tutorials" or "play relaxing music on YouTube."
- **Text Input**: If voice input fails, type your commands when prompted.
- **Exit**: To stop the assistant, say or type "exit," "bye," or "quit."

---

## Contributions
Contributions to improve the assistant are welcome! Feel free to submit a pull request or open an issue on the GitHub repository.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

**Developed by [Vinamra Saurav](https://github.com/VinamraSaurav).**
