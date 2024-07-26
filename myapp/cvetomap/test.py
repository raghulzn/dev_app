import json
from cvetomap import map

# CVE ID To Analyse
cve_id = input("Enter CVE ID To Analyze (Eg: CVE-2021-44228): ")

# Call the mappers main function
technical_analysis, executive_analysis, mitre_layer, stix_obj = map.main(cve_id,
                                                               "33be7796-4783-41fe-983f-09672b60cd16",
                                                               "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",
                                                               "nvd")

# Save reports individually
with open(f"{cve_id} (Technical Analysis).md", "w") as f:
    f.write(technical_analysis)

with open(f"{cve_id} (Executive Analysis).md", "w") as f:
    f.write(executive_analysis)

with open(f"{cve_id}-MITRE-ATT&CK-Layer.json", "w") as f:
    f.write(
        json.dumps(
            mitre_layer, indent=4
        )
    )

with open(f"STIX Bundle - {cve_id}.json", "w") as f:
    f.write(
        json.dumps(
            stix_obj, indent=4
        )
    )
