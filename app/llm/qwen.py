from openai import OpenAI, APITimeoutError, APIError
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
        return "LLM请求超时，请稍后再试"
    except APIError:
        return "LLM服务异常"
    except Exception as e:
        return f"未知错误：{str(e)}"
