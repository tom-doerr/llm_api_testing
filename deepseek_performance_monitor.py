#!/usr/bin/env python3

import time
import os
import csv
from datetime import datetime, timedelta
from litellm import completion

def measure_request():
    start_time = time.time()
    first_token_time = None
    total_tokens = 0
    
    response = completion(
        model="deepseek/deepseek-chat",
        messages=[{"role": "user", "content": "Tell me about ancient Rome"}],
        stream=True,
        max_tokens=1000
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
    tokens_per_second = total_tokens / (end_time - start_time) if (end_time - start_time) > 0 else 0
    
    return time_to_first_token, total_time, tokens_per_second, total_tokens

def main():
    end_time = datetime.now() + timedelta(hours=24)
    # Check if file exists to determine if we need to write header
    write_header = not os.path.exists('deepseek_performance.csv')
    
    with open('deepseek_performance.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        if write_header:
            writer.writerow([
                'timestamp', 
                'first_token_latency_ms', 
                'total_latency_ms',
                'tokens_per_second', 
                'total_tokens'
            ])
        
        while datetime.now() < end_time:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                first_token_latency, total_latency, tps, tokens = measure_request()
                writer.writerow([
                    timestamp, 
                    first_token_latency, 
                    total_latency,
                    tps, 
                    tokens
                ])
                csvfile.flush()  # Ensure data is written to disk immediately
                print(f"{timestamp} - First Token: {first_token_latency:.2f}ms, Total: {total_latency:.2f}ms, TPS: {tps:.2f}, Tokens: {tokens}")
            except Exception as e:
                print(f"Error: {e}")
            
            # time.sleep(60)
            time.sleep(2)

if __name__ == "__main__":
    main()
