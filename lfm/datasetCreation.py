# from huggingface_hub import HfApi, HfFolder

# # Initialize the Hugging Face API client
# api = HfApi()

# # Replace "your-username" and "lfm-spectrograms" with your HF username and desired dataset name
# dataset_repo = api.create_repo("mtylek/lfm-spectrograms", repo_type="dataset")


from datasets import load_dataset, Dataset, DatasetDict
from huggingface_hub import HfApi, upload_folder

# Upload the entire folder to the HF Hub
upload_folder(
    repo_id="mtylek/lfm-spectrograms",
    folder_path = r"C:\Users\matth\repos\text2image\lfm",
    repo_type="dataset",
)
