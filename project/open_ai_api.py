import openai

openai.api_key = 'your-api-key-here'

response = openai.File.create(
  file=open("path/to/your/dataset.jsonl"),
  purpose='fine-tune'
)

print(response)