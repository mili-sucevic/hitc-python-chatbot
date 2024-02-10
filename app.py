# Import necessary libraries
from flask import Flask, render_template, request, session, jsonify
import openai

# Create a Flask application
app = Flask(__name__, static_url_path='/static')
app.secret_key = '[YOUR-SECRET-KEY]'

# Set your OpenAI API key
openai.api_key = '[YOU-API-KEY]'

# Maximum number of messages to keep in chat history
MAX_HISTORY_SIZE = 20

# Function to generate OpenAI response based on user input and chat history
def generate_openai_response(user_input, chat_history=[]):
    # Append the user input to the chat history
    chat_history.append({"role": "user", "content": user_input})

    # Keep only the last N messages
    chat_history = chat_history[-MAX_HISTORY_SIZE:]

    # Call the OpenAI API with the chat history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
    )

    return response.choices[0].message.content

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle user input and get bot response
@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["user_message"]

    # Get the chat history from the session or initialize it
    chat_history = session.get("chat_history", [])

    # Call the function to generate a response based on user input and chat history
    bot_response = generate_openai_response(user_message, chat_history)

    # Append the user input and bot response to the chat history
    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": bot_response})

    # Keep only the last N messages in the chat history
    chat_history = chat_history[-MAX_HISTORY_SIZE:]

    # Update the chat history in the session
    session["chat_history"] = chat_history

    # Return the bot's response in JSON format
    return jsonify({"response": bot_response})

@app.route("/clear_history")
def clear_history():
    # Clear chat history logic
    session.pop("chat_history", None)
    return jsonify({"status": "success"})

# Run the application if the script is executed directly
if __name__ == "__main__":
    app.run(debug=True, port=7000)