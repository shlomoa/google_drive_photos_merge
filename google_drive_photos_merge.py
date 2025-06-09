#!/usr/bin/env python3

"""
Google Drive Photos Merge Script

This script scans a specified folder for duplicate files based on their file name and size
and generates an HTML file listing the duplicate file paths. The HTML report includes
interactive options to delete or keep files and a button to generate a cleanup script.

Usage:
    ./google_drive_photos_merge.py <folder_to_scan> <output_html_file> [--medias_only]

Arguments:
    <folder_to_scan>      The path to the folder containing the files to scan for duplicates.
    <output_html_file>    The path to the HTML file where the duplicate file paths will be saved.
    --medias_only         Optional flag to analyze only media files (images and videos).

Example:
    ./google_drive_photos_merge.py ~/photos ~/duplicates.html --medias_only

Features:
    - Identify duplicate files based on file name and size.
    - Optionally filter for media files (images and videos) using the --medias_only flag.
    - Generate an interactive HTML report with:
        - Separate tables for each cluster of duplicates.
        - Red "Delete" and green "Keep" buttons for each file.
        - A "Generate Cleanup Script" button to create a bash script for deleting selected files.
    - Progress indication during the duplicate identification process.

Requirements:
    - Python 3.8 or later
    - Ensure the script has executable permissions (chmod +x google_drive_photos_merge.py).

Author:
    Shlomo Anglister

Date:
    June 9, 2025
"""

import argparse
import hashlib
import os

def calculate_md5(file_path):
    """Calculate the MD5 checksum of a file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(4096), b""):
                hash_md5.update(chunk)
    except (OSError, IOError) as error:
        print(f"Error reading file {file_path}: {error}")
        return None
    return hash_md5.hexdigest()

def identify_duplicates(file_list):
    """Identify duplicate files based on file name and size."""
    file_map = {}
    duplicates = []

    for index, file_path in enumerate(file_list, start=1):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        file_key = (file_name, file_size)

        if file_key in file_map:
            duplicates.append((file_path, file_map[file_key]))
        else:
            file_map[file_key] = file_path

        # Print a dot for every 10 files processed
        if index % 10 == 0:
            print('.', end='', flush=True)

    print()  # Move to the next line after progress indication
    return duplicates

def is_media_file(file_path):
    """Check if a file is a media file (image or video)."""
    media_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".mp4", ".avi", ".mov", ".mkv"}
    return os.path.splitext(file_path)[1].lower() in media_extensions

def scan_folder_for_files(folder_path, filter_media_only):
    """Scan a folder and return a list of file paths, optionally filtering for media files."""
    all_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            if not filter_media_only or is_media_file(file_path):
                all_files.append(file_path)
    return all_files

def write_duplicates_to_html(duplicates_list, output_file_path):
    """Write the paths of duplicate files to an HTML file as a form."""
    with open(output_file_path, "w", encoding="utf-8") as html_file:
        html_file.write("<html>\n<head>\n")
        html_file.write("<style>\n")
        html_file.write("body { font-family: Arial, sans-serif; margin: 20px; }\n")
        html_file.write("h1, h2 { color: #333; }\n")
        html_file.write("table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }\n")
        html_file.write("th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }\n")
        html_file.write("th { background-color: #f4f4f4; }\n")
        html_file.write("button { padding: 5px 10px; border: none; cursor: pointer; }\n")
        html_file.write(".delete-button { background-color: red; color: white; }\n")
        html_file.write(".delete-button.selected { opacity: 0.6; }\n")
        html_file.write(".keep-button { background-color: green; color: white; }\n")
        html_file.write(".keep-button.selected { opacity: 0.6; }\n")
        html_file.write("#cleanup-button { margin-bottom: 20px; background-color: blue; color: white; padding: 10px 20px; }\n")
        html_file.write("</style>\n")
        html_file.write("</head>\n<body>\n")
        html_file.write("<h1>Duplicate Files</h1>\n")
        html_file.write("<form id='cleanup-form'>\n")

        # Move the Generate Cleanup Script button to the top
        html_file.write("<button type='button' id='cleanup-button'>Generate Cleanup Script</button>\n")

        for duplicates in duplicates_list:
            cluster_name = os.path.basename(duplicates[0])  # Use the file name of the first duplicate as the cluster name
            html_file.write(f"<h2>Cluster: {cluster_name}</h2>\n")
            html_file.write("<table>\n")
            html_file.write("<tr><th>File Path</th><th>Action</th></tr>\n")

            for duplicate in duplicates:
                html_file.write("<tr>\n")
                html_file.write(f"<td>{duplicate}</td>\n")
                html_file.write(
                    "<td>\n"
                    f"<button type='button' class='delete-button' data-file='{duplicate}'>Delete</button>\n"
                    f"<button type='button' class='keep-button' data-file='{duplicate}'>Keep</button>\n"
                    "</td>\n"
                )
                html_file.write("</tr>\n")

            html_file.write("</table>\n")

        html_file.write("</form>\n")

        html_file.write("<script>\n")
        html_file.write("let deleteFiles = [];\n")
        html_file.write("document.querySelectorAll('.delete-button').forEach(button => {\n")
        html_file.write("    button.addEventListener('click', () => {\n")
        html_file.write("        deleteFiles.push(button.getAttribute('data-file'));\n")
        html_file.write("        button.classList.add('selected');\n")
        html_file.write("        button.textContent = 'Deleted';\n")
        html_file.write("        button.disabled = true;\n")
        html_file.write("        const keepButton = button.parentElement.querySelector('.keep-button');\n")
        html_file.write("        if (keepButton) { keepButton.disabled = true; keepButton.classList.add('disabled'); }\n")
        html_file.write("    });\n")
        html_file.write("});\n")
        html_file.write("document.querySelectorAll('.keep-button').forEach(button => {\n")
        html_file.write("    button.addEventListener('click', () => {\n")
        html_file.write("        button.classList.add('selected');\n")
        html_file.write("        button.textContent = 'Kept';\n")
        html_file.write("        button.disabled = true;\n")
        html_file.write("        const deleteButton = button.parentElement.querySelector('.delete-button');\n")
        html_file.write("        if (deleteButton) { deleteButton.disabled = true; deleteButton.classList.add('disabled'); }\n")
        html_file.write("    });\n")
        html_file.write("});\n")
        html_file.write("document.getElementById('cleanup-button').addEventListener('click', () => {\n")
        html_file.write("    const scriptContent = deleteFiles.map(file => `rm '${file}'`).join('\\n');\n")
        html_file.write("    const blob = new Blob([scriptContent], { type: 'text/plain' });\n")
        html_file.write("    const link = document.createElement('a');\n")
        html_file.write("    link.href = URL.createObjectURL(blob);\n")
        html_file.write("    link.download = 'cleanup.sh';\n")
        html_file.write("    link.click();\n")
        html_file.write("});\n")
        html_file.write("</script>\n")

        html_file.write("</body>\n</html>\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Drive Photos Merge Script")
    parser.add_argument(
        "folder_to_scan",
        help="The path to the folder containing the files to scan for duplicates."
    )
    parser.add_argument(
        "output_html_file",
        help="The path to the HTML file where the duplicate file paths will be saved."
    )
    parser.add_argument(
        "--medias_only",
        action="store_true",
        help="Analyze only media files (images and videos)."
    )

    args = parser.parse_args()

    folder_to_scan_path = args.folder_to_scan
    output_html_file_path = args.output_html_file
    medias_only = args.medias_only

    scanned_files_list = scan_folder_for_files(folder_to_scan_path, medias_only)
    duplicates_found = identify_duplicates(scanned_files_list)

    write_duplicates_to_html(duplicates_found, output_html_file_path)
    print(f"Duplicate file paths have been written to {output_html_file_path}")
