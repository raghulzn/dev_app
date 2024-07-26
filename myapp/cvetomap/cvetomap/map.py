import json
from .nvd import connector as nvd
from .open_ai import connector as openai

"""
Ethos:
Vuln -> CVE -> CWE -> ATT&CK -> D3FEND
"""


def handle_nvd_response(response: dict) -> str:
    cwe = response.get("weaknesses", [])
    return cwe


function_map_enrichment = {
    "nvd": nvd.NvdConnector
}
function_map_handlers = {
    "nvd": handle_nvd_response
}


def main(cve_id: str, nvd_api_key: str, openai_key, source: str = "nvd", extra_context: dict = None):
    cve_info = function_map_enrichment.get(source)(nvd_api_key).entrypoint(cve_id)
    vuln_info = cve_info.get("result", {}).get("response", {}).get("vulnerabilities", [{"cve": {"": ""}}])
    vuln = vuln_info[0]["cve"] if vuln_info else None
    cwe_info = function_map_handlers.get(source)(vuln)
    ai_message_template = f"""Role: Act as a cyber security and MITRE and STIX 2.1 expert. 

I need you to give me potential MITRE ATT&CK techniques and D3FEND tactics for the following CVE & CWE information: 

```
CVE ID: {cve_id}
CWE Information: {cwe_info}
Vulnerability Information: {vuln}
Additional Information: {extra_context}
```

Analyze the above information and return the data in the following JSON structure.

Response Structure Definition
{{
"techniques": [list of dictionaries (example below) with all the MITRE TTPs related to that vulnerability]
"technical_analysis": "A full technical analysis of the vulnerability",
"executive_analysis": "A full executive analysis of the vulnerability"
}}

Do NOT deviate from the above structure. Do not create any additional keys apart from what is already defined

{{
"techniques": [
{{
            "techniqueID": "Valid MITRE 1 Technique ID",
            "comment": "{{CVE ID Being Analysed}} - Why this is relevant and how to defend against it",
            "color": "#ff6666"
        }},
        {{
            "techniqueID": "Valid MITRE n Technique ID",
            "comment": "Why this is relevant and how to defend against it",
            "color": "#ff6666"
        }},
        ...as many MITRE Techniques as are found...
],
"technical_analysis": "A full analysis consisting of whats impacted in the CVE, what is the problem, related attack techniques, impact of exploitation,defence techniques and procedures to implement processes to detect against this in the future. This should be a full well formatted report with specific sections for each of the important bits. Remember this report is meant for a very tehnical audience. Ensure to always include as much as information as possible", 
"executive_analysis": "A full analysis consisting of whats impacted in the CVE, what is the problem, related attack techniques, impact of exploitation,defence techniques and procedures to implement processes to detect against this in the future. This should be a full well formatted report with specific sections for each of the important bits. Remember this report is meant for a very non-technical executive audience. Highlight risks and impact of this.",
"stix_bundle": "A valid STIX 2.1 bundle expressing all the related techniques, risks and defense strategies for this CVE. This should be in proper relation and should visualize properly. This should be a valid JSON STIX 2.1 bundle. This STIX bundle must have the vulnerabiliity as the main object and all other other parts as induvidual objects with relations added to the main object. There should be no hanging nodes, and all relationships should be meaningful and to the correct entity with the correct label. All courses of actions are to be linked properly with the correct technique they mitigate and all the defense points must be added as notes"
}}
    """
    ai_system_template = f"""Act as a cyber security expert. 

Your prime directive is to provide potential MITRE ATT&CK techniques and D3FEND tactics for the following CVE & CWE information.

All responses MUST be in JSON
    """
    message_template = [
        {
            "role": "system",
            "content": ai_system_template
        },
        {
            "role": "user",
            "content": ai_message_template
        }
    ]
    ai_response = openai.OpenAiConnector(openai_key).entrypoint("gpt-4o", message_template)
    print(ai_response)
    ai_response = ai_response["result"]["response"]["choices"][0]["message"]["content"]
    ai_response = json.loads(ai_response)
    print(ai_response)

    mitre_layer = {
        "name": f"*{cve_id}",
        "version": "3.0",
        "description": f"MITRE ATT&CK layer describing attack and defense strategies of CVE ID - {cve_id}",
        "domain": "mitre-enterprise",
        "techniques": ai_response["techniques"],
        "legendItems": [
            {
                "label": "CVE ID Information",
                "color": "#ff6666"
            }
        ]
    }
    technical_analysis = ai_response["technical_analysis"]
    executive_analysis = ai_response["executive_analysis"]
    stix_obj = ai_response["stix_bundle"]
    return technical_analysis, executive_analysis, mitre_layer, stix_obj

