# Instagram Hashtag Generator

Local Streamlit app for generating Instagram hashtags with OpenAI.

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set your API key:

```bash
setx OPENAI_API_KEY "your_key"
```

4. Run the app:

```bash
streamlit run app.py
```

## Features

- Hashtag generation with OpenAI
- Content type selector
- Hashtag strategy selector
- Copy button
- Export to `.txt`
- 3 app languages: English, Ukrainian, Russian

## Deploy to Streamlit Community Cloud

1. Push the project to GitHub.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Click `New app`.
4. Select this repository: `rubin666666/instagram_hashtag_generator`
5. Set:
   - Branch: `main`
   - Main file path: `app.py`
6. In app settings, add a secret:

```toml
OPENAI_API_KEY = "your_key"
```

7. Deploy the app.

## Notes

- `requirements.txt` is enough for deployment, `packages.txt` is not required right now.
- Local secret file `.streamlit/secrets.toml` is ignored by git on purpose.
