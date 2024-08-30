import os

def update_index_rst(source_dir, index_rst_path):
    # Collect all .rst files in the source directory
    rst_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".rst"):
                # Calculate the relative path to the .rst file from the index_rst_path perspective
                relative_path = os.path.relpath(os.path.join(root, file), os.path.dirname(index_rst_path))
                # Remove the file extension for the toctree entry
                rst_files.append(relative_path[:-4].replace(os.sep, "/"))

    # Sort the files for consistent ordering
    rst_files.sort()

    # Write the entries to index.rst
    with open(index_rst_path, 'w') as index_file:
        index_file.write("Welcome to Your Project's documentation!\n")
        index_file.write("=========================================\n\n")
        index_file.write(".. toctree::\n")
        index_file.write("   :maxdepth: 2\n")
        index_file.write("   :caption: Contents:\n\n")
        
        for rst_file in rst_files:
            index_file.write(f"   {rst_file}\n")

    print(f"Updated {index_rst_path} with {len(rst_files)} entries.")

if __name__ == "__main__":
    # Assuming this script is located in the directory containing 'source'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(base_dir, "source")
    index_rst_path = os.path.join(base_dir, "index.rst")

    update_index_rst(source_dir, index_rst_path)
