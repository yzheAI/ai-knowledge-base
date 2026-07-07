from openai import OpenAI, APITimeoutError, APIError
from app.exceptions.exceptions import LLMTimeoutError, LLMServiceError
from app.config import API_KEY, LLM_BASE_URL


client = OpenAI(
    api_key=API_KEY,
    base_url=LLM_BASE_URL
)


def chat_with_qwen(prompt: str):
    try:
        response = client.chat.completions.create(
            model="qwen-plus",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )
        return response.choices[0].message.content
    except APITimeoutError:
        raise LLMTimeoutError()
    except APIError:
        raise LLMServiceError()
    except Exception:
        raise LLMServiceError("LLM未知错误")
