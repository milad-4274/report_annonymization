import json
import yaml
from pathlib import Path
from tqdm import tqdm
from string import Template
from utils import parse_radiology_report
from llm_caller import LLMCaller
from prompts import ANNONYMIATION_SYSTEM_PROMPT, ANNONYMIATION_USER_PROMPT, ENTITY_EXTRACTION_SYSTEM_PROMPT, ENTITY_EXTRACITON_USER_PROMPT


with open("config.yaml") as f:
    try:
        CONFIG = yaml.safe_load(f)
    except:
        raise ValueError("config.yaml file could not found")
    

def main():
    # FIND DATA
    data_path = Path(CONFIG["data"]["path"])
    output_dir = Path(CONFIG["data"]["output_dir"])
    if not output_dir.exists():
        output_dir.mkdir()
        
    # Convert prompt strings to string.Template objects
    anon_user_template = Template(ANNONYMIATION_USER_PROMPT)
    # entity_user_template = Template(ENTITY_EXTRACITON_USER_PROMPT)
    
    if not data_path.exists():
        raise ValueError(f"Data folder cannot be found {data_path}")
    
    total_files = len([p for p in data_path.iterdir() if p.is_file() and p.suffix[1:] in CONFIG["data"]["extensions"]])
    
    # ITERATE OVER DATA
    for file in tqdm(data_path.iterdir(), total=total_files):
        if not file.suffix[1:] in CONFIG["data"]["extensions"]:
            continue
    
        # LOAD FILE
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # PARSE FILE 
        before_json = parse_radiology_report(content)
        llm = LLMCaller(
            base_url= CONFIG["llm"]["base_url"],
            model_name= CONFIG["llm"]["model_name"],
            temperature= CONFIG["llm"]["temperature"],
        )
        deidentified_content = llm.generate(prompt= anon_user_template.substitute(report_text=before_json["indication"]), system_prompt=ANNONYMIATION_SYSTEM_PROMPT)
        # result = llm.generate_json(prompt=entity_user_template.substitute(anonymized_report_text=deidentified_content), system_prompt=ENTITY_EXTRACTION_SYSTEM_PROMPT)
        
        new_json = before_json.copy()
        new_json["indication"] = deidentified_content
        
        
        with open(output_dir / (file.stem + ".json") , "w") as f:
            json.dump(before_json, f)
        
        with open(output_dir / (file.stem + "_annonymized.json") , "w") as f:
            json.dump(new_json, f)
        
        # break

        
    
    # LLM CALL 
    
    # RETURN JSON

if __name__ == "__main__":
    main()