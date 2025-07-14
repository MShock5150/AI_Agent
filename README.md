# AI Agent with Function Calling

## Project Overview

This project is a Python-based AI agent that leverages the OpenAI API to perform tasks by interacting with external tools through **function calling**. The primary goal of this project was to explore the practical application of Large Language Models (LLMs) in building autonomous agents that can execute real-world actions, such as fetching live data from an API.

The agent is capable of understanding a user's request, determining which available tool is needed to fulfill it, and then calling that tool with the correct parameters.

## Key Features & Design

* **LLM Integration:** Utilizes the OpenAI API to power the agent's reasoning and decision-making capabilities.
* **Function Calling:** Implements the "function calling" pattern, allowing the LLM to request the execution of predefined Python functions.
* **External Tooling:** Includes example tools that can be called by the agent, such as fetching the current price of a stock or the current weather in a given location.
* **Structured Output:** The agent is designed to receive structured data (JSON) from the tools it calls and use that data to formulate a natural language response.
* **Extensible Architecture:** The system is designed to be easily extensible, allowing new tools and functions to be added to expand the agent's capabilities.

## How It Works

1.  A user provides a prompt to the agent (e.g., "What is the current price of NVDA?").
2.  The prompt, along with a list of available Python functions, is sent to the OpenAI API.
3.  The LLM analyzes the prompt and determines that the `get_stock_price` function is needed. It then returns a request to call that function with the appropriate argument (`ticker="NVDA"`).
4.  The Python script executes the local `get_stock_price` function, which fetches the data from an external financial API.
5.  The data returned by the function is sent back to the LLM in a second API call.
6.  The LLM uses this new information to generate a final, natural language answer for the user (e.g., "The current price of NVDA is $123.45.").

## How to Run

To run the agent, you will need an OpenAI API key.

1.  **Install Dependencies:**
    ```bash
    pip install openai
    ```
2.  **Set API Key:**
    Set your OpenAI API key as an environment variable.
    * On Linux/macOS:
        ```bash
        export OPENAI_API_KEY='your_api_key_here'
        ```
    * On Windows:
        ```bash
        set OPENAI_API_KEY='your_api_key_here'
        ```
3.  **Run the Agent:**
    From the root of the project directory, run the main script:
    ```bash
    python3 src/main.py
    ```

---

*This project was built as part of the backend development curriculum on [Boot.dev](https://www.boot.dev) to explore advanced AI agent architecture.*
