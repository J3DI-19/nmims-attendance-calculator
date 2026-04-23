"""
NMIMS Attendance Calculator (Fuzzy Match Version)
-------------------------------------------------

Features:
- Auto-detect PDF files in folder
- Parses daily attendance PDF
- Theory and Practical shown separately
- Combined attendance % shown
- 80% minimum attendance rule
- Extra classes needed for 80%
- Safe bunks remaining
- Automatic fuzzy matching of similar subject names
- No hardcoded subject names

Install:
pip install pdfplumber rapidfuzz

Run:
python attendance_summary.py
"""

import pdfplumber
import re
from pathlib import Path
from rapidfuzz import fuzz

MIN_ATTENDANCE = 80
SIMILARITY_THRESHOLD = 85


# =========================================================
# PDF SELECTOR
# =========================================================

def choose_pdf():
    pdf_files = list(Path.cwd().glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in current folder.")
        return None

    print("\nPDF files found:\n")

    for i, pdf in enumerate(pdf_files, 1):
        print(f"{i}. {pdf.name}")

    while True:
        try:
            choice = int(input("\nSelect PDF number: "))

            if 1 <= choice <= len(pdf_files):
                selected = pdf_files[choice - 1]
                print(f"\nSelected: {selected.name}\n")
                return str(selected)

            print("Invalid selection.")

        except ValueError:
            print("Please enter a valid number.")


# =========================================================
# CLEAN + NORMALIZE
# =========================================================

def clean_subject_name(raw_name):
    """
    Generic cleaner only.
    No hardcoded subjects.
    No subject-specific replacements.

    Goal:
    Remove metadata + attached suffixes
    so fuzzy matching can do the rest.
    """

    if not raw_name:
        return "UNKNOWN"

    name = str(raw_name).upper()

    # -----------------------------------
    # Remove punctuation
    # -----------------------------------
    name = re.sub(r"[^\w\s]", " ", name)

    # -----------------------------------
    # Remove attached suffixes at word ends
    #
    # Examples:
    # MANAGEMENTT1 -> MANAGEMENT
    # SKILLSP1 -> SKILLS
    # RESPT1 -> RESP
    # ANALYP1 -> ANALY
    # CYBERB2 -> removed later
    # -----------------------------------

    # remove T1 / T2 / T3 attached at end
    name = re.sub(r"T\d+\b", "", name)

    # remove P1 / P2 / P3 attached at end
    name = re.sub(r"P\d+\b", "", name)

    # remove B1 / B2 / B3
    name = re.sub(r"B\d+\b", "", name)

    # remove OE1 / OE2 / OE3
    name = re.sub(r"OE\d+\b", "", name)

    # -----------------------------------
    # Remove common metadata words
    # (generic, not subject-specific)
    # -----------------------------------

    remove_words = [
        "BT",
        "CYBER",
        "BTCYBER",
        "MBA",
        "THEO",
        "PRAC"
    ]

    for word in remove_words:
        name = re.sub(rf"\b{word}\b", "", name)

    # -----------------------------------
    # Normalize spacing automatically
    # -----------------------------------

    # collapse multiple spaces
    name = re.sub(r"\s+", " ", name)

    # trim
    name = name.strip()

    return name


def detect_type(raw_name):
    """
    Detect THEORY or PRACTICAL
    """

    raw = str(raw_name).upper()

    if "P1" in raw or "PRAC" in raw:
        return "PRACTICAL"

    if "T1" in raw or "THEO" in raw:
        return "THEORY"

    return "THEORY"


# =========================================================
# FUZZY GROUPING
# =========================================================

def find_best_match(subject_name, existing_subjects):
    """
    Match similar subjects automatically
    using fuzzy similarity
    """

    if not existing_subjects:
        return subject_name

    best_match = None
    best_score = 0

    for existing in existing_subjects:
        score = fuzz.ratio(subject_name, existing)

        if score > best_score:
            best_score = score
            best_match = existing

    if best_score >= SIMILARITY_THRESHOLD:
        return best_match

    return subject_name


# =========================================================
# CALCULATIONS
# =========================================================

def calculate_percent(attended, total):
    if total == 0:
        return 0.0
    return round((attended / total) * 100, 2)


def classes_needed_for_80(attended, total):
    if total == 0:
        return 0

    if calculate_percent(attended, total) >= MIN_ATTENDANCE:
        return 0

    x = 0
    while ((attended + x) / (total + x)) * 100 < MIN_ATTENDANCE:
        x += 1

    return x


def safe_bunks(attended, total):
    if total == 0:
        return 0

    x = 0
    while (attended / (total + x + 1)) * 100 >= MIN_ATTENDANCE:
        x += 1

    return x


# =========================================================
# PARSER
# =========================================================

def parse_attendance(pdf_path):
    """
    Parse PDF table:
    [Sr No, Course Name, Date, Start Time, End Time, Attendance]
    """

    subjects = {}

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:
                for row in table:
                    if not row or len(row) < 6:
                        continue

                    row = [str(cell).strip() if cell else "" for cell in row]
                    row_text = " ".join(row).lower()

                    # Skip headers
                    if (
                        "course name" in row_text
                        or "attendance report" in row_text
                        or "student name" in row_text
                        or "academic year" in row_text
                    ):
                        continue

                    raw_subject = row[1]
                    attendance = row[-1]

                    if attendance not in ["P", "A"]:
                        continue

                    lecture_type = detect_type(raw_subject)
                    cleaned_subject = clean_subject_name(raw_subject)

                    final_subject = find_best_match(
                        cleaned_subject,
                        subjects.keys()
                    )

                    if final_subject not in subjects:
                        subjects[final_subject] = {
                            "THEORY": {
                                "total": 0,
                                "present": 0
                            },
                            "PRACTICAL": {
                                "total": 0,
                                "present": 0
                            }
                        }

                    subjects[final_subject][lecture_type]["total"] += 1

                    if attendance == "P":
                        subjects[final_subject][lecture_type]["present"] += 1

    return subjects


# =========================================================
# REPORT
# =========================================================

def print_summary(subjects):
    print("\n" + "=" * 95)
    print("ATTENDANCE SUMMARY")
    print("=" * 95)

    for subject in sorted(subjects.keys()):
        data = subjects[subject]

        theory_total = data["THEORY"]["total"]
        theory_present = data["THEORY"]["present"]

        practical_total = data["PRACTICAL"]["total"]
        practical_present = data["PRACTICAL"]["present"]

        combined_total = theory_total + practical_total
        combined_present = theory_present + practical_present

        theory_percent = calculate_percent(
            theory_present,
            theory_total
        )

        practical_percent = calculate_percent(
            practical_present,
            practical_total
        )

        combined_percent = calculate_percent(
            combined_present,
            combined_total
        )

        needed = classes_needed_for_80(
            combined_present,
            combined_total
        )

        bunks = safe_bunks(
            combined_present,
            combined_total
        )

        print("\n" + "-" * 95)
        print(f"SUBJECT: {subject}")
        print("-" * 95)

        if theory_total > 0:
            print(
                f"Theory     : "
                f"{theory_present}/{theory_total} "
                f"-> {theory_percent}%"
            )

        if practical_total > 0:
            print(
                f"Practical  : "
                f"{practical_present}/{practical_total} "
                f"-> {practical_percent}%"
            )

        print(
            f"Combined   : "
            f"{combined_present}/{combined_total} "
            f"-> {combined_percent}%"
        )

        print(f"Need for 80% : {needed}")
        print(f"Safe Bunks   : {bunks}")

        if combined_percent < MIN_ATTENDANCE:
            print("STATUS       : BELOW 80%")
        else:
            print("STATUS       : SAFE")


# =========================================================
# MAIN
# =========================================================

def main():
    pdf_path = choose_pdf()

    if not pdf_path:
        return

    print(f"\nReading: {pdf_path}")

    subjects = parse_attendance(pdf_path)
    print_summary(subjects)


if __name__ == "__main__":
    main()