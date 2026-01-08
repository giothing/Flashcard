import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
from huggingface_hub import InferenceClient
import io
import os

st.set_page_config(page_title="GeoFlashcards", page_icon="🇬🇪")

HF_TOKEN = os.getenv("HF_TOKEN")
if not HF_TOKEN:
    st.error("Set your HF_TOKEN")
    st.stop()

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"
client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)

st.title("GeoFlashcards - AI Flashcard გენერატორი")
st.markdown("LLM-ით გენერირებული მაგალითები და აუდიო გახმოვანება")

languages = {
    "ინგლისური": "en",
    "გერმანული": "de",
    "რუსული": "ru",
    "ფრანგული": "fr",
    "ესპანური": "es",
    "იტალიური": "it"
}

def llm_sentence(translated_word, language):
messages = [
    {
        "role": "system",
        "content": "You are a language teacher. Create very simple beginner-friendly sentences."
    },
    {
        "role": "user",
        "content": (
            f"Write one short and natural sentence in {language} using the word '{word}'. "
            "Keep it simple, easy to understand, and do NOT explain the word."
        )
    }
]

    try:
        response = client.chat.completions.create(
            messages=messages,
            max_tokens=30,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "LLM generation failed"

def text_to_speech(text, lang):
    try:
        tts = gTTS(text=text, lang=lang)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp
    except:
        return None

target_lang_name = st.selectbox("აირჩიეთ სამიზნე ენა", list(languages.keys()))
target_lang = languages[target_lang_name]

num_cards = st.slider("ბარათების რაოდენობა", 3, 10, 3)

user_input = st.text_area("შეიყვანეთ სიტყვები", value="მზე წიგნი მეგობარი")

if st.button("გენერაცია"):
    if not user_input.strip():
        st.error("გთხოვთ შეიყვანეთ სიტყვები")
    else:
        words = [w.strip() for w in user_input.split() if w.strip()]

        words = (words * ((num_cards + len(words) - 1) // len(words)))[:num_cards]

        flashcards = []

        with st.spinner("AI ფიქრობს და ახმოვანებს..."):
            for word in words:
                translated = GoogleTranslator(
                    source="ka",
                    target=target_lang
                ).translate(word)

                example = llm_sentence(translated, target_lang)
                audio = text_to_speech(example, target_lang)

                flashcards.append({
                    "ქართული": word,
                    "თარგმანი": translated,
                    "მაგალითი": example,
                    "აუდიო": audio
                })

        st.success(f"გენერირებულია {len(flashcards)} ბარათი!")

        for card in flashcards:
            with st.expander(
                f"{card['ქართული']} ➡️ {card['თარგმანი']}",
                expanded=True
            ):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"**მაგალითი:** _{card['მაგალითი']}_")

                with col2:
                    if card["აუდიო"]:
                        st.audio(card["აუდიო"], format="audio/mp3")
                    else:
                        st.caption("აუდიო მიუწვდომელია")
