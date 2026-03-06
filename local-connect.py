import ollama

PROMPT = """
You are a strict JSON extraction engine.

Return ONLY valid JSON. No explanations.

Rules:
1. Output must strictly follow the schema.
2. If a value is partially specified (e.g., "March 2026"), normalize to the first day of that period:
   - Month + Year → YYYY-MM-01
   - Year only → YYYY-01-01
3. "skills" = professional skills explicitly mentioned.
4. "mentioned_technologies" = ANY programming languages, frameworks, databases, or cloud services mentioned in the text.
   This field MUST include all detected technologies, even if duplicated in "skills".
5. If no technologies are found, return [] (never null).
6. Do not invent information.

Schema:
{{
  "full_name": string | null,
  "email": string | null,
  "phone": string | null,
  "company": string | null,
  "job_title": string | null,
  "years_of_experience": number | null,
  "skills": string[],
  "location": string | null,
  "mentioned_technologies": string[],
  "availability": string | null
}}

Text:
{input_text}
"""

def make_prompt(query):
    return PROMPT.format(input_text=query)


msg = make_prompt(
    """
Hi, my name is Michael Johnson. 
I'm a Senior Backend Engineer at Stripe.
I have around 8 years of experience working mostly with Java, Spring Boot, AWS, and PostgreSQL.
You can reach me at michael.johnson@email.com or +1-202-555-0148.
Currently based in Berlin and open to new opportunities starting March 2026.
"""
)

print(msg)


res = ollama.chat(
    model='llama3.2',
    messages=[{"role": "user", "content": msg}],
    options={
        "temperature": 0.2,
        "num_ctx": 4096
    }
)

print(res.message.content)