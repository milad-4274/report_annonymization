import json
from pathlib import Path
from string import Template
import yaml
from tqdm import tqdm

from llm_caller import LLMCaller
from prompts import ANNONYMIATION_SYSTEM_PROMPT, ANNONYMIATION_USER_PROMPT
from utils import parse_radiology_report

# Load configuration parameters
with open("config.yaml") as f:
    try:
        CONFIG = yaml.safe_load(f)
    except Exception as e:
        raise ValueError("config.yaml file could not be found or parsed") from e


def main():
    # Setup input and output directory paths
    data_path = Path(CONFIG["data"]["path"])
    output_dir = Path(CONFIG["data"]["output_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)

    if not data_path.exists():
        raise ValueError(f"Data folder cannot be found: {data_path}")

    # Prepare user prompt template and target extensions set
    anon_user_template = Template(ANNONYMIATION_USER_PROMPT)
    valid_extensions = set(CONFIG["data"]["extensions"])

    # Count matching target files for progress tracking
    matching_files = [
        p for p in data_path.iterdir() if p.is_file() and p.suffix.lstrip(".") in valid_extensions
    ]

    # Initialize LLM client connection using config settings
    llm = LLMCaller(
        base_url=CONFIG["llm"]["base_url"],
        model_name=CONFIG["llm"]["model_name"],
        temperature=CONFIG["llm"]["temperature"],
    )

    # Process each report file
    for file in tqdm(matching_files, total=len(matching_files)):
        # Read raw report content
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()

        # Parse text report into structured section keys
        before_json = parse_radiology_report(content)

        # De-identify the indication section using LLM
        prompt_text = anon_user_template.substitute(
            report_text=before_json.get("indication", "")
        )
        deidentified_content = llm.generate(
            prompt=prompt_text, system_prompt=ANNONYMIATION_SYSTEM_PROMPT
        )

        # Create updated JSON structure with de-identified content
        new_json = before_json.copy()
        new_json["indication"] = deidentified_content

        # Save both original parsed JSON and anonymized JSON outputs
        with open(output_dir / f"{file.stem}.json", "w", encoding="utf-8") as f:
            json.dump(before_json, f, indent=2)

        with open(output_dir / f"{file.stem}_annonymized.json", "w", encoding="utf-8") as f:
            json.dump(new_json, f, indent=2)


if __name__ == "__main__":
    main()