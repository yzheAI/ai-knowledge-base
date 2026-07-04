from openai import OpenAI, APITimeoutError, APIError
from app.exceptions.exceptions import LLMTimeoutError, LLMServiceError
from app.config import API_KEY


client = OpenAI(
    api_key=API_KEY,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
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
