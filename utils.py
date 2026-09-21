import re
from typing import Dict

def parse_radiology_report(text: str) -> Dict[str, str]:
    """Parses a radiology report string into a dictionary of section headings and contents.
    
    Supports keys in any case (UPPERCASE, lowercase, Title Case)
    and strips Markdown formatting (e.g. **SECTION:**).
    """
    # Regex pattern matching headings like **INDICATION:**, INDICATION:, Indication:
    # Captures heading name in group 1, and section body content until the next heading or EOF.
    pattern = re.compile(
        r'(?:\*\*|\#\#\s*)?([A-Za-z\s]+?)(?:\*\*|\:)?\s*:\s*(.*?)(?=(?:\n\s*(?:\*\*|\#\#\s*)?[A-Za-z\s]+?(?:\*\*|\:)?\s*:|\Z))',
        re.DOTALL
    )

    parsed_sections = {}
    matches = pattern.findall(text)

    for heading, content in matches:
        clean_key = heading.strip().lower()  # Normalize keys to lowercase
        clean_content = content.strip()
        
        # Collapse multi-line text and clean extra spaces while preserving paragraphs
        clean_content = re.sub(r'[ \t]+', ' ', clean_content)
        clean_content = re.sub(r'\n+', '\n', clean_content)
        
        if clean_key:
            parsed_sections[clean_key] = clean_content

    return parsed_sections

def gender_mapper(sex_abbrevation):
    if sex_abbrevation == "F":
        return ["female", "woman", "girl"]
    elif sex_abbrevation == "M":
        return ["man", "male"]
