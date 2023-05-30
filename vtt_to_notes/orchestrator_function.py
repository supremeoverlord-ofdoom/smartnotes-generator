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
    model = SentenceTransformer('all-mpnet-base-v2') #this model is big so if you don't have much local storage just delete the models folder after running script
    model.save('model/')
    print("model directory is created and natural language processing model saved")
else: 
    print("natural language processing model already saved")

#get filenames of all vtt files in input folder
filenames = glob.glob('input/*.vtt')
# print(filenames)


#only run loop if inputs folder has .vtt files inside it
if filenames == []:
    print("No .vtt files detected in inputs folder, drop some in and try running orchestrator_function.py again")
else: 
    date_time = datetime.now().strftime("%m%d%Y_%H-%M-%S") #get date and time for folder name for batch
    #make unique folder to bundle output notes as a processed batch
    output_batch_folder = f"output/batch_processed_{date_time}" 
    os.makedirs(output_batch_folder) 
    #make unique folder to bundle input notes for archiving
    input_batch_folder = f"input/processed_files/batch_processed_{date_time}" 
    os.makedirs(input_batch_folder) 
    
    # looping SubtitleProcessor through all vtt files in input folder
    for input_file_path in filenames: 
        base_name = os.path.splitext(os.path.basename(input_file_path))[0]  # Extract base file name of input file
        current_date = datetime.now().strftime("%Y%m%d") # Get current date
        output_file_path = f'{output_batch_folder}/notes_{base_name}_{current_date}.txt' #concat unique file name for output_file
        processor.process_subtitles(input_file_path, output_file_path) #apply function process_subtitles 
        print(f"subtitle file: {input_file_path} successfully processed")
        shutil.move(input_file_path, input_batch_folder) #move input files into an archive folder
    print(f"all .vtt files in input folder processed, bye bye")

#command to run script
#python3 orchestrator_function.py



