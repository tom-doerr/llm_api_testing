#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def has_api_error(row):
    return any('APIError' in str(val) for val in row)

def analyze_data(df, api_errors_in_bad_lines=0):
    # Count different types of errors
    total_errors = df['error'].notna().sum()
    context_size_errors = df['error'].str.contains('ContextWindowExceeded|context length', na=False).sum()
    api_errors = df.apply(has_api_error, axis=1).sum() + api_errors_in_bad_lines
    real_errors = api_errors
    total_requests = len(df) + api_errors_in_bad_lines  # Include bad lines in total
    
    stats = {
        'default': {
            'average_tps': df['tokens_per_second'].mean(),
            'max_tps': df['tokens_per_second'].max(),
            'min_tps': df['tokens_per_second'].min(),
            'average_first_token_latency': df['first_token_latency_ms'].mean(),
            'max_first_token_latency': df['first_token_latency_ms'].max(),
            'min_first_token_latency': df['first_token_latency_ms'].min(),
            'average_total_latency': df['total_latency_ms'].mean(),
            'max_total_latency': df['total_latency_ms'].max(),
            'min_total_latency': df['total_latency_ms'].min(),
            'total_completion_tokens': df['completion_tokens'].sum(),
            'total_prompt_tokens': df['prompt_tokens'].sum(),
            'total_requests': total_requests,
            'average_prompt_tokens': df['prompt_tokens'].mean(),
            'error_rate': (real_errors / total_requests) * 100 if 'error' in df.columns else 0,
            'context_size_errors': context_size_errors
        }
    }
    return stats

def plot_data(df, output_dir, bad_lines_timestamps):
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), height_ratios=[3, 1])
    
    # Top subplot for latency and TPS
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Latency (ms)', color='tab:blue')
    ax1.plot(df['timestamp'], df['first_token_latency_ms'], 
            label='First Token Latency', color='tab:blue', alpha=0.7)
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.legend(loc='upper left')
    
    # Create secondary axis for TPS
    ax1_twin = ax1.twinx()
    ax1_twin.set_ylabel('Tokens per Second', color='tab:red')
    ax1_twin.plot(df['timestamp'], df['tokens_per_second'], 
            label='Tokens per Second', color='tab:red', alpha=0.7)
    ax1_twin.tick_params(axis='y', labelcolor='tab:red')
    ax1_twin.legend(loc='upper right')
    
    # Bottom subplot for error rate
    # Calculate rolling error rate
    window = '15min'  # 15 minute window
    
    # Create a DataFrame with all timestamps including bad lines
    all_errors_df = pd.DataFrame({
        'timestamp': pd.to_datetime(bad_lines_timestamps + df['timestamp'].tolist()),
        'has_api_error': [1] * len(bad_lines_timestamps) + [0] * len(df)
    })
    
    # Calculate rolling error rate
    df_rolling = all_errors_df.set_index('timestamp').resample(window).agg({
        'has_api_error': lambda x: x.sum() / len(x) * 100 if len(x) > 0 else 0
    }).fillna(0)
    
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Error Rate (%)')
    ax2.plot(df_rolling.index, df_rolling['has_api_error'], color='tab:orange', label='Error Rate')
    ax2.fill_between(df_rolling.index, df_rolling['has_api_error'], alpha=0.3, color='tab:orange')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Deepseek API Performance Over Time')
    plt.tight_layout()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save plot
    plot_path = os.path.join(output_dir, 'performance_plot.png')
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path

def main():
    # Read data and capture bad lines
    bad_lines = []
    bad_lines_timestamps = []
    
    def capture_bad_line(x):
        try:
            # Extract timestamp from the start of the line
            timestamp = x[0].split(',')[0]
            if 'APIError' in str(x):
                bad_lines_timestamps.append(timestamp)
            bad_lines.append(x)
        except:
            bad_lines.append(x)
    
    df = pd.read_csv('deepseek_performance.csv', engine='python', on_bad_lines=capture_bad_line)
    
    # Count API errors in bad lines
    api_errors_in_bad_lines = len(bad_lines_timestamps)
    
    # Filter out rows with errors for plotting
    df = df[df['error'].isna()]
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Analyze data
    stats = analyze_data(df, api_errors_in_bad_lines)
    
    # Plot data
    output_dir = 'performance_results'
    plot_path = plot_data(df, output_dir, bad_lines_timestamps)
    
    # Print statistics for each model
    for model, model_stats in stats.items():
        print(f"\nPerformance Statistics for {model}:")
        print(f"Average TPS: {model_stats['average_tps']:.2f}")
        print(f"Max TPS: {model_stats['max_tps']:.2f}")
        print(f"Min TPS: {model_stats['min_tps']:.2f}")
        print(f"\nAverage First Token Latency: {model_stats['average_first_token_latency']:.2f} ms")
        print(f"Max First Token Latency: {model_stats['max_first_token_latency']:.2f} ms")
        print(f"Min First Token Latency: {model_stats['min_first_token_latency']:.2f} ms")
        print(f"\nAverage Total Latency: {model_stats['average_total_latency']:.2f} ms")
        print(f"Max Total Latency: {model_stats['max_total_latency']:.2f} ms")
        print(f"Min Total Latency: {model_stats['min_total_latency']:.2f} ms")
        print(f"\nTotal Completion Tokens: {model_stats['total_completion_tokens']}")
        print(f"Total Prompt Tokens: {model_stats['total_prompt_tokens']}")
        print(f"Average Prompt Tokens: {model_stats['average_prompt_tokens']:.2f}")
        print(f"Total Requests: {model_stats['total_requests']}")
        print(f"API Error Rate: {model_stats['error_rate']:.2f}%")
        print(f"Context Size Errors: {model_stats['context_size_errors']}")
        print(f"Total API Errors: {int(model_stats['error_rate'] * model_stats['total_requests'] / 100)}")
    
    print(f"\nPlot saved to: {plot_path}")

if __name__ == "__main__":
    main()
