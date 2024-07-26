# CVETOMAP - CVE to MITRE ATT&CK Mapping Tool 

## Overview
`cvetomap` is a Python pip library that converts a given CVE ID to a full analysis. It maps the CVE to MITRE ATT&CK techniques and tactics and provides suggested defense techniques. The tool generates both a MITRE Layer for the attack and detailed reports tailored for both technical and executive audiences.

## Features
- Fetches CVE details using the NVD API.
- Utilizes OpenAI to generate a comprehensive technical and executive analysis.
- Maps the CVE to relevant MITRE ATT&CK techniques and D3FEND tactics.
- Outputs a structured JSON result and a MITRE ATT&CK layer.

## Installation

```bash
pip install cvetomap
```

## Usage

### Entry Point
The main function to use is:

```python
from cvetomap import map

technical_analysis, executive_analysis, mitre_layer = map.main(
    cve_id='CVE-XXXX-YYYY',
    nvd_api_key='YOUR_NVD_API_KEY',
    openai_key='YOUR_OPENAI_API_KEY',
    source='nvd',
    extra_context={...Extra context or data (Eg: ASM enrichments, TI Info etc.)...}
)
```

### Parameters
- `cve_id` (str): The CVE ID to analyze.
- `nvd_api_key` (str): API key for NVD (National Vulnerability Database) to fetch CVE details.
- `openai_key` (str): API key for OpenAI to generate the analysis.
- `source` (str): Data source for enrichment, default is `"nvd"`.
- `extra_context` (dict, optional): Additional context to provide in the analysis.

## Example
```python
from cvetomap import main

cve_id = 'CVE-2021-34527'
nvd_api_key = 'your_nvd_api_key'
openai_key = 'your_openai_api_key'
extra_context = {'environment': 'production'}

technical_analysis, executive_analysis, mitre_layer = main(cve_id, nvd_api_key, openai_key, extra_context=extra_context)

print(f"Technical Analysis: {technical_analysis}")
print(f"Executive Analysis: {executive_analysis}")
print(f"MITRE Layer: {json.dumps(mitre_layer, indent=2)}")
```

## Output
The `main` function will return three items:
1. `technical_analysis`: A comprehensive report for a technical audience, covering the CVE impact, related techniques and tactics, and defense strategies.
2. `executive_analysis`: A high-level report for an executive audience, highlighting the risks and impact of the CVE and suggested mitigation strategies.
3. `mitre_layer`: The JSON structure representing the MITRE ATT&CK layer, including mapped techniques and defenses.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request or open an issue to discuss any changes.

## License
[MIT License](LICENSE)