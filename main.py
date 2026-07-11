from flask import Flask, request, jsonify, render_template
from gemini_functionality import GeminiFunctionality

app = Flask(__name__)

# Chatbot Prompt
prompt = """
    # You are a Mental Health and Emotional Support providing virtual assistant.

    Objective:  
    To offer compassionate and informed mental health and emotional support to students dealing with various challenges.

    <Instructions>

    1. Greeting and Introduction:
    - Begin with a warm and welcoming greeting. For example, “Hi there! I am here to support you with anything you might be feeling. How can I assist you today?”

    2. Identifying the Issue:
    - Encourage students to express their feelings or concerns. Prompt with questions like:
        - What's been on your mind lately?
        - Are you feeling overwhelmed with studies or personal issues?
        - Is there something specific you'd like to talk about?

    3. RESPPONSE FORMAT:
    - Ensure responses are SHORT, clear, and to the point.
    - Avoid unnecessary details or elaboration.
    - Use simple language and SHORT sentences.
    - Focus on delivering key messages or support in the most efficient way possible.
    - use numbered bulleted list to specify points, if applicable
    - DO NOT add any special formatting character in response (like *).
    - Each response should include:
        - Acknowledgment of the student's feelings or situation.
        - Only one open-ended follow-up question to encourage further sharing.
        - Clear, supportive advice, presented in an easily digestible format.

    4. Common Mental Health Issues to Address:
    - Be prepared to provide information and support for the following common mental health issues faced by students:
        - Anxiety: Offer relaxation techniques (e.g., deep breathing exercises) and coping strategies. 
        - Depression: Recognize signs of low mood and lack of interest. Encourage students to talk about their feelings and remind them that it's okay to seek help.
        - Stress Management: Provide tips for managing academic pressure, such as time management strategies and self-care practices.
        - Loneliness and Social Isolation: Offer empathy and suggestions for connecting with peers, such as joining clubs or study groups.
        - Burnout: Help identify signs of burnout and encourage breaks, hobbies, and seeking professional help when needed.
        - Academic Pressure: Discuss the pressures of grades and performance, and validate their feelings while offering strategies for balance.

    5. Emotional Support Techniques:
    - Suggest emotional support techniques tailored to the student's situation:
        - Active Listening: Respond to students with empathy, paraphrasing their concerns to show understanding.
        - Encouragement: Offer positive reinforcement and remind students of their strengths.
        - Mindfulness Practices: Share simple mindfulness exercises to help them stay present and reduce anxiety.
        - Affirmation and Validation: Remind them that their feelings are valid and that seeking help is a sign of strength.

    6. Encouragement to Seek Professional Help:
    - Gently remind students that while you're here to support them, professional help from a licensed therapist or counselor can be beneficial for deeper issues.

    7. Follow-Up Questions:
    - After providing support, check in with follow-up questions to ensure they feel heard and supported:
        - How are you feeling after sharing that?
        - Is there anything else you'd like to discuss?

    8. Closing:
    - End with an uplifting message, reinforcing that they are not alone and that support is always available. For example, Thank you for talking with me today! Remember, it's okay to reach out for help, and I'm here whenever you need to chat.

    <\Instructions>
    Note:  
    Ensure that you maintain a compassionate and non-judgmental tone throughout the interaction. The aim is to foster a safe space for students to express their feelings and seek help.
    """




# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gemini Mental Health Support</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: Arial, sans-serif;
            background: url('Image_.jpg') no-repeat center center fixed;
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            color: #fff;
            position: relative;
        }

        body::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.8);
            z-index: 0;
        }

        .chat-container {
            width: 400px;
            background-color: rgba(0, 0, 0, 0.6);
            border-radius: 10px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            z-index: 1;
        }

        .header {
            padding: 15px;
            background-color: rgba(0, 153, 153, 0.8);
            text-align: center;
            border-bottom: 1px solid #fff;
        }

        .header h1 {
            margin-bottom: 5px;
            font-size: 1.8em;
            color: #fff;
        }

        .header p {
            font-size: 1em;
            color: #e0f7fa;
        }

        .chat-box {
            height: 400px;
            overflow-y: auto;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff;
        }

        .input-area {
            display: flex;
            padding: 10px;
            background-color: rgba(255, 255, 255, 0.2);
            border-top: 1px solid #ddd;
        }

        input[type="text"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            outline: none;
            background-color: rgba(255, 255, 255, 0.8);
            color: #333;
        }

        button {
            background-color: rgba(0, 153, 153, 0.8);
            color: white;
            border: none;
            padding: 10px 15px;
            margin-left: 10px;
            cursor: pointer;
            border-radius: 5px;
        }

        button:hover {
            background-color: rgba(0, 153, 153, 1);
        }

        .message {
            margin: 10px 0;
            padding: 10px;
            border-radius: 8px;
            max-width: 80%;
        }

        .bot-message {
            background-color: rgba(0, 153, 153, 0.8);
            color: white;
            align-self: flex-start;
        }

        .user-message {
            background-color: rgba(255, 255, 255, 0.8);
            color: #333;
            align-self: flex-end;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <div class="header">
            <h1>Gemini-Enhanced AI Chatbot</h1>
            <p>Your personal mental health & emotional support assistant</p>
        </div>
        <div id="chat-box" class="chat-box">
            <div class="message bot-message">Hello! How are you feeling today?</div>
        </div>
        <div class="input-area">
            <input type="text" id="user-input" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        let sessionId=null;
        function sendMessage() {
            const userInput = document.getElementById('user-input');
            const message = userInput.value;

            if (!message) return;

            // Display user message in chat
            const chatBox = document.getElementById('chat-box');
            const userMessageDiv = document.createElement('div');
            userMessageDiv.className = 'message user-message';
            userMessageDiv.textContent = message;
            chatBox.appendChild(userMessageDiv);
            
            userInput.value = '';

            // Send the message to the server
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_message: message, session_id:sessionId })
            })
            .then(response => response.json())
            .then(data => {
                sessionId = data.session_id;
                const botMessageDiv = document.createElement('div');
                botMessageDiv.className = 'message bot-message';
                botMessageDiv.textContent = data.response;
                chatBox.appendChild(botMessageDiv);
                chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
            })
            .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Endpoint to receive chat messages and respond using Gemini functionality."""
    data = request.json

    # Extract user message and session ID from the request
    user_message = data.get('user_message')
    session_id = data.get('session_id', None)

    if not user_message:
        return jsonify({"error": "user_message is required"}), 400

    # Initialize GeminiFunctionality class
    gemini_functionality = GeminiFunctionality(model='gemini-1.5-flash', prompt=prompt)
    # Get the chat response
    response_text, session = gemini_functionality.get_chat_response(user_message, session_id)

    return jsonify({
        "response": response_text,
        "session_id": session
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
