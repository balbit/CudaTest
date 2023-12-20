# CudaTest

Want to practice CUDA but only have access to Colab's computing resources?

Use this script to automatically upload your files to Drive, mount your Drive folder on Colab, and run it there!

For running CUDA code on Colab please refer to [this tutorial](https://github.com/notY0rick/cuda_practice)

## Setup

To get started with CudaTest, follow these steps:

1. Create a Google Drive folder, which you will be mounting on Colab
2. Set up a Drive API
   - Create a service account with access to your drive
   - Share your folder with this service account's email (probably called `something@project.iam.gserviceaccount.com`)
   - Copy your folder ID (navigate to the folder. In the URL, copy the LONG_ID of `drive/folders/{LONG_ID}`)
   - Create a json key for this account and store it somewhere secure
   - Update `utils/defaults.json` with a path to your API key and folder ID
3. Install stuff with
   - `pip install --upgrade google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib`

## Running

Develop in the repository. When you're ready to upload to Drive for testing, just run 

`python3 upload_to_drive.py file_name`!

The files should be uploaded/updated in Colab very quickly, and you can execute your testing scripts there.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).


Author: Elliot Liu
