
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="centered"
)

# Custom UI styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #f5fff9, #edf5ff);
}
.block-container {
    max-width: 800px;
    padding-top: 2rem;
}
h1 {
    color: #147d57;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #526477;
}
.stButton > button {
    background-color: #16845b;
    color: white;
    border-radius: 10px;
    width: 100%;
    height: 45px;
    border: none;
}
.stButton > button:hover {
    background-color: #106b48;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# App heading
st.title("✉️ AI Email Generator")
st.markdown(
    '<p class="subtitle">Create clear, professional emails in seconds.</p>',
    unsafe_allow_html=True
)

st.divider()

# Email input fields
with st.form("email_form"):
    recipient = st.text_input(
        "Recipient",
        placeholder="e.g. Client, professor, or manager"
    )

    purpose = st.text_input(
        "Email Purpose",
        placeholder="e.g. Follow up on a project proposal"
    )

    tone = st.selectbox(
        "Choose Email Tone",
        ["Professional", "Friendly", "Formal", "Concise"]
    )

    details = st.text_area(
        "Additional Details",
        placeholder="Enter important points to include...",
        height=140
    )

    submitted = st.form_submit_button("✨ Generate Email")

if submitted:
    if not recipient.strip() or not purpose.strip():
        st.warning("Please enter the recipient and email purpose.")

    else:
        try:
            # Read API key from Streamlit Secrets
            api_key = st.secrets["GROQ_API_KEY"]
            client = Groq(api_key=api_key)

            with st.spinner("Generating your email..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a professional email-writing "
                                "assistant. Write clear, natural emails. "
                                "Include a subject line and email body. "
                                "Do not invent facts."
                            )
                        },
                        {
                            "role": "user",
                            "content": f"""
Recipient: {recipient}
Purpose: {purpose}
Tone: {tone}
Additional details: {details}

Generate a suitable email with a subject line and body.
"""
                        }
                    ],
                    temperature=0.7,
                    max_tokens=700
                )

            email = response.choices[0].message.content

            st.success("Your email is ready!")
            st.subheader("📩 Generated Email")

            st.text_area(
                "Review and copy your email",
                value=email,
                height=280
            )

            st.download_button(
                label="⬇️ Download Email",
                data=email,
                file_name="generated_email.txt",
                mime="text/plain"
            )

        except KeyError:
            st.error(
                "GROQ_API_KEY is missing. Add it in "
                "Streamlit Cloud → App settings → Secrets."
            )

        except Exception as e:
            st.error(
                "Email generation failed. Check your API key, "
                "Groq model availability, and API usage limits."
            )
            st.caption(str(e))

st.divider()
st.caption("AI Email Generator | Powered by Streamlit and Groq")
