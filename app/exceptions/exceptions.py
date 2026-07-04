class DocumentNotFound(Exception):
    def __init__(self, message="上传文件为空"):
        self.message = message


class UnsupportedDocumentType(Exception):
    def __init__(self, message="文件类型不支持"):
        self.message = message


class DocumentEmptyError(Exception):
    def __init__(self, message="上传文件为空"):
        self.message = message


class LLMTimeoutError(Exception):
    def __init__(self, message="LLM请求超时"):
        self.message = message


class LLMServiceError(Exception):
    def __init__(self, message="LLM服务异常"):
        self.message = message


class KnowledgeBaseEmptyError(Exception):
    def __init__(self, message="知识库为空，请先上传文档"):
        self.message = message

