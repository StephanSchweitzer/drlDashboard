import os
import pandas as pd

def get_model_folders(base_directory):
    return [
        folder for folder in os.listdir(base_directory)
        if os.path.isdir(os.path.join(base_directory, folder))
    ]

def get_metrics_files(selected_model_folders, base_directory):
    """Returns a list of metrics CSV base filenames from selected model folders."""
    metrics_files = set()
    for model_folder in selected_model_folders:
        metrics_dir = os.path.join(base_directory, model_folder, "metrics")
        if os.path.exists(metrics_dir):
            metrics_files.update([
                os.path.splitext(f)[0]  # Base name without extension
                for f in os.listdir(metrics_dir)
                if f.endswith(".csv")
            ])
    return sorted(list(metrics_files))

def load_and_combine_data(selected_models, selected_metrics_files, base_directory):
    """Loads and combines metrics and hyperparameters data for selected models and metrics files."""
    data_list = []
    for model_folder in selected_models:
        model_path = os.path.join(base_directory, model_folder)
        for base_name in selected_metrics_files:
            metrics_path = os.path.join(model_path, "metrics", f"{base_name}.csv")
            hyperparams_path = os.path.join(model_path, "hyperparameters", f"{base_name}_hyperparameters.csv")
            if os.path.exists(metrics_path) and os.path.exists(hyperparams_path):
                try:
                    metrics_df = pd.read_csv(metrics_path)
                    hyperparams_df = pd.read_csv(hyperparams_path)
                    # Add model and base_name to identify data
                    metrics_df['model'] = model_folder
                    metrics_df['metrics_file'] = base_name
                    data_list.append({'metrics': metrics_df, 'hyperparams': hyperparams_df, 'model': model_folder, 'metrics_file': base_name})
                except Exception as e:
                    print(f"Error loading data for model {model_folder}, file {base_name}: {e}")
    return data_list
