import os


def get_python_files(folder):

    python_files = []

    for root, directories, files in os.walk(folder):

        for file in files:

            if file.endswith(".py"):

                full_path = os.path.join(
                    root,
                    file
                )

                python_files.append(full_path)

    return python_files