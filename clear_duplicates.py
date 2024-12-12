import os
import hashlib

def hash_file(filepath):
    """Generate a hash for the given file."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def get_hashes(folder):
    """Get a dictionary of file hashes for all .jpg files in the given folder."""
    file_hashes = {}
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                filepath = os.path.join(root, file)
                try:
                    file_hash = hash_file(filepath)
                    file_hashes[filepath] = file_hash
                    print(f"Hashed file: {filepath}")
                except Exception as e:
                    print(f"Error hashing file {filepath}: {e}")
    return file_hashes

def find_duplicates(folder1, folder2):
    """Compare two folders and find duplicate files based on their hashes."""
    hashes_folder1 = get_hashes(folder1)
    print(f"\nTotal files in {folder1}: {len(hashes_folder1)}")
    
    hashes_folder2 = get_hashes(folder2)
    print(f"Total files in {folder2}: {len(hashes_folder2)}")
    
    duplicates = []
    for filepath1, hash1 in hashes_folder1.items():
        for filepath2, hash2 in hashes_folder2.items():
            if hash1 == hash2:
                duplicates.append((filepath1, filepath2))
    
    return duplicates

def main():
    # Adjust the path to your data folder
    base_path = os.path.join('data')
    folder_positives = os.path.join(base_path, 'training_positives')
    folder_negatives = os.path.join(base_path, 'training_negatives')
    
    # Check if folders exist
    if not os.path.exists(folder_positives) or not os.path.exists(folder_negatives):
        print(f"Folders do not exist. Checked paths:")
        print(f"Positives folder: {folder_positives}")
        print(f"Negatives folder: {folder_negatives}")
        print(f"Current working directory: {os.getcwd()}")
        return
    
    # Find duplicates
    duplicates = find_duplicates(folder_positives, folder_negatives)
    
    # Print results
    if duplicates:
        print("\n=== Duplicates Found ===")
        for file1, file2 in duplicates:
            print("Duplicate files:")
            print(f"  1. {file1}")
            print(f"  2. {file2}")
            print()
    else:
        print("\nNo duplicates found.")

if __name__ == "__main__":
    main()