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
        "sidebar_title": "Control panel",
        "sidebar_copy": "Set the language, model, and output size before generating.",
        "api_key": "OpenAI API key",
        "api_key_help": "Optional if OPENAI_API_KEY is already saved in your system or Streamlit secrets.",
        "model": "Model",
        "hashtag_language": "Hashtag language",
        "count": "Number of hashtags",
        "hero_badge": "AI tool for creators and businesses",
        "brand_name": "TagLift AI",
        "hero_title": "Generate Instagram hashtags that look ready to publish",
        "hero_copy": "Create hashtag sets for posts, reels, stories, and product promos in seconds. Built for creators, personal brands, and small businesses.",
        "hero_point_1": "3 interface languages",
        "hero_point_2": "Copy or export instantly",
        "hero_point_3": "Popular + niche balance",
        "form_badge": "Generate",
        "form_title": "Describe your content",
        "form_copy": "Add the topic, choose the format, and let the app build a useful hashtag mix.",
        "topic": "Topic",
        "topic_placeholder": "Example: handmade candles, fitness coach, travel in Italy, coffee shop launch",
        "audience": "Target audience",
        "audience_placeholder": "Example: women entrepreneurs, skincare lovers, local coffee fans",
        "content_type": "Content type",
        "strategy": "Hashtag strategy",
        "generate": "Generate hashtags",
        "regenerate": "Regenerate",
        "enter_topic": "Enter a topic first.",
        "missing_key": "Add your OpenAI API key in the sidebar, Streamlit secrets, or set OPENAI_API_KEY.",
        "loading": "Generating hashtags...",
        "request_error": "OpenAI request failed",
        "result_badge": "Results",
        "result_title": "Your hashtag package",
        "result_copy": "Grouped for easier publishing. You can copy the full pack or download it as a text file.",
        "generated": "Generated hashtags",
        "copy": "Copy hashtags",
        "download": "Download .txt",
        "file_name": "instagram_hashtags.txt",
        "count_card": "Total hashtags",
        "lang_card": "Output language",
        "strategy_card": "Strategy",
        "content_card": "Format",
        "how_1_title": "Describe the post",
        "how_1_copy": "Enter the topic and audience so the app understands what the content is about.",
        "how_2_title": "Choose the direction",
        "how_2_copy": "Pick the content type, hashtag language, and strategy based on your goals.",
        "how_3_title": "Publish faster",
        "how_3_copy": "Copy the final set or export it to a text file for later use.",
        "who_title": "Perfect for",
        "who_1": "Small businesses",
        "who_2": "Creators and bloggers",
        "who_3": "Instagram shops",
        "who_4": "Experts and coaches",
        "footer": "Simple AI hashtag generation for Instagram content.",
        "footer_brand": "TagLift AI",
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
    },
    "Українська": {
        "sidebar_title": "Панель керування",
        "sidebar_copy": "Налаштуйте мову, модель і кількість результатів перед генерацією.",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Не обов'язково, якщо OPENAI_API_KEY вже збережено в системі або в Streamlit secrets.",
        "model": "Модель",
        "hashtag_language": "Мова хештегів",
        "count": "Кількість хештегів",
        "hero_badge": "AI-інструмент для авторів і бізнесу",
        "brand_name": "TagLift AI",
        "hero_title": "Генеруйте Instagram-хештеги, які вже готові до публікації",
        "hero_copy": "Створюйте набори хештегів для постів, рілсів, сторіс і промо-контенту за секунди. Для блогерів, особистих брендів і малого бізнесу.",
        "hero_point_1": "3 мови інтерфейсу",
        "hero_point_2": "Копіювання або експорт одразу",
        "hero_point_3": "Баланс популярних і нішевих тегів",
        "form_badge": "Генерація",
        "form_title": "Опишіть свій контент",
        "form_copy": "Додайте тему, виберіть формат і дозвольте застосунку зібрати корисний мікс хештегів.",
        "topic": "Тема",
        "topic_placeholder": "Наприклад: свічки ручної роботи, фітнес-тренер, подорож Італією, відкриття кав'ярні",
        "audience": "Цільова аудиторія",
        "audience_placeholder": "Наприклад: жінки-підприємиці, поціновувачі догляду за шкірою, фанати локальної кави",
        "content_type": "Тип контенту",
        "strategy": "Стратегія хештегів",
        "generate": "Згенерувати хештеги",
        "regenerate": "Згенерувати ще раз",
        "enter_topic": "Спочатку введіть тему.",
        "missing_key": "Додайте OpenAI API ключ у боковій панелі, Streamlit secrets або встановіть OPENAI_API_KEY.",
        "loading": "Генерую хештеги...",
        "request_error": "Помилка запиту до OpenAI",
        "result_badge": "Результат",
        "result_title": "Ваш пакет хештегів",
        "result_copy": "Результати згруповані для зручнішої публікації. Можна скопіювати весь набір або завантажити його у текстовий файл.",
        "generated": "Згенеровані хештеги",
        "copy": "Скопіювати хештеги",
        "download": "Завантажити .txt",
        "file_name": "instagram_hashtags.txt",
        "count_card": "Усього хештегів",
        "lang_card": "Мова результату",
        "strategy_card": "Стратегія",
        "content_card": "Формат",
        "how_1_title": "Опишіть пост",
        "how_1_copy": "Вкажіть тему та аудиторію, щоб застосунок зрозумів, про що ваш контент.",
        "how_2_title": "Оберіть напрям",
        "how_2_copy": "Задайте тип контенту, мову хештегів і стратегію залежно від вашої цілі.",
        "how_3_title": "Публікуйте швидше",
        "how_3_copy": "Скопіюйте готовий набір або експортуйте його в текстовий файл на потім.",
        "who_title": "Для кого підходить",
        "who_1": "Малий бізнес",
        "who_2": "Креатори та блогери",
        "who_3": "Instagram-магазини",
        "who_4": "Експерти та коучі",
        "footer": "Простий AI-інструмент для генерації Instagram-хештегів.",
        "footer_brand": "TagLift AI",
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
    },
    "Русский": {
        "sidebar_title": "Панель управления",
        "sidebar_copy": "Настройте язык, модель и количество результатов перед генерацией.",
        "api_key": "OpenAI API ключ",
        "api_key_help": "Необязательно, если OPENAI_API_KEY уже сохранен в системе или в Streamlit secrets.",
        "model": "Модель",
        "hashtag_language": "Язык хештегов",
        "count": "Количество хештегов",
        "hero_badge": "AI-инструмент для авторов и бизнеса",
        "brand_name": "TagLift AI",
        "hero_title": "Генерируйте Instagram-хештеги, которые уже готовы к публикации",
        "hero_copy": "Создавайте наборы хештегов для постов, рилсов, сторис и промо-контента за секунды. Для блогеров, личных брендов и малого бизнеса.",
        "hero_point_1": "3 языка интерфейса",
        "hero_point_2": "Копирование или экспорт сразу",
        "hero_point_3": "Баланс популярных и нишевых тегов",
        "form_badge": "Генерация",
        "form_title": "Опишите свой контент",
        "form_copy": "Добавьте тему, выберите формат и позвольте приложению собрать полезный набор хештегов.",
        "topic": "Тема",
        "topic_placeholder": "Например: свечи ручной работы, фитнес-тренер, путешествие по Италии, открытие кофейни",
        "audience": "Целевая аудитория",
        "audience_placeholder": "Например: женщины-предприниматели, любители ухода за кожей, поклонники локального кофе",
        "content_type": "Тип контента",
        "strategy": "Стратегия хештегов",
        "generate": "Сгенерировать хештеги",
        "regenerate": "Сгенерировать снова",
        "enter_topic": "Сначала введите тему.",
        "missing_key": "Добавьте OpenAI API ключ в боковой панели, Streamlit secrets или установите OPENAI_API_KEY.",
        "loading": "Генерирую хештеги...",
        "request_error": "Ошибка запроса к OpenAI",
        "result_badge": "Результат",
        "result_title": "Ваш пакет хештегов",
        "result_copy": "Результаты сгруппированы для более удобной публикации. Можно скопировать весь набор или скачать его в текстовый файл.",
        "generated": "Сгенерированные хештеги",
        "copy": "Скопировать хештеги",
        "download": "Скачать .txt",
        "file_name": "instagram_hashtags.txt",
        "count_card": "Всего хештегов",
        "lang_card": "Язык результата",
        "strategy_card": "Стратегия",
        "content_card": "Формат",
        "how_1_title": "Опишите пост",
        "how_1_copy": "Укажите тему и аудиторию, чтобы приложение поняло, о чем ваш контент.",
        "how_2_title": "Выберите направление",
        "how_2_copy": "Задайте тип контента, язык хештегов и стратегию в зависимости от вашей цели.",
        "how_3_title": "Публикуйте быстрее",
        "how_3_copy": "Скопируйте готовый набор или экспортируйте его в текстовый файл на потом.",
        "who_title": "Для кого подходит",
        "who_1": "Малый бизнес",
        "who_2": "Креаторы и блогеры",
        "who_3": "Instagram-магазины",
        "who_4": "Эксперты и коучи",
        "footer": "Простой AI-инструмент для генерации Instagram-хештегов.",
        "footer_brand": "TagLift AI",
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

    for key in GROUP_ORDER:
        if scaled[key] == 0:
            donor = max(GROUP_ORDER, key=lambda item: scaled[item])
            if scaled[donor] > 1:
                scaled[donor] -= 1
                scaled[key] += 1

    return scaled


def build_prompt(
    topic: str,
    content_type_key: str,
    audience: str,
    style_key: str,
    hashtag_language: str,
    count: int,
) -> str:
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

        Return the result in exactly 4 sections using these labels:
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
        - Put one hashtag per line.
        - No numbering, bullets, explanations, or extra text.
        - Avoid duplicates.
        - Keep hashtags relevant and commercially useful.
        """
    ).strip()


def parse_response(raw_text: str, total_count: int) -> dict[str, list[str]]:
    sections = {key: [] for key in GROUP_ORDER}
    current = None
    mapping = {
        "[POPULAR]": "popular",
        "[MEDIUM]": "medium",
        "[NICHE]": "niche",
        "[MICRO]": "micro",
    }

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


def copy_button(text: str, button_label: str) -> None:
    escaped_text = (
        text.replace("\\", "\\\\")
        .replace("`", "\\`")
        .replace("${", "\\${")
    )
    components.html(
        f"""
        <div style="margin: 0;">
          <button
            onclick="navigator.clipboard.writeText(`{escaped_text}`)"
            style="
              width:100%;
              background:linear-gradient(135deg, #111827 0%, #1f2937 100%);
              border:none;
              border-radius:16px;
              color:white;
              cursor:pointer;
              font-size:14px;
              font-weight:700;
              padding:12px 16px;
            "
          >
            {button_label}
          </button>
        </div>
        """,
        height=54,
    )


def localize_content_type(key: str, t: dict[str, str]) -> str:
    return t[f"content_{key}"]


def localize_style(key: str, t: dict[str, str]) -> str:
    return t[f"style_{key}"]


def group_label(key: str, t: dict[str, str]) -> str:
    return t[f"group_{key}"]


def render_metric(label: str, value: str) -> str:
    return f"""
    <div class="metric-card">
      <div class="metric-label">{label}</div>
      <div class="metric-value">{value}</div>
    </div>
    """


def render_group_card(title: str, tags: list[str]) -> str:
    chips = "".join(f'<span class="tag-chip">{tag}</span>' for tag in tags) or '<span class="tag-chip muted">...</span>'
    return f"""
    <div class="group-card">
      <div class="group-title">{title}</div>
      <div class="chip-wrap">{chips}</div>
    </div>
    """


st.markdown(
    """
    <style>
      :root {
        --ink: #1f2937;
        --muted: #6b7280;
        --card: rgba(255, 255, 255, 0.78);
        --border: rgba(31, 41, 55, 0.10);
        --accent-dark: #111827;
      }
      .stApp {
        background:
          radial-gradient(circle at 0% 0%, rgba(245, 158, 11, 0.22), transparent 28%),
          radial-gradient(circle at 100% 0%, rgba(217, 72, 95, 0.20), transparent 26%),
          radial-gradient(circle at 100% 100%, rgba(17, 24, 39, 0.08), transparent 24%),
          linear-gradient(180deg, #fff7f0 0%, #f8f0ea 54%, #fffaf6 100%);
      }
      .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2.8rem;
        max-width: 1200px;
      }
      [data-testid="stSidebar"] {
        border-right: 1px solid rgba(31, 41, 55, 0.08);
        background: rgba(255, 255, 255, 0.72);
      }
      .hero-shell,
      .panel-card,
      .info-card,
      .result-shell {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 28px;
        box-shadow: 0 24px 80px rgba(31, 41, 55, 0.08);
        backdrop-filter: blur(10px);
      }
      .hero-shell {
        padding: 2rem;
      }
      .badge {
        display: inline-block;
        padding: 0.45rem 0.8rem;
        border-radius: 999px;
        background: rgba(217, 72, 95, 0.10);
        color: #9f1239;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }
      .brand-row {
        display: flex;
        align-items: center;
        gap: 0.9rem;
        margin-bottom: 1rem;
      }
      .brand-logo {
        width: 56px;
        height: 56px;
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.9);
        padding: 0.4rem;
        box-shadow: 0 12px 24px rgba(31, 41, 55, 0.10);
      }
      .brand-name {
        color: var(--accent-dark);
        font-size: 1rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }
      .hero-title {
        margin: 0.9rem 0 0.7rem;
        font-size: clamp(2.1rem, 4vw, 4.1rem);
        line-height: 0.95;
        color: var(--accent-dark);
        font-weight: 900;
      }
      .hero-copy {
        max-width: 680px;
        font-size: 1.02rem;
        line-height: 1.6;
        color: var(--ink);
        margin-bottom: 1.2rem;
      }
      .hero-points,
      .metric-grid,
      .info-grid,
      .group-grid {
        display: grid;
        gap: 0.9rem;
      }
      .hero-points {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        margin-top: 1.4rem;
      }
      .hero-point,
      .metric-card,
      .info-card,
      .group-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(31, 41, 55, 0.08);
        border-radius: 22px;
      }
      .hero-point,
      .metric-card,
      .group-card,
      .info-card {
        padding: 1rem;
      }
      .hero-point,
      .metric-value,
      .group-title,
      .info-title {
        color: var(--accent-dark);
        font-weight: 800;
      }
      .panel-card,
      .result-shell {
        padding: 1.4rem;
      }
      .section-kicker {
        color: #9f1239;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }
      .section-title {
        margin: 0.35rem 0 0.45rem;
        color: var(--accent-dark);
        font-size: 1.55rem;
        font-weight: 800;
      }
      .section-copy,
      .metric-label,
      .info-copy,
      .footer-note {
        color: var(--muted);
      }
      .metric-grid {
        grid-template-columns: repeat(4, minmax(0, 1fr));
        margin: 1rem 0 1.2rem;
      }
      .group-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
      .chip-wrap,
      .audience-strip {
        display: flex;
        flex-wrap: wrap;
        gap: 0.6rem;
      }
      .tag-chip,
      .audience-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 0.78rem;
        border-radius: 999px;
        font-size: 0.9rem;
      }
      .tag-chip {
        background: #fff4ef;
        border: 1px solid rgba(217, 72, 95, 0.12);
        color: #7f1d1d;
      }
      .tag-chip.muted {
        color: var(--muted);
      }
      .info-grid {
        grid-template-columns: repeat(3, minmax(0, 1fr));
        margin-top: 1rem;
      }
      .audience-pill {
        background: rgba(17, 24, 39, 0.04);
        border: 1px solid rgba(17, 24, 39, 0.08);
        color: var(--accent-dark);
        font-weight: 700;
      }
      .footer-note {
        text-align: center;
        font-size: 0.9rem;
        margin-top: 1.6rem;
      }
      .stButton > button,
      .stDownloadButton > button {
        border-radius: 16px;
        min-height: 48px;
        font-weight: 800;
        border: none;
      }
      .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #d9485f 0%, #f97316 100%);
        color: white;
      }
      .stDownloadButton > button {
        background: white;
        color: var(--accent-dark);
        border: 1px solid rgba(31, 41, 55, 0.10);
      }
      div[data-testid="stTextInput"] input,
      div[data-testid="stSelectbox"] > div,
      div[data-testid="stTextArea"] textarea {
        border-radius: 16px;
      }
      @media (max-width: 900px) {
        .hero-points,
        .metric-grid,
        .info-grid,
        .group-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    app_language = st.selectbox("Language / Мова / Язык", APP_LANGUAGES, index=0)
    t = UI_TEXT[app_language]
    st.subheader(t["sidebar_title"])
    st.caption(t["sidebar_copy"])
    st.text_input(
        t["api_key"],
        type="password",
        key="api_key",
        help=t["api_key_help"],
    )
    model = st.selectbox(t["model"], ["gpt-4.1-mini", "gpt-4.1"], index=0)
    hashtag_language = st.selectbox(t["hashtag_language"], HASHTAG_LANGUAGES, index=0)
    count = st.slider(t["count"], min_value=15, max_value=40, value=30, step=5)


content_labels = {localize_content_type(key, t): key for key in CONTENT_TYPES}
style_labels = {localize_style(key, t): key for key in HASHTAG_STYLES}

hero_col, form_col = st.columns([1.25, 0.95], gap="large")

with hero_col:
    st.markdown(
        f"""
        <div class="hero-shell">
          <div class="brand-row">
            <img class="brand-logo" src="data:image/svg+xml;utf8,%3Csvg width='128' height='128' viewBox='0 0 128 128' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='16' y1='16' x2='112' y2='112' gradientUnits='userSpaceOnUse'%3E%3Cstop stop-color='%23F97316'/%3E%3Cstop offset='1' stop-color='%23D9485F'/%3E%3C/linearGradient%3E%3C/defs%3E%3Crect x='12' y='12' width='104' height='104' rx='28' fill='url(%23g)'/%3E%3Cpath d='M42 49H57V34H72V49H87V64H72V79H57V64H42V49Z' fill='%23FFF7F0'/%3E%3C/svg%3E" alt="TagLift AI" />
            <div class="brand-name">{t["brand_name"]}</div>
          </div>
          <span class="badge">{t["hero_badge"]}</span>
          <h1 class="hero-title">{t["hero_title"]}</h1>
          <p class="hero-copy">{t["hero_copy"]}</p>
          <div class="hero-points">
            <div class="hero-point">{t["hero_point_1"]}</div>
            <div class="hero-point">{t["hero_point_2"]}</div>
            <div class="hero-point">{t["hero_point_3"]}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with form_col:
    st.markdown(
        f"""
        <div class="panel-card">
          <div class="section-kicker">{t["form_badge"]}</div>
          <div class="section-title">{t["form_title"]}</div>
          <div class="section-copy">{t["form_copy"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    topic = st.text_input(t["topic"], placeholder=t["topic_placeholder"])
    audience = st.text_input(t["audience"], placeholder=t["audience_placeholder"])
    form_left, form_right = st.columns(2)
    with form_left:
        content_type_label = st.selectbox(t["content_type"], list(content_labels.keys()))
    with form_right:
        style_label = st.selectbox(t["strategy"], list(style_labels.keys()))
    action_left, action_right = st.columns(2)
    with action_left:
        generate = st.button(t["generate"], type="primary", use_container_width=True)
    with action_right:
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
        <div class="result-shell">
          <div class="section-kicker">{t["result_badge"]}</div>
          <div class="section-title">{t["result_title"]}</div>
          <div class="section-copy">{t["result_copy"]}</div>
          <div class="metric-grid">
            {render_metric(t["count_card"], str(total_generated))}
            {render_metric(t["lang_card"], last_language)}
            {render_metric(t["strategy_card"], localize_style(last_style, t))}
            {render_metric(t["content_card"], localize_content_type(last_content_type, t))}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    button_col, download_col = st.columns([0.35, 0.65])
    with button_col:
        copy_button(flat_hashtags, t["copy"])
    with download_col:
        st.download_button(
            t["download"],
            data=flat_hashtags,
            file_name=t["file_name"],
            mime="text/plain",
            use_container_width=True,
        )

    group_html = "".join(
        render_group_card(group_label(key, t), sections.get(key, []))
        for key in GROUP_ORDER
    )
    st.markdown(f'<div class="group-grid">{group_html}</div>', unsafe_allow_html=True)
    st.text_area(t["generated"], flat_hashtags, height=220)


st.markdown(
    f"""
    <div class="info-grid">
      <div class="info-card">
        <div class="info-title">{t["how_1_title"]}</div>
        <div class="info-copy">{t["how_1_copy"]}</div>
      </div>
      <div class="info-card">
        <div class="info-title">{t["how_2_title"]}</div>
        <div class="info-copy">{t["how_2_copy"]}</div>
      </div>
      <div class="info-card">
        <div class="info-title">{t["how_3_title"]}</div>
        <div class="info-copy">{t["how_3_copy"]}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="panel-card" style="margin-top: 1rem;">
      <div class="section-title">{t["who_title"]}</div>
      <div class="audience-strip">
        <span class="audience-pill">{t["who_1"]}</span>
        <span class="audience-pill">{t["who_2"]}</span>
        <span class="audience-pill">{t["who_3"]}</span>
        <span class="audience-pill">{t["who_4"]}</span>
      </div>
    </div>
    <div class="footer-note">{t["footer_brand"]} · {t["footer"]}</div>
    """,
    unsafe_allow_html=True,
)
