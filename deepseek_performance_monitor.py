import time
import csv
from datetime import datetime, timedelta
from litellm import completion

def measure_request():
    start_time = time.time()
    response = completion(
        model="deepseek/deepseek-chat",
        messages=[{"role": "user", "content": "Tell me about ancient Rome"}]
    )
    end_time = time.time()
    
    latency = (end_time - start_time) * 1000
    total_tokens = response['usage']['total_tokens']
    elapsed_time = end_time - start_time
    tokens_per_second = total_tokens / elapsed_time if elapsed_time > 0 else 0
    
    return latency, tokens_per_second, total_tokens

def main():
    end_time = datetime.now() + timedelta(hours=24)
    with open('deepseek_performance.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['timestamp', 'latency_ms', 'tokens_per_second', 'total_tokens'])
        
        while datetime.now() < end_time:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
                latency, tps, tokens = measure_request()
                writer.writerow([timestamp, latency, tps, tokens])
                print(f"{timestamp} - Latency: {latency:.2f}ms, TPS: {tps:.2f}, Tokens: {tokens}")
            except Exception as e:
                print(f"Error: {e}")
            
            # time.sleep(60)
            time.sleep(2)

if __name__ == "__main__":
    main()
