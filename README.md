<h1 align="center">📊 Deepseek Performance Monitoring</h1>

<p align="center">
    <a href="https://github.com/tom-doerr/llm_api_testing/stargazers"
        ><img
            src="https://img.shields.io/github/stars/tom-doerr/llm_api_testing?colorA=2c2837&colorB=c9cbff&style=for-the-badge&logo=starship style=flat-square"
            alt="Repository's starts"
    /></a>
    <a href="https://github.com/tom-doerr/llm_api_testing/issues"
        ><img
            src="https://img.shields.io/github/issues-raw/tom-doerr/llm_api_testing?colorA=2c2837&colorB=f2cdcd&style=for-the-badge&logo=starship style=flat-square"
            alt="Issues"
    /></a>
    <a href="https://github.com/tom-doerr/llm_api_testing/blob/main/LICENSE"
        ><img
            src="https://img.shields.io/github/license/tom-doerr/llm_api_testing?colorA=2c2837&colorB=b5e8e0&style=for-the-badge&logo=starship style=flat-square"
            alt="License"
    /><br />
    <a href="https://github.com/tom-doerr/llm_api_testing/commits/main"
        ><img
            src="https://img.shields.io/github/last-commit/tom-doerr/llm_api_testing/main?colorA=2c2837&colorB=ddb6f2&style=for-the-badge&logo=starship style=flat-square"
            alt="Latest commit"
    /></a>
    <a href="https://github.com/tom-doerr/llm_api_testing"
        ><img
            src="https://img.shields.io/github/repo-size/tom-doerr/llm_api_testing?colorA=2c2837&colorB=89DCEB&style=for-the-badge&logo=starship style=flat-square"
            alt="GitHub repository size"
    /></a>
</p>
  
  <p>
    <strong>A performance monitoring solution for Deepseek API using LiteLLM</strong>
  </p>
</div>

### Performance Plot
![Performance Plot](performance_results/performance_plot.png)

## 🚀 Features
- Measures response latency in milliseconds
- Calculates tokens processed per second
- Runs in 1-minute intervals
- Logs results to CSV file
- Runs for 24 hours

## 🛠️ Usage

1. Ensure LiteLLM is installed and configured
2. Set your Deepseek API key as an environment variable:
```bash
export DEEPSEEK_API_KEY='your_api_key_here'
```

3. Run the script:
```bash
python3 deepseek_performance_monitor.py
```

## 📈 Output

The script creates a CSV file `deepseek_performance.csv` with the following columns:
- timestamp: Measurement time
- first_token_latency_ms: Time to first token in milliseconds
- total_latency_ms: Total response time in milliseconds
- tokens_per_second: Tokens processed per second
- completion_tokens: Total tokens in the response (completion tokens)
- prompt_tokens: Number of tokens in the prompt

## 📋 Example Output

### Performance Statistics
```plaintext
Average TPS: 45.96
Max TPS: 47.43
Min TPS: 44.67

Average First Token Latency: 1030.93 ms
Max First Token Latency: 1184.10 ms
Min First Token Latency: 794.79 ms

Average Total Latency: 17826.14 ms
Max Total Latency: 20675.07 ms
Min Total Latency: 14632.69 ms

Total Completion Tokens Processed: 10657
Total Requests: 13
```
```
2025-01-11 04:02:02 - Latency: 1550.53ms, TPS: 9.67, Tokens: 15
2025-01-11 04:03:04 - Latency: 1317.85ms, TPS: 11.38, Tokens: 15
2025-01-11 04:04:05 - Latency: 1375.23ms, TPS: 10.91, Tokens: 15
```

## 📦 Requirements
- Python 3
- LiteLLM
- Deepseek API key

## 📝 Notes
- The script will run for 24 hours unless interrupted
- Errors are logged to console but don't stop execution
- Results are saved to CSV for later analysis
