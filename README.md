# 🇬🇪 GeoFlashcards - AI Flashcard Generator

GeoFlashcards არის AI აპლიკაცია, რომელიც ქართული სიტყვების საფუძველზე ქმნის უცხოენოვან ფლეშბარათებს, მაგალითებსა და აუდიო ფაილებს.

## 🚀 როგორ ჩავრთოთ აპლიკაცია

### 1. დააინსტალირეთ ბიბლიოთეკები

გახსენით ტერმინალი და ჩაწერეთ:

```bash
pip install streamlit deep-translator gTTS huggingface_hub
```

### 2. Hugging Face Token-ის მომზადება

* დარეგისტრირდით Hugging Face-ზე.
* Settings → Access Tokens-ში შექმენით ახალი "Read" ტოკენი.
* თქვენს კომპიუტერში შექმენით Environment Variable სახელით `HF_TOKEN`.

### 3. აპლიკაციის გაშვება

```bash
streamlit run app.py
```
