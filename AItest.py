import os
import google.generativeai as genai

# Configure the API key (ensure the API_KEY environment variable is set)
genai.configure(api_key="AIzaSyD6ZDCbcjONe3qZcaVgSpkuTp2kKRqPkHE")

# Create the model with the configuration
generation_config = {
    "temperature": 1.15,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You are an expert in suggesting gifts for people. Your task is to engage "
        "in conversations about gift-giving and provide thoughtful suggestions. "
        "Understand the user’s preferences, occasion, and budget to offer personalized "
        "gift ideas. Use relatable examples, humor, and creativity to make the interaction "
        "enjoyable. Ask clarifying questions to better understand the recipient’s personality "
        "and interests. Offer practical tips for wrapping, presenting, or adding a personal touch "
        "to the gift. Tailor suggestions to fit a range of scenarios, from simple and inexpensive "
        "to elaborate and luxurious."
        "Also when giving suggestion, give some trending product description, prices, customer ratings and where to find the item "
    ),
)

history = []

print("Hello, how can I help you today?")
print("")

while True:
    try:
        user_input = input("You: ")

        # Start the chat session
        chat_session = model.start_chat(history=history)

        # Get the response from the model
        response = chat_session.send_message(user_input)

        model_response = response.text

        print(f'Giftinator 3000: {model_response}\n')

        # Update the conversation history
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "assistant", "parts": [model_response]})
    except Exception as e:
        print(f"An error occurred: {e}")
        break 