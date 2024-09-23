import os
import shutil
import argparse

# List of directories and files to ignore during copying
EXCLUDE_DIRS = ['bin', 'obj', '.git', '.vs', 'node_modules']
EXCLUDE_FILES = ['*.dll', '*.pdb', '*.exe', '*.cache', '.DS_Store', 'Thumbs.db']

def rename_in_file(file_path, old_name, new_name):
    try:
        with open(file_path, 'r') as file:
            content = file.read()

        content = content.replace(old_name, new_name)

        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

def create_project_directory(project_name, source, destination):
    project_path = os.path.join(destination, project_name)

    # Create the project directory if it doesn't exist
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    # Copy files from the template while excluding unnecessary directories and files
    print(f"Copying template files from {source} to {project_path}")
    shutil.copytree(
        source, 
        project_path, 
        ignore=shutil.ignore_patterns(*EXCLUDE_DIRS, *EXCLUDE_FILES), 
        dirs_exist_ok=True
    )

    return project_path

def rename_files_and_content(project_path, new_name, old_name):
    # Rename .csproj and .sln files
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if old_name in file:
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, file.replace(old_name, new_name))
                
                # First rename the file itself
                try:
                    shutil.move(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} to {new_file_path}")
                except Exception as e:
                    print(f"Error renaming {old_file_path} to {new_file_path}: {e}")
                
                # Then replace occurrences of the old name inside the file content
                rename_in_file(new_file_path, old_name, new_name)

    # Recursively rename inside the rest of the project
    for dirpath, _, filenames in os.walk(project_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rename_in_file(file_path, old_name, new_name)

def create_project(project_name, source, destination="./NewProjects"):
    # Ensure the source path is absolute
    source_path = os.path.abspath(source)
    destination_path = os.path.abspath(destination)

    # Step 1: Create project directory and copy files from the template
    project_path = create_project_directory(project_name, source_path, destination_path)

    # Step 2: Rename files and content
    rename_files_and_content(project_path, project_name, "MyTemplate")

    print(f"Project '{project_name}' successfully created at {project_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a new project from a template.')
    parser.add_argument('project_name', type=str, help='The name of the project to be created')
    parser.add_argument('--source', type=str, default='./template', help='The source directory containing the template files')
    parser.add_argument('--destination', type=str, default='./NewProjects', help='The destination directory where the new project will be created')

    args = parser.parse_args()

    create_project(args.project_name, args.source, args.destination)
