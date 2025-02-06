#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

def analyze_data(df):
    stats = {}
    for model in df['model'].unique():
        model_df = df[df['model'] == model]
        stats[model] = {
            'average_tps': model_df['tokens_per_second'].mean(),
            'max_tps': model_df['tokens_per_second'].max(),
            'min_tps': model_df['tokens_per_second'].min(),
            'average_first_token_latency': model_df['first_token_latency_ms'].mean(),
            'max_first_token_latency': model_df['first_token_latency_ms'].max(),
            'min_first_token_latency': model_df['first_token_latency_ms'].min(),
            'average_total_latency': model_df['total_latency_ms'].mean(),
            'max_total_latency': model_df['total_latency_ms'].max(),
            'min_total_latency': model_df['total_latency_ms'].min(),
            'total_completion_tokens': model_df['completion_tokens'].sum(),
            'total_prompt_tokens': model_df['prompt_tokens'].sum(),
            'total_requests': len(model_df),
            'average_prompt_tokens': model_df['prompt_tokens'].mean(),
            'error_rate': (model_df['error'].notna().sum() / len(model_df)) * 100
        }
    return stats

def plot_data(df, output_dir):
    # Create a plot for each model
    for model in df['model'].unique():
        model_df = df[df['model'] == model]
        
        plt.figure(figsize=(12, 6))
        
        # Create primary axis for latency
        ax1 = plt.gca()
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Latency (ms)', color='tab:blue')
        ax1.plot(model_df['timestamp'], model_df['first_token_latency_ms'], 
                label='First Token Latency', color='tab:blue', alpha=0.7)
        ax1.tick_params(axis='y', labelcolor='tab:blue')
        ax1.legend(loc='upper left')
        
        # Create secondary axis for TPS
        ax2 = ax1.twinx()
        ax2.set_ylabel('Tokens per Second', color='tab:red')
        ax2.plot(model_df['timestamp'], model_df['tokens_per_second'], 
                label='Tokens per Second', color='tab:red', alpha=0.7)
        ax2.tick_params(axis='y', labelcolor='tab:red')
        ax2.legend(loc='upper right')
        
        plt.title(f'Deepseek API Performance Over Time - {model}')
        plt.xticks(rotation=45)
        plt.tight_layout()
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Save plot
    plot_path = os.path.join(output_dir, 'performance_plot.png')
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path

def main():
    # Read data and handle error column
    df = pd.read_csv('deepseek_performance.csv', on_bad_lines='skip')
    # Filter out rows with errors for plotting
    df = df[df['error'].isna()]
    
    # Convert timestamp to datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Analyze data
    stats = analyze_data(df)
    
    # Plot data
    output_dir = 'performance_results'
    plot_path = plot_data(df, output_dir)
    
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
        print(f"Error Rate: {model_stats['error_rate']:.2f}%")
    
    print(f"\nPlot saved to: {plot_path}")

if __name__ == "__main__":
    main()
