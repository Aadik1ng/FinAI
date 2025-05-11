import subprocess
import os
from datetime import datetime

def get_tracked_files():
    """Get list of files that are not ignored by git"""
    result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True, text=True)
    untracked = result.stdout.strip().split('\n')
    
    result = subprocess.run(['git', 'ls-files'], capture_output=True, text=True)
    tracked = result.stdout.strip().split('\n')
    
    return set(tracked + untracked)

def read_commit_messages():
    """Read commit messages from file_mapping.txt"""
    messages = {}
    with open('file_mapping.txt', 'r') as f:
        current_section = None
        for line in f:
            line = line.strip()
            if line.startswith('##'):
                current_section = line[3:].strip()
            elif line.startswith('-') and ':' in line:
                # Extract file path and message from lines like "- file_path: message"
                parts = line[1:].strip().split(':', 1)
                if len(parts) == 2:
                    file_path = parts[0].strip()
                    message = parts[1].strip()
                    messages[file_path] = message
    return messages

def commit_files():
    """Commit files with their specific messages"""
    messages = read_commit_messages()
    
    # Initialize git if not already initialized
    if not os.path.exists('.git'):
        subprocess.run(['git', 'init'])
        
    # Create or checkout main branch
    try:
        subprocess.run(['git', 'checkout', 'main'], check=False)
    except:
        subprocess.run(['git', 'checkout', '-b', 'main'], check=False)
    
    # First, add this script itself
    if os.path.exists('commit_script.py'):
        subprocess.run(['git', 'add', 'commit_script.py'])
        subprocess.run(['git', 'commit', '-m', 'Add commit script for automated file commits'])
        subprocess.run(['git', 'push', 'origin', 'main'])
        print("Committed commit_script.py to repository")
    
    # Commit each file with its specific message
    for file_path, message in messages.items():
        print(f"\nProcessing: {file_path} with message: {message}")
        if file_path.endswith('/'):
            # It's a directory
            if not os.path.exists(file_path):
                os.makedirs(file_path, exist_ok=True)
                print(f"Created directory: {file_path}")
            
            # Create a placeholder file if directory is empty
            placeholder_file = os.path.join(file_path, "README.md")
            if not os.listdir(file_path) or not any(f for f in os.listdir(file_path) if not f.startswith('.')):
                with open(placeholder_file, 'w') as f:
                    f.write(f"# {file_path}\n\n{message}")
                print(f"Created placeholder README.md in {file_path}")
            
            # Force add all files in the directory
            if os.path.exists(file_path):
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        file_to_add = os.path.join(root, file)
                        # Force add even if in gitignore
                        subprocess.run(['git', 'add', '-f', file_to_add])
                        print(f"Force-added: {file_to_add}")
                
                # Commit with the specific description
                subprocess.run(['git', 'commit', '-m', message])
                print(f"Committed directory {file_path}")
                
                # Push to main branch
                subprocess.run(['git', 'push', 'origin', 'main'])
                print(f"Pushed {file_path} to main branch")
        else:
            # It's a file
            if os.path.exists(file_path):
                # Force add the file even if in gitignore
                subprocess.run(['git', 'add', '-f', file_path])
                print(f"Force-added: {file_path}")
                
                # Commit with the specific description
                subprocess.run(['git', 'commit', '-m', message])
                print(f"Committed {file_path}")
                
                # Push to main branch
                subprocess.run(['git', 'push', 'origin', 'main'])
                print(f"Pushed {file_path} to main branch")
            else:
                print(f"File not found: {file_path} - creating placeholder")
                # Create directory if needed
                dir_path = os.path.dirname(file_path)
                if dir_path and not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                
                # Create placeholder file
                with open(file_path, 'w') as f:
                    f.write(f"# {file_path}\n\n{message}")
                
                # Force add and commit the placeholder
                subprocess.run(['git', 'add', '-f', file_path])
                subprocess.run(['git', 'commit', '-m', message])
                subprocess.run(['git', 'push', 'origin', 'main'])
                print(f"Created, committed and pushed placeholder for {file_path}")
    
    # Final push to make sure everything is pushed
    subprocess.run(['git', 'push', 'origin', 'main'])
    print("\nPushed all commits to main branch")

if __name__ == "__main__":
    commit_files() 