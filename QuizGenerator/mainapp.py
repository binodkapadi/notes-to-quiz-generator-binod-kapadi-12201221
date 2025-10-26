import streamlit as st
import json
import os
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()


genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


@st.cache_data
def fetch_questions(text_content, quiz_level):
    RESPONSE_JSON = {
        "mcq": [
            {
                "mcq": "multiple choice question1",
                "options": {
                    "a": "choice here",
                    "b": "choice here",
                    "c": "choice here",
                    "d": "choice here"
                },
                "correct": "correct choice option"
            }
        ]
    }

    PROMPT_TEMPLATE = """
    TEXT: {text_content}

    You are an expert in generating MCQ type quiz based on the provided content.
    Given the above text, create a quiz of 6 multiple choice questions keeping difficulty level as {quiz_level}.
    Make sure questions are unique and relevant to the text.
    Format your response EXACTLY as valid JSON similar to the RESPONSE_JSON below.
    Do not include markdown or code block formatting (no ``` or json tags).

    RESPONSE_JSON example:
    {RESPONSE_JSON}
    """

    formatted_template = PROMPT_TEMPLATE.format(
        text_content=text_content, quiz_level=quiz_level, RESPONSE_JSON=RESPONSE_JSON
    )

    
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(formatted_template)

    extracted_response = response.text.strip()
    print("RAW GEMINI RESPONSE:\n", extracted_response)

   
    if extracted_response.startswith("```"):
        extracted_response = extracted_response.strip("`")
        if extracted_response.startswith("json"):
            extracted_response = extracted_response[len("json"):].strip()

   
    try:
        parsed = json.loads(extracted_response)
        return parsed.get("mcq", [])
    except Exception as e:
        st.error(f"❌ Error parsing Gemini response: {e}")
        st.code(extracted_response, language="json")
        return []


def main():
    st.title("🧠 Quiz Generator App")

    
    if os.path.exists("style.css"):
        with open("style.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

   
    text_content = st.text_area("📘 Paste the text content here:")
    quiz_level = st.selectbox("🎯 Select quiz level:", ["Easy", "Medium", "Hard"])
    quiz_level_lower = quiz_level.lower()

    
    if "quiz_generated" not in st.session_state:
        st.session_state.quiz_generated = False
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "selected_options" not in st.session_state:
        st.session_state.selected_options = []
    if "marks" not in st.session_state:
        st.session_state.marks = 0

    
    if st.button("🚀 Generate Quiz"):
        if not text_content.strip():
            st.warning("⚠️ Please paste some text before generating a quiz.")
        else:
            with st.spinner("Generating quiz... Please wait ⏳"):
                questions = fetch_questions(text_content, quiz_level_lower)
                if questions:
                    st.session_state.questions = questions
                    st.session_state.quiz_generated = True
                    st.session_state.selected_options = [None] * len(questions)
                    st.success("✅ Quiz generated successfully!")
                else:
                    st.error("Failed to generate quiz. Try again!")

    
    if st.session_state.quiz_generated and st.session_state.questions:
        st.subheader("📝 Your Quiz")

        correct_answers = []

        for i, question in enumerate(st.session_state.questions):
            st.markdown(f"**Q{i+1}. {question['mcq']}**")
            options = list(question["options"].values())
            correct_answers.append(question["correct"])

            selected = st.radio(
                label=f"Select your answer for question {i+1}",
                options=options,
                key=f"q{i}_radio",
                index=None  
            )
            st.session_state.selected_options[i] = selected

       
        marks = 0

        if st.button("Submit"):
            for i, question in enumerate(st.session_state.questions):
                correct_option = correct_answers[i]
                selected_option = st.session_state.selected_options[i]

                st.markdown(f"### Question {i+1}: {question['mcq']}")
                st.write(f"Your answer: **{selected_option or 'No answer selected'}**")

                if selected_option == correct_option or selected_option.strip().lower() == question["options"].get(correct_option, "").strip().lower():
                    st.success(f"✅ Correct! Answer: {correct_option}")
                    marks += 1
                else:
                    st.error(f"❌ Wrong! Correct answer: {correct_option}")

            st.session_state.marks = marks
            st.header(f"🏆 Your Total Score: {marks}/{len(st.session_state.questions)}")


if __name__ == "__main__":
    main()
