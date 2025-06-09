<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Copilot Instructions for Google Drive Photos Merge Project

## Project Overview
This project is a Python script designed to identify duplicate files in a folder, generate an HTML report with options to delete or keep files, and create a cleanup script for deleting selected files. It supports filtering for media files only and provides progress indication during processing.

## Key Features
- **Duplicate Identification**: Based on file name and size.
- **HTML Report**: Interactive report with delete/keep buttons and a "Generate Cleanup Script" button.
- **Media File Filtering**: Option to analyze only media files (images and videos).
- **Progress Indication**: Displays progress during duplicate identification.

## Development Notes
- The main script is `google_drive_photos_merge.py`.
- The script uses `argparse` for command-line argument handling.
- The HTML report includes JavaScript for interactivity.
- Tasks are defined in `.vscode/tasks.json` for running the script with appropriate arguments.

## Usage
- Run the script using the following command:
  ```bash
  python google_drive_photos_merge.py <folder_to_scan> <output_html_file> [--medias_only]
  ```
- Replace `<folder_to_scan>` and `<output_html_file>` with the appropriate paths.
- Use the `--medias_only` flag to filter for media files.

## Debugging
- Line breaks have been added to the generated HTML for better readability.
- JavaScript issues with newline characters have been resolved by escaping them properly.

## Additional Notes
- Ensure Python 3.8 or later is installed.
- The script is compatible with Windows and uses `pwsh.exe` as the default shell for terminal commands.
