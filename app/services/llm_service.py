import logging

from openai import OpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

client = OpenAI(
    api_key = settings.LLM_API_KEY,
    base_url = settings.LLM_BASE_URL,
)

def generate_answer(prompt: str) -> str:
    prompt = prompt.strip()

    if not prompt:
        raise ValueError("prompt不能为空")

    try:
        response = client.chat.completions.create(
            model = settings.LLM_MODEL,
            messages = [
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=0.2,
        )

        answer = response.choices[0].message.content

        if not answer:
            return "模型未返回有效回答"

        logger.info("LLM回答生成成功")

        return answer.strip()

    except Exception:
        logger.exception("LLM调用失败")
        raise