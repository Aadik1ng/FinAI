#!/bin/bash

# Initialize git if not already initialized
if [ ! -d .git ]; then
    git init
    git branch -M main
fi

# Function to process each file entry
process_file() {
    local file_path="$1"
    local description="$2"
    
    # Skip if it's a directory or empty
    if [[ -z "$file_path" ]] || [[ "$file_path" == */ ]]; then
        return
    fi
    
    # Check if file exists
    if [ ! -f "$file_path" ]; then
        echo "Warning: File $file_path does not exist, skipping..."
        return
    fi
    
    echo "Processing: $file_path"
    echo "Description: $description"
    
    # Add the file to git
    git add "$file_path"
    
    # Check if the file was actually added
    if git diff --staged --quiet; then
        echo "No changes to commit for $file_path"
        return
    fi
    
    # Commit with the specific description for this file
    git commit -m "$description"
    
    # Push to main branch
    git push origin main
    
    echo "Successfully committed and pushed $file_path with message: $description"
    echo "----------------------------------------"
}

# First, add all Python files in src and its subdirectories
find src -name "*.py" -type f | while read -r file; do
    description=""
    # Get the description from file_mapping.txt
    while IFS= read -r line; do
        if [[ "$line" == *"$(basename "$file")"* ]]; then
            description=$(echo "$line" | cut -d':' -f2- | sed 's/^ //')
            break
        fi
    done < file_mapping.txt
    
    if [ -n "$description" ]; then
        process_file "$file" "$description"
    else
        # If no description found, use a default one
        process_file "$file" "Added $(basename "$file") to the project"
    fi
done

# Add all Python files in tests directory
find tests -name "*.py" -type f | while read -r file; do
    description=""
    # Get the description from file_mapping.txt
    while IFS= read -r line; do
        if [[ "$line" == *"$(basename "$file")"* ]]; then
            description=$(echo "$line" | cut -d':' -f2- | sed 's/^ //')
            break
        fi
    done < file_mapping.txt
    
    if [ -n "$description" ]; then
        process_file "$file" "$description"
    else
        # If no description found, use a default one
        process_file "$file" "Added test file $(basename "$file")"
    fi
done

# Process root level files
while IFS= read -r line; do
    # Skip empty lines and headers
    if [[ -z "$line" ]] || [[ "$line" == \#* ]] || [[ "$line" == \#\#* ]]; then
        continue
    fi
    
    # Extract file path and description
    if [[ "$line" == -* ]]; then
        # Get the full line after the dash
        full_line=$(echo "$line" | sed 's/^- //')
        # Split on first colon
        file_path=$(echo "$full_line" | cut -d':' -f1)
        description=$(echo "$full_line" | cut -d':' -f2- | sed 's/^ //')
        
        # Only process files that are not in src/ or tests/
        if [[ "$file_path" != src/* ]] && [[ "$file_path" != tests/* ]]; then
            process_file "$file_path" "$description"
        fi
    fi
done < file_mapping.txt

# Add any remaining untracked files
git add .
git commit -m "Add remaining project files"
git push origin main

echo "All files have been committed and pushed to main branch." 