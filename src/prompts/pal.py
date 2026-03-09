def make_extract_prompt(pid, text: str) -> str:
    return f"""
You are a deterministic JSON extraction engine.

Return EXACTLY one JSON object and NOTHING else.

Task:
1) Extract all AREA measurements only.
   Supported units:
    - square meters (m2, sqm, square meters)
    - square feet (sq ft, sqft, ft2)
    - hectares (ha)
    - acres (ac)
2) IGNORE PERIMETERS, DISTANCES, HEIGHTS, DIAMETERS.
3) Output ONLY VALID JSON array and NOTHING else.
4) NOT generate code

Output format:
[{{"property_id": number, "value": number, "unit": string}}]

Examples:
Input: <pid>12</pid> <text>"Plot is 35000 sq ft, perimeter 500 meters, garden 200 m2"</text>
Valid Output: [{{"property_id": 12, "value": 35000, "unit": "sqft"}}, {{"property_id": 12, "value": 200, "unit": "m2"}}]

Input: <pid>29</pid> <text>"2 acres of land, 500 meters from school, small yard of 50 sqm"</text>
Valid Output: [{{"property_id": 29, "value": 2, "unit": "ac"}}, {{"property_id": 29, "value": 50, "unit": "sqm"}}]

Input: <pid>34</pid> <text>"Plot is 35000 sq ft, perimeter 500 meters, garden 200 m2"</text>
Invalid Output: [{{"property_id": 34, "value": 35000, "unit": "sqft"}}, {{"property_id": 34, "value": 500, "unit": "m"}}, {{"property_id": 34, "value": 200, "unit": "m2"}}]

Input: <pid>56</pid> <text>"Plot is 4000 sq ft, perimeter 2,100 meters"</text>
Invalid Output: [{{"property_id": 56, "value": 4000, "unit": "sqft"}}, {{"property_id": 56, "value": 2100, "unit": "m"}}]

Input: <pid>87</pid> <text>"Plot is 4000 sq ft, perimeter 600 meters"</text>
Invalid Output: [{{"property_id": 87, "value": 4000, "unit": "sqft"}}, {{"property_id": 87, "value": 600, "unit": "m"}}]

Input: <pid>7</pid> <text>"Plot is 4000 sq ft, perimeter 2,100 meters"</text>
Invalid Output: [{{"value": 4000, "unit": "sqft"}}]


NOT generate code!
<pid>
{pid}
</pid>
<text>
{text}
</text>
""".strip()


def make_code_gen_prompt() -> str:
    return """
You are a Python code generator.

`import json` and the variable `data` are already defined before your code runs.
Do NOT redefine them. Do NOT add import statements.

`data` is a list of dicts like:
[{"property_id": 2, "value": 45000, "unit": "sqft"}]

Task: convert each area value to square meters, group by property_id, sum, then print result as JSON.

Conversions:
- m2, sqm, square meters -> no conversion needed
- sq ft, sqft, ft2       -> multiply by 0.092903
- ha                     -> multiply by 10000
- ac                     -> multiply by 4046.86

Output: last line must be exactly:
print(json.dumps(result))
where result = {str(property_id): total_m2}

Example final output: {"2": 4180.635}

Return ONLY the logic code. No imports. No markdown. No explanation.
""".strip()
