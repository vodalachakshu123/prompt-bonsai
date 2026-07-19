# Integrations

## OpenAI

```python
from openai import OpenAI
from prompt_bonsai import compress

client = OpenAI()

prompt = "Your very long prompt..."
compressed = compress(prompt, ratio=0.4)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": compressed}]
)
```

## LangChain

```python
from prompt_bonsai import Compressor
from langchain_core.prompts import PromptTemplate

compressor = Compressor(target_ratio=0.3)

# Compress context before using in template
context = compressor.compress(large_document).text

template = PromptTemplate.from_template(
    "Answer based on: {context}\n\nQuestion: {question}"
)
```

## LiteLLM

```python
from prompt_bonsai import compress
import litellm

prompt = compress(long_prompt, ratio=0.4)
response = litellm.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
```

## Custom Integration

```python
from prompt_bonsai import Compressor

class CompressedLLM:
    def __init__(self, base_llm, compressor=None):
        self.llm = base_llm
        self.compressor = compressor or Compressor()

    def invoke(self, prompt):
        compressed = self.compressor.compress(prompt).text
        return self.llm.invoke(compressed)
```
