import re
import yaml
from pathlib import Path
import json
from utils import gender_mapper
from difflib import SequenceMatcher
import pandas as pd

with open("config.yaml") as f:
    try:
        CONFIG = yaml.safe_load(f)
    except Exception as e:
        raise ValueError("config.yaml file could not be found") from e
    

def main():
    all_data_path = Path(CONFIG["data"]["path"]) / CONFIG["data"]["excel"]    
    output_dir = Path(CONFIG["data"]["output_dir"])
    
    df = pd.read_excel(all_data_path)
    
    results = []
    
    for file in output_dir.iterdir():
        if "annonymized" in file.stem:
            continue
            
        file_id = int(file.stem.split("_")[1])
        patient_info = df[df["id"] == file_id][["age", "sex"]]
        
        with open(file, "r") as f:
            raw_report = json.load(f)
        
        annonymized_path = file.parent / (file.stem + "_annonymized.json")
        if not annonymized_path.exists():
            continue
            
        with open(annonymized_path, "r") as f:
            annonymized = json.load(f)
            
        # Descriptive status trackers for this file
        age_status = "Age Not Present in Raw Report"
        gender_status = "Gender Not Present in Raw Report"
            
        for key in raw_report:
            if key not in annonymized:
                continue

            age = str(patient_info["age"].iloc[0])
            gender = patient_info["sex"].iloc[0]
            
            # --- AGE CHECK ---
            if age_status == "Age Not Present in Raw Report" and age in raw_report[key]:
                if age in annonymized[key]:
                    age_status = "Age Found (Not Anonymized)"
                elif "age" in annonymized[key].lower():
                    age_status = "Age Anonymized"

            # --- GENDER CHECK ---
            if gender_status == "Gender Not Present in Raw Report":
                for s in gender_mapper(gender):
                    pattern = rf"(?:[\s-]|^)\b{re.escape(s)}\b(?:[\s\.,-]|$)"

                    if re.search(pattern, raw_report[key], re.IGNORECASE):
                        if re.search(pattern, annonymized[key], re.IGNORECASE):
                            gender_status = "Gender Found (Not Anonymized)"
                            break
                        elif "gender" in annonymized[key].lower():
                            gender_status = "Gender Anonymized"
                            break

            # Sequence Matcher for text modifications
            raw_words = raw_report[key].split()
            annonymized_words = annonymized[key].split()
            matcher = SequenceMatcher(None, raw_words, annonymized_words)
            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == "replace":
                    original = " ".join(raw_words[i1:i2])
                    replacement = " ".join(annonymized_words[j1:j2])

        # Store record for final summary
        results.append({
            "File": file.name,
            "Patient ID": file_id,
            "Age Result": age_status,
            "Gender Result": gender_status
        })

    # Summary Report
    results_df = pd.DataFrame(results)
    
    print("\n--- SUMMARY REPORT ---")
    print(results_df.to_string(index=False))
    
    # Value Counts Breakdown
    print("\n--- AGE BREAKDOWN ---")
    print(results_df["Age Result"].value_counts())

    print("\n--- GENDER BREAKDOWN ---")
    print(results_df["Gender Result"].value_counts())

if __name__ == "__main__":
    main()