import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json

import pyttsx3
from gpt4all import GPT4All

def speak(text):
    engine = pyttsx3.init()  # Initialize the TTS engine
    engine.say(text)         # Queue the text to say
    engine.runAndWait()      # Process and play the speech

model = GPT4All("gpt4all-13b-snoozy-q4_0.gguf", model_path="./models")
StreamerName = ""
GameName = ""

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
credentials = flow.run_local_server(port=0)

youtube = build("youtube", "v3", credentials=credentials)

def get_live_chat_id():
    broadcasts = youtube.liveBroadcasts().list(
        part="snippet,status",
        mine=True
    ).execute()

    active_broadcasts = [b for b in broadcasts.get("items", []) if b["status"]["lifeCycleStatus"] == "live"]

    if not active_broadcasts:
        print("❌ No active broadcasts found.")
        return None

    live_chat_id = active_broadcasts[0]["snippet"]["liveChatId"]
    print("✅ Live chat ID obtained:", live_chat_id)
    return live_chat_id

live_chat_id = get_live_chat_id()
if not live_chat_id:
    exit()

def send_message(message):
    youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": live_chat_id,
                "type": "textMessageEvent",
                "textMessageDetails": {
                    "messageText": message
                }
            }
        }
    ).execute()

def process_messages(messages):
    
    lastmessage = ''
    for message in messages:
        text = message["snippet"]["textMessageDetails"]["messageText"].strip().lower()
        
        author = message['authorDetails']['displayName']
        lastmessage = text
        if(author == "Nightbot"):
            break
        print(f"{author}: {text}")

# =========================== !!!!!!! Here is the prompt !!!!!!!!!!!!!!!! =================================
# =========================== !!!!!!! Here is the prompt !!!!!!!!!!!!!!!! =================================
# =========================== !!!!!!! Here is the prompt !!!!!!!!!!!!!!!! =================================
# =========================== !!!!!!! Here is the prompt !!!!!!!!!!!!!!!! =================================
    response = model.generate("As a gaming streamer named + " + StreamerName + ", who is playing " + GameName + ", generate a response to this live chat message in one sentence, without completing or repeating the viewer’s message. The viewer’s message is: " + lastmessage + " Your response should be relevant, engaging, and natural as if you were interacting with a live audience during a stream.", max_tokens=50)
    print("gpt4all:" + response)
    # send_message(response)
    speak(response)

print("🤖 Bot is running... (Press Ctrl+C to stop)")
next_page_token = None

try:
    while True:
        response = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="snippet,authorDetails",
            pageToken=next_page_token
        ).execute()

        messages = response.get("items", [])
        if messages:
            process_messages(messages)

        next_page_token = response.get("nextPageToken")
        # time.sleep(int(response.get("pollingIntervalMillis", 2000)) / 1000)
        time.sleep(5)

except KeyboardInterrupt:
    print("🛑 Bot stopped by user.")
