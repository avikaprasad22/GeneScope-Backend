import os
import google.generativeai as genai

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key
api_key = os.getenv("CHATAPIKEY")
# Configure the API key (ensure the API_KEY environment variable is set)

genai.configure(api_key=api_key)


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
        "You are a highly intelligent and professional AI assistant designed for business support. "
        "Your primary role is to provide exceptional customer service while leveraging deep expertise in market analysis, "
        "inventory management, and sales strategy. You have access to real-time data and can present current sales trends,"
        " identify growth opportunities, and assist with complex decision-making. You communicate clearly, offer strategic"
        " recommendations, and adapt your guidance to each unique business scenario. Be proactive, concise, and data-driven."
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

        print(f'Captain Cruncher: {model_response}\n')

        # Update the conversation history
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "assistant", "parts": [model_response]})
    except Exception as e:
        print(f"An error occurred: {e}")
        break 