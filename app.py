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
        "lang_switch": "Language",
        "hero_badge": "Instagram AI hashtag tool",
        "hero_title": "Generate cleaner hashtags in one click",
        "hero_copy": "Built for creators, shops, and small businesses that want faster Instagram publishing without messy prompt work.",
        "settings_title": "Generation settings",
        "topic": "Topic",
        "topic_placeholder": "Example: handmade candles, fitness coach, coffee shop launch",
        "audience": "Target audience",
        "audience_placeholder": "Example: women entrepreneurs, skincare lovers, local coffee fans",
        "content_type": "Content type",
        "strategy": "Hashtag strategy",
        "hashtag_language": "Hashtag language",
        "model": "Model",
        "count": "Hashtag count",
        "api_key": "OpenAI API key",
        "api_key_help": "Optional if OPENAI_API_KEY already exists in Streamlit secrets or your environment.",
        "generate": "Generate hashtags",
        "regenerate": "Regenerate",
        "enter_topic": "Enter a topic first.",
        "missing_key": "Add your OpenAI API key in the form or app secrets.",
        "loading": "Generating hashtags...",
        "request_error": "OpenAI request failed",
        "result_title": "Generated hashtag pack",
        "result_copy": "Copy the full pack or use the grouped cards below.",
        "copy": "Copy all hashtags",
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
        "benefit_1": "3 interface languages",
        "benefit_2": "Copy or export instantly",
        "benefit_3": "Balanced reach and relevance",
        "empty_title": "Ready to generate",
        "empty_copy": "Fill the form, add a topic, and create a clean hashtag pack for your next Instagram post.",
    },
    "Українська": {
        "brand": "TagLift AI",
        "lang_switch": "Мова",
        "hero_badge": "Instagram AI-інструмент для хештегів",
        "hero_title": "Генеруйте чистіші хештеги в один клік",
        "hero_copy": "Для блогерів, магазинів і малого бізнесу, яким треба швидше готувати Instagram-пости без хаотичних промптів.",
        "settings_title": "Налаштування генерації",
        "topic": "Тема",
        "topic_placeholder": "Наприклад: свічки ручної роботи, фітнес-тренер, відкриття кав'ярні",
        "audience": "Цільова аудиторія",
        "audience_placeholder": "Наприклад: жінки-підприємиці, поціновувачі догляду за шкірою, фанати локальної кави",
        "content_type": "Тип контенту",
        "strategy": "Стратегія хештегів",
        "hashtag_language": "Мова хештегів",
        "model": "Модель",
        "count": "Кількість хештегів",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Не обов'язково, якщо OPENAI_API_KEY вже є в secrets або середовищі.",
        "generate": "Згенерувати хештеги",
        "regenerate": "Згенерувати ще раз",
        "enter_topic": "Спочатку введіть тему.",
        "missing_key": "Додайте OpenAI API ключ у форму або secrets застосунку.",
        "loading": "Генерую хештеги...",
        "request_error": "Помилка запиту до OpenAI",
        "result_title": "Згенерований пакет хештегів",
        "result_copy": "Скопіюйте весь набір або використовуйте згруповані картки нижче.",
        "copy": "Скопіювати всі хештеги",
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
        "benefit_1": "3 мови інтерфейсу",
        "benefit_2": "Копіювання або експорт одразу",
        "benefit_3": "Баланс охоплення і релевантності",
        "empty_title": "Готово до генерації",
        "empty_copy": "Заповніть форму, введіть тему і створіть охайний набір хештегів для наступного Instagram-поста.",
    },
    "Русский": {
        "brand": "TagLift AI",
        "lang_switch": "Язык",
        "hero_badge": "Instagram AI-инструмент для хештегов",
        "hero_title": "Генерируйте более чистые хештеги в один клик",
        "hero_copy": "Для блогеров, магазинов и малого бизнеса, которым нужно быстрее готовить Instagram-посты без хаотичных промптов.",
        "settings_title": "Настройки генерации",
        "topic": "Тема",
        "topic_placeholder": "Например: свечи ручной работы, фитнес-тренер, открытие кофейни",
        "audience": "Целевая аудитория",
        "audience_placeholder": "Например: женщины-предприниматели, любители ухода за кожей, поклонники локального кофе",
        "content_type": "Тип контента",
        "strategy": "Стратегия хештегов",
        "hashtag_language": "Язык хештегов",
        "model": "Модель",
        "count": "Количество хештегов",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Необязательно, если OPENAI_API_KEY уже есть в secrets или окружении.",
        "generate": "Сгенерировать хештеги",
        "regenerate": "Сгенерировать снова",
        "enter_topic": "Сначала введите тему.",
        "missing_key": "Добавьте OpenAI API ключ в форму или secrets приложения.",
        "loading": "Генерирую хештеги...",
        "request_error": "Ошибка запроса к OpenAI",
        "result_title": "Сгенерированный пакет хештегов",
        "result_copy": "Скопируйте весь набор или используйте сгруппированные карточки ниже.",
        "copy": "Скопировать все хештеги",
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
        "benefit_1": "3 языка интерфейса",
        "benefit_2": "Копирование или экспорт сразу",
        "benefit_3": "Баланс охвата и релевантности",
        "empty_title": "Готово к генерации",
        "empty_copy": "Заполните форму, введите тему и создайте аккуратный набор хештегов для следующего Instagram-поста.",
    },
}


def get_api_key() -> Optional[str]:
    return (
        st.session_state.get("api_key")
        or st.secrets.get("OPENAI_API_KEY", None)
        or os.getenv("OPENAI_API_KEY")
    )


def get_client() -> Optional[OpenAI]:
    api_key = get_api_key()
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def compute_group_sizes(total_count: int) -> dict[str, int]:
    base = {"popular": 5, "medium": 10, "niche": 10, "micro": 5}
    total_base = sum(base.values())
    scaled = {}
    remainders = []
    for key, value in base.items():
        raw = value * total_count / total_base
        scaled[key] = int(raw)
        remainders.append((raw - scaled[key], key))
    missing = total_count - sum(scaled.values())
    for _, key in sorted(remainders, reverse=True):
        if missing <= 0:
            break
        scaled[key] += 1
        missing -= 1
    return scaled


def build_prompt(topic: str, content_type_key: str, audience: str, style_key: str, hashtag_language: str, count: int) -> str:
    sizes = compute_group_sizes(count)
    return dedent(
        f"""
        You are an Instagram growth assistant.
        Generate exactly {count} Instagram hashtags for this content.
        Topic: {topic}
        Content type: {CONTENT_TYPES[content_type_key]}
        Target audience: {audience or "General audience"}
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
        - Return hashtags only.
        - One hashtag per line.
        - No numbering or explanations.
        - Avoid duplicates.
        """
    ).strip()


def parse_response(raw_text: str, total_count: int) -> dict[str, list[str]]:
    sections = {key: [] for key in GROUP_ORDER}
    current = None
    mapping = {"[POPULAR]": "popular", "[MEDIUM]": "medium", "[NICHE]": "niche", "[MICRO]": "micro"}
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


def copy_button(text: str, button_label: str) -> None:
    escaped_text = text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    components.html(
        f"""
        <button
          onclick="navigator.clipboard.writeText(`{escaped_text}`)"
          style="
            width:100%;
            background:#111827;
            color:#ffffff;
            border:none;
            border-radius:14px;
            padding:12px 16px;
            font-weight:700;
            cursor:pointer;
          "
        >{button_label}</button>
        """,
        height=52,
    )


def render_metric(label: str, value: str) -> str:
    return f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>'


def render_group_card(title: str, tags: list[str]) -> str:
    chips = "".join(f'<span class="chip">{tag}</span>' for tag in tags)
    return f'<div class="group-card"><div class="group-title">{title}</div><div class="chip-wrap">{chips}</div></div>'


st.markdown(
    """
    <style>
      .stApp {
        background:
          radial-gradient(circle at top left, rgba(249, 115, 22, 0.14), transparent 24%),
          radial-gradient(circle at top right, rgba(217, 70, 99, 0.12), transparent 24%),
          linear-gradient(180deg, #fffaf7 0%, #fff6ef 100%);
      }
      .block-container {
        max-width: 1120px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
      }
      [data-testid="stSidebar"] {
        background: #fffaf7;
      }
      .topbar, .hero, .workspace, .result-box {
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(17,24,39,0.08);
        border-radius: 24px;
        box-shadow: 0 18px 50px rgba(17,24,39,0.06);
      }
      .topbar {
        padding: 0.9rem 1rem;
        margin-bottom: 1rem;
      }
      .brandline {
        display:flex;
        align-items:center;
        gap:0.8rem;
      }
      .brandicon {
        width:42px;
        height:42px;
        border-radius:14px;
        background: linear-gradient(135deg, #f97316 0%, #d94663 100%);
        color:#fff;
        display:flex;
        align-items:center;
        justify-content:center;
        font-weight:900;
        font-size:1.2rem;
      }
      .brandname {
        font-size:1rem;
        font-weight:900;
        color:#111827;
        letter-spacing:0.03em;
      }
      .hero {
        padding: 1.35rem;
        margin-bottom: 1rem;
      }
      .badge {
        display:inline-block;
        background:#fff1f2;
        color:#be123c;
        font-size:0.74rem;
        font-weight:800;
        border-radius:999px;
        padding:0.42rem 0.78rem;
        text-transform:uppercase;
        letter-spacing:0.05em;
        margin-bottom:0.8rem;
      }
      .hero h1 {
        font-size: clamp(2rem, 4vw, 3.7rem);
        line-height: 0.98;
        color:#111827;
        margin:0;
      }
      .hero p {
        color:#4b5563;
        font-size:1rem;
        line-height:1.6;
        max-width:760px;
        margin:0.9rem 0 0;
      }
      .benefits {
        display:grid;
        grid-template-columns:repeat(3,minmax(0,1fr));
        gap:0.8rem;
        margin-top:1rem;
      }
      .benefit {
        border:1px solid rgba(17,24,39,0.08);
        background:#fff;
        border-radius:18px;
        padding:0.9rem 1rem;
        font-weight:700;
        color:#111827;
      }
      .workspace {
        padding: 1.15rem;
      }
      .section-title {
        font-size:1.25rem;
        font-weight:800;
        color:#111827;
        margin-bottom:0.8rem;
      }
      .metric-grid, .group-grid {
        display:grid;
        gap:0.8rem;
      }
      .metric-grid {
        grid-template-columns:repeat(4,minmax(0,1fr));
        margin: 1rem 0;
      }
      .metric {
        background:#fff;
        border:1px solid rgba(17,24,39,0.08);
        border-radius:18px;
        padding:0.9rem;
      }
      .metric-label {
        color:#6b7280;
        font-size:0.78rem;
        margin-bottom:0.2rem;
      }
      .metric-value {
        color:#111827;
        font-weight:800;
      }
      .result-box {
        padding:1.1rem;
        margin-top:1rem;
      }
      .group-grid {
        grid-template-columns:repeat(2,minmax(0,1fr));
      }
      .group-card {
        background:#fff;
        border:1px solid rgba(17,24,39,0.08);
        border-radius:18px;
        padding:1rem;
      }
      .group-title {
        font-weight:800;
        color:#111827;
        margin-bottom:0.75rem;
      }
      .chip-wrap {
        display:flex;
        flex-wrap:wrap;
        gap:0.55rem;
      }
      .chip {
        display:inline-flex;
        align-items:center;
        padding:0.48rem 0.74rem;
        border-radius:999px;
        background:#fff4ef;
        color:#7c2d12;
        border:1px solid rgba(249,115,22,0.12);
        font-size:0.88rem;
      }
      .empty {
        text-align:center;
        padding:1.8rem 1rem 1.2rem;
        color:#6b7280;
      }
      .empty-title {
        color:#111827;
        font-size:1.25rem;
        font-weight:800;
        margin-bottom:0.4rem;
      }
      .stButton > button, .stDownloadButton > button {
        border-radius:14px;
        min-height:48px;
        font-weight:800;
        border:none;
      }
      .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ef4444 0%, #f97316 100%);
        color:white;
      }
      .stDownloadButton > button {
        background:#fff;
        color:#111827;
        border:1px solid rgba(17,24,39,0.1);
      }
      @media (max-width: 900px) {
        .benefits, .metric-grid, .group-grid {
          grid-template-columns:1fr;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    app_language = st.selectbox("Language / Мова / Язык", APP_LANGUAGES, index=0)

t = UI_TEXT[app_language]

top_left, top_right = st.columns([0.72, 0.28])
with top_left:
    st.markdown(
        f"""
        <div class="topbar">
          <div class="brandline">
            <div class="brandicon">+</div>
            <div class="brandname">{t["brand"]}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with top_right:
    app_language = st.selectbox(t["lang_switch"], APP_LANGUAGES, index=APP_LANGUAGES.index(app_language), key="lang_top")
    t = UI_TEXT[app_language]

st.markdown(
    f"""
    <div class="hero">
      <div class="badge">{t["hero_badge"]}</div>
      <h1>{t["hero_title"]}</h1>
      <p>{t["hero_copy"]}</p>
      <div class="benefits">
        <div class="benefit">{t["benefit_1"]}</div>
        <div class="benefit">{t["benefit_2"]}</div>
        <div class="benefit">{t["benefit_3"]}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


content_labels = {localize_content_type(key, t): key for key in CONTENT_TYPES}
style_labels = {localize_style(key, t): key for key in HASHTAG_STYLES}

st.markdown('<div class="workspace">', unsafe_allow_html=True)
st.markdown(f'<div class="section-title">{t["settings_title"]}</div>', unsafe_allow_html=True)

row1 = st.columns([1.2, 1, 0.9])
with row1[0]:
    topic = st.text_input(t["topic"], placeholder=t["topic_placeholder"])
with row1[1]:
    audience = st.text_input(t["audience"], placeholder=t["audience_placeholder"])
with row1[2]:
    api_key = st.text_input(t["api_key"], type="password", key="api_key", help=t["api_key_help"])

row2 = st.columns(4)
with row2[0]:
    content_type_label = st.selectbox(t["content_type"], list(content_labels.keys()))
with row2[1]:
    style_label = st.selectbox(t["strategy"], list(style_labels.keys()))
with row2[2]:
    hashtag_language = st.selectbox(t["hashtag_language"], HASHTAG_LANGUAGES, index=0)
with row2[3]:
    model = st.selectbox(t["model"], ["gpt-4.1-mini", "gpt-4.1"], index=0)

row3 = st.columns([1, 1, 1.2])
with row3[0]:
    count = st.slider(t["count"], min_value=15, max_value=40, value=30, step=5)
with row3[1]:
    generate = st.button(t["generate"], type="primary", use_container_width=True)
with row3[2]:
    regenerate = st.button(t["regenerate"], use_container_width=True)

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

if sections and flat_hashtags:
    st.markdown(
        f"""
        <div class="result-box">
          <div class="section-title">{t["result_title"]}</div>
          <div style="color:#6b7280; margin-top:-0.35rem;">{t["result_copy"]}</div>
          <div class="metric-grid">
            {render_metric(t["count_card"], str(total_generated))}
            {render_metric(t["lang_card"], last_language)}
            {render_metric(t["strategy_card"], localize_style(last_style, t))}
            {render_metric(t["format_card"], localize_content_type(last_content_type, t))}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    action_cols = st.columns([0.34, 0.66])
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
    group_html = "".join(render_group_card(group_label(key, t), sections.get(key, [])) for key in GROUP_ORDER)
    st.markdown(f'<div class="group-grid" style="margin-top:0.8rem;">{group_html}</div>', unsafe_allow_html=True)
    st.text_area(t["result_title"], flat_hashtags, height=190, label_visibility="collapsed")
else:
    st.markdown(
        f"""
        <div class="result-box empty">
          <div class="empty-title">{t["empty_title"]}</div>
          <div>{t["empty_copy"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("</div>", unsafe_allow_html=True)
