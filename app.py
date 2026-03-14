import os
from textwrap import dedent
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI


st.set_page_config(
    page_title="Instagram Hashtag Generator",
    page_icon="#",
    layout="centered",
)


CONTENT_TYPES = {
    "Post": "A regular Instagram feed post",
    "Reel": "A short-form Instagram Reel",
    "Story": "An Instagram Story",
    "Product promo": "A promotional product-focused post",
    "Personal brand": "A personal branding post",
}

HASHTAG_STYLES = {
    "Balanced": "Mix reach and relevance evenly.",
    "Growth": "Favor discovery and higher-reach tags.",
    "Niche": "Favor specific audience-targeted tags.",
}

UI_TEXT = {
    "English": {
        "app_title": "Instagram Hashtag Generator",
        "hero_eyebrow": "Instagram AI Tool",
        "hero_title": "Hashtag Generator",
        "hero_copy": "Generate ready-to-use Instagram hashtags for posts, reels, stories, and product promos.",
        "settings": "Settings",
        "app_language": "App language",
        "api_key": "OpenAI API key",
        "api_key_help": "Optional if OPENAI_API_KEY is already set in your system.",
        "model": "Model",
        "hashtag_language": "Hashtag language",
        "count": "Number of hashtags",
        "topic": "Topic",
        "topic_placeholder": "Example: handmade candles, fitness coach, coffee shop, travel in Italy",
        "content_type": "Content type",
        "strategy": "Hashtag strategy",
        "audience": "Target audience",
        "audience_placeholder": "Example: small business owners, skincare lovers, new moms",
        "generate": "Generate hashtags",
        "enter_topic": "Enter a topic first.",
        "missing_key": "Add your OpenAI API key in the sidebar or set OPENAI_API_KEY.",
        "loading": "Generating hashtags...",
        "request_error": "OpenAI request failed",
        "generated": "Generated hashtags",
        "copy": "Copy hashtags",
        "result": "Result",
        "download": "Download .txt",
        "file_name": "instagram_hashtags.txt",
    },
    "Українська": {
        "app_title": "Генератор хештегів для Instagram",
        "hero_eyebrow": "Instagram AI Інструмент",
        "hero_title": "Генератор хештегів",
        "hero_copy": "Створюйте готові хештеги для постів, рілсів, сторіс і промо-контенту.",
        "settings": "Налаштування",
        "app_language": "Мова застосунку",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Не обов'язково, якщо OPENAI_API_KEY вже збережено в системі.",
        "model": "Модель",
        "hashtag_language": "Мова хештегів",
        "count": "Кількість хештегів",
        "topic": "Тема",
        "topic_placeholder": "Наприклад: свічки ручної роботи, фітнес-тренер, кав'ярня, подорож Італією",
        "content_type": "Тип контенту",
        "strategy": "Стратегія хештегів",
        "audience": "Цільова аудиторія",
        "audience_placeholder": "Наприклад: власники малого бізнесу, поціновувачі догляду за шкірою, молоді мами",
        "generate": "Згенерувати хештеги",
        "enter_topic": "Спочатку введіть тему.",
        "missing_key": "Додайте OpenAI API ключ у боковій панелі або встановіть OPENAI_API_KEY.",
        "loading": "Генерую хештеги...",
        "request_error": "Помилка запиту до OpenAI",
        "generated": "Згенеровані хештеги",
        "copy": "Скопіювати хештеги",
        "result": "Результат",
        "download": "Завантажити .txt",
        "file_name": "instagram_hashtags.txt",
    },
    "Русский": {
        "app_title": "Генератор хештегов для Instagram",
        "hero_eyebrow": "Instagram AI Инструмент",
        "hero_title": "Генератор хештегов",
        "hero_copy": "Создавайте готовые хештеги для постов, рилсов, сторис и промо-контента.",
        "settings": "Настройки",
        "app_language": "Язык приложения",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Необязательно, если OPENAI_API_KEY уже сохранен в системе.",
        "model": "Модель",
        "hashtag_language": "Язык хештегов",
        "count": "Количество хештегов",
        "topic": "Тема",
        "topic_placeholder": "Например: свечи ручной работы, фитнес-тренер, кофейня, путешествие по Италии",
        "content_type": "Тип контента",
        "strategy": "Стратегия хештегов",
        "audience": "Целевая аудитория",
        "audience_placeholder": "Например: владельцы малого бизнеса, любители ухода за кожей, молодые мамы",
        "generate": "Сгенерировать хештеги",
        "enter_topic": "Сначала введите тему.",
        "missing_key": "Добавьте OpenAI API ключ в боковой панели или установите OPENAI_API_KEY.",
        "loading": "Генерирую хештеги...",
        "request_error": "Ошибка запроса к OpenAI",
        "generated": "Сгенерированные хештеги",
        "copy": "Скопировать хештеги",
        "result": "Результат",
        "download": "Скачать .txt",
        "file_name": "instagram_hashtags.txt",
    },
}


def get_client() -> Optional[OpenAI]:
    api_key = st.session_state.get("api_key") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def build_prompt(
    topic: str,
    content_type: str,
    audience: str,
    style: str,
    language: str,
    count: int,
) -> str:
    return dedent(
        f"""
        You are an Instagram growth assistant.

        Generate exactly {count} Instagram hashtags for this content:
        Topic: {topic}
        Content type: {CONTENT_TYPES[content_type]}
        Target audience: {audience or "General audience"}
        Hashtag strategy: {HASHTAG_STYLES[style]}
        Language preference: {language}

        Requirements:
        - Keep the hashtags highly relevant to the topic.
        - Avoid banned, spammy, or repetitive hashtags.
        - Split the output into:
          5 popular hashtags
          10 medium hashtags
          10 niche hashtags
          5 micro-niche hashtags
        - If the requested total is not 30, keep the same idea but scale the groups proportionally.
        - Return hashtags only.
        - Put one hashtag per line.
        - Do not add numbering, explanations, headings, or bullets.
        """
    ).strip()


def copy_button(text: str, button_label: str) -> None:
    escaped_text = (
        text.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )
    components.html(
        f"""
        <div style="margin: 0.25rem 0 0.75rem 0;">
          <button
            onclick="navigator.clipboard.writeText(`{escaped_text}`)"
            style="
              background:#111827;
              border:none;
              border-radius:999px;
              color:white;
              cursor:pointer;
              font-size:14px;
              font-weight:600;
              padding:10px 18px;
            "
          >
            {button_label}
          </button>
        </div>
        """,
        height=54,
    )


st.markdown(
    """
    <style>
      .stApp {
        background:
          radial-gradient(circle at top left, rgba(255, 119, 48, 0.18), transparent 30%),
          radial-gradient(circle at top right, rgba(225, 48, 108, 0.18), transparent 28%),
          linear-gradient(180deg, #fff9f5 0%, #fff 45%, #fff4f7 100%);
      }
      .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2rem;
      }
      .hero-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(17, 24, 39, 0.07);
        border-radius: 24px;
        padding: 1.4rem 1.4rem 1rem;
        box-shadow: 0 20px 60px rgba(17, 24, 39, 0.08);
        margin-bottom: 1.2rem;
      }
      .eyebrow {
        color: #c2410c;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
      }
      .hero-title {
        color: #111827;
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.1;
        margin: 0.2rem 0 0.5rem;
      }
      .hero-copy {
        color: #374151;
        font-size: 1rem;
        margin-bottom: 0;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    app_language = st.selectbox("Language / Мова / Язык", list(UI_TEXT.keys()), index=0)
    t = UI_TEXT[app_language]
    st.subheader(t["settings"])
    st.text_input(
        t["api_key"],
        type="password",
        key="api_key",
        help=t["api_key_help"],
    )
    model = st.selectbox(t["model"], ["gpt-4.1-mini", "gpt-4.1"], index=0)
    language = st.selectbox(t["hashtag_language"], ["English", "Ukrainian", "Russian"], index=0)
    count = st.slider(t["count"], min_value=15, max_value=40, value=30, step=5)

st.title(t["app_title"])
st.markdown(
    f"""
    <div class="hero-card">
      <div class="eyebrow">{t["hero_eyebrow"]}</div>
      <div class="hero-title">{t["hero_title"]}</div>
      <p class="hero-copy">
        {t["hero_copy"]}
      </p>
    </div>
    """,
    unsafe_allow_html=True,
)

topic = st.text_input(
    t["topic"],
    placeholder=t["topic_placeholder"],
)

col1, col2 = st.columns(2)
with col1:
    content_type = st.selectbox(t["content_type"], list(CONTENT_TYPES.keys()))
with col2:
    style = st.selectbox(t["strategy"], list(HASHTAG_STYLES.keys()))

audience = st.text_input(
    t["audience"],
    placeholder=t["audience_placeholder"],
)

generate = st.button(t["generate"], type="primary", use_container_width=True)

if generate:
    if not topic.strip():
        st.warning(t["enter_topic"])
    else:
        client = get_client()
        if client is None:
            st.error(t["missing_key"])
        else:
            prompt = build_prompt(
                topic=topic.strip(),
                content_type=content_type,
                audience=audience.strip(),
                style=style,
                language=language,
                count=count,
            )
            try:
                with st.spinner(t["loading"]):
                    response = client.responses.create(
                        model=model,
                        input=prompt,
                    )
                hashtags = response.output_text.strip()
                st.session_state["hashtags"] = hashtags
            except Exception as exc:
                st.error(f'{t["request_error"]}: {exc}')

hashtags = st.session_state.get("hashtags", "")

if hashtags:
    st.subheader(t["generated"])
    copy_button(hashtags, t["copy"])
    st.text_area(t["result"], hashtags, height=320, label_visibility="collapsed")
    st.download_button(
        t["download"],
        data=hashtags,
        file_name=t["file_name"],
        mime="text/plain",
        use_container_width=True,
    )
