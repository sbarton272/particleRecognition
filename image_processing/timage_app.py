import timage_v0 as tim
import sys

fname = input('paste directory colletion text file name here or type q to quit: ',)
if fname == 'q':
    sys.exit()
with open(fname) as f:
    content = f.readlines()
directory_list = [x.strip('\n') for x in content]

#run the pipeline from timage_v0
tim.adjust_pipeline(directory_list)
