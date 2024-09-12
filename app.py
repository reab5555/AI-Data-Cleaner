import gradio as gr
import pandas as pd
from clean import clean_data
from report import create_full_report, REPORT_DIR
import os
import tempfile

def clean_and_visualize(file, progress=gr.Progress()):
    # Load the data
    df = pd.read_csv(file.name)
    
    # Clean the data
    cleaned_df = None
    nonconforming_cells_before = None
    process_times = None
    removed_columns = None
    removed_rows = None
    
    for progress_value, status_text in clean_data(df):
        if isinstance(status_text, tuple):
            cleaned_df, nonconforming_cells_before, process_times, removed_columns, removed_rows = status_text
            progress(progress_value, desc="Cleaning completed")
        else:
            progress(progress_value, desc=status_text)
    
    # Generate full visualization report
    create_full_report(
        df,
        cleaned_df,
        nonconforming_cells_before,
        process_times,
        removed_columns,
        removed_rows
    )
    
    # Save cleaned DataFrame to a temporary CSV file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
        cleaned_df.to_csv(tmp_file.name, index=False)
        cleaned_csv_path = tmp_file.name
    
    # Collect all generated images
    image_files = [os.path.join(REPORT_DIR, f) for f in os.listdir(REPORT_DIR) if f.endswith('.png')]
    
    return cleaned_csv_path, image_files

def launch_app():
    with gr.Blocks() as app:
        gr.Markdown("# AI Data Cleaner")
        
        with gr.Row():
            file_input = gr.File(label="Upload CSV File", file_count="single", file_types=[".csv"])
        
        with gr.Row():
            clean_button = gr.Button("Start Cleaning")
        
        with gr.Row():
            progress_bar = gr.Progress()
        
        with gr.Row():
            cleaned_file_output = gr.File(label="Cleaned CSV", visible=True)
        
        with gr.Row():
            output_gallery = gr.Gallery(
                label="Visualization Results", 
                show_label=True, 
                elem_id="gallery", 
                columns=[3],
                rows=[3], 
                object_fit="contain", 
                height="auto",
                visible=False  # Initially set to invisible
            )
        
        def process_and_show_results(file):
            cleaned_csv_path, image_files = clean_and_visualize(file, progress=progress_bar)
            return (
                cleaned_csv_path,
                gr.Gallery(visible=True, value=image_files)  # Make gallery visible and update its content
            )
        
        clean_button.click(
            fn=process_and_show_results,
            inputs=file_input,
            outputs=[cleaned_file_output, output_gallery]
        )
    
    app.launch()

if __name__ == "__main__":
    launch_app()