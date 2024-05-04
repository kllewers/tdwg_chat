import openai

def query_fine_tuned_model(prompt):
    try:
        # Your OpenAI API key
        openai.api_key = 'sk-proj-fxWoeMvuAD0R9xacMWPzT3BlbkFJ33vuRJn3G2vVnj7SjUF3'

        # Name of your fine-tuned model
        model_name = 'ft:davinci-002:personal::9LCg3jWz'

        # Sending a prompt to the model using the new API interface
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Printing the response from the model
        print(response['choices'][0]['message']['content'])

    except Exception as e:
        print(f"An error occurred: {e}")

# Example prompt
user_prompt = "Can you give me information about dwc:Taxon?"
query_fine_tuned_model(user_prompt)
