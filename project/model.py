import openai
api_key = 'placeholder'

from openai import OpenAI
client = OpenAI(api_key=api_key)

"POST https://api.openai.com/v1/completions"

completion = client.completions.create(
  model="placehold",
  prompt= "Can you give me information about dwc:Taxon?",
  max_tokens= 1000,
  temperature=0
)

print(completion)