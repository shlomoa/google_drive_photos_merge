# 📸 Organizing Google Drive Photos: A Local Deduplication Workflow in Python

## ❗ Problem Description

When using Google Drive to back up and sync photos across multiple devices or over time, it’s easy to end up with multiple copies of the same file. These duplicates often:
- Have identical file names and sizes  
- Live in different subfolders  
- Make organizing your photo collection tedious and frustrating  
- Waste valuable local storage space  

Traditional deduplication tools often require cloud API access, are platform-specific, or provide little control over what gets deleted. The goal here was to create a **local, lightweight, interactive tool** that gives you full visibility and control—without relying on any cloud services.

---

## 🧠 Assumptions & Prerequisites

To successfully use this project, the following knowledge and environment setup is assumed:

### Technical Requirements
- ✅ [Python 3.8+](https://www.python.org/downloads/) installed on your system  
- ✅ Ability to run Python scripts from the command line  
- ✅ Basic familiarity with using the terminal:  
  - [macOS Terminal](https://support.apple.com/guide/terminal/welcome/mac)  
  - [Linux Terminal](https://ubuntu.com/tutorials/command-line-for-beginners#1-overview)  
  - [Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/)  
- ✅ Comfortable opening `.html` files in a browser  
- ✅ (Optional) If running on Windows, familiarity with [WSL (Windows Subsystem for Linux)](https://learn.microsoft.com/en-us/windows/wsl/)  
  - You can install it using:  
    ```powershell
    wsl --install
    ```

### Functional Setup
- ✅ Google Drive must be installed and synced locally ([Download here](https://www.google.com/drive/download/))  
- ✅ Files you want to deduplicate must be marked as "Available offline"  
- ✅ Your system must have enough local storage to hold the full set of synced files (see storage section below for how to check)

---

## 💾 Installing Google Drive for Desktop & Keeping Files Local

To use this tool, your Google Drive content must be available **locally** on your machine. Here's how:

### 1. Install Google Drive for Desktop
- Download and install Google Drive from [https://www.google.com/drive/download/](https://www.google.com/drive/download/)
- Sign in with your Google account
- During setup, choose **"Mirror files"** rather than stream-only (this stores the files locally).

### 2. Ensure All Files Are Available Offline
- Open File Explorer and locate the Google Drive folder.
- Right-click on the top-level folder (or any subfolder you want to include).
- Select **"Offline access" → "Available offline"**.
- This will download all files in that folder to your local disk.

> 📌 **Important:** The script only works with files physically present on your computer. Ensure everything is fully synced before running it.

---

## ⚠️ Storage Disclaimer & How to Check Space

Make sure your local drive has enough space to mirror your entire Google Drive content.

### 🔍 Check Google Drive Storage Usage
- Visit [https://drive.google.com/drive/quota](https://drive.google.com/drive/quota)
- You’ll see your total usage and a breakdown by file type

### 💽 Check Local Disk Space

**On Linux/macOS/WSL:**
```bash
df -h ~
```

**On Windows:**
- Open File Explorer
- Right-click on your drive (usually C:)
- Select **Properties**
- Look for **Free space**

---

## 🧪 How This Project Was Created

This project was developed using a rapid, iterative approach centered around modern AI tooling and developer productivity:

### 👨‍💻 Development Environment
- Built in **Visual Studio Code** with **GitHub Copilot** enabled.
- Copilot was instrumental in suggesting boilerplate code, HTML structure, and even refining logic for duplicate detection and file handling.

### 🔁 Development Cycle
- Began with a functional specification: deduplicate local photos by name and size.
- Used Copilot to scaffold the Python script, then refined logic manually for filtering media types and generating the interactive HTML output.
- Each change was tested locally on a Google Drive–synced folder with simulated duplicates.

### 📝 Blog Post Generation
- This blog post was drafted with help from **ChatGPT**, using an outline and iterative edits.
- The workflow alternated between writing in natural language and technical translation—speeding up documentation significantly.
- Final formatting and structure were adjusted manually to ensure clarity and flow.

---

## 🛠️ How It Works

The script performs the following steps:

1. **Folder Scan**  
   It recursively walks through the given directory and gathers all files. Optionally, it can filter for media files (images and videos) only.

2. **Duplicate Detection**  
   Files are considered duplicates if they share the same **filename** and **file size**.

3. **Interactive HTML Report**  
   An HTML file is generated showing each group of duplicates in a separate table. For each file, you’ll see:
   - A **red delete button** to mark it for removal  
   - A **green keep button** to preserve it  

4. **One-Click Cleanup Script**  
   A **"Generate Cleanup Script"** button at the top creates a downloadable `cleanup.sh` with `rm` commands for files marked for deletion.

---

## 🧪 Example Usage

```bash
./google_drive_photos_merge.py ~/GoogleDrive/photos ~/duplicates.html --medias_only
```

Open the resulting HTML file in your browser, choose which files to delete, and generate the cleanup script.

---

## 💡 Why This Approach?

- **Local-Only**: No cloud API or credentials needed  
- **Visual Review**: See all duplicate clusters in a browser before deleting  
- **Safe**: Nothing is removed until you execute the script  

---

## 🔍 Tech Stack

- Python 3.8+  
- Standard libraries: `os`, `argparse`, `hashlib`  
- Pure HTML + JavaScript frontend  
- Works on Linux, macOS, and WSL on Windows  

---

## 🚀 Future Improvements

While the current method—using file name and size—is fast, a more robust approach would involve hashing file contents.

### 🔁 Comparison: Filename + Size vs MD5 Hashing

| Approach            | Pros                                                                 | Cons                                                                  |
|---------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------|
| **Filename + Size** | ✅ Very fast (no file reading required)<br>✅ Low CPU usage            | ❌ False positives if different files share same name and size         |
| **MD5 Checksum**    | ✅ Detects true duplicates even if names differ<br>✅ No false matches | ❌ Slower (reads entire file contents)<br>❌ Higher CPU and I/O demand |

### 🧭 Other Ideas
- 🖼️ Show thumbnails in the HTML report  
- ⏳ Auto-select oldest/newest file per group  
- 🧪 Add a dry-run mode for safe preview  

---

## 📝 Generating and Using the Cleanup Script

1. **Generate the Cleanup Script**:
   - After running the script and reviewing the HTML report, click the **"Generate Cleanup Script"** button at the top of the report.
   - This will download a file named `cleanup.sh` containing commands to delete the selected files.

2. **Make the Script Executable**:
   - On Linux/macOS/WSL:
     ```bash
     chmod +x cleanup.sh
     ```
   - On Windows (using WSL):
     ```bash
     chmod +x cleanup.sh
     ```

3. **Run the Script**:
   - Execute the script to delete the selected files:
     ```bash
     ./cleanup.sh
     ```

> **Note**: Ensure you review the script before running it to confirm it contains the intended delete commands.

If your photo collection could use some decluttering, this tool gives you full control in a fast, local workflow.

**Happy cleaning! 🧹**
