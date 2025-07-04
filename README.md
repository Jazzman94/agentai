# 🤖 AgentAI

AgentAI is a simple CLI agent that uses [Google AI](https://ai.google.dev/) *gemini-2.0-flash-001 model* to perform various file and code operations through natural language commands.

## ✨ Features

- 📁 List files and directories
- 📖 Read file contents
- 🐍 Execute Python files with optional arguments
- ✍️ Write or overwrite files
- 🗣️ Natural language interaction via CLI

## 🎯 Motivation

AgentAI CLI was coded in semi-guided project from the [Boot.dev](https://www.boot.dev/courses/build-ai-agent-python) course. Special thanks to the Boot.dev team for the excellent guided projects and learning materials!

## 🔧 Installation

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Jazzman94/agentai.git
   cd agentai
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```
   
   If you don't have uv installed, install it with: `pip install uv`

3. **Set up API key:**
   - Create your API key in [Google AI Studio](https://ai.google.dev/gemini-api/docs/api-key#best_practices)
   - Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

4. **Test installation:**
   ```bash
   python main.py "Hello world!" --verbose
   ```

## ⚡ Usage

### Basic Commands

```bash
# Basic interaction
python main.py "List all Python files in the current directory"

# Verbose mode for detailed output
python main.py "Read the contents of lorem.txt" --verbose

# File operations
python main.py "Create a new file called test.py with a hello world function"

# Code execution
python main.py "Run the calculator.py file with argument 5"
```

### Configuration

The agent's behavior is controlled by the `prompts.system_prompt` variable, which defines the CLI agent's purpose and capabilities.

Important configuration parameters in `config.py`:

```python
MAX_CHARS = 10000      # Maximum characters per message
WORKING_DIR = "./calculator"  # Working directory for operations
MAX_ITERS = 20         # Maximum iterations in single request
```

Feel free to adjust these values based on your needs:
- Change `WORKING_DIR` to point to your desired working directory
- Modify `MAX_CHARS` to allow longer/shorter messages
- Adjust `MAX_ITERS` for more complex operations

### 🚀 Advanced Usage

Don't hesitate to experiment! Here's how to test the agent's full potential:

#### Example: Building a REST API

1. **Create a new working directory:**
   ```bash
   mkdir example
   ```

2. **Update configurateion**
   ```python
   # In config.py
   WORKING_DIR = "./example"
   ```
3. **Run a complex task**
- Run for example following:
```bash
python main.py "Create a simple REST API server using FastAPI framework with simple GET, POST, PUT, DELETE endpoints. Write down a manual how to run it and test it properly. Provide me a list of needed packages to install."
```

## 📁 Project Structure

```
agentai/
├── main.py           # Entry point
├── config.py         # Configuration settings
├── prompts.py        # System prompts
├── .env              # API keys (create this)
├── pyproject.toml    # Dependencies
└── README.md
```

## 🙏 Acknowledgments

- [Boot.dev](https://www.boot.dev/) for the excellent AI agent course
- Google AI team for the Gemini API

⭐ If you find this project helpful, please give it a star on GitHub!