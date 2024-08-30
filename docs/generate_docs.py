import os
import subprocess
import sys

def generate_rst_files(src_dir, output_dir, exclude_dirs):
    exclude_dirs = [os.path.abspath(d) for d in exclude_dirs]

    for root, dirs, files in os.walk(src_dir):
        # Exclude directories
        dirs[:] = [d for d in dirs if os.path.abspath(os.path.join(root, d)) not in exclude_dirs]
        # Check if the current directory should be excluded
        if os.path.abspath(root) in exclude_dirs:
            continue

        # Generate .rst files for each Python file
        for file in files:
            if file.endswith(".py"):
                module_name = os.path.splitext(os.path.relpath(os.path.join(root, file), src_dir))[0].replace(os.sep, ".")
                rst_file = os.path.join(output_dir, f"{module_name}.rst")
                
                # Create the directory if it does not exist
                os.makedirs(os.path.dirname(rst_file), exist_ok=True)

                # Create the .rst file for the module
                with open(rst_file, "w") as f:
                    f.write(f"{module_name}\n")
                    f.write("=" * len(module_name) + "\n\n")
                    f.write(f".. automodule:: {module_name}\n")
                    f.write("   :members:\n")
                    f.write("   :undoc-members:\n")
                    f.write("   :show-inheritance:\n")

def update_index_rst(output_dir):
    index_path = os.path.join(output_dir, "index.rst")
    with open(index_path, "w") as index_file:
        index_file.write("Welcome to Your Project's documentation!\n")
        index_file.write("=========================================\n\n")
        index_file.write(".. toctree::\n")
        index_file.write("   :maxdepth: 2\n\n")
        
        # Add each .rst file to the toctree
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".rst") and file != "index.rst":
                    module_path = os.path.relpath(os.path.join(root, file), output_dir)
                    module_path = module_path.replace(os.sep, "/")
                    module_path = module_path.replace(".rst", "")
                    index_file.write(f"   {module_path}\n")

def build_docs():
    subprocess.run(["make", "html"])

if __name__ == "__main__":
    src_dir = "../src"
    output_dir = "source"
    exclude_dirs = sys.argv[1:]

    generate_rst_files(src_dir, output_dir, exclude_dirs)
    update_index_rst(output_dir)
    build_docs()
