# Yahoo Finance Assistant

<div style="text-align: center;">
  <img src="im/8809337116958753029.gif" alt="Example" />
</div>

This project implements a chatbot that utilizes Yahoo Finance data to aid quantitative analysts. We use the smallest model from Groq API (https://groq.com) to generate responses to user queries.

## Dependencies

- **LangChain**: Language model (LLM) integration. [LangChain GitHub](https://github.com/langchain-ai/langchain)
- **LangSmith**: LangChain debugging and monitoring. [LangSmith GitHub](https://github.com/langchain-ai/langsmith-sdk)
- **yfinance**: Yahoo Finance data. [yfinance GitHub](https://github.com/ranaroussi/yfinance)
- **quantstats**: Stock returns data analysis. [quantstats GitHub](https://github.com/ranaroussi/quantstats)

## Environment Variables

Make sure to set the following environment variables:

- `GROQ_API_KEY`: API key for accessing the Groq service. Obtain this key from [Groq API](https://console.groq.com/keys).
- `LANGCHAIN_TRACING_V2`: Enable LangChain tracing. Set it to `true` to activate tracing.
- `LANGCHAIN_ENDPOINT`: Endpoint for the LangChain API. Set it to `https://api.smith.langchain.com`.
- `LANGCHAIN_API_KEY`: API key for accessing the LangChain service. Obtain this key from [Langchain API](https://smith.langchain.com/).
- `LANGCHAIN_PROJECT`: The project ID for your LangChain project. Find this information in your LangChain project settings.

## Installation

Use pip to install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

To run the assistant, execute:

```bash
chainlit run main.py
```


## License

This project is licensed under the MIT License
