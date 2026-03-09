def make_prompt_hidden(property_id: str, text: str) -> str:
    pid = str(property_id)
    return f"""
You are a deterministic JSON extraction engine.

Think step-by-step internally before answering.
Do NOT output your reasoning.

Return EXACTLY one JSON object and NOTHING else.

Output format:
{{ "{pid}": number | null }}

Task:
Extract the total land plot area.

Allowed units:
- m2, sqm, square meters
- sq ft, sqft, ft2
- hectares (ha)

Conversions:
- 1 hectare = 10000 square meters
- 1 square foot = 0.092903 square meters

Rounding:
Round to exactly 2 decimals.

Internal reasoning steps (do not output):
1. Scan the text for numbers associated with land/plot area.
2. Ignore building area, living area, perimeter, distances, and heights.
3. Identify the unit (m2, sqft, ha).
4. Normalize the number (remove commas if needed).
5. Convert to square meters if required.
6. Round to exactly 2 decimals.
7. Output JSON.

If no valid land plot area exists:
{{ "{pid}": null }}


<text>
{text}
</text>
""".strip()


def make_prompt_visible(pid: str, text: str):
    return f"""
You are a deterministic JSON extraction engine.

Return EXACTLY one JSON object and NOTHING else AFTER the <answer> tag.

You MUST output in this exact structure:
<think>
TRACE:
- found_area_text: <copy the exact matched substring or "none">
- unit: <m2|sqft|ha|none>
- raw_value: <number as seen in text or "none">
- converted_to_m2: <number with decimal dot or "none">
- rounded_m2: <number with 2 decimals or "none">
</think>
<answer>
{{"{pid}": number | null}}
</answer>

Rules:
1) JSON must contain exactly one key: "{pid}"
2) Value must be JSON number or null (not string)
3) Decimal dot only. No thousands separators.
4) If number, it must match: ^\d+(\.\d+)?$

Task:
Extract ONLY total land plot area if explicitly expressed as:
- square meters (m2, sqm, square meters)
- square feet (sq ft, sqft, ft2)
- hectares (ha)

Conversions:
- 1 hectare = 10000 square meters
- 1 square foot = 0.092903 square meters

Rounding:
Round to exactly 2 decimals.

If no valid land plot area exists:
{{"{pid}": null}}

Examples:

Example 1:
Input:
"In a prime suburban location, this residential plot covers 2.5 hectares."

Output:
<think>
TRACE:
- found_area_text: "covers 2.5 hectares"
- unit: ha
- raw_value: 2.5
- converted_to_m2: 25000
- rounded_m2: 25000.00
</think>
<answer>
{{"{pid}": 25000.00}}
</answer>

Example 2:
Input:
"In a prestigious residential area, this plot covers 45,000 square feet."

Output:
<think>
TRACE:
- found_area_text: "covers 45,000 square feet"
- unit: sqft
- raw_value: 45000
- converted_to_m2: 4180.635
- rounded_m2: 4180.64
</think>
<answer>
{{"{pid}": 4180.64}}
</answer>

<text>
{text}
</text>
"""