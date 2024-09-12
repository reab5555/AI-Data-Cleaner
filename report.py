import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

REPORT_DIR = f"cleaning_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(REPORT_DIR, exist_ok=True)

def save_plot(fig, filename):
    fig.savefig(os.path.join(REPORT_DIR, filename), dpi=400, bbox_inches='tight')
    plt.close(fig)

def plot_heatmap(df, title):
    plt.figure(figsize=(12, 8))
    sns.heatmap(df.isnull(), cbar=False, cmap='Reds')
    plt.title(title)
    plt.tight_layout()
    save_plot(plt.gcf(), f'{title.lower().replace(" ", "_")}.png')


def plot_valid_data_percentage(original_df, cleaned_df):
    original_valid = (original_df.notna().sum() / len(original_df)) * 100
    cleaned_valid = (cleaned_df.notna().sum() / len(cleaned_df)) * 100
    
    # Combine the data and fill missing values with 0
    combined_data = pd.concat([original_valid, cleaned_valid], axis=1, keys=['Original', 'Cleaned']).fillna(0)
    
    plt.figure(figsize=(15, 8))
    
    x = range(len(combined_data))
    width = 0.35
    
    plt.bar(x, combined_data['Original'], width, label='Before Cleaning', alpha=0.8)
    plt.bar([i + width for i in x], combined_data['Cleaned'], width, label='After Cleaning', alpha=0.8)
    
    plt.xlabel('Columns')
    plt.ylabel('Percentage of Valid Data')
    plt.title('Percentage of Valid Data Before and After Cleaning')
    plt.xticks([i + width/2 for i in x], combined_data.index, rotation=90)
    plt.legend()
    
    # Add percentage labels on the bars with smaller font size
    for i, v in enumerate(combined_data['Original']):
        plt.text(i, v, f'{v:.1f}%', ha='center', va='bottom', fontsize=6)
    for i, v in enumerate(combined_data['Cleaned']):
        plt.text(i + width, v, f'{v:.1f}%', ha='center', va='bottom', fontsize=6)
    
    plt.tight_layout()
    plt.savefig(os.path.join(REPORT_DIR, 'valid_data_percentage.png'))
    plt.close()

def plot_column_schemas(df):
    schemas = df.dtypes.astype(str).value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Generate a color palette with as many colors as there are bars
    colors = plt.cm.rainbow(np.linspace(0, 1, len(schemas)))
    
    # Plot the bars
    bars = ax.bar(schemas.index, schemas.values, color=colors)
    
    ax.set_title('Column Data Types')
    ax.set_xlabel('Data Type')
    ax.set_ylabel('Count')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}',
                ha='center', va='bottom')
    
    save_plot(fig, 'column_schemas.png')

def plot_nonconforming_cells(nonconforming_cells):
    # Ensure that nonconforming_cells is a dictionary
    if isinstance(nonconforming_cells, dict):
        # Proceed with plotting if it's a dictionary
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Generate a color palette with as many colors as there are bars
        colors = plt.cm.rainbow(np.linspace(0, 1, len(nonconforming_cells)))
        
        # Plot the bars
        bars = ax.bar(list(nonconforming_cells.keys()), list(nonconforming_cells.values()), color=colors)
        
        ax.set_title('Nonconforming Cells by Column')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Number of Nonconforming Cells')
        plt.xticks(rotation=90)
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:,}',
                    ha='center', va='bottom')
        
        save_plot(fig, 'nonconforming_cells.png')
    else:
        print(f"Expected nonconforming_cells to be a dictionary, but got {type(nonconforming_cells)}.")



def plot_column_distributions(original_df, cleaned_df):
    numeric_columns = original_df.select_dtypes(include=[np.number]).columns
    num_columns = len(numeric_columns)

    if num_columns == 0:
        print("No numeric columns found for distribution plots.")
        return

    # Create subplots for distributions
    fig, axes = plt.subplots(nrows=(num_columns + 2) // 3, ncols=3, figsize=(18, 5 * ((num_columns + 2) // 3)))
    axes = axes.flatten() if num_columns > 1 else [axes]

    for i, column in enumerate(numeric_columns):
        if column in cleaned_df.columns:
            sns.histplot(original_df[column].dropna(), ax=axes[i], kde=True, color='blue', label='Before Cleaning', alpha=0.5)
            sns.histplot(cleaned_df[column].dropna(), ax=axes[i], kde=True, color='orange', label='After Cleaning', alpha=0.5)
            axes[i].set_title(f'{column} - Distribution Before & After Cleaning')
            axes[i].legend()

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    save_plot(fig, 'distributions_before_after_cleaning.png')


def plot_boxplot_with_outliers(df):
    print("Plotting boxplots with outliers...")
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    num_columns = len(numeric_columns)

    if num_columns == 0:
        print("No numeric columns found for boxplot.")
        return

    # Create subplots based on the number of numeric columns
    fig, axes = plt.subplots(nrows=(num_columns + 2) // 3, ncols=3, figsize=(15, 5 * ((num_columns + 2) // 3)))
    axes = axes.flatten() if num_columns > 1 else [axes]

    for i, column in enumerate(numeric_columns):
        sns.boxplot(x=df[column], ax=axes[i])
        axes[i].set_title(f'Boxplot of {column} with Outliers')

    # Remove any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    save_plot(fig, 'boxplots_with_outliers.png')


def plot_correlation_heatmap(df):
    # Select only numeric, float, and integer columns
    numeric_df = df.select_dtypes(include=[np.number])

    # Compute the correlation matrix
    correlation_matrix = numeric_df.corr()

    # Plot the heatmap
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax, cbar_kws={'label': 'Correlation'})
    ax.set_title('Correlation Heatmap')
    save_plot(fig, 'correlation_heatmap.png')



def plot_process_times(process_times):
    # Convert seconds to minutes
    process_times_minutes = {k: v / 60 for k, v in process_times.items()}

    # Separate main processes and column cleaning processes
    main_processes = {k: v for k, v in process_times_minutes.items() if not k.startswith("Clean column:")}
    column_processes = {k: v for k, v in process_times_minutes.items() if k.startswith("Clean column:")}

    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))

    # Plot main processes
    bars1 = ax1.bar(main_processes.keys(), main_processes.values())
    ax1.set_title('Main Process Times')
    ax1.set_ylabel('Time (minutes)')
    ax1.tick_params(axis='x', rotation=45)

    # Plot column cleaning processes
    bars2 = ax2.bar(column_processes.keys(), column_processes.values())
    ax2.set_title('Column Cleaning Times')
    ax2.set_ylabel('Time (minutes)')
    ax2.tick_params(axis='x', rotation=90)

    # Add value labels on top of each bar
    for ax, bars in zip([ax1, ax2], [bars1, bars2]):
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{height:.2f}', ha='center', va='bottom')

    # Add total time to the plot
    total_time = sum(process_times_minutes.values())
    fig.suptitle(f'Process Times (Total: {total_time:.2f} minutes)', fontsize=16)

    plt.tight_layout()
    save_plot(fig, 'process_times.png')


def create_full_report(original_df, cleaned_df, nonconforming_cells_before, process_times, removed_columns, removed_rows):
    os.makedirs(REPORT_DIR, exist_ok=True)

    sns.set_style("whitegrid")
    plt.rcParams['figure.dpi'] = 400

    print("Plotting valid data percentages...")
    plot_valid_data_percentage(original_df, cleaned_df)

    print("Plotting column schemas...")
    plot_column_schemas(cleaned_df)

    print("Plotting nonconforming cells before cleaning...")
    plot_nonconforming_cells(nonconforming_cells_before)

    print("Plotting column distributions...")
    plot_column_distributions(original_df, cleaned_df)

    print("Plotting process times...")
    plot_process_times(process_times)

    print("Plotting heatmaps...")
    plot_heatmap(original_df, "Missing Values Before Cleaning")

    print("Plotting correlation heatmap...")
    plot_correlation_heatmap(cleaned_df)

    print(f"All visualization reports saved in directory: {REPORT_DIR}")