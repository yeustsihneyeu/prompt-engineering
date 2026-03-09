def make_prompt(property_id: str, text: str) -> str:
    pid = str(property_id)
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

Example 1:
Input:
"In a prime suburban location, this residential plot covers 2.5 hectares. The property features a 500-meter boundary and is within 3 kilometers of top-rated schools and shopping centers. The area is known for its peaceful environment and scenic views."

Output: {{"{pid}": 25000.00}}


Example 2:
Input:
"This unique piece of land measures 1.2 hectares (12,000 square meters), offering a vast and versatile canvas for a transformative project. Located in a prime commercial district, the property boasts a strategic position with a frontage of 80 meters along a major thoroughfare. The land is rectangular in shape, with a depth of 150 meters and a perimeter of 460 meters. The site is currently zoned for mixed-use development, allowing for a combination of residential, retail, and office spaces. The property is situated just 300 meters from a bustling transportation hub, ensuring excellent connectivity and accessibility. The land also features a gentle slope with an average gradient of 5%, providing opportunities for unique architectural designs and panoramic views. With an elevation ranging from 25 to 35 meters above sea level, the property benefits from excellent drainage and natural lighting. Additionally, the site includes utility access points for water, electricity, and high-speed internet, each located within 50 meters of the property's boundaries. With its prime location, ample size, and development potential, this property presents an exceptional investment opportunity."

Output: {{"{pid}": 12000.00}}


Example 3:
Input:
"In a prestigious residential area, this plot covers 45,000 square feet with a 600-meter perimeter. Two kilometers from the nearest school and shopping center, it’s ideal for family homes. At an elevation of 100 meters, the climate is pleasant year-round. The land supports luxury residences or a small community and includes a historic building from the early 1900s, standing 12 meters tall."

Output: {{"{pid}": 4180.64}}

<text>
{text}
</text>
""".strip()