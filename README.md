# TagLift AI

TagLift AI is a polished Streamlit app that creates ready-to-use hashtags for multiple social media platforms with OpenAI.

Built for creators, small businesses, personal brands, coaches, and online shops that want faster content packaging without manually searching for hashtags.

## What the app does

- generates hashtags for Instagram, TikTok, YouTube, LinkedIn, Pinterest, Facebook, and X
- supports 3 interface languages: English, Ukrainian, Russian
- supports 3 hashtag output languages: English, Ukrainian, Russian
- works for posts, short videos, stories, carousels, product promos, and personal brand content
- groups results into popular, medium, niche, and micro-niche hashtags
- lets users copy the final set or download it as `.txt`

## Included sales assets

- [Product page copy](C:\Users\rubin\OneDrive\Рабочий стол\Projects\Бусінес\instagram_hashtag_generator\PRODUCT_PAGE.md)
- [Marketing copy](C:\Users\rubin\OneDrive\Рабочий стол\Projects\Бусінес\instagram_hashtag_generator\MARKETING_COPY.md)
- [Launch checklist](C:\Users\rubin\OneDrive\Рабочий стол\Projects\Бусінес\instagram_hashtag_generator\LAUNCH_CHECKLIST.md)
- [Brandmark](C:\Users\rubin\OneDrive\Рабочий стол\Projects\Бусінес\instagram_hashtag_generator\assets\brandmark.svg)

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API key:

```bash
setx OPENAI_API_KEY "your_key"
```

4. Run the app:

```bash
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push the project to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click `New app`.
4. Select the repository: `rubin666666/instagram_hashtag_generator`
5. Use:
   - Branch: `main`
   - Main file path: `app.py`
6. Add a secret in the app settings:

```toml
OPENAI_API_KEY = "your_key"
```

7. Deploy.

## Notes

- `requirements.txt` is enough for this deployment.
- `.streamlit/secrets.toml` is ignored by git on purpose.
