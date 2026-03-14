import os
from textwrap import dedent
from typing import Optional

import streamlit as st
import streamlit.components.v1 as components
from openai import OpenAI


st.set_page_config(
    page_title="TagLift AI",
    page_icon="assets/favicon.svg",
    layout="wide",
    initial_sidebar_state="collapsed",
)


APP_LANGUAGES = ["English", "Українська", "Русский"]
HASHTAG_LANGUAGES = ["English", "Ukrainian", "Russian"]
CONTENT_TYPES = {
    "post": "A regular Instagram feed post",
    "reel": "A short-form Instagram Reel",
    "story": "An Instagram Story",
    "product_promo": "A promotional product-focused post",
    "personal_brand": "A personal branding post",
}
HASHTAG_STYLES = {
    "balanced": "Mix reach and relevance evenly.",
    "growth": "Favor discovery and higher reach.",
    "niche": "Favor audience specificity and buyer intent.",
}
GROUP_ORDER = ["popular", "medium", "niche", "micro"]


UI_TEXT = {
    "English": {
        "brand": "TagLift AI",
        "language": "Language",
        "hero_badge": "Instagram-inspired AI tool",
        "hero_title": "Generate Instagram hashtags in a clean, simple flow",
        "hero_copy": "Describe the post, choose the format, and get a ready-to-use hashtag pack without digging through random prompts.",
        "step_1": "1. Describe your content",
        "step_2": "2. Get your hashtag pack",
        "topic": "Topic",
        "topic_placeholder": "Example: handmade candles, fitness coach, coffee shop opening",
        "audience": "Target audience",
        "audience_placeholder": "Example: local coffee fans, women entrepreneurs, skincare lovers",
        "content_type": "Content type",
        "strategy": "Strategy",
        "hashtag_language": "Hashtag language",
        "model": "Model",
        "count": "Hashtag count",
        "api_key": "OpenAI API key",
        "api_key_help": "Optional if OPENAI_API_KEY already exists in app secrets.",
        "generate": "Generate hashtags",
        "regenerate": "Regenerate",
        "enter_topic": "Enter a topic first.",
        "missing_key": "Add your OpenAI API key in the field above or in app secrets.",
        "loading": "Generating hashtags...",
        "request_error": "OpenAI request failed",
        "result_title": "Generated hashtags",
        "result_copy": "Your result is grouped by popularity and niche level so it is easier to use.",
        "copy": "Copy all",
        "download": "Download TXT",
        "file_name": "instagram_hashtags.txt",
        "count_card": "Total",
        "lang_card": "Language",
        "strategy_card": "Strategy",
        "format_card": "Format",
        "group_popular": "Popular",
        "group_medium": "Medium",
        "group_niche": "Niche",
        "group_micro": "Micro-niche",
        "content_post": "Post",
        "content_reel": "Reel",
        "content_story": "Story",
        "content_product_promo": "Product promo",
        "content_personal_brand": "Personal brand",
        "style_balanced": "Balanced",
        "style_growth": "Growth",
        "style_niche": "Niche",
        "tip_1": "Use for posts, reels, and stories",
        "tip_2": "Copy everything with one click",
        "tip_3": "Switch between 3 languages",
        "empty_title": "No hashtags yet",
        "empty_copy": "Fill in the topic and click generate to see the hashtag pack here.",
    },
    "Українська": {
        "brand": "TagLift AI",
        "language": "Мова",
        "hero_badge": "AI-інструмент у стилі Instagram",
        "hero_title": "Генеруйте Instagram-хештеги в чистому і простому потоці",
        "hero_copy": "Опишіть пост, виберіть формат і отримайте готовий набір хештегів без хаотичних промптів.",
        "step_1": "1. Опишіть свій контент",
        "step_2": "2. Отримайте пакет хештегів",
        "topic": "Тема",
        "topic_placeholder": "Наприклад: свічки ручної роботи, фітнес-тренер, відкриття кав'ярні",
        "audience": "Цільова аудиторія",
        "audience_placeholder": "Наприклад: фанати локальної кави, жінки-підприємиці, поціновувачі догляду",
        "content_type": "Тип контенту",
        "strategy": "Стратегія",
        "hashtag_language": "Мова хештегів",
        "model": "Модель",
        "count": "Кількість хештегів",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Не обов'язково, якщо OPENAI_API_KEY вже є в secrets застосунку.",
        "generate": "Згенерувати хештеги",
        "regenerate": "Згенерувати ще раз",
        "enter_topic": "Спочатку введіть тему.",
        "missing_key": "Додайте OpenAI API ключ у поле вище або в secrets застосунку.",
        "loading": "Генерую хештеги...",
        "request_error": "Помилка запиту до OpenAI",
        "result_title": "Згенеровані хештеги",
        "result_copy": "Результат згрупований за популярністю і нішевістю, щоб ним було простіше користуватись.",
        "copy": "Скопіювати все",
        "download": "Завантажити TXT",
        "file_name": "instagram_hashtags.txt",
        "count_card": "Усього",
        "lang_card": "Мова",
        "strategy_card": "Стратегія",
        "format_card": "Формат",
        "group_popular": "Популярні",
        "group_medium": "Середні",
        "group_niche": "Нішеві",
        "group_micro": "Мікроніша",
        "content_post": "Пост",
        "content_reel": "Рілс",
        "content_story": "Сторіс",
        "content_product_promo": "Промо продукту",
        "content_personal_brand": "Особистий бренд",
        "style_balanced": "Баланс",
        "style_growth": "Ріст",
        "style_niche": "Ніша",
        "tip_1": "Для постів, рілсів і сторіс",
        "tip_2": "Копіювання в один клік",
        "tip_3": "Перемикання між 3 мовами",
        "empty_title": "Хештегів ще немає",
        "empty_copy": "Заповніть тему і натисніть генерацію, щоб побачити тут результат.",
    },
    "Русский": {
        "brand": "TagLift AI",
        "language": "Язык",
        "hero_badge": "AI-инструмент в стиле Instagram",
        "hero_title": "Генерируйте Instagram-хештеги в чистом и простом интерфейсе",
        "hero_copy": "Опишите пост, выберите формат и получите готовый набор хештегов без хаотичных промптов.",
        "step_1": "1. Опишите свой контент",
        "step_2": "2. Получите пакет хештегов",
        "topic": "Тема",
        "topic_placeholder": "Например: свечи ручной работы, фитнес-тренер, открытие кофейни",
        "audience": "Целевая аудитория",
        "audience_placeholder": "Например: поклонники локального кофе, женщины-предприниматели, любители ухода",
        "content_type": "Тип контента",
        "strategy": "Стратегия",
        "hashtag_language": "Язык хештегов",
        "model": "Модель",
        "count": "Количество хештегов",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Необязательно, если OPENAI_API_KEY уже есть в secrets приложения.",
        "generate": "Сгенерировать хештеги",
        "regenerate": "Сгенерировать снова",
        "enter_topic": "Сначала введите тему.",
        "missing_key": "Добавьте OpenAI API ключ в поле выше или в secrets приложения.",
        "loading": "Генерирую хештеги...",
        "request_error": "Ошибка запроса к OpenAI",
        "result_title": "Сгенерированные хештеги",
        "result_copy": "Результат сгруппирован по популярности и нишевости, чтобы им было проще пользоваться.",
        "copy": "Скопировать все",
        "download": "Скачать TXT",
        "file_name": "instagram_hashtags.txt",
        "count_card": "Всего",
        "lang_card": "Язык",
        "strategy_card": "Стратегия",
        "format_card": "Формат",
        "group_popular": "Популярные",
        "group_medium": "Средние",
        "group_niche": "Нишевые",
        "group_micro": "Микрониша",
        "content_post": "Пост",
        "content_reel": "Рилс",
        "content_story": "Сторис",
        "content_product_promo": "Промо продукта",
        "content_personal_brand": "Личный бренд",
        "style_balanced": "Баланс",
        "style_growth": "Рост",
        "style_niche": "Ниша",
        "tip_1": "Для постов, рилсов и сторис",
        "tip_2": "Копирование в один клик",
        "tip_3": "Переключение между 3 языками",
        "empty_title": "Хештегов пока нет",
        "empty_copy": "Заполните тему и нажмите генерацию, чтобы увидеть здесь результат.",
    },
}


def get_api_key() -> Optional[str]:
    return st.session_state.get("api_key") or st.secrets.get("OPENAI_API_KEY", None) or os.getenv("OPENAI_API_KEY")


def get_client() -> Optional[OpenAI]:
    api_key = get_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def compute_group_sizes(total_count: int) -> dict[str, int]:
    base = {"popular": 5, "medium": 10, "niche": 10, "micro": 5}
    total = sum(base.values())
    result = {}
    remainder = []
    for key, value in base.items():
        raw = value * total_count / total
        result[key] = int(raw)
        remainder.append((raw - result[key], key))
    missing = total_count - sum(result.values())
    for _, key in sorted(remainder, reverse=True):
        if missing <= 0:
            break
        result[key] += 1
        missing -= 1
    return result


def build_prompt(topic: str, content_type_key: str, audience: str, style_key: str, hashtag_language: str, count: int) -> str:
    sizes = compute_group_sizes(count)
    return dedent(
        f"""
        You are an Instagram growth assistant.
        Generate exactly {count} Instagram hashtags.
        Topic: {topic}
        Content type: {CONTENT_TYPES[content_type_key]}
        Audience: {audience or "General audience"}
        Strategy: {HASHTAG_STYLES[style_key]}
        Hashtag language: {hashtag_language}

        Return exactly these sections:
        [POPULAR]
        [MEDIUM]
        [NICHE]
        [MICRO]

        Section sizes:
        [POPULAR]: {sizes["popular"]}
        [MEDIUM]: {sizes["medium"]}
        [NICHE]: {sizes["niche"]}
        [MICRO]: {sizes["micro"]}

        Rules:
        - hashtags only
        - one hashtag per line
        - no explanations
        - no duplicates
        """
    ).strip()


def parse_response(raw_text: str, total_count: int) -> dict[str, list[str]]:
    sections = {key: [] for key in GROUP_ORDER}
    mapping = {"[POPULAR]": "popular", "[MEDIUM]": "medium", "[NICHE]": "niche", "[MICRO]": "micro"}
    current = None
    for line in raw_text.splitlines():
        value = line.strip()
        if not value:
            continue
        if value in mapping:
            current = mapping[value]
            continue
        if current and value.startswith("#"):
            sections[current].append(value)
    if any(sections.values()):
        return sections
    hashtags = [line.strip() for line in raw_text.splitlines() if line.strip().startswith("#")]
    sizes = compute_group_sizes(total_count)
    start = 0
    for key in GROUP_ORDER:
        end = start + sizes[key]
        sections[key] = hashtags[start:end]
        start = end
    return sections


def flatten_sections(sections: dict[str, list[str]]) -> str:
    return "\n".join(tag for key in GROUP_ORDER for tag in sections[key])


def localize_content_type(key: str, t: dict[str, str]) -> str:
    return t[f"content_{key}"]


def localize_style(key: str, t: dict[str, str]) -> str:
    return t[f"style_{key}"]


def group_label(key: str, t: dict[str, str]) -> str:
    return t[f"group_{key}"]


def render_metric(label: str, value: str) -> str:
    return f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>'


def render_group_card(title: str, tags: list[str]) -> str:
    chips = "".join(f'<span class="tag-chip">{tag}</span>' for tag in tags)
    return f'<div class="group-card"><div class="group-title">{title}</div><div class="tag-wrap">{chips}</div></div>'


def copy_button(text: str, button_label: str) -> None:
    escaped_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    components.html(
        f"""
        <button onclick="navigator.clipboard.writeText(`{escaped_text}`)"
          style="
            width:100%;
            border:none;
            border-radius:16px;
            padding:12px 16px;
            background:linear-gradient(135deg,#fd1d1d 0%,#f56040 34%,#f77737 58%,#fcaf45 100%);
            color:#fff;
            font-weight:800;
            cursor:pointer;
          ">
          {button_label}
        </button>
        """,
        height=52,
    )


st.markdown(
    """
    <style>
      :root {
        --ig-pink: #d62976;
        --ig-purple: #962fbf;
        --ig-orange: #f77737;
        --ig-yellow: #fcaf45;
        --ig-red: #fd1d1d;
        --bg: #16181d;
        --bg-soft: #1e2128;
        --panel: #20242c;
        --panel-2: #262b34;
        --ink: #f3f4f6;
        --muted: #aeb6c2;
        --border: rgba(255,255,255,0.08);
      }
      .stApp {
        background:
          radial-gradient(circle at top left, rgba(214,41,118,0.13), transparent 24%),
          radial-gradient(circle at top right, rgba(150,47,191,0.12), transparent 24%),
          radial-gradient(circle at bottom left, rgba(252,175,69,0.10), transparent 22%),
          linear-gradient(180deg, #111318 0%, #16181d 100%);
      }
      .block-container {
        max-width: 1140px;
        padding-top: 2.4rem;
        padding-bottom: 2rem;
      }
      .stApp header {
        background: transparent;
      }
      .stApp [data-testid="stHeader"] {
        background: transparent;
      }
      .topbar, .hero-card {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 26px;
        box-shadow: 0 18px 48px rgba(0,0,0,0.28);
      }
      .topbar {
        padding: 1.1rem 1.2rem;
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
      }
      .topbar::before {
        content: "";
        position: absolute;
        inset: 0;
        background:
          linear-gradient(90deg, rgba(253,29,29,0.10) 0%, rgba(214,41,118,0.10) 35%, rgba(150,47,191,0.06) 100%);
        pointer-events: none;
      }
      .topbar-inner {
        display:flex;
        align-items:center;
        justify-content:flex-start;
        gap:1rem;
        position: relative;
        z-index: 1;
      }
      .brand-box {
        display:flex;
        align-items:center;
        gap:0.85rem;
        flex: 1 1 auto;
      }
      .brand-mark {
        width:52px;
        height:52px;
        border-radius:16px;
        display:flex;
        align-items:center;
        justify-content:center;
        color:#fff;
        font-weight:900;
        font-size:0.92rem;
        letter-spacing:0.06em;
        background: linear-gradient(135deg, #fd1d1d 0%, #d62976 38%, #962fbf 70%, #f77737 100%);
        box-shadow: 0 10px 24px rgba(214,41,118,0.26);
      }
      .brand-name {
        color: var(--ink);
        font-size: 1.18rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }
      .brand-subtitle {
        color: var(--muted);
        font-weight: 700;
        margin-left: auto;
      }
      .brand-copy {
        display:flex;
        flex-direction:column;
        gap:0.15rem;
      }
      .brand-tagline {
        color:#ff93bf;
        font-size:0.72rem;
        font-weight:800;
        letter-spacing:0.05em;
        text-transform:uppercase;
      }
      .hero-card {
        padding: 1.4rem;
        margin-bottom: 1rem;
      }
      .hero-badge {
        display:inline-block;
        padding:0.42rem 0.78rem;
        border-radius:999px;
        background:rgba(214,41,118,0.12);
        color:#ff78b0;
        font-size:0.76rem;
        font-weight:800;
        text-transform:uppercase;
        letter-spacing:0.05em;
        margin-bottom:0.85rem;
      }
      .hero-grid {
        display:grid;
        grid-template-columns: 1.2fr 0.8fr;
        gap:1rem;
        align-items:start;
      }
      .hero-title {
        color:var(--ink);
        font-size: clamp(2rem, 4vw, 3.4rem);
        line-height:0.98;
        font-weight:900;
        margin:0;
      }
      .hero-copy {
        color:var(--muted);
        font-size:1rem;
        line-height:1.65;
        margin:0.9rem 0 0;
        max-width:680px;
      }
      .tip-stack {
        display:grid;
        gap:0.7rem;
      }
      .tip {
        background:var(--panel-2);
        border:1px solid var(--border);
        border-radius:18px;
        padding:0.9rem 1rem;
        color:#f9fafb;
        font-weight:700;
      }
      .panel-shell, .results-shell {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 24px;
        box-shadow: 0 18px 48px rgba(0,0,0,0.22);
        padding: 1.1rem;
      }
      .section-eyebrow {
        color:#ff93bf;
        font-size:0.76rem;
        font-weight:800;
        letter-spacing:0.05em;
        text-transform:uppercase;
        margin-bottom:0.45rem;
      }
      .section-title {
        color:var(--ink);
        font-size:1.22rem;
        font-weight:800;
        margin-bottom:0.35rem;
      }
      .metric-grid, .group-grid {
        display:grid;
        gap:0.8rem;
      }
      .metric-grid {
        grid-template-columns:repeat(4,minmax(0,1fr));
        margin:0.95rem 0;
      }
      .metric-card {
        background:var(--panel-2);
        border:1px solid var(--border);
        border-radius:18px;
        padding:0.9rem;
      }
      .metric-label {
        color:var(--muted);
        font-size:0.76rem;
        margin-bottom:0.18rem;
      }
      .metric-value {
        color:var(--ink);
        font-weight:800;
      }
      .group-grid {
        grid-template-columns:repeat(2,minmax(0,1fr));
      }
      .group-card {
        background:var(--panel-2);
        border:1px solid var(--border);
        border-radius:18px;
        padding:1rem;
      }
      .group-title {
        color:var(--ink);
        font-weight:800;
        margin-bottom:0.7rem;
      }
      .tag-wrap {
        display:flex;
        flex-wrap:wrap;
        gap:0.55rem;
      }
      .tag-chip {
        display:inline-flex;
        align-items:center;
        border-radius:999px;
        padding:0.48rem 0.72rem;
        font-size:0.88rem;
        color:#ffd6e8;
        background:rgba(214,41,118,0.14);
        border:1px solid rgba(214,41,118,0.22);
      }
      .empty-state {
        background:var(--panel-2);
        border:1px dashed rgba(255,255,255,0.14);
        border-radius:18px;
        padding:1.6rem 1rem;
        text-align:center;
      }
      .empty-title {
        color:var(--ink);
        font-size:1.15rem;
        font-weight:800;
        margin-bottom:0.35rem;
      }
      .empty-copy, .result-copy {
        color:var(--muted);
      }
      .stButton > button, .stDownloadButton > button {
        min-height:48px;
        border-radius:16px;
        font-weight:800;
        border:none;
      }
      .stButton > button[kind="primary"] {
        color:#fff;
        background:linear-gradient(135deg,#fd1d1d 0%,#d62976 42%,#962fbf 100%);
      }
      .stButton > button:not([kind="primary"]) {
        color:var(--ink);
        background:var(--panel-2);
        border:1px solid var(--border);
      }
      .stDownloadButton > button {
        color:var(--ink);
        background:var(--panel-2);
        border:1px solid var(--border);
      }
      .subtle-note {
        color: var(--muted);
        font-size: 0.92rem;
        margin-bottom: 1rem;
      }
      div[data-testid="stTextInput"] input,
      div[data-testid="stSelectbox"] > div,
      div[data-testid="stTextArea"] textarea {
        background: var(--panel-2);
        color: var(--ink);
        border: 1px solid var(--border);
        border-radius: 16px;
        box-shadow: none !important;
        outline: none !important;
      }
      div[data-testid="stTextInput"] > div,
      div[data-testid="stTextInput"] > div > div,
      div[data-testid="stTextArea"] > div,
      div[data-testid="stTextArea"] > div > div,
      div[data-testid="stSelectbox"] > div,
      div[data-baseweb="select"],
      div[data-baseweb="input"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
      }
      div[data-testid="stTextInput"] input:focus,
      div[data-testid="stTextArea"] textarea:focus,
      div[data-baseweb="input"] input:focus {
        border: 1px solid rgba(214, 41, 118, 0.35) !important;
        box-shadow: 0 0 0 1px rgba(214, 41, 118, 0.18) !important;
        outline: none !important;
      }
      div[data-testid="stTextInput"] input::placeholder,
      textarea::placeholder {
        color: #8d95a3;
      }
      div[data-baseweb="select"] > div {
        background: var(--panel-2);
        color: var(--ink);
      }
      label, .stMarkdown, .stText, p {
        color: var(--ink);
      }
      [data-testid="stSliderTickBarMin"],
      [data-testid="stSliderTickBarMax"] {
        background: rgba(255,255,255,0.12);
      }
      @media (max-width: 900px) {
        .hero-grid, .metric-grid, .group-grid {
          grid-template-columns:1fr;
        }
        .brand-subtitle {
          display:none;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


app_language = st.session_state.get("app_language", APP_LANGUAGES[0])
t = UI_TEXT[app_language]
content_labels = {localize_content_type(key, t): key for key in CONTENT_TYPES}
style_labels = {localize_style(key, t): key for key in HASHTAG_STYLES}

st.markdown(
    f"""
    <div class="topbar">
      <div class="topbar-inner">
        <div class="brand-box">
          <div class="brand-mark">TL</div>
          <div class="brand-copy">
            <div class="brand-name">{t["brand"]}</div>
            <div class="brand-tagline">{t["hero_badge"]}</div>
          </div>
          <div class="brand-subtitle">Hashtag generator</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="hero-card">
      <div class="hero-badge">{t["hero_badge"]}</div>
      <div class="hero-grid">
        <div>
          <h1 class="hero-title">{t["hero_title"]}</h1>
          <p class="hero-copy">{t["hero_copy"]}</p>
        </div>
        <div class="tip-stack">
          <div class="tip">{t["tip_1"]}</div>
          <div class="tip">{t["tip_2"]}</div>
          <div class="tip">{t["tip_3"]}</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([0.98, 1.02], gap="large")

with left_col:
    st.markdown(
        f"""
        <div class="panel-shell">
          <div class="section-eyebrow">Step 1</div>
          <div class="section-title">{t["step_1"]}</div>
          <div class="subtle-note">{t["hero_copy"]}</div>
        """,
        unsafe_allow_html=True,
    )
        topic = st.text_input(t["topic"], placeholder=t["topic_placeholder"])
        audience = st.text_input(t["audience"], placeholder=t["audience_placeholder"])
        row1 = st.columns(2)
        with row1[0]:
            content_type_label = st.selectbox(t["content_type"], list(content_labels.keys()))
        with row1[1]:
            style_label = st.selectbox(t["strategy"], list(style_labels.keys()))
        row2 = st.columns(2)
        with row2[0]:
            hashtag_language = st.selectbox(t["hashtag_language"], HASHTAG_LANGUAGES, index=0)
        with row2[1]:
            count = st.slider(t["count"], min_value=15, max_value=40, value=30, step=5)
        row3 = st.columns(2)
        with row3[0]:
            model = st.selectbox(t["model"], ["gpt-4.1-mini", "gpt-4.1"], index=0)
        with row3[1]:
            app_language = st.selectbox(t["language"], APP_LANGUAGES, index=APP_LANGUAGES.index(app_language), key="app_language")
            t = UI_TEXT[app_language]
            content_labels = {localize_content_type(key, t): key for key in CONTENT_TYPES}
            style_labels = {localize_style(key, t): key for key in HASHTAG_STYLES}
        row4 = st.columns(2)
        with row4[0]:
            st.text_input(t["api_key"], type="password", key="api_key", help=t["api_key_help"])
        with row4[1]:
            st.caption(t["api_key_help"])
        row5 = st.columns(2)
        with row5[0]:
            generate = st.button(t["generate"], type="primary", use_container_width=True)
        with row5[1]:
            regenerate = st.button(t["regenerate"], use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

content_type_key = content_labels[content_type_label]
style_key = style_labels[style_label]
should_generate = generate or (regenerate and bool(st.session_state.get("last_topic")))

if should_generate:
    active_topic = topic.strip() or st.session_state.get("last_topic", "")
    active_audience = audience.strip() or st.session_state.get("last_audience", "")
    if not active_topic:
        st.warning(t["enter_topic"])
    else:
        client = get_client()
        if client is None:
            st.error(t["missing_key"])
        else:
            st.session_state["last_topic"] = active_topic
            st.session_state["last_audience"] = active_audience
            st.session_state["last_content_type"] = content_type_key
            st.session_state["last_style"] = style_key
            st.session_state["last_language"] = hashtag_language
            st.session_state["last_count"] = count
            try:
                with st.spinner(t["loading"]):
                    response = client.responses.create(
                        model=model,
                        input=build_prompt(
                            topic=active_topic,
                            content_type_key=content_type_key,
                            audience=active_audience,
                            style_key=style_key,
                            hashtag_language=hashtag_language,
                            count=count,
                        ),
                    )
                raw_text = response.output_text.strip()
                sections = parse_response(raw_text, count)
                st.session_state["hashtags_sections"] = sections
                st.session_state["hashtags_flat"] = flatten_sections(sections)
            except Exception as exc:
                st.error(f'{t["request_error"]}: {exc}')

sections = st.session_state.get("hashtags_sections")
flat_hashtags = st.session_state.get("hashtags_flat", "")
last_language = st.session_state.get("last_language", hashtag_language)
last_style = st.session_state.get("last_style", style_key)
last_content_type = st.session_state.get("last_content_type", content_type_key)
total_generated = len(flat_hashtags.splitlines()) if flat_hashtags else 0

with right_col:
    st.markdown(
        f"""
        <div class="results-shell">
          <div class="section-eyebrow">Step 2</div>
          <div class="section-title">{t["step_2"]}</div>
        """,
        unsafe_allow_html=True,
    )
        if sections and flat_hashtags:
            st.markdown(
                f"""
                <div class="section-title" style="font-size:1.3rem; margin-top:0.35rem; margin-bottom:0.15rem;">{t["result_title"]}</div>
                <div class="result-copy">{t["result_copy"]}</div>
                <div class="metric-grid">
                  {render_metric(t["count_card"], str(total_generated))}
                  {render_metric(t["lang_card"], last_language)}
                  {render_metric(t["strategy_card"], localize_style(last_style, t))}
                  {render_metric(t["format_card"], localize_content_type(last_content_type, t))}
                </div>
                """,
                unsafe_allow_html=True,
            )
            action_cols = st.columns([0.42, 0.58])
            with action_cols[0]:
                copy_button(flat_hashtags, t["copy"])
            with action_cols[1]:
                st.download_button(
                    t["download"],
                    data=flat_hashtags,
                    file_name=t["file_name"],
                    mime="text/plain",
                    use_container_width=True,
                )
            groups_html = "".join(render_group_card(group_label(key, t), sections.get(key, [])) for key in GROUP_ORDER)
            st.markdown(f'<div class="group-grid" style="margin-top:0.85rem;">{groups_html}</div>', unsafe_allow_html=True)
            st.text_area(t["result_title"], flat_hashtags, height=170, label_visibility="collapsed")
        else:
            st.markdown(
                f"""
                <div class="empty-state">
                  <div class="empty-title">{t["empty_title"]}</div>
                  <div class="empty-copy">{t["empty_copy"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)
