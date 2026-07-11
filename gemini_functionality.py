import base64
import time
import uuid
import json
from vertexai.generative_models import (
    GenerativeModel, 
    Content,
    Part
)
from vertexai.generative_models import GenerativeModel

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# File to store chat history
chat_hist = "student_chat.json"


class GeminiFunctionality:

    def __init__(self, model: str, parameters: Dict[str, str] = None, prompt: str = ""):

        self.parameters = parameters
        self.model = model
        self.session = {}
        self.prompt = prompt
        self.chat_model = GenerativeModel(model)
        self.chat_histories = self.load_history()
        self.chat_session = None

    def load_history(self):
        try:
            with open(chat_hist, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # Return an empty dict if no history exists

    def save_history(self, history):
        with open(chat_hist, "w") as file:
            json.dump(history, file, indent=4)

    def generate_session_id(self):
        return str(uuid.uuid4())

    def deactivate_expired_sessions(self):
        current_time = time.time()
        for session_id, data in list(self.chat_histories.items()):
            if (
                data["active"] and current_time - data["created_at"] > 1800
            ):  # 30 minutes
                logger.info(f"Deactivating expired session: {session_id}")
                self.chat_histories[session_id]["active"] = False

    def get_chat_response(
        self, user_message: str, session: Optional[str] = None) -> tuple[str, str]:

        # Deactivate expired sessions periodically
        self.deactivate_expired_sessions()

        # If a session ID is provided and exists, continue the session
        if (
            session
            and session in self.chat_histories
            and self.chat_histories[session]["active"]
        ):
            # Use existing session
            logger.debug(f"Using existing session ID: {session}")

        else:
            session = self.generate_session_id()
            self.chat_histories[session] = {
                "messages": [],
                "created_at": time.time(),
                "active": True,
            }
            logger.info(f"Created new session: {session}")
        chat_history = self.chat_histories[session]

        context = [
            Content(role=message["role"], parts=[Part.from_text(message["content"])])
            for message in chat_history["messages"]
        ]


        self.chat_session = self.chat_model.start_chat(history=context)

        # Get model response
        model_response = self.chat_session.send_message(user_message)

        # Store user message in chat history
        chat_history["messages"].append({"role": "user", "content": user_message})

        # Append model's response to chat history
        chat_history["messages"].append(
            {"role": "model", "content": model_response.text}
        )

        # Save updated history back to file
        self.chat_histories[session]["messages"] = chat_history["messages"]
        self.save_history(self.chat_histories)

        return model_response.text, session
