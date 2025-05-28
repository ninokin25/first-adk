from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from weather_agent.agent import weather_agent

### ここから追加
import asyncio
from google.genai import types # メッセージを作成するため
### ここまで

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

async def call_agent_async(query: str):
  """クエリをAgentへ送信し、コンソールへ出力します。 Sends a query to the agent and prints the final response."""
  print(f"\n>>> User Query: {query}")

  # ADKのフォーマットでメッセージを作成
  content = types.Content(role='user', parts=[types.Part(text=query)])

  final_response_text = "Agent did not produce a final response." # Default

  # 重要: `run_async` は Agentロジックを実行して、Eventを作成します。
  # イベントを反復処理して最終応答を見つけます。
  async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content):
      # コメントインすると全イベントが出力されます。
      # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

      # 重要: is_final_response() で反復の終了を判定
      if event.is_final_response():
          if event.content and event.content.parts:
             # 最初の部分ではテキスト応答を想定
             final_response_text = event.content.parts[0].text
          elif event.actions and event.actions.escalate: # 潜在的なエラー/エスカレーションを処理する
             final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
          # 他のエラー処理があれば記述する
          break # 最終応答が見つかったら反復処理を終了

  print(f"<<< Agent Response: {final_response_text}")

### ここから追加
async def run_conversation():
    await call_agent_async("ロンドンの天気は?")
    await call_agent_async("パリについては？") # エラーの確認
    await call_agent_async("ニューヨークの天気を教えて下さい。")

async def main():

    # 会話を非同期実行
    await run_conversation()

if __name__ == "__main__":
    asyncio.run(main())

### ここまで