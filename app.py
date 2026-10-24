import os
import gradio as gr
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY missing. Add it to your .env file."
    )

client = Groq(api_key=api_key)


def generate_email(recipient, purpose, tone, details):
    if not recipient.strip() or not purpose.strip():
        return "Please enter the recipient and email purpose."

    prompt = f"""
    Write an email with the following details:

    Recipient: {recipient}
    Purpose: {purpose}
    Tone: {tone}
    Additional details: {details}

    Include a subject line and email body.
    Keep it clear and relevant.
    Do not invent facts.
    """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional email writer."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating email: {e}"


with gr.Blocks(title="AI Email Generator") as app:
    gr.Markdown("# AI Email Generator")
    gr.Markdown("Generate emails with the help of AI.")

    recipient = gr.Textbox(label="Recipient")
    purpose = gr.Textbox(label="Email Purpose")

    tone = gr.Dropdown(
        choices=["Professional", "Friendly", "Formal", "Concise"],
        value="Professional",
        label="Email Tone"
    )

    details = gr.Textbox(
        label="Additional Details",
        lines=4
    )

    generate = gr.Button("Generate Email")
    output = gr.Textbox(label="Generated Email", lines=12)

    generate.click(
        fn=generate_email,
        inputs=[recipient, purpose, tone, details],
        outputs=output
    )


if __name__ == "__main__":
    app.launch()
