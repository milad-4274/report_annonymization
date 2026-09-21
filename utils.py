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

# --- Example Usage ---
if __name__ == "__main__":
    report_text = """**CT PELVIS**

**Indication:** 58-year-old female presenting with right-sided pelvic pain. Clinical query regarding diverticulitis versus sacroiliitis.

**Technique:** Axial CT images were acquired through the pelvis without intravenous contrast. Multiplanar reformations were performed in the coronal and sagittal planes.

**Findings:**
The visualized loops of the bowel within the pelvis demonstrate no evidence of wall thickening, pericolic fat stranding, or abscess formation to suggest acute diverticulitis. There is no free intraperitoneal air or pelvic fluid collection noted.

The urinary bladder is partially filled and appears unremarkable, with smooth wall contours and no obvious intraluminal masses. The prostate is not applicable; the uterus and adnexa are visualized and appear stable for the patient's age, though there are small, benign-appearing uterine leiomyomas.

Regarding the musculoskeletal system, there is severe degenerative change involving the right sacroiliac joint. This is characterized by marked joint space narrowing, prominent subchondral sclerosis, and several marginal osteophytes. There is some mild irregularity of the joint surfaces, but no aggressive erosions or active inflammatory fluid collections are seen. The left sacroiliac joint remains well-preserved with normal joint space and no sclerotic changes.

The hip joints are intact. There is a small, incidental cystic lesion in the left femoral head, likely a benign geode. The pelvic girdle and visualized lumbar spine show mild osteophytic spurring consistent with age-related spondylosis. The visualized soft tissues of the pelvic wall are symmetric and unremarkable.

**Conclusion:**
Severe osteoarthritis of the right sacroiliac joint. No evidence of acute sacroiliitis or associated inflammatory complications."""

    result = parse_radiology_report(report_text)
    
    import json
    print(json.dumps(result, indent=2))