import json
import httpx
from .config import settings

SYSTEM_PROMPT = """
You are a financial regulatory analyst.
Extract only information explicitly supported by the supplied regulatory text.
Return JSON:
{
  "obligations": ["..."],
  "topics": ["payments", "KYC", "AML", "sanctions", "data", "cross-border"],
  "effective_dates": ["..."]
}
Do not invent obligations or dates.
"""

async def extract_with_llm(text: str) -> dict:
    if not settings.llm_enabled or not settings.openai_api_key:
        raise RuntimeError("LLM is disabled or API key is missing.")

    url = settings.openai_base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": settings.openai_model,
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text[:18000]},
        ],
    }
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}

    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    return json.loads(data["choices"][0]["message"]["content"])
