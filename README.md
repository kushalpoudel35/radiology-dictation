# radiology-dictation
Python script to dictate locally using Google's MedASR model

## Step 1: Install Python

Go to python.org/downloads and download Python.
Run the installer and tick “Add Python to PATH” at the bottom of the first screen, then click Install.

## Step 2: Get access to the model

Create a free account at huggingface.co and log in.
Open huggingface.co/google/medasr and accept the license if it asks.
Go to Settings → Access Tokens → create a token (Read type) and copy it.

## Step 3: Install the tools
Press the Windows key, type cmd, and open it. Paste these one at a time:
```
mkdir C:\medasr
cd C:\medasr
python -m venv env
env\Scripts\activate
pip install "transformers>=5.0.0" torch librosa sounddevice numpy pyperclip huggingface_hub
```

This takes a few minutes. Then log in:
```
hf auth login
```

Paste your token when asked. Nothing shows as you paste, which is normal.

## Step 4: Create the dictation script

Copy the `dictate.py` file into `C:\medasr` folder.

## Step 5: Run it
- Copy the `MedASR.bat` file into `C:\medasr` folder.
- Double click to run it.
- The first run downloads the model, so wait for “Loading model...”. Then press Enter, speak, press Enter again, and the text appears and is copied to the clipboard. As long as you repeat this, the text is added to the running report.
- The clipboard always holds the whole report so far, with sections separated by a blank line. So you can paste once at the end, or after each section.
- Type n then Enter to start a new report. Do this between patients so reports don’t mix.
- Type s then Enter to print the full report.
- Type q then Enter to quit.