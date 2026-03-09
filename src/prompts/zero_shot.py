def make_prompt(pid: str, text: str) -> str:
    return f"""
You are a deterministic JSON extraction engine.

Return EXACTLY one JSON object and NOTHING else.

Output format:
{{ "{pid}": number | null }}

Rules:
1) The JSON object must contain exactly one key: "{pid}".
2) The value must be either a JSON number or null (not a string).
3) Use decimal dot (.) only. No thousands separators.
4) If value is a number, it must match: ^\\d+(\\.\\d+)?$

Task:
Extract ONLY total land plot area if explicitly expressed as:
- square meters (m2, sqm, square meters)
- square feet (sq ft, sqft, ft2)
- hectares (ha)

Allowed numbers:
- Area value must come from <text>.
- Conversion constants may come from these instructions.

Conversions:
- 1 hectare = 10000 square meters
- 1 square foot = 0.092903 square meters

Rounding:
Round to exactly 2 decimals.

If no valid land plot area in allowed units exists:
{{ "{pid}": null }}

<text>
{text}
</text>
""".strip()