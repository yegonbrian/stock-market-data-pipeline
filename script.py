import os

project_dir = '/media/kybrian/SONOY/Pro/PORTFOLIO-PROJECTS/stock-market-data-pipeline'
bash_file = 'project_structure.sh'

with open(bash_file, 'w') as f:
    f.write('#!/bin/bash\n\n')
    
    for root, dirs, files in os.walk(project_dir):
        # Create directories
        for dir_name in dirs:
            dir_path = os.path.relpath(os.path.join(root, dir_name), project_dir)
            f.write(f'mkdir -p {dir_path}\n')
        
        # Create files
        for file_name in files:
            file_path = os.path.relpath(os.path.join(root, file_name), project_dir)
            f.write(f'touch {file_path}\n')

print(f'Bash script {bash_file} created successfully!')
