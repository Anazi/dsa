# 🐚 Shell (Bash) Cheat Sheet
> A comprehensive, structured Bash shell cheat sheet with *commands grouped by functionality* and *clear inline comments explaining why they are used*. Ideal for DevOps, scripting, and Linux usage.
---
## 📚 Table of Contents
- [📁 File and Directory Operations](#-file-and-directory-operations)
- [📝 File Viewing and Editing](#-file-viewing-and-editing)
- [🔎 Searching and Filtering](#-searching-and-filtering)
- [🔁 Loops and Conditionals](#-loops-and-conditionals)
- [📦 Archiving and Compression](#-archiving-and-compression)
- [🧪 File Permissions and Ownership](#-file-permissions-and-ownership)
- [🧰 Process Management](#-process-management)
- [🌐 Networking Tools](#-networking-tools)
- [📜 Scripting Basics](#-scripting-basics)
- [🧮 Text Processing with awk](#-text-processing-with-awk)
    - [🔹 Basic Usage](#-basic-usage)
    - [🔹 Using a Custom Delimiter (e.g., CSV)](#-using-a-custom-delimiter-eg-csv)
    - [🔹 Filtering Based on Conditions](#-filtering-based-on-conditions)
    - [🔹 Summing Column Values](#-summing-column-values)
    - [🔹 Adding Headers and Footers](#-adding-headers-and-footers)
    - [🔹 Count Occurrences of Unique Fields](#-count-occurrences-of-unique-fields)
    - [🔹 Summary Table](#-summary-table)
- [📎 Miscellaneous Tips](#-miscellaneous-tips)

---
## 📁 File and Directory Operations
```bash
ls -la                    # List all files with permissions and hidden files
cd /path/to/dir           # Change directory
mkdir new_folder          # Create a directory
touch file.txt            # Create a new empty file
cp file.txt /dest/        # Copy file
mv file.txt newname.txt   # Rename or move file
rm file.txt               # Delete file
rm -rf folder/            # Delete folder recursively
```
> 💡 Why? These are basic operations for navigating and managing files.
---
## 📝 File Viewing and Editing
```bash
cat file.txt              # View file content
head -n 10 file.txt       # Show first 10 lines
tail -f log.txt           # Follow log file live
less file.txt             # Scrollable view of large files
nano file.txt             # Simple terminal editor
vi file.txt               # Advanced terminal editor
```
> 💡 Why? Useful for quick reads, log watching, or editing configs on servers.
---
## 🔎 Searching and Filtering
```bash
grep "pattern" file.txt           # Search for string in file
grep -r "pattern" /dir            # Recursively search files
find . -name "*.log"              # Find files by name
find /dir -type f -mtime -1       # Files modified in last 24 hrs
```
> 💡 Why? Powerful tools to locate data or troubleshoot logs quickly.
---
## 🔁 Loops and Conditionals
```bash
for file in *.txt; do echo $file; done       # Loop over files
if [ -f file.txt ]; then echo exists; fi     # Check if file exists
while read line; do echo $line; done < file  # Read file line by line
```
> 💡 Why? Used in automation and scripting for conditional execution.
---
## 📦 Archiving and Compression
```bash
tar -czf archive.tar.gz folder/     # Create compressed archive
tar -xzf archive.tar.gz             # Extract compressed archive
zip -r archive.zip folder/          # Create zip archive
unzip archive.zip                   # Extract zip archive
```
> 💡 Why? To compress and share large file sets or take backups.
---
## 🧪 File Permissions and Ownership
```bash
chmod +x script.sh             # Make script executable
chmod 644 file.txt             # rw-r--r--
chown user:group file.txt      # Change file ownership
```
> 💡 Why? Critical for securing files and enabling script execution.
---
## 🧰 Process Management
```bash
ps aux                         # List all running processes
top                            # Interactive process monitor
kill -9 <pid>                  # Force kill process
htop                           # Enhanced top (if installed)
```
> 💡 Why? To diagnose and kill rogue or resource-heavy processes.
---
## 🌐 Networking Tools
```bash
ping google.com                # Check network reachability
curl https://example.com      # Fetch content from URL
wget http://example.com/file  # Download file
netstat -tuln                 # Show listening ports
```
> 💡 Why? Helpful in debugging connectivity and making HTTP calls.
---
## 📜 Scripting Basics
```bash
#!/bin/bash
echo "Hello, $USER!"          # Print greeting with username
```
```bash
# Run script
bash script.sh
```
> 💡 Why? This is how automation and DevOps pipelines are built.
---

## 🧮 Text Processing with `awk`
> `awk` is a powerful text-processing tool used for pattern scanning, data extraction, and reporting. It works line-by-line and field-by-field, making it great for structured data like logs, CSVs, or whitespace-separated text.
### 🔹 Basic Usage
```bash
awk '{print $1}' file.txt
```
> ✅ Why? Prints the first column of each line — useful for field extraction.
### 🔹 Using a Custom Delimiter (e.g., CSV)
```bash
awk -F, '{print $2}' data.csv
```
> ✅ Why? Extracts second field from comma-separated values.
### 🔹 Filtering Based on Conditions
```bash
awk '$3 > 100 {print $1, $3}' file.txt
```
> ✅ Why? Shows only lines where the 3rd column is greater than 100.
### 🔹 Summing Column Values
```bash
awk '{sum += $2} END {print sum}' file.txt
```
> ✅ Why? Adds up all values in column 2.
### 🔹 Adding Headers and Footers
```bash
awk 'BEGIN {print "Start"} {print $1} END {print "End"}' file.txt
```
> ✅ Why? Useful for printing custom messages or doing setup/teardown actions in scripts.
### 🔹 Count Occurrences of Unique Fields
```bash
awk '{count[$1]++} END {for (word in count) print word, count[word]}' file.txt
```
> ✅ Why? Shows how many times each value in column 1 appears — useful for frequency analysis.
### 🔹 Summary Table
| Task                        | Example                                           |
|-----------------------------|---------------------------------------------------|
| Print specific field        | `awk '{print $2}' file`                          |
| Set delimiter               | `awk -F: '{print $1}' /etc/passwd`              |
| Filter rows by condition    | `awk '$3 > 5' file`                              |
| Calculate column sum        | `awk '{sum += $2} END {print sum}' file`         |
| Count occurrences           | `awk '{count[$1]++} END {for(i in count) print i, count[i]}' file` |
| Add header/footer logic     | `awk 'BEGIN{print "Start"} {print} END{print "Done"}' file` |

---

## 📎 Miscellaneous Tips
```bash
history                       # Show command history
alias ll='ls -la'             # Create shortcut
df -h                         # Disk usage
du -sh *                      # Directory sizes
uptime                        # System load
```
> 💡 Why? Improves efficiency and gives system visibility.
