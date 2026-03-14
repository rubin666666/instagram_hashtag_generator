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
PLATFORMS = {
    "instagram": "Instagram",
    "tiktok": "TikTok",
    "youtube": "YouTube",
    "linkedin": "LinkedIn",
    "pinterest": "Pinterest",
    "facebook": "Facebook",
    "x": "X",
}
CONTENT_TYPES = {
    "post": "A standard social media post",
    "short_video": "A short vertical video",
    "story": "A story-style post",
    "carousel": "A multi-slide carousel post",
    "product_promo": "A promotional product-focused post",
    "personal_brand": "A personal branding post",
}
HASHTAG_STYLES = {
    "balanced": "Mix reach and relevance evenly.",
    "growth": "Favor discovery and higher reach.",
    "niche": "Favor audience specificity and buyer intent.",
}
GOALS = {
    "reach": "Maximize reach and discovery.",
    "sales": "Attract buyers and commercial intent.",
    "authority": "Build expertise and trust.",
    "community": "Create engagement and loyal audience fit.",
}
GROUP_ORDER = ["popular", "medium", "niche", "micro"]
PLATFORM_GUIDES = {
    "instagram": "Prioritize discoverability, niche relevance, and a natural Instagram mix.",
    "tiktok": "Favor trend-aware, punchy, discovery-focused tags that fit TikTok culture.",
    "youtube": "Favor searchable, topic-driven tags that support video discovery.",
    "linkedin": "Keep hashtags professional, industry-relevant, and less spammy.",
    "pinterest": "Favor descriptive, keyword-rich tags that match search intent and inspiration topics.",
    "facebook": "Keep hashtags broad but restrained, with readable tags and practical relevance.",
    "x": "Keep hashtags concise, topical, and suitable for fast-moving conversation.",
}


UI_TEXT = {
    "English": {
        "brand": "TagLift AI",
        "language": "Language",
        "choose_language": "Choose your language",
        "language_welcome": "Select the interface language to continue.",
        "continue": "Continue",
        "footer_language": "Change interface language",
        "footer_title": "Interface settings",
        "footer_copy": "You can change the app language here any time.",
        "hero_badge": "Multi-platform AI tool",
        "hero_title": "Generate social media hashtags in one clean flow",
        "hero_copy": "Choose a platform, describe the content, and get a ready-to-use hashtag pack for your post, video, story, or campaign.",
        "step_1": "1. Describe your content",
        "step_2": "2. Get your hashtag pack",
        "platform": "Platform",
        "goal": "Goal",
        "goal_hint": "Pick the main outcome you want from this post.",
        "apply_presets": "Apply platform defaults",
        "recommended_setup": "Recommended setup",
        "reset_form": "Reset form",
        "examples_title": "Quick examples",
        "examples_copy": "Start from a ready-made example, then tweak it for your niche.",
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
        "topic_too_short": "Make the topic a little more specific.",
        "loading": "Generating hashtags...",
        "request_error": "OpenAI request failed",
        "result_title": "Generated hashtags",
        "result_copy": "Your result is grouped by popularity and niche level so it is easier to use.",
        "caption_title": "Suggested caption",
        "caption_copy": "Use it as-is or edit it before posting.",
        "history_title": "Recent generations",
        "history_empty": "Your recent hashtag packs will appear here.",
        "history_restore": "Use again",
        "history_clear": "Clear history",
        "copy": "Copy all",
        "copy_caption": "Copy caption",
        "download": "Download TXT",
        "file_name": "social_media_hashtags.txt",
        "count_card": "Total",
        "platform_card": "Platform",
        "lang_card": "Language",
        "strategy_card": "Strategy",
        "format_card": "Format",
        "goal_card": "Goal",
        "platform_instagram": "Instagram",
        "platform_tiktok": "TikTok",
        "platform_youtube": "YouTube",
        "platform_linkedin": "LinkedIn",
        "platform_pinterest": "Pinterest",
        "platform_facebook": "Facebook",
        "platform_x": "X",
        "group_popular": "Popular",
        "group_medium": "Medium",
        "group_niche": "Niche",
        "group_micro": "Micro-niche",
        "content_post": "Post",
        "content_short_video": "Short video",
        "content_story": "Story",
        "content_carousel": "Carousel",
        "content_product_promo": "Product promo",
        "content_personal_brand": "Personal brand",
        "style_balanced": "Balanced",
        "style_growth": "Growth",
        "style_niche": "Niche",
        "goal_reach": "Reach",
        "goal_sales": "Sales",
        "goal_authority": "Authority",
        "goal_community": "Community",
        "tip_1": "Instagram, TikTok, YouTube, LinkedIn, Pinterest, and more",
        "tip_2": "Copy everything with one click",
        "tip_3": "Switch interface and hashtag output between 3 languages",
        "empty_title": "No hashtags yet",
        "empty_copy": "Fill in the topic, pick the platform, and click generate to see your caption and hashtag pack here.",
        "empty_points": "Platform presets, grouped hashtags, ready caption, recent history",
        "example_1": "Handmade candle launch",
        "example_2": "Fitness coach short video",
        "example_3": "Coffee shop opening promo",
    },
    "Українська": {
        "brand": "TagLift AI",
        "language": "Мова",
        "choose_language": "Оберіть мову",
        "language_welcome": "Виберіть мову інтерфейсу, щоб продовжити.",
        "continue": "Продовжити",
        "footer_language": "Змінити мову інтерфейсу",
        "footer_title": "Налаштування інтерфейсу",
        "footer_copy": "Тут можна будь-коли змінити мову застосунку.",
        "hero_badge": "AI-інструмент для соцмереж",
        "hero_title": "Генеруйте хештеги для соцмереж в одному чистому потоці",
        "hero_copy": "Оберіть платформу, опишіть контент і отримайте готовий набір хештегів для поста, відео, сторіс або кампанії.",
        "step_1": "1. Опишіть свій контент",
        "step_2": "2. Отримайте пакет хештегів",
        "platform": "Платформа",
        "goal": "Ціль",
        "goal_hint": "Оберіть головний результат, який має дати цей контент.",
        "apply_presets": "Застосувати пресети платформи",
        "recommended_setup": "Рекомендоване налаштування",
        "reset_form": "Очистити форму",
        "examples_title": "Швидкі приклади",
        "examples_copy": "Почніть із готового прикладу, а потім підлаштуйте його під свою нішу.",
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
        "topic_too_short": "Зробіть тему трохи конкретнішою.",
        "loading": "Генерую хештеги...",
        "request_error": "Помилка запиту до OpenAI",
        "result_title": "Згенеровані хештеги",
        "result_copy": "Результат згрупований за популярністю і нішевістю, щоб ним було простіше користуватись.",
        "caption_title": "Запропонований підпис",
        "caption_copy": "Можна використати як є або відредагувати перед публікацією.",
        "history_title": "Останні генерації",
        "history_empty": "Тут з'являтимуться ваші останні набори хештегів.",
        "history_restore": "Використати знову",
        "history_clear": "Очистити історію",
        "copy": "Скопіювати все",
        "copy_caption": "Скопіювати підпис",
        "download": "Завантажити TXT",
        "file_name": "social_media_hashtags.txt",
        "count_card": "Усього",
        "platform_card": "Платформа",
        "lang_card": "Мова",
        "strategy_card": "Стратегія",
        "format_card": "Формат",
        "goal_card": "Ціль",
        "platform_instagram": "Instagram",
        "platform_tiktok": "TikTok",
        "platform_youtube": "YouTube",
        "platform_linkedin": "LinkedIn",
        "platform_pinterest": "Pinterest",
        "platform_facebook": "Facebook",
        "platform_x": "X",
        "group_popular": "Популярні",
        "group_medium": "Середні",
        "group_niche": "Нішеві",
        "group_micro": "Мікроніша",
        "content_post": "Пост",
        "content_short_video": "Коротке відео",
        "content_story": "Сторіс",
        "content_carousel": "Карусель",
        "content_product_promo": "Промо продукту",
        "content_personal_brand": "Особистий бренд",
        "style_balanced": "Баланс",
        "style_growth": "Ріст",
        "style_niche": "Ніша",
        "goal_reach": "Охоплення",
        "goal_sales": "Продажі",
        "goal_authority": "Експертність",
        "goal_community": "Спільнота",
        "tip_1": "Instagram, TikTok, YouTube, LinkedIn, Pinterest та інші",
        "tip_2": "Копіювання в один клік",
        "tip_3": "Інтерфейс і хештеги трьома мовами",
        "empty_title": "Хештегів ще немає",
        "empty_copy": "Заповніть тему, оберіть платформу і натисніть генерацію, щоб побачити тут підпис і набір хештегів.",
        "empty_points": "Пресети платформ, згруповані хештеги, готовий підпис, історія генерацій",
        "example_1": "Запуск handmade свічок",
        "example_2": "Коротке відео фітнес-тренера",
        "example_3": "Промо відкриття кав'ярні",
    },
    "Русский": {
        "brand": "TagLift AI",
        "language": "Язык",
        "choose_language": "Выберите язык",
        "language_welcome": "Выберите язык интерфейса, чтобы продолжить.",
        "continue": "Продолжить",
        "footer_language": "Изменить язык интерфейса",
        "footer_title": "Настройки интерфейса",
        "footer_copy": "Здесь можно в любой момент изменить язык приложения.",
        "hero_badge": "AI-инструмент для соцсетей",
        "hero_title": "Генерируйте хештеги для соцсетей в одном чистом интерфейсе",
        "hero_copy": "Выберите платформу, опишите контент и получите готовый набор хештегов для поста, видео, сторис или кампании.",
        "step_1": "1. Опишите свой контент",
        "step_2": "2. Получите пакет хештегов",
        "platform": "Платформа",
        "goal": "Цель",
        "goal_hint": "Выберите главный результат, который должен дать этот контент.",
        "apply_presets": "Применить пресеты платформы",
        "recommended_setup": "Рекомендуемая настройка",
        "reset_form": "Очистить форму",
        "examples_title": "Быстрые примеры",
        "examples_copy": "Начните с готового примера, а потом подстройте его под свою нишу.",
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
        "topic_too_short": "Сделайте тему чуть конкретнее.",
        "loading": "Генерирую хештеги...",
        "request_error": "Ошибка запроса к OpenAI",
        "result_title": "Сгенерированные хештеги",
        "result_copy": "Результат сгруппирован по популярности и нишевости, чтобы им было проще пользоваться.",
        "caption_title": "Предложенный caption",
        "caption_copy": "Можно использовать как есть или отредактировать перед публикацией.",
        "history_title": "Последние генерации",
        "history_empty": "Здесь будут появляться ваши последние наборы хештегов.",
        "history_restore": "Использовать снова",
        "history_clear": "Очистить историю",
        "copy": "Скопировать все",
        "copy_caption": "Скопировать caption",
        "download": "Скачать TXT",
        "file_name": "social_media_hashtags.txt",
        "count_card": "Всего",
        "platform_card": "Платформа",
        "lang_card": "Язык",
        "strategy_card": "Стратегия",
        "format_card": "Формат",
        "goal_card": "Цель",
        "platform_instagram": "Instagram",
        "platform_tiktok": "TikTok",
        "platform_youtube": "YouTube",
        "platform_linkedin": "LinkedIn",
        "platform_pinterest": "Pinterest",
        "platform_facebook": "Facebook",
        "platform_x": "X",
        "group_popular": "Популярные",
        "group_medium": "Средние",
        "group_niche": "Нишевые",
        "group_micro": "Микрониша",
        "content_post": "Пост",
        "content_short_video": "Короткое видео",
        "content_story": "Сторис",
        "content_carousel": "Карусель",
        "content_product_promo": "Промо продукта",
        "content_personal_brand": "Личный бренд",
        "style_balanced": "Баланс",
        "style_growth": "Рост",
        "style_niche": "Ниша",
        "goal_reach": "Охват",
        "goal_sales": "Продажи",
        "goal_authority": "Экспертность",
        "goal_community": "Комьюнити",
        "tip_1": "Instagram, TikTok, YouTube, LinkedIn, Pinterest и другие",
        "tip_2": "Копирование в один клик",
        "tip_3": "Интерфейс и хештеги на 3 языках",
        "empty_title": "Хештегов пока нет",
        "empty_copy": "Заполните тему, выберите платформу и нажмите генерацию, чтобы увидеть здесь caption и набор хештегов.",
        "empty_points": "Пресеты платформ, сгруппированные хештеги, готовый caption, история генераций",
        "example_1": "Запуск handmade свечей",
        "example_2": "Короткое видео фитнес-тренера",
        "example_3": "Промо открытия кофейни",
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


def platform_defaults(platform_key: str) -> dict[str, object]:
    defaults = {
        "instagram": {"content_type": "post", "style": "balanced", "goal": "reach", "count": 25},
        "tiktok": {"content_type": "short_video", "style": "growth", "goal": "reach", "count": 12},
        "youtube": {"content_type": "short_video", "style": "niche", "goal": "authority", "count": 15},
        "linkedin": {"content_type": "post", "style": "niche", "goal": "authority", "count": 8},
        "pinterest": {"content_type": "carousel", "style": "niche", "goal": "sales", "count": 18},
        "facebook": {"content_type": "post", "style": "balanced", "goal": "community", "count": 10},
        "x": {"content_type": "post", "style": "growth", "goal": "reach", "count": 6},
    }
    return defaults.get(platform_key, defaults["instagram"])


def build_prompt(
    platform_key: str,
    topic: str,
    content_type_key: str,
    audience: str,
    style_key: str,
    goal_key: str,
    hashtag_language: str,
    count: int,
) -> str:
    sizes = compute_group_sizes(count)
    platform_name = PLATFORMS[platform_key]
    return dedent(
        f"""
        You are a social media growth assistant.
        Generate exactly {count} hashtags for {platform_name}.
        Platform guidance: {PLATFORM_GUIDES[platform_key]}
        Topic: {topic}
        Content type: {CONTENT_TYPES[content_type_key]}
        Audience: {audience or "General audience"}
        Strategy: {HASHTAG_STYLES[style_key]}
        Goal: {GOALS[goal_key]}
        Hashtag language: {hashtag_language}

        Return exactly these sections:
        [CAPTION]
        [POPULAR]
        [MEDIUM]
        [NICHE]
        [MICRO]

        Caption rules:
        - write 2 to 4 short lines
        - match the chosen platform voice
        - include a soft call to action
        - do not include hashtags inside the caption

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


def parse_response(raw_text: str, total_count: int) -> tuple[str, dict[str, list[str]]]:
    sections = {key: [] for key in GROUP_ORDER}
    mapping = {"[POPULAR]": "popular", "[MEDIUM]": "medium", "[NICHE]": "niche", "[MICRO]": "micro"}
    current = None
    caption_lines = []
    for line in raw_text.splitlines():
        value = line.strip()
        if not value:
            continue
        if value == "[CAPTION]":
            current = "caption"
            continue
        if value in mapping:
            current = mapping[value]
            continue
        if current == "caption":
            caption_lines.append(value)
            continue
        if current and value.startswith("#"):
            sections[current].append(value)
    if any(sections.values()):
        return "\n".join(caption_lines).strip(), sections
    hashtags = [line.strip() for line in raw_text.splitlines() if line.strip().startswith("#")]
    sizes = compute_group_sizes(total_count)
    start = 0
    for key in GROUP_ORDER:
        end = start + sizes[key]
        sections[key] = hashtags[start:end]
        start = end
    caption = "\n".join(line.strip() for line in raw_text.splitlines() if line.strip() and not line.strip().startswith("#"))
    return caption.strip(), sections


def flatten_sections(sections: dict[str, list[str]]) -> str:
    return "\n".join(tag for key in GROUP_ORDER for tag in sections[key])


def localize_content_type(key: str, t: dict[str, str]) -> str:
    return t[f"content_{key}"]


def localize_platform(key: str, t: dict[str, str]) -> str:
    return t[f"platform_{key}"]


def localize_goal(key: str, t: dict[str, str]) -> str:
    return t[f"goal_{key}"]


def localize_style(key: str, t: dict[str, str]) -> str:
    return t[f"style_{key}"]


def group_label(key: str, t: dict[str, str]) -> str:
    return t[f"group_{key}"]


def render_metric(label: str, value: str) -> str:
    return f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>'


def render_group_card(title: str, tags: list[str]) -> str:
    chips = "".join(f'<span class="tag-chip">{tag}</span>' for tag in tags)
    return f'<div class="group-card"><div class="group-title">{title}</div><div class="tag-wrap">{chips}</div></div>'


def push_history_item(item: dict[str, str]) -> None:
    history = st.session_state.get("generation_history", [])
    history = [item] + [entry for entry in history if entry.get("topic") != item.get("topic") or entry.get("platform_key") != item.get("platform_key")]
    st.session_state["generation_history"] = history[:6]


def restore_history_item(item: dict[str, str]) -> None:
    st.session_state["platform_key"] = item["platform_key"]
    st.session_state["content_type_key"] = item["content_type_key"]
    st.session_state["style_key"] = item["style_key"]
    st.session_state["goal_key"] = item["goal_key"]
    st.session_state["hashtag_language"] = item["hashtag_language"]
    st.session_state["count_value"] = item["count"]
    st.session_state["topic_input"] = item["topic"]
    st.session_state["audience_input"] = item["audience"]
    st.session_state["last_preset_platform"] = item["platform_key"]


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
        --muted: #c2cad6;
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
      .examples-wrap {
        margin-bottom: 1rem;
      }
      .history-list {
        display:grid;
        gap:0.7rem;
        margin-top:0.85rem;
      }
      .history-item {
        background:var(--panel-2);
        border:1px solid var(--border);
        border-radius:16px;
        padding:0.85rem 0.95rem;
      }
      .history-item strong {
        color:var(--ink);
        display:block;
        margin-bottom:0.2rem;
      }
      .history-item span {
        color:var(--muted);
        font-size:0.88rem;
      }
      .language-gate {
        max-width: 520px;
        margin: 10vh auto 0;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 28px;
        box-shadow: 0 18px 48px rgba(0,0,0,0.28);
        padding: 1.6rem;
        text-align: center;
      }
      .gate-copy {
        color: var(--muted);
        max-width: 360px;
        margin: 0 auto 0.9rem;
        line-height: 1.6;
      }
      .gate-controls {
        max-width: 520px;
        margin: 0.9rem auto 0;
      }
      .lang-option {
        display:block;
        width:100%;
        text-align:left;
        border-radius:18px;
        border:1px solid var(--border);
        background: var(--panel-2);
        color: var(--ink);
        padding:0.95rem 1rem;
        font-weight:700;
        margin-bottom:0.65rem;
      }
      .lang-option.active {
        border-color: rgba(214,41,118,0.45);
        box-shadow: 0 0 0 1px rgba(214,41,118,0.18);
        background: linear-gradient(135deg, rgba(253,29,29,0.12) 0%, rgba(214,41,118,0.10) 100%);
      }
      .footer-wrap {
        margin-top: 1.2rem;
        padding-top: 0.6rem;
        border-top: 1px solid rgba(255,255,255,0.06);
      }
      .footer-title {
        color: var(--ink);
        font-weight: 800;
        margin-bottom: 0.2rem;
      }
      .footer-copy {
        color: var(--muted);
        font-size: 0.9rem;
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
      .tiny-note {
        color: var(--muted);
        font-size: 0.82rem;
        margin-top: -0.15rem;
        margin-bottom: 0.65rem;
      }
      div[data-testid="stTextInput"],
      div[data-testid="stSelectbox"],
      div[data-testid="stTextArea"],
      div[data-testid="stSlider"] {
        width: 100%;
      }
      div[data-baseweb="input"],
      div[data-baseweb="select"] {
        background: var(--panel-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        min-height: 52px !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
      }
      div[data-baseweb="select"] > div,
      div[data-baseweb="input"] > div {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
      }
      div[data-baseweb="input"] input,
      .stApp input[type="text"],
      .stApp input[type="password"],
      .stApp textarea {
        background: transparent !important;
        color: var(--ink) !important;
        border: none !important;
        box-shadow: none !important;
      }
      div[data-baseweb="input"] input::placeholder,
      .stApp input[type="text"]::placeholder,
      .stApp input[type="password"]::placeholder,
      .stApp textarea::placeholder {
        color: #a9b2c2 !important;
      }
      div[data-baseweb="select"] input,
      div[data-baseweb="select"] span,
      div[data-baseweb="select"] div,
      div[data-baseweb="select"] svg {
        color: var(--ink) !important;
        fill: var(--ink) !important;
      }
      div[data-baseweb="input"] svg {
        color: var(--muted) !important;
        fill: var(--muted) !important;
      }
      div[data-baseweb="select"] * {
        color: var(--ink) !important;
      }
      div[data-baseweb="input"]:focus-within,
      div[data-baseweb="select"]:focus-within {
        border-color: rgba(214, 41, 118, 0.35) !important;
        box-shadow: 0 0 0 1px rgba(214, 41, 118, 0.18) !important;
      }
      textarea {
        background: var(--panel-2) !important;
        color: var(--ink) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
      }
      button[title="View fullscreen"],
      button[aria-label="View fullscreen"] {
        display: none !important;
      }
      ul[role="listbox"] {
        background: var(--panel-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: 18px !important;
        box-shadow: 0 18px 48px rgba(0,0,0,0.32) !important;
      }
      ul[role="listbox"] li {
        background: transparent !important;
        color: var(--ink) !important;
      }
      ul[role="listbox"] li:hover,
      ul[role="listbox"] li[aria-selected="true"] {
        background: rgba(214,41,118,0.14) !important;
        color: var(--ink) !important;
      }
      label, .stMarkdown, .stText, p {
        color: var(--ink);
      }
      [data-testid="stCaptionContainer"] {
        color: var(--muted) !important;
      }
      [data-testid="stSlider"] label {
        margin-bottom: 0.4rem !important;
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

if "app_language" not in st.session_state:
    st.session_state["app_language"] = APP_LANGUAGES[0]

if "language_confirmed" not in st.session_state:
    st.session_state["language_confirmed"] = False

if "language_gate_choice" not in st.session_state:
    st.session_state["language_gate_choice"] = APP_LANGUAGES[0]

app_language = st.session_state.get("app_language", APP_LANGUAGES[0])
t = UI_TEXT[app_language]
if "platform_key" not in st.session_state:
    st.session_state["platform_key"] = "instagram"
if "content_type_key" not in st.session_state:
    st.session_state["content_type_key"] = "post"
if "style_key" not in st.session_state:
    st.session_state["style_key"] = "balanced"
if "goal_key" not in st.session_state:
    st.session_state["goal_key"] = "reach"
if "hashtag_language" not in st.session_state:
    st.session_state["hashtag_language"] = HASHTAG_LANGUAGES[0]
if "count_value" not in st.session_state:
    st.session_state["count_value"] = 25
if "model_name" not in st.session_state:
    st.session_state["model_name"] = "gpt-4.1-mini"
if "generation_history" not in st.session_state:
    st.session_state["generation_history"] = []

if not st.session_state["language_confirmed"]:
    gate_lang = st.session_state.get("language_gate_choice", app_language)
    gate_t = UI_TEXT[gate_lang]
    left_space, center_col, right_space = st.columns([0.26, 0.48, 0.26])
    with center_col:
        st.markdown(
            f"""
            <div class="language-gate">
              <div class="brand-mark" style="margin:0 auto 1rem;">TL</div>
              <div class="section-title">{gate_t["choose_language"]}</div>
              <div class="gate-copy">{gate_t["language_welcome"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('<div class="gate-controls">', unsafe_allow_html=True)
        for option in APP_LANGUAGES:
            css_class = "lang-option active" if option == gate_lang else "lang-option"
            button_type = "primary" if option == gate_lang else "secondary"
            if st.button(option, key=f"gate_lang_{option}", use_container_width=True, type=button_type):
                gate_lang = option
                st.session_state["language_gate_choice"] = option
                st.rerun()
        gate_t = UI_TEXT[gate_lang]
        if st.button(gate_t["continue"], type="primary", use_container_width=True):
            st.session_state["app_language"] = gate_lang
            st.session_state["language_confirmed"] = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

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
          <div class="brand-subtitle">Social hashtag generator</div>
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

example_configs = [
    {
        "label": t["example_1"],
        "platform": "instagram",
        "content_type": "post",
        "style": "balanced",
        "goal": "sales",
        "topic": "handmade soy candle launch with cozy home decor vibe",
        "audience": "gift shoppers, home decor lovers, women 24-40",
    },
    {
        "label": t["example_2"],
        "platform": "tiktok",
        "content_type": "short_video",
        "style": "growth",
        "goal": "reach",
        "topic": "fitness coach quick morning mobility routine",
        "audience": "busy professionals, beginner fitness audience",
    },
    {
        "label": t["example_3"],
        "platform": "facebook",
        "content_type": "product_promo",
        "style": "balanced",
        "goal": "community",
        "topic": "grand opening promotion for a neighborhood coffee shop",
        "audience": "local residents, remote workers, coffee lovers",
    },
]

platform_key = st.session_state["platform_key"]
defaults = platform_defaults(platform_key)
if st.session_state.get("last_preset_platform") != platform_key:
    st.session_state["content_type_key"] = defaults["content_type"]
    st.session_state["style_key"] = defaults["style"]
    st.session_state["goal_key"] = defaults["goal"]
    st.session_state["count_value"] = defaults["count"]
    st.session_state["last_preset_platform"] = platform_key

left_col, right_col = st.columns([0.98, 1.02], gap="large")

with left_col:
    st.markdown(
        f"""
        <div class="section-eyebrow">Step 1</div>
        <div class="section-title">{t["step_1"]}</div>
        <div class="subtle-note">{t["hero_copy"]}</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""
        <div class="examples-wrap">
          <div class="section-title" style="font-size:1rem; margin-bottom:0.1rem;">{t["examples_title"]}</div>
          <div class="tiny-note">{t["examples_copy"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    example_cols = st.columns(3)
    for idx, example in enumerate(example_configs):
        with example_cols[idx]:
            if st.button(example["label"], key=f"example_{idx}", use_container_width=True):
                st.session_state["platform_key"] = example["platform"]
                st.session_state["content_type_key"] = example["content_type"]
                st.session_state["style_key"] = example["style"]
                st.session_state["goal_key"] = example["goal"]
                st.session_state["topic_input"] = example["topic"]
                st.session_state["audience_input"] = example["audience"]
                st.session_state["count_value"] = platform_defaults(example["platform"])["count"]
                st.session_state["last_preset_platform"] = example["platform"]
                st.rerun()

    topic = st.text_input(t["topic"], placeholder=t["topic_placeholder"], key="topic_input")
    audience = st.text_input(t["audience"], placeholder=t["audience_placeholder"], key="audience_input")
    row1 = st.columns(2)
    with row1[0]:
        platform_key = st.selectbox(
            t["platform"],
            list(PLATFORMS.keys()),
            format_func=lambda key: localize_platform(key, t),
            key="platform_key",
        )
        recommended = platform_defaults(platform_key)
        st.markdown(
            f'<div class="tiny-note">{t["recommended_setup"]}: {localize_goal(recommended["goal"], t)} · {localize_style(recommended["style"], t)} · {recommended["count"]}</div>',
            unsafe_allow_html=True,
        )
    with row1[1]:
        content_type_key = st.selectbox(
            t["content_type"],
            list(CONTENT_TYPES.keys()),
            format_func=lambda key: localize_content_type(key, t),
            key="content_type_key",
        )
    row2 = st.columns(2)
    with row2[0]:
        style_key = st.selectbox(
            t["strategy"],
            list(HASHTAG_STYLES.keys()),
            format_func=lambda key: localize_style(key, t),
            key="style_key",
        )
    with row2[1]:
        goal_key = st.selectbox(
            t["goal"],
            list(GOALS.keys()),
            format_func=lambda key: localize_goal(key, t),
            key="goal_key",
        )
        st.markdown(f'<div class="tiny-note">{t["goal_hint"]}</div>', unsafe_allow_html=True)
    row3 = st.columns(2)
    with row3[0]:
        hashtag_language = st.selectbox(t["hashtag_language"], HASHTAG_LANGUAGES, key="hashtag_language")
    with row3[1]:
        count = st.slider(t["count"], min_value=5, max_value=40, step=1, key="count_value")
    row4 = st.columns(2)
    with row4[0]:
        model = st.selectbox(t["model"], ["gpt-4.1-mini", "gpt-4.1"], key="model_name")
    with row4[1]:
        st.text_input(t["api_key"], type="password", key="api_key", help=t["api_key_help"])
    row5 = st.columns(2)
    with row5[0]:
        generate = st.button(t["generate"], type="primary", use_container_width=True)
    with row5[1]:
        regenerate = st.button(t["regenerate"], use_container_width=True)
    row6 = st.columns(2)
    with row6[0]:
        apply_presets = st.button(t["apply_presets"], use_container_width=True)
    with row6[1]:
        reset_form = st.button(t["reset_form"], use_container_width=True)
    if apply_presets:
        defaults = platform_defaults(platform_key)
        st.session_state["content_type_key"] = defaults["content_type"]
        st.session_state["style_key"] = defaults["style"]
        st.session_state["goal_key"] = defaults["goal"]
        st.session_state["count_value"] = defaults["count"]
        st.session_state["last_preset_platform"] = platform_key
        st.rerun()
    if reset_form:
        defaults = platform_defaults(platform_key)
        st.session_state["topic_input"] = ""
        st.session_state["audience_input"] = ""
        st.session_state["content_type_key"] = defaults["content_type"]
        st.session_state["style_key"] = defaults["style"]
        st.session_state["goal_key"] = defaults["goal"]
        st.session_state["count_value"] = defaults["count"]
        st.session_state["caption_text"] = ""
        st.session_state["hashtags_sections"] = None
        st.session_state["hashtags_flat"] = ""
        st.rerun()

should_generate = generate or (regenerate and bool(st.session_state.get("last_topic")))

if should_generate:
    active_topic = topic.strip() or st.session_state.get("last_topic", "")
    active_audience = audience.strip() or st.session_state.get("last_audience", "")
    if not active_topic:
        st.warning(t["enter_topic"])
    elif len(active_topic) < 4:
        st.warning(t["topic_too_short"])
    else:
        client = get_client()
        if client is None:
            st.error(t["missing_key"])
        else:
            st.session_state["last_topic"] = active_topic
            st.session_state["last_audience"] = active_audience
            st.session_state["last_platform"] = platform_key
            st.session_state["last_content_type"] = content_type_key
            st.session_state["last_style"] = style_key
            st.session_state["last_goal"] = goal_key
            st.session_state["last_language"] = hashtag_language
            st.session_state["last_count"] = count
            try:
                with st.spinner(t["loading"]):
                    response = client.responses.create(
                        model=model,
                        input=build_prompt(
                            platform_key=platform_key,
                            topic=active_topic,
                            content_type_key=content_type_key,
                            audience=active_audience,
                            style_key=style_key,
                            goal_key=goal_key,
                            hashtag_language=hashtag_language,
                            count=count,
                        ),
                    )
                raw_text = response.output_text.strip()
                caption_text, sections = parse_response(raw_text, count)
                flat_hashtags = flatten_sections(sections)
                st.session_state["caption_text"] = caption_text
                st.session_state["hashtags_sections"] = sections
                st.session_state["hashtags_flat"] = flat_hashtags
                push_history_item(
                    {
                        "topic": active_topic,
                        "audience": active_audience,
                        "platform_key": platform_key,
                        "platform": localize_platform(platform_key, t),
                        "content_type_key": content_type_key,
                        "style_key": style_key,
                        "goal_key": goal_key,
                        "goal": localize_goal(goal_key, t),
                        "hashtag_language": hashtag_language,
                        "count": count,
                    }
                )
            except Exception as exc:
                st.error(f'{t["request_error"]}: {exc}')

sections = st.session_state.get("hashtags_sections")
caption_text = st.session_state.get("caption_text", "")
flat_hashtags = st.session_state.get("hashtags_flat", "")
history = st.session_state.get("generation_history", [])
last_platform = st.session_state.get("last_platform", platform_key)
last_language = st.session_state.get("last_language", hashtag_language)
last_content_type = st.session_state.get("last_content_type", content_type_key)
last_goal = st.session_state.get("last_goal", goal_key)
total_generated = len(flat_hashtags.splitlines()) if flat_hashtags else 0

with right_col:
    st.markdown(
        f"""
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
              {render_metric(t["platform_card"], localize_platform(last_platform, t))}
              {render_metric(t["goal_card"], localize_goal(last_goal, t))}
              {render_metric(t["format_card"], localize_content_type(last_content_type, t))}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
            <div class="section-title" style="font-size:1rem; margin-top:0.2rem; margin-bottom:0.15rem;">{t["caption_title"]}</div>
            <div class="result-copy">{t["caption_copy"]}</div>
            """,
            unsafe_allow_html=True,
        )
        caption_cols = st.columns([0.42, 0.58])
        with caption_cols[0]:
            copy_button(caption_text, t["copy_caption"])
        with caption_cols[1]:
            st.caption(f'{t["lang_card"]}: {last_language}')
        st.text_area(t["caption_title"], caption_text, height=120, key="caption_result", label_visibility="collapsed")

        action_cols = st.columns([0.42, 0.58])
        with action_cols[0]:
            copy_button(flat_hashtags, t["copy"])
        with action_cols[1]:
            st.download_button(
                t["download"],
                data=f"{caption_text}\n\n{flat_hashtags}".strip(),
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
              <div class="tiny-note" style="margin-top:0.8rem;">{t["empty_points"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="section-title" style="font-size:1rem; margin-top:1rem; margin-bottom:0.15rem;">{t["history_title"]}</div>
        <div class="result-copy">{t["history_empty"] if not history else ""}</div>
        """,
        unsafe_allow_html=True,
    )
    if history:
        for idx, item in enumerate(history):
            st.markdown(
                f'<div class="history-item"><strong>{item["topic"]}</strong><span>{item["platform"]} · {item["goal"]}</span></div>',
                unsafe_allow_html=True,
            )
            if st.button(t["history_restore"], key=f"restore_history_{idx}", use_container_width=True):
                restore_history_item(item)
                st.rerun()
        if st.button(t["history_clear"], key="clear_history", use_container_width=True):
            st.session_state["generation_history"] = []
            st.rerun()

st.markdown('<div class="footer-wrap">', unsafe_allow_html=True)
footer_cols = st.columns([0.34, 0.66])
with footer_cols[0]:
    st.markdown(f'<div class="footer-title">{t["footer_title"]}</div><div class="footer-copy">{t["footer_copy"]}</div>', unsafe_allow_html=True)
with footer_cols[1]:
    footer_select_col, _ = st.columns([0.42, 0.58])
    with footer_select_col:
        new_language = st.selectbox(
            t["footer_language"],
            APP_LANGUAGES,
            index=APP_LANGUAGES.index(app_language),
            key="footer_language_select",
        )
if new_language != app_language:
    st.session_state["app_language"] = new_language
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)
