# smartnotes-generator

This repo can be run locally to convert transcript files from videos into notes to help automate your study workflow or if you just don't want to watch a video and prefer reading notes. This is useful if you can't download an audio file to convert to text.

You can extract these files by:

1. go to developer tools in browser by going inspecting page containing the video
2. go to network tab and search for "subtitle" or "transcript" (may have to refresh page for file to appear)
3. when the file appears click right click it and select 'open in new tab'
4. download file

NOTE: these scripts **currently are only set up to process .vtt** files
So if a video uses different format of transcript files (eg json ect) it won't detect or be able to process it

### Set Up Steps for Project

1. Fork and clone repo
2. Once you have cloned the repo locally, create virtual environment (make sure you are in the root directory)
   `python3 -m venv venv`

3. Activate virtual environment
   `source ~/venv/bin/activate`

4. Install requirements
   `pip install -r requirements.txt`

5. Optional but recommended - set python version (NOTE command requires pyenv https://github.com/pyenv/pyenv)
   `pyenv install $(cat .python-version) && pyenv local $(cat .python-version)`

## Running Project

1. go into the vtt_to_notes/ folder
`cd vtt_to_notes`

2. drop any number of files you want to convert, into folder: vtt_to_notes/input

3. run the orchestrator_function.py script
`python3 orchestrator_function.py`

- your transcript should now be processed and you can find the output text files in the vtt_to_notes/output folder batched into timestamped folder
- if you need to cross check any of the txt files with the source transcripts, you can search for the same timestamped folder name in the vtt_to_notes/input/processed_files folder and you will find you source transcripts there

## Flow Chart of Project

![Flow Chart](/documentation/overall-process-flowchart.jpg)
