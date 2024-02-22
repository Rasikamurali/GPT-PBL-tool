import openai 
openai.api_key = "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"
gpt_model = "gpt-3.5-turbo"

def call_gpt4(content, prompt): 
    response = openai.chat.completions.create(
    model=gpt_model,
    messages=[
        {"role": "system", "content": content},
        {"role": "user", "content": prompt }
        ]
    )
    goals = response.choices[0].message.content.split("\n")
    return goals
