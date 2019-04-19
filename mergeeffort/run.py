import subprocess
import os

for i in range(10):
    input_file = os.getcwd() + '/input' + str(i) + '.csv'
    output_file = os.getcwd() + '/output' + str(i) + '.csv'
    log_file = os.getcwd() + '/log' + str(i) + '.txt'
    subprocess.run(['screen','-dmL','-Logfile',log_file,'python3','run_repos.py',input_file,output_file])