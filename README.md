# Youtube chatbot that Generates Responses using Large language models and Reads it for you (YGRLR)

* This is a short python program that uses gpt4all to generate responses to your youtube livestream chat. Response genration time may vary according to your hardware. By default, the prompt is set for a gaming stream, so if you want anything else, you might want to play around with the prompts and parameters.

* It will download a llm model when you first run it, so you need an extra 7GB of storage. If you want to use a different model, it is pretty straightforward to change in the code.

#### Installation:
1. Make an application and get the client secret(in json format) from google console
2. Download and save it as 'client_secret.json' into this project directory
3. Open your favourite terminal in this directory and enter the following commands. If your are not sure, use powershell on windows. I trust Linux users should do fine on their own.
4. ```python -m venv chatbot-env```
5. ```./chatbot-env/Scripts/activate```
6. ```pip install google-auth-oauthlib google-api-python-client pyttsx3 gpt4all```
7. Change `streamername` and `gamename` variable as needed. Also the prompt if you want.
8. Run by python ./chatbot.py

### Warning: This program uses libraries that I have not tested their security personally. I recommend you use it in your 'unlisted' streams with your friends or people you trust. Use it at your own risk.