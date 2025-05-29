from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from weather_agent.agent import weather_agent
from dotenv import load_dotenv
import logging
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.ERROR)

load_dotenv()

session_service = InMemorySessionService()

APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_001" # 今回は固定のセッションIDで実行

session = session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID
)

print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")

runner = Runner(
    agent=weather_agent, # 実行するAgent
    app_name=APP_NAME,
    session_service=session_service
)
print(f"Runner created for agent '{runner.agent.name}'.")
