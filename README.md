# Radiology Report Anonymization & Processing Pipeline

An automated Python pipeline designed to parse, de-identify, and extract clinical entities from raw unstructured radiology reports using Large Language Models (LLMs) via an OpenAI-compatible API backend (such as Ollama or vLLM).

---

## 📌 Project Overview

Processing medical text requires strict compliance with privacy standards while preserving key clinical information. This project automates the workflow of reading raw markdown or text radiology reports, breaking them down into structured JSON sections, and leveraging local LLMs to mask Sensitive Personal Information (SPI) such as patient age and gender.

### Key Features
* **Section Parsing:** Regex-based parser supporting flexible header cases (`INDICATION:`, `**Findings:**`, etc.) to structure unstructured medical reports into JSON dictionaries.
* **LLM De-identification:** Context-aware anonymization that replaces demographic identifiers (`32-year-old male`) with generic placeholder tags (`[AGE]-year-old [GENDER]`) without altering clinical diagnoses.
* **Robust LLM Connector:** Custom OpenAI-compatible client wrapper (`LLMCaller`) with built-in retry mechanisms (`tenacity`) and JSON mode fallback parsing.
* **Batch Processing:** Progress-tracked batch execution using `tqdm` for handling datasets.

---

## 🛠 Project Structure

```text
.
├── main.py           # Pipeline entry point; handles batch data loading, parsing, and LLM orchestration
├── llm_caller.py     # OpenAI-compatible API wrapper with retry logic and JSON formatting
├── utils.py          # Helper functions for report section regex parsing and gender keyword expansion
├── prompts.py        # System and user prompt templates for anonymization and entity extraction
├── config.yaml       # Configuration file for data paths, file extensions, and LLM endpoint parameters
├── data/             # Input directory containing raw radiology report files (.md)
└── result/           # Output directory storing raw parsed JSONs and anonymized JSONs
```

---

## ⚙️ Prerequisites & Setup

### 1. Environment & Dependencies

Ensure you have Python 3.9+ installed. Install the required Python dependencies:

```bash
pip install openai PyYAML tqdm tenacity pandas scikit-learn
```

### 2. Local LLM Backend (Ollama)

This project defaults to using **Ollama** serving a local model (e.g., `qwen2.5-coder:1.5b` or `qwen2.5:7b`).

1. Install Ollama from [ollama.com](https://ollama.com).
2. Pull your target model:
   ```bash
   ollama pull qwen2.5-coder:1.5b
   ```
3. Ensure the local server is running at `http://localhost:11434`.

---

## 🚀 Configuration & Execution

### 1. Configuration (`config.yaml`)

Update `config.yaml` to match your directory structure and LLM backend specs:

```yaml
data:
  path: "data"                         # Directory containing input .md files
  extensions: 
    - "md"                             # Extensions to process
  output_dir: "result"                 # Directory where JSON outputs are saved
  excel: "RapRI_prompt_design.xlsx"    # Supplemental reference data

llm:
  base_url: "http://localhost:11434/v1" # Local Ollama endpoint
  model_name: "qwen2.5-coder:1.5b"    # LLM target model
  temperature: 0.0                    # Low temperature for deterministic outputs
```

### 2. Running the Pipeline

Place your raw radiology reports (in Markdown `.md` format) into the `data/` folder, then execute:

```bash
python main.py
```

---

## 📊 Processing Workflow & Sample Output

### Input Format (`data/sample_report.md`)

```markdown
**CT CHEST WITH CONTRAST**

**Indication:** 32-year-old male presenting with chest pain. Evaluate for pulmonary embolism.

**Findings:**
The lungs are clear. There is no evidence of focal consolidation...

**Conclusion:**
Single 3 cm pulmonary artery aneurysm in the right lower lobe.
```

### Generated Outputs (`result/`)

For every processed file (e.g., `sample.md`), two JSON files are generated in the `result/` directory:

#### 1. Raw Structured Output (`sample.json`)
```json
{
  "ct chest with contrast": "",
  "indication": "32-year-old male presenting with chest pain. Evaluate for pulmonary embolism.",
  "findings": "The lungs are clear. There is no evidence of focal consolidation...",
  "conclusion": "Single 3 cm pulmonary artery aneurysm in the right lower lobe."
}
```

#### 2. Anonymized Output (`sample_annonymized.json`)
```json
{
  "ct chest with contrast": "",
  "indication": "[AGE]-year-old [GENDER] presenting with chest pain. Evaluate for pulmonary embolism.",
  "findings": "The lungs are clear. There is no evidence of focal consolidation...",
  "conclusion": "Single 3 cm pulmonary artery aneurysm in the right lower lobe."
}
```