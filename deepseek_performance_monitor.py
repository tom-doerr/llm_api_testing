#!/usr/bin/env python3

import time
import os
import csv
import random
import argparse
from datetime import datetime, timedelta
from litellm import completion

def generate_random_prompt():
    """Generate a random prompt with log-distributed length"""
    import random
    import string
    import math
    
    # Generate length with log distribution (more short prompts)
    min_length = 1  
    max_length = 1000000  # Maximum 1 million characters
    log_min = math.log(min_length)
    log_max = math.log(max_length)
    log_length = random.uniform(log_min, log_max)
    length = int(math.exp(log_length))
    
    # Generate random content
    characters = string.ascii_letters + string.digits + string.punctuation + ' '
    content = ''.join(random.choice(characters) for _ in range(length))
    print("content:", content)
    print("length:", length)
    
    return content

def measure_request(model):
    start_time = time.time()
    first_token_time = None
    total_tokens = 0
    prompt_tokens = 0
    
    # Generate random prompt
    prompt_content = generate_random_prompt()
    
    # First get prompt tokens from a non-streaming request
    initial_response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt_content}],
        stream=False,
    )
    prompt_tokens = initial_response.get('usage', {}).get('prompt_tokens', 0)
    
    # Then make the streaming request for timing measurements
    response = completion(
        model=model,
        messages=[{"role": "user", "content": prompt_content}],
        stream=True,
    )
    
    for chunk in response:
        if first_token_time is None:
            first_token_time = time.time()
        content = chunk['choices'][0]['delta'].get('content', '')
        if content:  # Only count tokens if content exists
            total_tokens += len(content.split())
    
    end_time = time.time()
    
    time_to_first_token = (first_token_time - start_time) * 1000 if first_token_time else 0
    total_time = (end_time - start_time) * 1000
    # tokens_per_second = total_tokens / (end_time - start_time) if (end_time - start_time) > 0 else 0
    tokens_per_second = total_tokens / (end_time - first_token_time)
    
    return time_to_first_token, total_time, tokens_per_second, total_tokens, prompt_tokens

def parse_args():
    parser = argparse.ArgumentParser(description='Monitor Deepseek API performance')
    parser.add_argument('--duration', type=int, default=72,
                       help='Duration to run in hours (default: 72)')
    parser.add_argument('--interval', type=int, default=60,
                       help='Interval between requests in seconds (default: 60)')
    parser.add_argument('--output', type=str, default='deepseek_performance.csv',
                       help='Output CSV file (default: deepseek_performance.csv)')
    parser.add_argument('--reasoner-ratio', type=float, default=0.1,
                       help='Probability of using deepseek-reasoner model (default: 0.1)')
    return parser.parse_args()

def main():
    args = parse_args()
    end_time = datetime.now() + timedelta(hours=args.duration)
    # Check if file exists to determine if we need to write header
    write_header = not os.path.exists('deepseek_performance.csv')
    
    with open(args.output, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow([
                'timestamp', 
                'first_token_latency_ms', 
                'total_latency_ms',
                'tokens_per_second', 
                'completion_tokens',
                'prompt_tokens',
                'error',
                'model'
            ])
        
        while datetime.now() < end_time:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Select model based on reasoner ratio
            model = "deepseek/deepseek-reasoner" if random.random() < args.reasoner_ratio else "deepseek/deepseek-chat"
            try:
                first_token_latency, total_latency, tps, tokens, prompt_tokens = measure_request(model)
                writer.writerow([
                    timestamp, 
                    first_token_latency, 
                    total_latency,
                    tps, 
                    tokens,
                    prompt_tokens,
                    '',  # No error
                    model
                ])
                csvfile.flush()  # Ensure data is written to disk immediately
                print(f"{timestamp} - First Token: {first_token_latency:.2f}ms, Total: {total_latency:.2f}ms, TPS: {tps:.2f}, Completion Tokens: {tokens}, Prompt Tokens: {prompt_tokens}")
            except Exception as e:
                error_str = str(e)
                print(f"Error: {error_str}")
                writer.writerow([
                    timestamp, 
                    '',  # No latency data
                    '', 
                    '', 
                    '',
                    '',
                    error_str,
                    model
                ])
                csvfile.flush()
            
            time.sleep(args.interval)

if __name__ == "__main__":
    main()
