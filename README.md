<h1 align="center">Deepseek Performance Monitoring</h1>

<p align="center">
  <a href="https://github.com/tom_doerr/llm_api_testing/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/tom_doerr/llm_api_testing/ci.yml?style=flat-square" alt="CI Status">
  </a>
  <a href="https://github.com/tom_doerr/llm_api_testing/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/tom_doerr/llm_api_testing?style=flat-square" alt="License">
  </a>
  <a href="https://github.com/tom_doerr/llm_api_testing/releases">
    <img src="https://img.shields.io/github/v/release/tom_doerr/llm_api_testing?style=flat-square" alt="Release">
  </a>
  <a href="https://github.com/tom_doerr/llm_api_testing/issues">
    <img src="https://img.shields.io/github/issues/tom_doerr/llm_api_testing?style=flat-square" alt="Issues">
  </a>
</p>

<p align="center">
  A comprehensive performance monitoring solution for Deepseek API using LiteLLM
</p>

## Features
- Measures response latency in milliseconds
- Calculates tokens processed per second
- Runs in 1-minute intervals
- Logs results to CSV file
- Runs for 24 hours

## Usage

1. Ensure LiteLLM is installed and configured
2. Set your Deepseek API key as an environment variable:
```bash
export DEEPSEEK_API_KEY='your_api_key_here'
```

3. Run the script:
```bash
python3 deepseek_performance_monitor.py
```

## Output

The script creates a CSV file `deepseek_performance.csv` with the following columns:
- timestamp: Measurement time
- first_token_latency_ms: Time to first token in milliseconds
- total_latency_ms: Total response time in milliseconds
- tokens_per_second: Tokens processed per second
- total_tokens: Total tokens in the response

## Example Output
```
2025-01-11 04:02:02 - Latency: 1550.53ms, TPS: 9.67, Tokens: 15
2025-01-11 04:03:04 - Latency: 1317.85ms, TPS: 11.38, Tokens: 15
2025-01-11 04:04:05 - Latency: 1375.23ms, TPS: 10.91, Tokens: 15
```

## Requirements
- Python 3
- LiteLLM
- Deepseek API key

## Notes
- The script will run for 24 hours unless interrupted
- Errors are logged to console but don't stop execution
- Results are saved to CSV for later analysis
