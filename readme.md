## TerminAI 🤖
Run ChatGPT directly from the terminal with optimized response formatting. 🚀

____
### Features
* Run powershell commands with natural language
* Adopt personas in your responses
* Highlight text with color
* optimized formatting for terminal
* Quit the chat by saying goodbye
  
___
### How to install ⚙️
* Clone this repository
* rename **.env.example** to **.env**
* Add your *API Key* from chatgpt to the **.env** file
* Run the script ``add_to_path.ps1`` in order to add this folder to *PATH* in windows environment variables.
*(This will make the app run as a native command in your terminal)*
___
### How to run 🏃‍♂️‍➡️
* Open PowerShell
* Type ```ai "hello world"``` 
* Done 🎉
___
### List of arguments ✏️
* ```ai "your message" -q```: send a message and quit after the response *(always use quotes in your messages)*
* ```ai```: opens the chat
* ```ai "your message"```: opens the chat with a message
* `q` | ``bye`` | `see ya`: quit the chat
___
### Settings 
All you need to run this project is to provide your own API Key from chatgpt. [See how to get one in this article](https://dev.to/onlinemsr/how-to-get-chatgpt-api-key-a-step-by-step-guide-507k)

`API_KEY` Your API Key

`MODEL` The gpt model being used

`TEMPERATURE` A higher temperature (e.g., 0.8 or 1.0) makes outputs more diverse and creative, while a lower temperature (e.g., 0.1 or 0.2) makes responses more deterministic and focused. 

`CURRENT_PERSONA` The current persona adopted by the model

___
### Personas
Allows you to customize the behavior of your model by writing instructions in the file ``personas.json``.

### Template
    <!-- example -->
    "Alyx": {
        "persona": "Alyx Vance from Half-Life",
        "name": "Alyx",
        "traits": "Witty, sarcastic, resourceful, a little rebellious",
        "tone": "Humorous with a bit of sarcasm.",
        "theme": "Sci-fi, post-apocalyptic, resistance fighter.",
        "references": "Headcrabs, Striders, Combine forces, Black Mesa, Resistance, etc...",
        "guidelines": "For each user request, generate a response that fits Alyx's personality and the Half-Life universe. Use humor that relates to her background as a resistance fighter in a post-apocalyptic world, dealing with the Combine forces. Don’t forget to throw in a little sarcasm and wit!"
    },

___
### Demonstration

#### just chatting
https://github.com/user-attachments/assets/1885212b-3603-4b94-8317-e028425ab431

#### Running commands with natural language
https://github.com/user-attachments/assets/3b79f764-764c-4795-94c7-c79f46293e2d

___
![MIT License](https://img.shields.io/badge/MIT-green?style=for-the-badge) ![PowerShell](https://img.shields.io/badge/powershell-5391FE?style=for-the-badge&logo=powershell&logoColor=white) ![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
