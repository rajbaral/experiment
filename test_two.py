import os
import shutil
import argparse

# List of directories and files to ignore during copying
EXCLUDE_DIRS = ['bin', 'obj', '.git', '.vs', 'node_modules']
EXCLUDE_FILES = ['*.dll', '*.pdb', '*.exe', '*.cache', '.DS_Store', 'Thumbs.db']

def ignore_patterns(ignore_dirs, ignore_files):
    """Custom ignore function to exclude specific files and directories."""
    def _ignore_patterns(path, names):
        ignored_names = set()
        
        # Ignore directories
        for directory in ignore_dirs:
            if directory in names:
                ignored_names.add(directory)
        
        # Ignore files with specified patterns
        for pattern in ignore_files:
            for name in names:
                if name.endswith(pattern):
                    ignored_names.add(name)
        
        return ignored_names
    return _ignore_patterns

def rename_in_file(file_path, old_name, new_name):
    """Replace old name with new name inside the content of the file."""
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        content = content.replace(old_name, new_name)
        with open(file_path, 'w') as file:
            file.write(content)
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

def create_project_directory(project_name, source, destination):
    """Copy the contents of the template to the new project directory without creating nested directories."""
    project_path = os.path.join(destination, project_name)

    # Create the project directory if it doesn't exist
    if not os.path.exists(project_path):
        os.makedirs(project_path)
    
    # Copy only the contents of the template directory, not the root template folder itself
    print(f"Copying template files from {source} to {project_path}")
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        dest_path = os.path.join(project_path, item)

        # Skip excluded directories and files
        if os.path.isdir(item_path) and os.path.basename(item_path) in EXCLUDE_DIRS:
            print(f"Skipping directory: {item_path}")
            continue
        if os.path.isfile(item_path) and any(item_path.endswith(ext) for ext in EXCLUDE_FILES):
            print(f"Skipping file: {item_path}")
            continue

        # Copy directories or files
        if os.path.isdir(item_path):
            shutil.copytree(item_path, dest_path, ignore=ignore_patterns(EXCLUDE_DIRS, EXCLUDE_FILES), dirs_exist_ok=True)
        else:
            shutil.copy2(item_path, dest_path)

    return project_path

def rename_files_and_content(project_path, new_name, old_name):
    """Rename .csproj, .sln files, and their content inside the project."""
    # Rename .csproj and .sln files in the root and subdirectories
    for root, _, files in os.walk(project_path):
        for file in files:
            if old_name in file:
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, file.replace(old_name, new_name))

                # Rename the file itself
                try:
                    shutil.move(old_file_path, new_file_path)
                    print(f"Renamed: {old_file_path} to {new_file_path}")
                except Exception as e:
                    print(f"Error renaming {old_file_path} to {new_file_path}: {e}")
                
                # Rename occurrences of the old name inside the file content
                rename_in_file(new_file_path, old_name, new_name)

    # Recursively rename inside the rest of the project
    for dirpath, _, filenames in os.walk(project_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rename_in_file(file_path, old_name, new_name)

def create_project(project_name, source, destination="./NewProjects"):
    """Create the project with the specified project name from a template."""
    # Ensure the source path is absolute
    source_path = os.path.abspath(source)
    destination_path = os.path.abspath(destination)

    # Step 1: Create project directory and copy files from the template
    project_path = create_project_directory(project_name, source_path, destination_path)

    # Step 2: Rename files and content
    rename_files_and_content(project_path, project_name, "TemplateProject")

    print(f"Project '{project_name}' successfully created at {project_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a new project from a template.')
    parser.add_argument('project_name', type=str, help='The name of the project to be created')
    parser.add_argument('--source', type=str, default='./template', help='The source directory containing the template files')
    parser.add_argument('--destination', type=str, default='./NewProjects', help='The destination directory where the new project will be created')

    args = parser.parse_args()

    create_project(args.project_name, args.source, args.destination)
