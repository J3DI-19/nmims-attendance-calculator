# NMIMS Attendance Calculator

A smart Python-based attendance calculator for NMIMS students that reads attendance PDF reports automatically and generates a clean subject-wise attendance summary.

This version includes fuzzy subject matching, so even if subject names vary slightly across PDFs, they are grouped correctly without hardcoding subject names.

---

## Features

* Auto-detect PDF files in the current folder
* Select PDF directly from terminal
* Parses daily attendance PDF reports
* Theory and Practical attendance shown separately
* Combined attendance percentage calculation
* 80% minimum attendance rule support
* Calculates extra classes needed to reach 80%
* Calculates safe bunks remaining
* Automatic fuzzy matching for similar subject names
* No hardcoded subject names

---

## Example Output

```text
SUBJECT: PROJECT MANAGEMENT

Theory     : 18/22 -> 81.82%
Practical  : 9/10 -> 90.0%
Combined   : 27/32 -> 84.38%

Need for 80% : 0
Safe Bunks   : 2
STATUS       : SAFE
```

---

## Installation

Install required dependencies:

```bash
pip install pdfplumber rapidfuzz
```

---

## How to Use

### Step 1

Place your attendance PDF file in the same folder as:

```bash
attendance_summary.py
```

### Step 2

Run the script:

```bash
python attendance_summary.py
```

### Step 3

Select the PDF from the list shown in terminal.

The program will automatically parse the attendance and generate the full summary.

---

## How It Works

The script:

1. Detects all PDF files in the folder
2. Lets you choose which PDF to process
3. Extracts attendance tables using `pdfplumber`
4. Cleans and normalizes subject names
5. Uses fuzzy matching (`rapidfuzz`) to group similar subjects
6. Separates Theory and Practical classes
7. Calculates:

   * attendance %
   * classes needed for 80%
   * safe bunks remaining

---

## Tech Stack

* Python
* pdfplumber
* rapidfuzz
* Regular Expressions (Regex)

---

## Why This Exists

NMIMS attendance PDFs often have inconsistent subject naming and are painful to track manually.

This tool removes that problem completely and helps students instantly know:

* whether they are safe
* how many classes they can skip
* how many classes they must attend

---

## Future Improvements

Possible upgrades:

* Excel export
* GUI version
* Semester-wise analytics
* Attendance trend graphs
* Web app version

---

## License

MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Author
-J3DI

Built to make attendance survival easier.
