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

  ## 📈 Evaluation Results Sample

python .\evaluation.py
```
--- SUMMARY REPORT ---
                               File  Patient ID     Age Result                  Gender Result
            prompt_001_rapport.json           1 Age Anonymized              Gender Anonymized
            prompt_002_rapport.json           2 Age Anonymized              Gender Anonymized
            prompt_003_rapport.json           3 Age Anonymized              Gender Anonymized
            prompt_004_rapport.json           4 Age Anonymized              Gender Anonymized
            prompt_005_rapport.json           5 Age Anonymized              Gender Anonymized
            prompt_006_rapport.json           6 Age Anonymized              Gender Anonymized
            prompt_007_rapport.json           7 Age Anonymized              Gender Anonymized
            prompt_008_rapport.json           8 Age Anonymized              Gender Anonymized
            prompt_009_rapport.json           9 Age Anonymized              Gender Anonymized
            prompt_010_rapport.json          10 Age Anonymized              Gender Anonymized
            prompt_011_rapport.json          11 Age Anonymized              Gender Anonymized
            prompt_012_rapport.json          12 Age Anonymized Gender Found (Not Anonymized)
            prompt_013_rapport.json          13 Age Anonymized              Gender Anonymized
            prompt_014_rapport.json          14 Age Anonymized              Gender Anonymized
            prompt_015_rapport.json          15 Age Anonymized              Gender Anonymized
            prompt_016_rapport.json          16 Age Anonymized              Gender Anonymized
            prompt_017_rapport.json          17 Age Anonymized              Gender Anonymized
            prompt_018_rapport.json          18 Age Anonymized              Gender Anonymized
            prompt_019_rapport.json          19 Age Anonymized              Gender Anonymized
            prompt_020_rapport.json          20 Age Anonymized              Gender Anonymized
            prompt_021_rapport.json          21 Age Anonymized              Gender Anonymized
            prompt_022_rapport.json          22 Age Anonymized              Gender Anonymized
            prompt_023_rapport.json          23 Age Anonymized              Gender Anonymized
            prompt_024_rapport.json          24 Age Anonymized              Gender Anonymized
            prompt_025_rapport.json          25 Age Anonymized              Gender Anonymized
            prompt_026_rapport.json          26 Age Anonymized              Gender Anonymized
            prompt_027_rapport.json          27 Age Anonymized              Gender Anonymized
            prompt_028_rapport.json          28 Age Anonymized              Gender Anonymized
            prompt_029_rapport.json          29 Age Anonymized              Gender Anonymized
            prompt_030_rapport.json          30 Age Anonymized              Gender Anonymized
            prompt_031_rapport.json          31 Age Anonymized              Gender Anonymized
            prompt_032_rapport.json          32 Age Anonymized              Gender Anonymized
            prompt_033_rapport.json          33 Age Anonymized              Gender Anonymized
            prompt_034_rapport.json          34 Age Anonymized              Gender Anonymized
            prompt_035_rapport.json          35 Age Anonymized              Gender Anonymized
            prompt_036_rapport.json          36 Age Anonymized              Gender Anonymized
            prompt_037_rapport.json          37 Age Anonymized              Gender Anonymized
            prompt_038_rapport.json          38 Age Anonymized              Gender Anonymized
            prompt_039_rapport.json          39 Age Anonymized              Gender Anonymized
            prompt_040_rapport.json          40 Age Anonymized              Gender Anonymized
            prompt_041_rapport.json          41 Age Anonymized              Gender Anonymized
            prompt_042_rapport.json          42 Age Anonymized              Gender Anonymized
            prompt_043_rapport.json          43 Age Anonymized              Gender Anonymized
            prompt_044_rapport.json          44 Age Anonymized              Gender Anonymized
            prompt_045_rapport.json          45 Age Anonymized              Gender Anonymized
            prompt_046_rapport.json          46 Age Anonymized              Gender Anonymized
            prompt_047_rapport.json          47 Age Anonymized              Gender Anonymized
            prompt_048_rapport.json          48 Age Anonymized              Gender Anonymized
            prompt_049_rapport.json          49 Age Anonymized              Gender Anonymized
            prompt_050_rapport.json          50 Age Anonymized              Gender Anonymized
            prompt_051_rapport.json          51 Age Anonymized              Gender Anonymized
            prompt_052_rapport.json          52 Age Anonymized              Gender Anonymized
            prompt_053_rapport.json          53 Age Anonymized              Gender Anonymized
            prompt_054_rapport.json          54 Age Anonymized              Gender Anonymized
            prompt_055_rapport.json          55 Age Anonymized              Gender Anonymized
            prompt_056_rapport.json          56 Age Anonymized              Gender Anonymized
            prompt_057_rapport.json          57 Age Anonymized              Gender Anonymized
            prompt_058_rapport.json          58 Age Anonymized              Gender Anonymized
            prompt_059_rapport.json          59 Age Anonymized              Gender Anonymized
            prompt_060_rapport.json          60 Age Anonymized              Gender Anonymized
            prompt_061_rapport.json          61 Age Anonymized              Gender Anonymized
            prompt_062_rapport.json          62 Age Anonymized              Gender Anonymized
            prompt_063_rapport.json          63 Age Anonymized              Gender Anonymized
            prompt_064_rapport.json          64 Age Anonymized              Gender Anonymized
            prompt_065_rapport.json          65 Age Anonymized              Gender Anonymized
            prompt_066_rapport.json          66 Age Anonymized              Gender Anonymized
            prompt_067_rapport.json          67 Age Anonymized              Gender Anonymized
            prompt_068_rapport.json          68 Age Anonymized              Gender Anonymized
            prompt_069_rapport.json          69 Age Anonymized              Gender Anonymized
            prompt_070_rapport.json          70 Age Anonymized              Gender Anonymized
            prompt_071_rapport.json          71 Age Anonymized              Gender Anonymized
            prompt_072_rapport.json          72 Age Anonymized              Gender Anonymized
            prompt_073_rapport.json          73 Age Anonymized              Gender Anonymized
            prompt_074_rapport.json          74 Age Anonymized              Gender Anonymized
            prompt_075_rapport.json          75 Age Anonymized              Gender Anonymized
            prompt_076_rapport.json          76 Age Anonymized              Gender Anonymized
            prompt_077_rapport.json          77 Age Anonymized              Gender Anonymized
            prompt_078_rapport.json          78 Age Anonymized              Gender Anonymized
            prompt_079_rapport.json          79 Age Anonymized              Gender Anonymized
            prompt_080_rapport.json          80 Age Anonymized              Gender Anonymized
            prompt_081_rapport.json          81 Age Anonymized              Gender Anonymized
            prompt_082_rapport.json          82 Age Anonymized              Gender Anonymized
            prompt_083_rapport.json          83 Age Anonymized              Gender Anonymized
            prompt_084_rapport.json          84 Age Anonymized              Gender Anonymized
            prompt_085_rapport.json          85 Age Anonymized              Gender Anonymized
            prompt_086_rapport.json          86 Age Anonymized              Gender Anonymized
            prompt_087_rapport.json          87 Age Anonymized              Gender Anonymized
            prompt_088_rapport.json          88 Age Anonymized              Gender Anonymized
            prompt_089_rapport.json          89 Age Anonymized              Gender Anonymized
            prompt_090_rapport.json          90 Age Anonymized              Gender Anonymized
            prompt_091_rapport.json          91 Age Anonymized              Gender Anonymized
            prompt_092_rapport.json          92 Age Anonymized              Gender Anonymized
            prompt_093_rapport.json          93 Age Anonymized              Gender Anonymized
            prompt_094_rapport.json          94 Age Anonymized              Gender Anonymized
            prompt_095_rapport.json          95 Age Anonymized              Gender Anonymized
            prompt_096_rapport.json          96 Age Anonymized              Gender Anonymized
            prompt_097_rapport.json          97 Age Anonymized              Gender Anonymized
            prompt_098_rapport.json          98 Age Anonymized              Gender Anonymized
            prompt_099_rapport.json          99 Age Anonymized              Gender Anonymized
            prompt_100_rapport.json         100 Age Anonymized              Gender Anonymized
            prompt_101_rapport.json         101 Age Anonymized              Gender Anonymized
            prompt_102_rapport.json         102 Age Anonymized              Gender Anonymized
            prompt_103_rapport.json         103 Age Anonymized              Gender Anonymized
            prompt_104_rapport.json         104 Age Anonymized              Gender Anonymized
            prompt_105_rapport.json         105 Age Anonymized              Gender Anonymized
            prompt_106_rapport.json         106 Age Anonymized              Gender Anonymized
            prompt_107_rapport.json         107 Age Anonymized              Gender Anonymized
            prompt_108_rapport.json         108 Age Anonymized              Gender Anonymized
            prompt_109_rapport.json         109 Age Anonymized              Gender Anonymized
            prompt_110_rapport.json         110 Age Anonymized              Gender Anonymized
            prompt_111_rapport.json         111 Age Anonymized              Gender Anonymized
            prompt_112_rapport.json         112 Age Anonymized              Gender Anonymized
            prompt_113_rapport.json         113 Age Anonymized              Gender Anonymized
            prompt_114_rapport.json         114 Age Anonymized              Gender Anonymized
            prompt_115_rapport.json         115 Age Anonymized              Gender Anonymized
            prompt_116_rapport.json         116 Age Anonymized              Gender Anonymized
            prompt_117_rapport.json         117 Age Anonymized              Gender Anonymized
            prompt_118_rapport.json         118 Age Anonymized              Gender Anonymized
            prompt_119_rapport.json         119 Age Anonymized              Gender Anonymized
            prompt_120_rapport.json         120 Age Anonymized              Gender Anonymized
            prompt_121_rapport.json         121 Age Anonymized              Gender Anonymized
            prompt_122_rapport.json         122 Age Anonymized              Gender Anonymized
            prompt_123_rapport.json         123 Age Anonymized              Gender Anonymized
            prompt_124_rapport.json         124 Age Anonymized              Gender Anonymized
            prompt_125_rapport.json         125 Age Anonymized              Gender Anonymized
            prompt_126_rapport.json         126 Age Anonymized              Gender Anonymized
            prompt_127_rapport.json         127 Age Anonymized              Gender Anonymized
            prompt_128_rapport.json         128 Age Anonymized              Gender Anonymized
            prompt_129_rapport.json         129 Age Anonymized              Gender Anonymized
            prompt_130_rapport.json         130 Age Anonymized              Gender Anonymized
            prompt_131_rapport.json         131 Age Anonymized              Gender Anonymized
            prompt_132_rapport.json         132 Age Anonymized              Gender Anonymized
            prompt_133_rapport.json         133 Age Anonymized              Gender Anonymized
            prompt_134_rapport.json         134 Age Anonymized              Gender Anonymized
            prompt_135_rapport.json         135 Age Anonymized              Gender Anonymized
            prompt_136_rapport.json         136 Age Anonymized              Gender Anonymized
            prompt_137_rapport.json         137 Age Anonymized              Gender Anonymized
            prompt_138_rapport.json         138 Age Anonymized              Gender Anonymized
            prompt_139_rapport.json         139 Age Anonymized              Gender Anonymized
            prompt_140_rapport.json         140 Age Anonymized              Gender Anonymized
            prompt_141_rapport.json         141 Age Anonymized              Gender Anonymized
            prompt_142_rapport.json         142 Age Anonymized              Gender Anonymized
            prompt_143_rapport.json         143 Age Anonymized              Gender Anonymized
            prompt_144_rapport.json         144 Age Anonymized              Gender Anonymized
            prompt_145_rapport.json         145 Age Anonymized              Gender Anonymized
            prompt_146_rapport.json         146 Age Anonymized              Gender Anonymized
            prompt_147_rapport.json         147 Age Anonymized              Gender Anonymized
            prompt_148_rapport.json         148 Age Anonymized              Gender Anonymized
            prompt_149_rapport.json         149 Age Anonymized              Gender Anonymized
            prompt_150_rapport.json         150 Age Anonymized              Gender Anonymized
            prompt_151_rapport.json         151 Age Anonymized              Gender Anonymized
            prompt_152_rapport.json         152 Age Anonymized              Gender Anonymized
            prompt_153_rapport.json         153 Age Anonymized              Gender Anonymized
            prompt_154_rapport.json         154 Age Anonymized              Gender Anonymized
            prompt_155_rapport.json         155 Age Anonymized              Gender Anonymized
            prompt_156_rapport.json         156 Age Anonymized              Gender Anonymized
            prompt_157_rapport.json         157 Age Anonymized              Gender Anonymized
            prompt_158_rapport.json         158 Age Anonymized              Gender Anonymized
            prompt_159_rapport.json         159 Age Anonymized              Gender Anonymized
            prompt_160_rapport.json         160 Age Anonymized              Gender Anonymized
            prompt_161_rapport.json         161 Age Anonymized              Gender Anonymized
            prompt_162_rapport.json         162 Age Anonymized              Gender Anonymized
            prompt_163_rapport.json         163 Age Anonymized              Gender Anonymized
            prompt_164_rapport.json         164 Age Anonymized Gender Found (Not Anonymized)
            prompt_165_rapport.json         165 Age Anonymized              Gender Anonymized
            prompt_166_rapport.json         166 Age Anonymized              Gender Anonymized
            prompt_167_rapport.json         167 Age Anonymized              Gender Anonymized
            prompt_168_rapport.json         168 Age Anonymized              Gender Anonymized
            prompt_169_rapport.json         169 Age Anonymized              Gender Anonymized
            prompt_170_rapport.json         170 Age Anonymized              Gender Anonymized
            prompt_171_rapport.json         171 Age Anonymized              Gender Anonymized
            prompt_172_rapport.json         172 Age Anonymized              Gender Anonymized
            prompt_173_rapport.json         173 Age Anonymized              Gender Anonymized
            prompt_174_rapport.json         174 Age Anonymized Gender Found (Not Anonymized)
            prompt_175_rapport.json         175 Age Anonymized              Gender Anonymized
            prompt_176_rapport.json         176 Age Anonymized              Gender Anonymized
            prompt_177_rapport.json         177 Age Anonymized              Gender Anonymized
            prompt_178_rapport.json         178 Age Anonymized              Gender Anonymized
            prompt_179_rapport.json         179 Age Anonymized              Gender Anonymized
            prompt_180_rapport.json         180 Age Anonymized              Gender Anonymized
            prompt_181_rapport.json         181 Age Anonymized              Gender Anonymized
            prompt_182_rapport.json         182 Age Anonymized              Gender Anonymized
            prompt_183_rapport.json         183 Age Anonymized              Gender Anonymized
            prompt_184_rapport.json         184 Age Anonymized              Gender Anonymized
            prompt_185_rapport.json         185 Age Anonymized              Gender Anonymized
            prompt_186_rapport.json         186 Age Anonymized              Gender Anonymized
            prompt_187_rapport.json         187 Age Anonymized              Gender Anonymized
            prompt_188_rapport.json         188 Age Anonymized              Gender Anonymized
            prompt_189_rapport.json         189 Age Anonymized              Gender Anonymized
            prompt_190_rapport.json         190 Age Anonymized              Gender Anonymized
            prompt_191_rapport.json         191 Age Anonymized              Gender Anonymized
            prompt_192_rapport.json         192 Age Anonymized              Gender Anonymized
            prompt_193_rapport.json         193 Age Anonymized              Gender Anonymized
            prompt_194_rapport.json         194 Age Anonymized              Gender Anonymized
            prompt_195_rapport.json         195 Age Anonymized              Gender Anonymized
            prompt_196_rapport.json         196 Age Anonymized              Gender Anonymized
            prompt_197_rapport.json         197 Age Anonymized              Gender Anonymized
            prompt_198_rapport.json         198 Age Anonymized              Gender Anonymized
            prompt_199_rapport.json         199 Age Anonymized              Gender Anonymized
            prompt_200_rapport.json         200 Age Anonymized              Gender Anonymized

--- AGE BREAKDOWN ---
Age Result
Age Anonymized    200
Name: count, dtype: int64

--- GENDER BREAKDOWN ---
Gender Result
Gender Anonymized                197
Gender Found (Not Anonymized)      3
Name: count, dtype: int64
```