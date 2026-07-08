def build_prompt(
        query,
        content_text,
        history
):
    prompt = f"""
            请根据给定资料回答问题。
            历史对话：
            {history}
            资料：
            {content_text}
            问题：
            {query}
            如果资料不足，请回答：未在知识库中找到相关信息。
            """
    return prompt
