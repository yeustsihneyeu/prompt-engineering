class Model():
    def __init__(self, model_name: str, short_name: str):
       self.model_name = model_name
       self.short_name = short_name


def get_models():
    return [
        Model("llama3.2", "llama3.2"),
        Model("gemma2:9b", "gemma2"),
        Model("qwen2.5:7b", "qwen2.5")
    ]