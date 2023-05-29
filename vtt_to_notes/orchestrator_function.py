from subtitle_processor import SubtitleProcessor
# Library to import pre-trained model for sentence embeddings
from sentence_transformers import SentenceTransformer
import glob #for file name reading
import os
from datetime import datetime
import shutil #for auto moving files

#create an instance of the class
processor = SubtitleProcessor()

#import model conditionally
path = "model"
# Check whether the specified path (model/) exists or not
isExist = os.path.exists(path)
if not isExist:
    # if directory does not exist, create directory and import and save SentenceTransformer model
    os.makedirs(path)
    model = SentenceTransformer('all-mpnet-base-v2')
    model.save('model/')
    print("model directory is created and natural language processing model saved")
else: 
    print("natural language processing model already saved")

#get filenames of all vtt files in input folder
filenames = glob.glob('input/*.vtt')
# print(filenames)
#store location of files to go once processed
archive_destination = 'input/processed_files'

#make unique folder to bundle output notes as a processed batch
date_time = datetime.now().strftime("%m%d%Y_%H-%M-%S") #get date and time for output folder for batch
output_batch_folder = f"output/batch_processed_{date_time}" 
os.makedirs(output_batch_folder) 
    
# looping SubtitleProcessor through all vtt files in input folder
for input_file_path in filenames: 
    base_name = os.path.splitext(os.path.basename(input_file_path))[0]  # Extract base file name of input file
    current_date = datetime.now().strftime("%Y%m%d") # Get current date
    output_file_path = f'{output_batch_folder}/notes_{base_name}_{current_date}.txt' #concat unqique file name for output_file
    processor.process_subtitles(input_file_path, output_file_path) #apply function process_subtitles 
    print(f"subtitle file: {input_file_path} successfully processed")
    shutil.move(input_file_path, archive_destination) #move input files into an archive folder
print(f"all .vtt files in input folder processed, bye bye")

#python3 orchestrator_function.py



