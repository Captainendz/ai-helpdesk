from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="TinyLlama/TinyLlama-1.1B-Chat-v1.0"
)

def generate_response(issue, knowledge):

    prompt = f"""
Issue: {issue}

Relevant Fix:
{knowledge}

Write a short IT support solution.
"""

    result = generator(
        prompt,
        max_new_tokens=40,
        temperature=0.2,
        do_sample=True,
        repetition_penalty=1.2
    )

    generated_text = result[0]["generated_text"]

    response = generated_text.replace(prompt, "").strip()

    return response